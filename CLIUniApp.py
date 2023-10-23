from Utils import *
from Database import *
from Subject import *
from Student import *
from StudentControllerCLI import *

class University:
    def __init__(self) -> None:
        self._students = StudentController.readStudents() #self._students acts as a cache for all student data in University class

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
        #TODO: @Christian call delete from Database class
        pass

    def groupStudents(self) -> None:
        #TODO: @Christian read from self._students and print data
        pass

    def partitionStudents(self) -> None:
        #TODO: @Christian read from self._students and print data
        pass

    def removeStudent(self) -> None:
        #TODO: @Christian remove student from self._students and from file. Remember to call StudentController.deleteStudent
        pass

    def showStudents(self) -> None:
        #TODO: @Christian read from self._students and print data
        pass

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
        if self._students:
            for student in self._students:
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
            if self._students:
                for student in self._students:
                    if student.getEmail() == emailInput:
                        studentExists = True
            
            if studentExists:
                printc(f"\tStudent {student.getName()} already exists","red")
            else:
                nameInput = input("\tName: ")
                printc(f"\tEnrolling Student {nameInput}","yellow")
                newStudent = Student(nameInput,emailInput,passwordInput)
                StudentController.createStudent(newStudent)
                self._students = StudentController.readStudents()
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