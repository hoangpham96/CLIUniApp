from Utils import *
import tkinter as tk
import tkinter.messagebox as mb
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

    #Read datafile. Since file is in JSON format, result will be returned in List of Dictionaries format
    def read(self) -> any:
        result = []

        with open(DATA_FILENAME,'r') as handler:
            result = json.load(handler)
            handler.close()

        return result

    #Update datafile. Expects data in List of Dictionaries format
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
            #Expects subjects argument in List of Dictionaries format
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
    def changePassword(self, newPassword) -> None:
        self._password = newPassword

    #Enrol subject
    def enrol(self, sub) -> None:
        self._subjects.append(sub)

    #Remove subject
    def removeSubject(self, subjectIndex) -> None:
        self._subjects.pop(subjectIndex)

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
    
    #Create Student in Database
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
        
    def main(self):     
        root = tk.Tk()
        root.geometry("300x200")
        root.title("University App")
        root.configure(bg=GUI_BG)
        root.resizable(False,False)
        
        box = tk.LabelFrame(root, text="Sign In", bg=GUI_BG, fg='white', padx=20, pady=20, font=GUI_FONT)
        box.columnconfigure(0, weight=1)
        box.columnconfigure(1, weight=3)
        box.place(rely=0.5, relx=0.5, anchor="center")
        
        emailLable = tk.Label(box, text="Email:", justify="left", bg=GUI_BG, fg=GUI_FONT_YELLOW, font=GUI_FONT)
        emailLable.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        
        passwordLabel = tk.Label(box, text="Password:", justify="left", bg=GUI_BG, fg=GUI_FONT_YELLOW, font=GUI_FONT)
        passwordLabel.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
        
        emailText = tk.StringVar()
        emailField = tk.Entry(box, textvariable=emailText)
        emailField.grid(column=1, row=0, padx=5, pady=5)
        emailField.focus()
        
        passwordText = tk.StringVar()
        passwordField = tk.Entry(box, textvariable=passwordText, show="*")
        passwordField.grid(column=1, row=1, padx=5, pady=5)
        
        cancelButton = tk.Button(box, text="Cancel", command=lambda: root.quit())
        cancelButton.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
        
        def login():
            studentToLogin = None
            if self._students:
                for student in self._students:
                    if student.getEmail() == emailText and student.getPassword() == passwordText:   
                        studentToLogin = student

            #If successful login
            if studentToLogin:
                info = "Login Successful"
                mb.showinfo(title="Login Confirmation", message = info)
            else:
                info = "Login Failed"
                mb.showinfo(title="Login Confirmation", message = info)
        
        loginButton = tk.Button(box, text="Login", command=login)
        loginButton.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)
        
        root.mainloop()

#Starting the app
if __name__ == '__main__':
    uni = University()
    uni.main()