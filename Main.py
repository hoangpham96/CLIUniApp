from Utils import printc
from Utils import inputc

class Student:
    def __init__(self,name,email,password) -> None:
        self._id = self.generateId()
        self._name = name
        self._email = email
        self._password = password
        self._subjects = []

    def generateId(self):
        return None

    def changePassword(self,password):
        #TODO: check password
        self._password = password

    def enrol(self):
        pass

    def remove(self):
        pass

    def show(self):
        pass

    def menu(self):
        pass

class Subject:
    def __init__(self) -> None:
        self._id = self.generateId()
        self._mark = self.generateMark()
        self._grade = self.calculateGrade()

    def generateId(self):
        return None
    
    def generateMark(self):
        return None

    def calculateGrade(self):
        return None

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
        pass

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
                case 'l': break
                case 'r': self.studentRegister()
                case 'x': break
                case _: print("Unknown choice")

    def studentRegister(self):
        printc("\tStudent sign up","green")
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