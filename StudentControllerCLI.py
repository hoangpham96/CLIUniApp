from Database import *
from Student import *

class StudentController:
    #Change Password
    def changePassword(student) -> None:
        newPassword = input("\t\tNew Password: ")
        while not checkPasswordFormat(newPassword):
            printc("\t\tIncorrect password format - try again", "red")
            newPassword = input("\t\tNew Password: ")

        newPasswordConfirm = input("\t\tConfirm Password: ")
        while newPassword != newPasswordConfirm:
            printc("\t\tPassword does not match - try again", "red")
            newPasswordConfirm = input("\t\tConfirm Password: ")

        student.changePassword(newPassword)
        StudentController.updateStudent(student)

    #Enrol subject
    def enrol(student) -> None:
        if len(student.getSubjects()) < 4:
            sub = Subject()
            printc(f"\t\tEnrolling in Subject-{sub.getId()}","yellow")
            student.enrol(sub)
            printc(f"\t\tYou are now enrolled in {len(student.getSubjects())} out of 4 subjects","yellow")
        else:
            printc("\t\tStudents are allowed to enrol in 4 subjects only","red")
        StudentController.updateStudent(student)

    #Remove subject
    def removeSubject(student) -> None:
        if len(student.getSubjects()) == 0:
            printc("\t\tNo subjects enrolled","red")
            return

        removeId = input("\t\tRemove Subject by ID: ")
        found = False
        for index, sub in enumerate(student.getSubjects()):
            if sub.getId() == removeId:
                printc(f"\t\tDropping Subject-{sub.getId()}","yellow")
                student.removeSubject(index)
                printc(f"\t\tYou are now enrolled in {len(student.getSubjects())} out of 4 subjects","yellow")
                found = True
                break
        
        if not found:
            printc(f"\t\tSubject {removeId} does not exist", "red")
        StudentController.updateStudent(student)

    #Show all student's subjects
    def showSubjects(student) -> None:
        printc(f"\t\tShowing {len(student.getSubjects())} subjects","yellow")
        for sub in student.getSubjects():
            print(f"\t\t[ Subject::{sub.getId()} -- mark = {sub.getMark(): >3} -- grade = {sub.getGrade(): >3} ]")

    #Student Menu
    def studentMenu(student) -> None:
        choice = ''
        while choice != 'x':
            choice = inputc("\t\tStudent Course Menu (c/e/r/s/x): ","cyan").lower()

            match choice:
                case 'c': StudentController.changePassword(student)
                case 'e': StudentController.enrol(student)
                case 'r': StudentController.removeSubject(student)
                case 's': StudentController.showSubjects(student)
                case 'x': break
                case _: printc("\t\tUnknown choice","red")

    #Read Student from Database
    def readStudents() -> []:
        db = Database()
        if not db.check():
            return []

        result = []

        for data in db.read():
            student = Student(data["name"], data["email"], data["password"], data["subjects"], data["id"])
            result.append(student)

        return result
    
    #create Student in Database
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

    #Find Student
    def findStudent(studentID) -> Student:
        allStudents = StudentController.readStudents()
        for student in allStudents:
            if student.getId() == studentID:
                return student
        return None

    #Commit the changes to database
    def updateDatabase(data) -> None:
        db = Database()
        if not db.check():
            db.create()
        
        result = [d.toDict() for d in data]

        db.update(result)