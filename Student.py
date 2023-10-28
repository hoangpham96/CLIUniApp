from Subject import *
import random

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
        from StudentControllerCLI import StudentController #Avoiding circular import

        exception = [student.getId() for student in StudentController.readStudents()]
        id = random.randint(1,999999)
        while id in exception and len(exception) < 999999:
            id = random.randint(1,999999)
        return f"{id:06d}"

    #Change Password
    def changePassword(self, newPassword) -> None:
        self._password = newPassword

    #Enrol subject
    def enrol(self, subject) -> None:
        self._subjects.append(subject)

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

    #Get Average mark of all subjects. Returns None if there is no Subject
    def getSubjectsAverageMark(self) -> float:
        if self._subjects:
            allMarks = [s.getMark() for s in self._subjects]
            return sum(allMarks) / len(allMarks)
        return None
    
    #Get Average grade of all subjects. Returns None if there is no Subject
    def getSubjectsAverageGrade(self) -> str:
        if self._subjects:
            avgMark = self.getSubjectsAverageMark()
            if avgMark:
                return Subject.calculateGradeOnMark(avgMark)
        return None

    #Get Summary of student (Name, ID, AvgGrade, AvgMark). Return only Name and ID if no Subjects
    def getStudentSummary(self) -> str:
        if self._subjects:
            return f"{self._name} :: {self._id} --> GRADE: {self.getSubjectsAverageGrade()} - MARK: {self.getSubjectsAverageMark():.2f}"
        return f"{self._name} :: {self._id}"

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