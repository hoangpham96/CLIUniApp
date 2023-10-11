from Utils import *
import random
import json
import os

class Student:
    def __init__(self, name, email, password, subjects = [], id = None) -> None:
        if id:
            self._id = id
        else:
            self._id = self.generateId()
        self._name = name
        self._email = email
        self._password = password
        self._subjects = subjects

    def generateId(self):
        exception = [student.getId() for student in StudentController.readStudents()]
        id = random.randint(1,999999)
        while id in exception:
            id = random.randint(1,999999)
        return f"{id:06d}"

    def changePassword(self):
        #TODO: implement password format checker
        newPassword = input("\t\tNew Password: ")
        newPasswordConfirm = input("\t\tConfirm Password: ")

        while newPassword != newPasswordConfirm:
            printc("\t\tPassword does not match - try again", "red")
            newPasswordConfirm = input("\t\tConfirm Password: ")

        self._password = newPassword
        StudentController.updateStudents(self)

    def enrol(self):
        if len(self._subjects) < 4:
            sub = Subject()
            printc(f"\t\tEnrolling in Subject-{sub.getId()}","yellow")
            self._subjects.append(sub)
            printc(f"\t\tYou are now enrolled in {len(self._subjects)} out of 4 subjects","yellow")
        else:
            printc("\t\tStudents are allowed to enrol in 4 subjects only","red")
        #TODO: save subject

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
            printc("\t\tSubject {removeId} does not exist", "red")
        #TODO: save subject

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

    def getPassword(self):
        return self._password
    
    #Convert to Dictionary so that it can be saved as JSON format
    def toDict(self):
        return {"id": self._id, "name":self._name, "email":self._email, "password":self._password, "subjects":[s.toDict() for s in self._subjects]}

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

    #Convert to Dictionary so that it can be saved as JSON format
    def toDict(self):
        return {"id": self._id, "mark":self._mark, "grade":self._grade}

#Class to create a 'connection' to the database. In this case, it is a .data file
class Database:
    def check(self):
        return os.path.exists(DATA_FILENAME)

    def create(self):
        if not self.check():
            with open(DATA_FILENAME,'w') as handler:
                handler.write("")
                handler.close()

    def read(self):
        result = []

        with open(DATA_FILENAME,'r') as handler:
            result = json.load(handler)
            handler.close()

        return result

    def update(self, data):
        with open(DATA_FILENAME,'w') as handler:
            json.dump(data,handler,indent="\t")
            handler.close()

    def delete(self):
        if self.check():
            os.remove(DATA_FILENAME)

#Class to control the handling of Student data
#TODO: Figure out a better way to do this than Class method
class StudentController:
    @classmethod
    def createStudent(cls,student):
        result = cls.readStudents()
        result.append(student)
        cls.updateDatabase(result)
    
    @classmethod
    def readStudents(cls):
        db = Database()

        result = []

        for data in db.read():
            student = Student(data["name"],data["email"],data["password"],data["subjects"],data["id"])
            result.append(student)

        return result

    @classmethod
    def updateStudents(cls,student):
        result = cls.readStudents()
        for index, st in enumerate(result):
            if st.getId() == student.getId():
                result[index] = student

        cls.updateDatabase(result)

    @classmethod
    def deleteStudents(cls,student):
        result = cls.readStudents()
        for index, st in enumerate(result):
            if st.getId() == student.getId():
                result.pop(index)

        cls.updateDatabase(result)

    @classmethod
    def updateDatabase(cls, data):
        db = Database()
        
        result = [d.toDict() for d in data]

        db.update(result)

class University:
    def __init__(self) -> None:
        self._students = StudentController.readStudents()

    def adminMenu(self):
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

    def clearDatabase(self):
        pass

    def groupStudents(self):
        pass

    def partitionStudents(self):
        pass

    def removeStudent(self):
        pass

    def showStudents(self):
        #TODO: pretify this
        print(StudentController.readStudents())

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
        emailInput = input("\tEmail: ")
        passwordInput = input("\tPassword: ")

        #Check student login. If no match, Student Login will be a None object
        studentLogin = None
        for student in self._students:
            if student.getEmail() == emailInput and student.getPassword() == passwordInput:   
                studentLogin = student

        #If successful login
        if studentLogin:
            studentLogin.menu()
        else:
            printc("\tStudent does not exist","red")

    def studentRegister(self):
        printc("\tStudent Sign Up","green")
        emailInput = input("\tEmail: ")
        passwordInput = input("\tPassword: ")
        if checkEmailFormat(emailInput) and checkPasswordFormat(passwordInput):
            printc("\tEmail and password format acceptable","yellow")
        
            studentExists = False
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