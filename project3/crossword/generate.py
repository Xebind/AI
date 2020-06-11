import sys
import operator

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
                    print("#", end="")
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
        #print(f"{self.domains}")
        self.ac3()
        #print(f"{self.domains}")
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for variable in self.domains:
            removedwords = []
            for word in self.domains[variable]:

                if len(word) !=  variable.length:
                    removedwords.append(word)
            for word in removedwords:
                    self.domains[variable].remove(word)

        return

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x,y]
        if overlap is not None:
            removedwords = []
            for word1 in self.domains[x]:
                counter = 0
                for word2 in self.domains[y]:
                    if word1[overlap[0]] != word2[overlap[1]]:
                        counter = counter + 1
                if len(self.domains[y]) == counter:
                    removedwords.append(word1)

            if len(removedwords) == 0:
                return False
            else:
                for word in removedwords:
                    if word in self.domains[x]:
                        self.domains[x].remove(word)
                return True
        else:
            return False


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            arcs = []
            for variable1 in self.domains:
                for variable2 in self.domains:
                    if variable2 != variable1:
                        arcs.append((variable1,variable2))

        #print(f"{arcs}")
        while len(arcs) > 0:
            check = self.revise(arcs[0][0], arcs[0][1])
            if check:
                if len(self.domains[arcs[0][0]]) == 0:
                    return False
                else:
                    for variable in self.crossword.neighbors(arcs[0][0]):
                        if variable != arcs[0][1]:
                            arcs.append((variable, arcs[0][0]))
            arcs.pop(0)
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #print(f"checking :{key} in assignment {assignment} from values {self.domains}")

        if len(assignment) == 0:
            return False

        for key in assignment:
            if len(self.domains) != len((assignment.values())):
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for key1 in assignment:
            # PROBABLEMENTE HAY QUE ARREGLAR ESTO UN POCO
            if len(assignment[key1]) != key1.length:
                return False

            for key2 in assignment:
                if key1 != key2 and assignment[key1] == assignment[key2]:
                    return False

            for neighbor in self.crossword.neighbors(key1):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[key1,neighbor]
                    if assignment[key1][overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        affections = dict.fromkeys(self.domains[var])
        #print(f"{affections}")

        for value in affections:
            counter = 0
            for neighbor in self.crossword.neighbors(var):
                for value2 in self.domains[neighbor]:
                    overlap = self.crossword.overlaps[var,neighbor]
                    if value[overlap[0]] != value2[overlap[1]]:
                        counter = counter + 1
            affections[value] = counter

        sortedtuples = sorted(affections.items(), key=lambda x: x[1])
        #print(f"{sortedtuples}")

        sortedlist = [i[0] for i in sortedtuples]
        #print(f"{sortedlist}")
        return sortedlist

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        helpfuldict = dict.fromkeys(self.domains)
        for variable in list(helpfuldict):
            helpfuldict[variable] = (len(self.domains[variable]), len(self.crossword.neighbors(variable)))
            if variable in assignment:
                del helpfuldict[variable]

        sortedlist = sorted(helpfuldict.items(), key=lambda item: (item[1][0], -item[1][1]))
        return sortedlist[0][0]

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
        for value in self.order_domain_values(var,assignment):
            assignment[var] = value
            inferences = self.Inference(assignment, var)
            if inferences != None:

                #print(f"{assignment[var]}")
                for inference in inferences:
                    # ADD INFERENCES TO ASSIGNMENT
                    assignment[inference] = inferences[inference]
            #print(f"{assignment}")
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
            else:
                del assignment[var]
                for inference in inferences:
                    del assignment[inference]

        return None


    def Inference(self, assignment, var):
        arcs = []
        for variable in self.crossword.neighbors(var):
            arcs.append((variable,var))
        inferences = dict()
        if self.ac3(arcs):
            for x in self.crossword.neighbors(var):
                # CORREJIR EN EL FUTURO
                if len(self.domains[x]) == 1:
                    #print(f"{list(self.domains[x])[0]}")
                    inferences[x] = list(self.domains[x])[0]

            return inferences



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
