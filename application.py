import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    cash = rows[0]["cash"]

    stocks = db.execute("SELECT symbol, sum(shares) as total_shares FROM transactions WHERE (user_id = :user_id) GROUP BY symbol HAVING total_shares > 0 ", user_id=session["user_id"])
    quotes={}

    total_stock_value = 0

    for stock in stocks:
        quotes[stock["symbol"]] = lookup(stock["symbol"])
        request = lookup(stock["symbol"])
        price = request["price"]
        amount = stock["total_shares"]
        total_stock_value += price * amount

    total = cash + total_stock_value

    return render_template("index.html", quotes=quotes, stocks=stocks, cash=cash, total=total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = lookup(request.form.get("symbol"))
        if not symbol:
            return apology("must provide valid Symbol", 400)

        price = symbol["price"]

        try:
            amount = int(request.form.get("shares"))
        except:
            return apology("shares must be bigger than 0", 400)

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash = rows[0]["cash"]

        total = price * amount

        if total > cash:
            return apology("not enough funds", 400)

        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price = total, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, price, shares) VALUES(:user_id, :symbol, :price, :shares)",
                    user_id=session["user_id"],
                    symbol=symbol["symbol"],
                    price=price,
                    shares=amount)

        flash("Done!")

        return redirect("/")

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT symbol, shares, price, time FROM transactions WHERE user_id = :user_id ORDER BY time ASC",
                                user_id=session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        quote = lookup(request.form.get("symbol"))

        # Ensure Symbol was submitted
        if quote == 0:
            return apology("must provide valid Symbol", 400)

        return render_template("quote_result.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure passwords match
        if request.form.get("password") != request.form.get("password_check"):
            return apology("passwords do not match", 403)

        # Query database for username
        check = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username isnt already taken
        if len(check) == 1:
            return apology("username already in use", 403)

        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash, cash) VALUES(?, ?, ?)",
                    username, hash, 10000)

        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = lookup(request.form.get("symbol"))
        if not symbol:
            return apology("must provide valid Symbol", 400)

        price = symbol["price"]

        try:
            amount = int(request.form.get("shares"))
        except:
            return apology("shares must be bigger than 0", 400)

        total = price * amount

        stocks = db.execute("SELECT symbol, sum(shares) as total_shares FROM transactions WHERE (user_id = :user_id) GROUP BY symbol HAVING total_shares > 0 ", user_id=session["user_id"])

        for stock in stocks:
            if (stock["symbol"] == (request.form.get("symbol")).upper and stock["total_shares"] < int(request.form.get("shares"))):
                return apology("can not sell more than you own", 400)

        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price = total, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, price, shares) VALUES(:user_id, :symbol, :price, :shares)",
                    user_id=session["user_id"],
                    symbol=request.form.get("symbol"),
                    price=price,
                    shares = (0 - amount))

        flash("Done!")

        return redirect("/")

    else:
        return render_template("sell.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    """add money"""
    if request.method == "POST":
        cash = request.form.get("cash")
        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :user_id", cash = cash, user_id=session["user_id"])

        flash("Done!")

        return redirect("/")

    else:
        return render_template("add.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
