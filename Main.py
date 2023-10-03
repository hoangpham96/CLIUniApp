class Student:
    pass

class Subject:
    pass

class Database:
    pass

class University:
    def __init__(self) -> None:
        pass

    def adminMenu(self):
        choice = ''
        while choice != 'x':
            choice = input("\tAdmin System (c/g/p/r/s/x): ").lower()

            match choice:
                case 'c': break
                case 'g': break
                case 'p': break
                case 'r': break
                case 's': break
                case 'x': break
                case _: print("Unknown choice")

    def studentMenu(self):
        choice = ''
        while choice != 'x':
            choice = input("\tStudent System (l/r/x): ").lower()

            match choice:
                case 'l': break
                case 'r': break
                case 'x': break
                case _: print("Unknown choice")

    def menu(self):
        choice = ''
        while choice != 'x':
            choice = input("University System: (A)dmin, (S)tudent, or e(X)it: ").lower()

            match choice:
                case 'a': self.adminMenu()
                case 's': self.studentMenu()
                case 'x': break
                case _: print("Unknown choice")

        print("Thank You!")

#Starting the app
if __name__ == '__main__':
    uni = University()
    uni.menu()