from Utils import *
import random
import json
import os

#Class to create a 'connection' to the database. In this case, it is a .data file
class Database:
    #Check if datafile exists
    def check(self) -> None:
        return os.path.exists(DATA_FILENAME)

    #Create datafile
    def create(self) -> None:
        with open(DATA_FILENAME,'w') as handler:
            handler.write("")
            handler.close()

    #Read datafile
    def read(self) -> any:
        result = []

        with open(DATA_FILENAME,'r') as handler:
            result = json.load(handler)
            handler.close()

        return result

    #Update datafile
    def update(self, data) -> None:
        with open(DATA_FILENAME,'w') as handler:
            json.dump(data,handler,indent="\t")
            handler.close()

    #Delete datafile
    def delete(self) -> None:
        if self.check():
            os.remove(DATA_FILENAME)

class Subject:
    def __init__(self, id = None, mark = None, grade = None) -> None:
        if id:
            self._id = id
        else:
            self._id = self.generateId()

        if mark:
            self._mark = mark
        else:
            self._mark = self.generateMark()

        if grade:
            self._grade = grade
        else:
            self._grade = self.calculateGrade()

    #Auto Generate ID. Also includes check to see if subject id exists or not
    def generateId(self) -> str:
        existingSubjects = []
        for student in StudentController.readStudents():
            existingSubjects.extend(student.getSubjects())
        exception = [subject.getId() for subject in existingSubjects]

        id = random.randint(1,999)
        while id in exception and len(exception) < 999:
            id = random.randint(1,999)
        return f"{id:03d}"   

    #Generate student mark 
    def generateMark(self) -> int:
        return random.randint(25,100)

    #Calculate the student grade based on mark
    def calculateGrade(self) -> str:
        grade = ""
        
        if self._mark >= 85:
            grade = "HD"
        elif self._mark >= 75:
            grade = "D"
        elif self._mark >= 65:
            grade = "C"
        elif self._mark >= 50:
            grade = "P"
        else:
            grade = "Z"

        return grade

    #Get ID
    def getId(self) -> str:
        return self._id
    
    #Get Mark
    def getMark(self) -> int:
        return self._mark
    
    #Get Grade
    def getGrade(self) -> str:
        return self._grade

    #Convert to Dictionary so that it can be saved as JSON format
    def toDict(self) -> dict:
        return {"id": self._id, 
                "mark":self._mark, 
                "grade":self._grade}
    
class Student:
    def __init__(self, name, email, password, subjects = [], id = None) -> None:
        if id:
            self._id = id
        else:
            self._id = self.generateId()

        self._name = name
        self._email = email
        self._password = password

        if subjects:
            self._subjects = [Subject(s["id"], s["mark"], s["grade"]) for s in subjects]
        else:
            self._subjects = []

    #Auto Generate ID. Also includes check to see if subject id exists or not
    def generateId(self) -> str:
        exception = [student.getId() for student in StudentController.readStudents()]
        id = random.randint(1,999999)
        while id in exception:
            id = random.randint(1,999999)
        return f"{id:06d}"

    #Change Password
    def changePassword(self) -> None:
        newPassword = input("\t\tNew Password: ")
        while not checkPasswordFormat(newPassword):
            printc("\t\tIncorrect password format - try again", "red")
            newPassword = input("\t\tNew Password: ")

        newPasswordConfirm = input("\t\tConfirm Password: ")
        while newPassword != newPasswordConfirm:
            printc("\t\tPassword does not match - try again", "red")
            newPasswordConfirm = input("\t\tConfirm Password: ")

        self._password = newPassword
        StudentController.updateStudent(self)

    #Enrol subject
    def enrol(self) -> None:
        if len(self._subjects) < 4:
            sub = Subject()
            printc(f"\t\tEnrolling in Subject-{sub.getId()}","yellow")
            self._subjects.append(sub)
            printc(f"\t\tYou are now enrolled in {len(self._subjects)} out of 4 subjects","yellow")
        else:
            printc("\t\tStudents are allowed to enrol in 4 subjects only","red")
        StudentController.updateStudent(self)

    #Remove subject
    def remove(self) -> None:
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
        StudentController.updateStudent(self)

    #Show all student's subjects
    def show(self) -> None:
        printc(f"\t\tShowing {len(self._subjects)} subjects","yellow")
        for sub in self._subjects:
            print(f"\t\t[ Subject::{sub.getId()} -- mark = {sub.getMark(): >3} -- grade = {sub.getGrade(): >3} ]")

    #Student Menu
    def menu(self) -> None:
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

    #Get ID
    def getId(self) -> str:
        return self._id
    
    #Get Name
    def getName(self) -> str:
        return self._name
    
    #Get Email
    def getEmail(self) -> str:
        return self._email
    
    #Get Subjects
    def getSubjects(self) -> []:
        return self._subjects

    #Get Password
    def getPassword(self) -> str:
        return self._password
    
    #Convert to Dictionary so that it can be saved as JSON format
    def toDict(self) -> dict:
        return {"id": self._id, 
                "name":self._name, 
                "email":self._email, 
                "password":self._password, 
                "subjects":[s.toDict() for s in self._subjects]}

#Class to control the handling of Student data
class StudentController:
    #Read Student from Database
    def readStudents() -> [any]:
        db = Database()
        if not db.check():
            return []

        result = []

        for data in db.read():
            student = Student(data["name"], data["email"], data["password"], data["subjects"], data["id"])
            result.append(student)

        return result
    
    #Read Student in Database
    def createStudent(student) -> None:
        result = StudentController.readStudents()
        result.append(student)
        StudentController.updateDatabase(result)

    #Update Student in Database
    def updateStudent(student) -> None:
        result = StudentController.readStudents()
        for index, st in enumerate(result):
            if st.getId() == student.getId():
                result[index] = student

        StudentController.updateDatabase(result)

    #Delete Student in Database
    def deleteStudent(student) -> None:
        result = StudentController.readStudents()
        for index, st in enumerate(result):
            if st.getId() == student.getId():
                result.pop(index)

        StudentController.updateDatabase(result)

    #Commit the changes to database
    def updateDatabase(data) -> None:
        db = Database()
        if not db.check():
            db.create()
        
        result = [d.toDict() for d in data]

        db.update(result)

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
        studentLogin = None
        if self._students:
            for student in self._students:
                if student.getEmail() == emailInput and student.getPassword() == passwordInput:   
                    studentLogin = student

        #If successful login
        if studentLogin:
            studentLogin.menu()
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