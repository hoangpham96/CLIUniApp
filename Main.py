from Utils import printc
from Utils import inputc
import random

class Student:
    def __init__(self,name,email,password) -> None:
        self._id = self.generateId()
        self._name = name
        self._email = email
        self._password = password
        self._subjects = []

    def generateId(self):
        #TODO: implement functionality to exclude existing student ID
        id = random.randint(1,999999)
        return f"{id:06d}"

    def changePassword(self):
        pass

    def enrol(self):
        pass

    def remove(self):
        pass

    def show(self):
        pass

    def menu(self):
        choice = ''
        while choice != 'x':
            choice = inputc("\t\tStudent Course Menu (c/e/r/s/x): ","cyan").lower()

            match choice:
                case 'c': self.changePassword()
                case 'e': self.enrol()
                case 'r': self.remove()
                case 's': self.show()
                case 'x': break
                case _: printc("Unknown choice","red")

class Subject:
    def __init__(self) -> None:
        self._id = self.generateId()
        self.generateMark()
        self.calculateGrade()

    def generateId(self):
        #TODO: implement functionality to exclude existing student ID
        id = random.randint(1,999)
        return f"{id:03d}"   
     
    def generateMark(self):
        self._mark = random.randint(25,100)

    def calculateGrade(self):
        if self._mark >= 85:
            self._grade = "HD"
        elif self._mark >= 75:
            self._grade = "D"
        elif self._mark >= 65:
            self._grade = "C"
        elif self._mark >= 50:
            self._grade = "P"
        else:
            self._grade = "Z"

class Database:
    def check(self):
        pass

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

class University:
    def __init__(self) -> None:
        self.students = [Student("test","test","test")] #TODO: replace with student data read from file

    def adminMenu(self):
        choice = ''
        while choice != 'x':
            choice = inputc("\tAdmin System (c/g/p/r/s/x): ","cyan").lower()

            match choice:
                case 'c': break
                case 'g': break
                case 'p': break
                case 'r': break
                case 's': break
                case 'x': break
                case _: printc("Unknown choice","red")

    def studentMenu(self):
        choice = ''
        while choice != 'x':
            choice = inputc("\tStudent System (l/r/x): ","cyan").lower()

            match choice:
                case 'l': self.studentLogin()
                case 'r': self.studentRegister()
                case 'x': break
                case _: print("Unknown choice")

    def studentLogin(self):
        printc("\tStudent Sign In","green")
        emailInput = input("\tEmail: ").lower()
        passwordInput = input("\tPassword: ").lower()
        #TODO: email/password verification logic
        self.students[0].menu()

    def studentRegister(self):
        printc("\tStudent Sign Up","green")
        emailInput = input("\tEmail: ").lower()
        passwordInput = input("\tPassword: ").lower()
        #TODO: email/password verification logic
        nameInput = input("\tName: ").lower()
        #TODO: save new student data

    def menu(self):
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