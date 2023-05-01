'''
AC3 takes any binary constraints and solves it
plan:

graphical interface that allows user to select which application of AC3 is showcased

option 1: Timetable
    Constraints: prerequisites, corequisites, time
    
    Algorithm logic: 2 options: Student Page and Professor Page
                                    Students select time period (number of semesters) and courses desired (median of 5) and time of course
                                    Professors add courses (classrooms, time, credits, prereqs and coreqs)
    For professors, relatively trivial - make sure slot selected is available 
                    constraints: cant be teaching 2 courses at once, cant have 2 courses in same room
    For students, relatively complicated - encode constraints (no 2 courses at same time, prereq and coreq, max number of credits, number of credits needed)


'''


class AC3:
    # constraints will be given as a list of or triplets
    op = {
        "=": (lambda x, y: x==y),
        "!=": (lambda x, y: x!=y),
        ">": (lambda x, y: x>y),
        "<": (lambda x, y: x<y),
        ">=": (lambda x, y: x>=y),
        "<=": (lambda x, y: x<=y),
    }
    def reverse(self, operator):
        if operator == ">":
            return "<"
        elif operator =="<":
            return ">"
        elif operator == ">=":
            return "<="
        elif operator == "<=":
            return ">="
        return operator
    def __init__(self, variables=[], domains={}, Constraints=[]):
        self.variables = variables
        self.domains = domains
        self.Constraints = Constraints
    
    def makeBinaryConstraints(self):
        reversedConstraints = []
        for constraint in self.Constraints:
            reversedConstraints.append(constraint)
            reversedConstraints.append([constraint[2], self.reverse(constraint[1]), constraint[0]])
        self.Constraints = reversedConstraints
    def solve(self):
        # begin by initializing binary constraints (adding reversed arcs to binary constraints)
        self.makeBinaryConstraints()
        # initialize agenda (add all arcs to it)
        agenda = self.Constraints
        while agenda:
            # take first arc in agenda
            arc = agenda[0]
            # suppose there is no change and all values are valid (all constraints are satisfied)
            change = False
            # for all possible values of left variable, check if they are consistent
            for leftVar in self.domains[arc[0]]:
                # suppose current value of left variable is not consistent
                consistent = False
                # check if any of the values of right variable is consistent (if the constraint can be satisfied with current value of left variable)
                for rightVar in self.domains[arc[2]]:
                    if self.op[arc[1]](leftVar,rightVar):
                       consistent = True
                # if consistency cant be achieved with current value of left variable
                if consistent == False:
                    # remove left variable value from the domain of the left variable
                    self.domains[arc[0]].remove(leftVar)
                    # if we removed a value from the domain of the left variable, we must append all constraints including that variable on right side
                    change = True
            # remove arc from agenda
            agenda = agenda[1:]
            # if there was a change
            if change == True:
                # check all constraints 
                for constraint in self.Constraints:
                    # if the variable was on the right side of an arc that is not in the agenda, add the arc to the agenda
                    if constraint[2] == arc[0] and constraint not in agenda:
                        agenda.append(constraint)
            
        

''' Following code can be used for testing Sudoku back-tracking solving algorithm (to be improved
m = [
                    [3,0,0,8,0,0,0,0,1],
                    [0,0,0,0,0,2,0,0,0],
                    [0,4,1,5,0,0,8,3,0],
                    [0,2,0,0,0,1,0,0,0],
                    [8,5,0,4,0,3,0,1,7],
                    [0,0,0,7,0,0,0,2,0],
                    [0,8,5,0,0,9,7,4,0],
                    [0,0,0,1,0,0,0,0,0],
                    [9,0,0,0,0,7,0,0,6]
                ]
S = Sudoku(m)
S.solve()
'''