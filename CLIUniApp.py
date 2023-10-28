from Utils import *
from Database import *
from Subject import *
from Student import *
from StudentControllerCLI import *

class University:    
    #Admin Menu
    def adminMenu(self) -> None:
        choice = ''
        while choice != 'x':
            choice = inputc("\tAdmin System (c/g/p/r/s/x): ","cyan").lower()

            match choice:
                case 'c': self.clearDatabase()
                case 'g': self.groupStudents()
                case 'p': self.partitionStudents()
                case 'r': self.removeStudent()
                case 's': self.showStudents()
                case 'x': break
                case _: printc("\tUnknown choice","red")

    def clearDatabase(self) -> None:
        printc(f"\tClearing students database","yellow")
        choice = inputc("\tAre you sure you want to clear the database (Y)ES/(N)O: ","red")
        if choice.lower() == "y":
            db = Database()
            db.delete()
            printc(f"\tStudents data cleared","yellow")

    def groupStudents(self) -> None:
        printc("\tGrade Grouping", "yellow")

        allstudents = StudentController.readStudents()
        if allstudents: #If there's data
            gradeGroups = {}
            for student in allstudents:
                studentAvgGrade = student.getSubjectsAverageGrade()
                if studentAvgGrade: #If Student can have average grade (has at least 1 subject)
                    if studentAvgGrade in gradeGroups:
                        gradeGroups[studentAvgGrade].append(student)
                    else:
                        gradeGroups[studentAvgGrade] = [student]

            University.displayCohorts(gradeGroups)

        else:
            print("\t\t< Nothing to Display >")

    def partitionStudents(self) -> None:
        printc("\tPASS/FAIL Partition", "yellow")

        allstudents = StudentController.readStudents()
        if allstudents: #If there's data
            passFail = {"PASS": [], "FAIL": []}
            for student in allstudents:
                studentAvgGrade = student.getSubjectsAverageGrade()
                if studentAvgGrade: #If Student can have average grade (has at least 1 subject)
                    if studentAvgGrade != 'Z':
                        passFail["PASS"].append(student)
                    else:
                        passFail["FAIL"].append(student)

            University.displayCohorts(passFail)

        else:
            print("\t\t< Nothing to Display >")

    @staticmethod
    #Function to display a dictionary as Key --> List
    def displayCohorts(cohort) -> None:
        for group in cohort:
            groupStr = "["
            for student in cohort[group]:
                if groupStr != "[":
                    groupStr += ", "
                groupStr += student.getStudentSummary()
            groupStr += "]"
            print(f"\t{group} --> {groupStr}")

    def removeStudent(self) -> None:
        choice = input("\tRemove by ID: ")
        studentToRemove = StudentController.findStudent(choice)
        if studentToRemove:
            printc(f"\tRemoving Student {choice} Account","yellow")
            StudentController.deleteStudent(studentToRemove)
        else:
            printc(f"\tStudent {choice} does not exist","red")

    def showStudents(self) -> None:
        printc("\tStudent List", "yellow")

        allstudents = StudentController.readStudents()
        if allstudents:
            for student in allstudents:
                print(f"\t{student.getName()} :: {student.getId()} --> Email: {student.getEmail()}")
        else:
            print("\t\t< Nothing to Display >")

    #Student Menu
    def studentMenu(self) -> None:
        choice = ''
        while choice != 'x':
            choice = inputc("\tStudent System (l/r/x): ","cyan").lower()

            match choice:
                case 'l': self.studentLogin()
                case 'r': self.studentRegister()
                case 'x': break
                case _: printc("\tUnknown choice","red")

    #Login Student
    def studentLogin(self) -> None:
        printc("\tStudent Sign In","green")
        emailInput = input("\tEmail: ")
        passwordInput = input("\tPassword: ")

        #Check student login. If no match, Student Login will be a None object
        studentToLogin = None
        allStudents = StudentController.readStudents()
        if allStudents:
            for student in allStudents:
                if student.getEmail() == emailInput and student.getPassword() == passwordInput:   
                    studentToLogin = student

        #If successful login
        if studentToLogin:
            StudentController.studentMenu(studentToLogin)
        else:
            printc("\tStudent does not exist","red")

    #Register Student
    def studentRegister(self) -> None:
        printc("\tStudent Sign Up","green")
        emailInput = input("\tEmail: ")
        passwordInput = input("\tPassword: ")
        if checkEmailFormat(emailInput) and checkPasswordFormat(passwordInput):
            printc("\tEmail and password format acceptable","yellow")
        
            studentExists = False
            allStudents = StudentController.readStudents()
            if allStudents:
                for student in allStudents:
                    if student.getEmail() == emailInput:
                        studentExists = True
            
            if studentExists:
                printc(f"\tStudent {student.getName()} already exists","red")
            else:
                nameInput = input("\tName: ")
                printc(f"\tEnrolling Student {nameInput}","yellow")
                newStudent = Student(nameInput,emailInput,passwordInput)
                StudentController.createStudent(newStudent)
        else:
            printc("\tIncorrect email or password format","red")

    #Main University Menu
    def menu(self) -> None:
        choice = ''
        while choice != 'x':
            choice = inputc("University System: (A)dmin, (S)tudent, or e(X)it: ","cyan").lower()

            match choice:
                case 'a': self.adminMenu()
                case 's': self.studentMenu()
                case 'x': break
                case _: printc("Unknown choice","red")

        printc("Thank You!","yellow")

#Starting the app
if __name__ == '__main__':
    uni = University()
    uni.menu()