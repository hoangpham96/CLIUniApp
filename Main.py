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
        if len(self._subjects) < 4:
            sub = Subject()
            printc(f"\t\tEnrolling in Subject-{sub.getId()}","yellow")
            self._subjects.append(sub)
            printc(f"\t\tYou are now enrolled in {len(self._subjects)} out of 4 subjects","yellow")
        else:
            printc("\t\tStudents are allowed to enrol in 4 subjects only","red")

    def remove(self):
        if len(self._subjects) == 0:
            printc("\t\tNo subjects enrolled","red")
            return

        removeId = input("\t\tRemove Subject by ID: ")
        found = False
        for index, sub in enumerate(self._subjects):
            if sub.getId() == removeId:
                printc(f"\t\tDropping Subject-{sub.getId()}","yellow")
                self._subjects.pop(index)
                printc(f"\t\tYou are now enrolled in {len(self._subjects)} out of 4 subjects","yellow")
                found = True
                break
        
        if not found:
            printc("\t\tSubject could not be found", "red")

    def show(self):
        printc(f"\t\tShowing {len(self._subjects)} subjects","yellow")
        for sub in self._subjects:
            print(f"\t\t[ Subject::{sub.getId()} -- mark = {sub.getMark(): >3} -- grade = {sub.getGrade(): >3} ]")

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
                case _: printc("\t\tUnknown choice","red")

    def getId(self):
        return self._id
    
    def getName(self):
        return self._name
    
    def getEmail(self):
        return self._email
    
    def getSubjects(self):
        return self._subjects

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

    def getId(self):
        return self._id
    
    def getMark(self):
        return self._mark
    
    def getGrade(self):
        return self._grade

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
                case _: printc("\tUnknown choice","red")

    def studentMenu(self):
        choice = ''
        while choice != 'x':
            choice = inputc("\tStudent System (l/r/x): ","cyan").lower()

            match choice:
                case 'l': self.studentLogin()
                case 'r': self.studentRegister()
                case 'x': break
                case _: printc("\tUnknown choice","red")

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