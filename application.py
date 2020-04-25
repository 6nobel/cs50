import os
import requests
import json
import calendar
import dateutil.parser
import datetime

from datetime import datetime, timedelta
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gasoline.db")

@app.route("/")
def index():
    return render_template("index.html")

def dist_LER(radius1):
    """Look up """

    # Contact API
    try:
        response = requests.get(f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.242080&lng=7.476610&rad={radius1}&sort=price&type=diesel&apikey=ec85a6a6-3227-6287-b254-d2ddf96dec72")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        data = response.json()
        return data
    except (KeyError, TypeError, ValueError):
        return None

def dist_OL(radius1):
    """Look up """

    # Contact API
    try:
        response = requests.get(f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.144870&lng=8.188970&rad={radius1}&sort=price&type=diesel&apikey=ec85a6a6-3227-6287-b254-d2ddf96dec72")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        data = response.json()
        return data
    except (KeyError, TypeError, ValueError):
        return None



@app.route("/LER", methods=["GET", "POST"])
def LER():
    if request.method == "POST":
        answer_LER = dist_LER(request.form.get("radius1"))
        station_LER = answer_LER["stations"]

        return render_template("LER.html", answer_LER=station_LER)

    else:
        answer_LER = dist_LER(3)
        station_LER = answer_LER["stations"]
        return render_template("LER.html", answer_LER=station_LER)

@app.route("/OL", methods=["GET", "POST"])
def OL():
    if request.method == "POST":
        answer_OL = dist_OL(request.form.get("radius1"))
        station_OL = answer_OL["stations"]

        return render_template("OL.html", answer_OL=station_OL)

    else:
        answer_OL = dist_OL(3)
        station_OL = answer_OL["stations"]

        return render_template("OL.html", answer_OL=station_OL)


@app.route("/comparison", methods=["GET", "POST"])
def comparison():
    if request.method == "POST":
        if (request.form.get("radius2") == None):
            answer_LER = dist_LER(3)
            station_LER = answer_LER["stations"]
            answer_OL = dist_OL(request.form.get("radius1"))
            station_OL = answer_OL["stations"]
        else:
            answer_LER = dist_LER(request.form.get("radius2"))
            station_LER = answer_LER["stations"]
            answer_OL = dist_OL(3)
            station_OL = answer_OL["stations"]

        return render_template("comparison.html", answer_LER=station_LER, answer_OL=station_OL)

    else:
        answer_LER = dist_LER(3)
        station_LER = answer_LER["stations"]
        answer_OL = dist_OL(3)
        station_OL = answer_OL["stations"]

        return render_template("comparison.html", answer_LER=station_LER, answer_OL=station_OL)

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if request.method == "POST":

        day_today = datetime.today().strftime('%A')
        day_today = day_today.lower()

        answer_OL = dist_OL(3)
        station_OL = answer_OL["stations"]

        IDs = []
        indexes = []

        for key in station_OL:
            ID = key["id"]
            IDs.append(ID)

        for i in range(len(IDs)):
            #calculate target
            data = db.execute(f"SELECT date, diesel FROM {day_today} WHERE station_uuid = '{IDs[i]}'")

            time_target = int(request.form.get("time1"))

            for row in data:
                date_time_str = row["date"]
                temp = dateutil.parser.parse(date_time_str)
                row["date"] = temp.hour

            summ_target = 0
            counter_target = 0

            for row in data:
                if row["date"] >= (time_target - 1) and row["date"] <= (time_target + 1):
                    summ_target += float(row["diesel"])
                    counter_target += 1

            if counter_target > 0:
                avg_target = summ_target / counter_target
            else:
                for row in data:
                    if row["date"] >= (time_target - 2) and row["date"] <= (time_target + 2):
                        summ_target += float(row["diesel"])
                        counter_target += 1

            if  counter_target > 0:
                avg_target = summ_target / counter_target
            else:
                for row in data:
                    if row["date"] >= (time_target - 6) and row["date"] <= (time_target + 6):
                        summ_target += float(row["diesel"])
                        counter_target += 1
                        avg_target = summ_target / counter_target

            #calculate current
            data_current = db.execute(f"SELECT date, diesel FROM {day_today} WHERE station_uuid = '{IDs[0]}'")

            time_temp = datetime.now()
            time_current = time_temp.hour + 2

            for row in data_current:
                date_time_str = row["date"]
                temp = dateutil.parser.parse(date_time_str)
                row["date"] = temp.hour

            summ_current = 0
            counter_current = 0

            for row in data_current:
                if row["date"] >= (time_current - 1) and row["date"] <= (time_current + 1):
                    summ_current += float(row["diesel"])
                    counter_current += 1

            if counter_current > 0:
                avg_current = summ_current / counter_current
            else:
                for row in data:
                    if row["date"] >= (time_current - 2) and row["date"] <= (time_current + 2):
                        summ_current += float(row["diesel"])
                        counter_current += 1

            if  counter_current > 0:
                avg_current = summ_current / counter_current
            else:
                for row in data:
                    if row["date"] >= (time_current - 6) and row["date"] <= (time_current + 6):
                        summ_current += float(row["diesel"])
                        counter_current += 1
                        avg_current = summ_current / counter_current

            #calculate the diffice-index between current and target
            index = round((avg_current - avg_target), 3)
            indexes.append(index)

        counter = 0

        for i in station_OL:
            i.update( {'index': indexes[counter]} )
            i.update( {'new_price': round((i['price'] + indexes[counter]), 3)} )
            counter += 1

        return render_template("prediction.html", answer_OL=station_OL, indexes=indexes)

    else:
        day_today = datetime.today().strftime('%A')
        return render_template("prediction.html", day_today=day_today)