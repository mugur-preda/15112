# importing the CSP module and Pandas module 
import AC3 as csp 
import pandas as pd 

# function to read data from excel file
def readFile(filePath):
    global dataframe
    # reading the excel file using Pandas
    dataframe = pd.read_excel(filePath)

# Course class 
class Course:
    def __init__(self, name = "", semester = "", days = "", startTime = "", endTime = "", credits = 0, professor = "", classroom = "",  prereq = [], coreq = []):
        # initializing the attributes of the course class
        self.name = str(name)
        self.semester = str(semester)
        self.days = str(days)
        self.startTime = str(startTime)
        self.endTime = str(endTime)
        self.credits = int(credits)
        self.professor = str(professor)
        self.classroom = str(classroom)
        self.prereq = prereq
        self.coreq = coreq

    def __str__(self):
        # print the attributes of the course class
        print(self.name)
        print(self.semester)
        print(self.startTime)
        print(self.endTime)
        print(self.credits)
        print(self.professor)
        print(self.classroom)
        print(self.prereq)
        print(self.coreq)
        return ""

# TimeTable class 
class TimeTable:
    def __init__(self):
        # initializing the attributes of the timetable class
        self.courseList = []     # List of courses
        self.courseNumber = {}   # Mapping of course names to course objects
        self.constraints = []   # List of constraints
        self.solution = {}       # Dictionary to store the solution of the CSP
        self.maxCredits = 64     # Maximum credits allowed in a semester
        self.semesters = 0       # Number of semesters
        self.begin = "Fall"      # Beginning semester
        self.updateCourseList()  # Updating the course list using the data read from excel file

    # Function to initialize an empty timetable
    def emptyTimeTable(self, semesters, begin):
        self.semesters = semesters
        self.begin = begin
        self.updateCourseList()
        # Determining the start semester based on the beginning semester
        if(self.begin == "Fall"):
            start = 1
        else:
            start = 2
        # Assigning solution to each course according to the semester it's offered
        for course in self.courseList:
            if(course.semester == "Fall"):
                self.solution[course] = [i for i in range(start + 1 - start%2, self.semesters+start,2)]
            if(course.semester == "Spring"):
                self.solution[course] = [i for i in range(start + start%2, self.semesters+start,2)]
            if(course.semester == "FallSpring"):
                self.solution[course] = [i for i in range(start, self.semesters+start)]

    # Function to update the course list using the data read from excel file
    def updateCourseList(self):
        # Reset courseList
        self.courseList = []

        # Loop through all columns in dataframe
        for col in range(len(dataframe.columns)):
            # Extract relevant data from each column
            name = str(dataframe.iloc[:,col].name)
            semester = str(dataframe.iloc[:,col][0])
            days = str(dataframe.iloc[:, col][1])
            startTime = str(dataframe.iloc[:,col][2])
            endTime = str(dataframe.iloc[:,col][3])
            credits = int(dataframe.iloc[:,col][4])
            professor = str(dataframe.iloc[:,col][5])
            classroom = str(dataframe.iloc[:,col][6])
            prereq = str(dataframe.iloc[:,col][7])

            # Split prereq into a list if it's not "None"
            if(prereq!="None"):
                prereq = prereq.split(',')
            else:
                prereq = []

            coreq = str(dataframe.iloc[:,col][8])

            # Split coreq into a list if it's not "None"
            if(coreq!="None"):
                coreq = coreq.split(',')
            else:
                coreq = []

            # Create a new course object
            course =  Course(name, semester, days, startTime, endTime, credits, professor, classroom, prereq, coreq)

            # Add course to courseNumber dictionary
            self.courseNumber[name] = course

            # Add course to courseList
            self.courseList.append(course)

        # Loop through all courses in courseList
        for course in self.courseList:
            p = []
            c = []

            # Loop through all prereqs for this course
            for number in course.prereq:
                # If the prereq exists in courseNumber dictionary, add it to p
                if(number in self.courseNumber):
                    p.append(self.courseNumber[number])

            # Loop through all coreqs for this course
            for number in course.coreq:
                # If the coreq exists in courseNumber dictionary, add it to c
                if(number in self.courseNumber):
                    c.append(self.courseNumber[number])

            # Update the prereq and coreq for this course
            course.prereq = p
            course.coreq = c

    def fixTiming(self):
        # create empty list for each day of the week
        timings = []
        # 7 can be altered if we wish a different allocation of days/week (currently all days are available 24/7)
        for i in range(7):
            timings.append([])
        
        # for each day of the week, we create 5-minute slots (288/day; 288 slots /24 hours = 12 slots an hour -> one each 5 minutes)
        for day in timings:
            for i in range(288):
                day.append([])
        
        # all slots are now available
        for course in self.courseList:
            start_time = course.startTime
            end_time = course.endTime
            days = course.days
            
            # convert start_time to minutes since midnight
            begin = (int(start_time[0]) * 10 + int(start_time[1])) * 60 + int(start_time[3]) * 10 + int(start_time[4])
            if start_time[5] == 'P':
                begin += 720
            if int(start_time[0]) * 10 + int(start_time[1]) == 12:
                if start_time[5] == 'A':
                    begin = 0 + int(start_time[3]) * 10 + int(start_time[4])
                elif start_time[5] == 'P':  
                    begin = 720 + int(start_time[3]) * 10 + int(start_time[4])
            
            # round begin time to nearest 5 minutes
            begin = (begin // 5) * 5
            
            # convert end_time to minutes since midnight
            end = (int(end_time[0]) * 10 + int(end_time[1])) * 60 + int(end_time[3]) * 10 + int(end_time[4])
            if end_time[5] == 'P':
                end += 720
            if int(end_time[0]) * 10 + int(end_time[1]) == 12:
                if end_time[5] == 'A':
                    end = 0 + int(end_time[3]) * 10 + int(end_time[4])
                elif end_time[5] == 'P':  
                    end = 720 + int(end_time[3]) * 10 + int(end_time[4])
            
            # round end time to nearest 5 minutes
            end = (end // 5) * 5
            
            # for each day the course runs
            for letterDay in course.days:    
                if letterDay == 'U':
                    day = 0
                elif letterDay == 'M':
                    day = 1
                elif letterDay == 'T':
                    day = 2
                elif letterDay == 'W':
                    day = 3
                elif letterDay == 'R':
                    day = 4
                elif letterDay == 'F':
                    day = 5
                elif letterDay == 'S':
                    day = 6
            for day in timings:
                for slot in day:
                    if len(slot) > 1:
                        for course1 in slot:
                            for course2 in slot:
                                # Check if the two courses are not equal and the constraint is not already in the list
                                if course1 != course2 and [course1, "!=", course2] not in self.constraints and [course2, "!=", course1] not in self.constraints:
                                    # Add the inequality constraint to the list of constraints
                                    self.constraints.append([course1, "!=", course2])
    def fixReqs(self):
        # This function adds constraints to self.constraints based on course prerequisites and corequisites.
        for course in self.courseList:
            # For each course, iterate through its prerequisites and add a constraint that the course must come after each prerequisite.
            for prereq in course.prereq:
                self.constraints.append([course, ">", prereq])
            # For each course, iterate through its corequisites and add a constraint that the course must be taken in the same semester as each corequisite.
            for coreq in course.coreq:
                self.constraints.append([course, "=", coreq])

    def solve(self, semesters, begin):
        # This function solves the course scheduling problem using AC3 algorithm.
        # First, empty the timetable for the given number of semesters starting from the given beginning semester.
        self.emptyTimeTable(semesters, begin)
        # Fix the timing constraints based on the course timings.
        self.fixTiming()
        # Fix the requirements constraints based on the course prerequisites and corequisites.
        self.fixReqs()
        # Create an AC3 solver object with the course list, timetable solution, and constraints.
        sol = csp.AC3(self.courseList, self.solution, self.constraints)
        # Solve the problem using the AC3 algorithm.
        sol.solve()
        # Return the solution.
        return sol