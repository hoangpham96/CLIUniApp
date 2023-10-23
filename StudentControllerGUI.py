from Database import *
from Student import *

class StudentController:
    #Validate credentials
    def validateCredentials(email,password):
        studentToLogin = None
        _students = StudentController.readStudents()
        if _students:
            for student in _students:
                if student.getEmail() == email and student.getPassword() == password:   
                    studentToLogin = student
                    
        return studentToLogin
    
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
