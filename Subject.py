import random

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
        from StudentControllerCLI import StudentController #Avoiding circular import

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
        return Subject.calculateGradeOnMark(self._mark)

    #Reusable function to calculate grade based on mark
    @staticmethod
    def calculateGradeOnMark(mark) -> str:        
        if mark >= 85:
            return "HD"
        elif mark >= 75:
            return "D"
        elif mark >= 65:
            return "C"
        elif mark >= 50:
            return "P"
        else:
            return "Z"
    
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
        
    #Convert to String for easy printing
    def __str__(self) -> str:
        return f"Subject: {self._id}, Mark: {self._mark}, Grade: {self._grade}"