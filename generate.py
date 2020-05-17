import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        excluded = self.domains.copy()
        for x in self.domains:
            for y in self.domains[x].copy():
                if len(y) != x.length:
                    excluded[x].remove(y)

        self.domains = excluded.copy()

    def revise(self, X, Y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        excluded = self.domains.copy()
        if self.crossword.overlaps[X,Y] != None:
            for keyX in self.domains[X].copy():
                constraint = keyX[self.crossword.overlaps[X,Y][0]]
                count = 0
                no_match = 0
                for keyY in self.domains[Y]:
                    count += 1
                    if keyY[self.crossword.overlaps[X,Y][1]] != constraint:
                        no_match += 1                  

                if count == no_match:
                    revised = True
                    excluded[X].remove(keyX)

            self.domains = excluded.copy()
        
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = list()
        if arcs == None:
            for key, value in self.crossword.overlaps.items():
                if value == None:
                    continue
                else:
                    queue.append(key)    
        else:
            queue = arcs

        while queue:
            temp = queue[0]
            queue.remove(queue[0])
            if self.revise(temp[0],temp[1]):
                if self.domains[temp[0]] == None:
                    return False
                for key in self.crossword.neighbors(temp[0]):
                    if key != temp[1]:
                        queue.append((temp[0], key))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        complete = False
        if len(assignment) == len(self.domains):
            complete = True
        
        return complete

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        if len(assignment) > 1:
            for key1, value1 in assignment.items():
                for key2, value2 in assignment.items():
                    if key1 != key2 and self.crossword.overlaps[key1,key2] != None:
                        if value1[self.crossword.overlaps[key1,key2][0]] != value2[self.crossword.overlaps[key1,key2][1]]:
                            return False
        doubles = 0
        for key1, value1 in assignment.items():
            doubles = 0
            for key2, value2 in assignment.items():
                if value1 == value2:
                    doubles += 1
        if doubles > 1:
            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        unordered_values = list()
        ruled_out = dict()
              
        for key in self.domains[var]:
            unordered_values.append(key)
      
        for key in unordered_values:
            counter = 0
            for neighbour in (self.crossword.neighbors(var) - set(assignment.keys())):
                for key2 in self.domains[neighbour]:
                    if key[self.crossword.overlaps[var,neighbour][0]] != key2[self.crossword.overlaps[var,neighbour][1]]:
                        counter += 1
            ruled_out[key] = counter

        ordered_values = sorted(ruled_out, key= ruled_out.get)      

        return ordered_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        unassigned_var = dict()
        for key, value in self.domains.items():
            if key not in assignment:
                unassigned_var[key] = len(value)

        return_key = 0
        length_key = 0
        for key, value in unassigned_var.items():
            if value > length_key:
                length_key = value
                return_key = key
            elif value == length_key:
                if len(self.crossword.neighbors(key)) > len(self.crossword.neighbors(return_key)):
                    return_key = key

        return return_key

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
