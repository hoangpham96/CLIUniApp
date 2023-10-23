from Utils import *
from Database import *
from Subject import *
from Student import *
from StudentControllerGUI import *

import tkinter as tk
import tkinter.messagebox as mb
  
#Class to control the handling of Student data
class SubjectsWindow(tk.Toplevel):
    def __init__(self,master,student):
        super().__init__(master=master)
        self.title("Enrollment List")
        self.geometry("300x200")
        x = master.winfo_x()
        y = master.winfo_y()
        self.geometry(f"+{x}+{y}")
        self.configure(bg=GUI_BG)
        self.resizable(False,False)
        
        subjectsBox = tk.LabelFrame(self, text="Subjects", bg=GUI_BG, fg='white', padx=20, pady=20, font=GUI_FONT)
        subjectsBox.columnconfigure(0, weight=1)
        subjectsBox.columnconfigure(1, weight=3)
        subjectsBox.place(rely=0.5, relx=0.5, anchor="center")
        
        subjects = student.getSubjects()
        listVar = tk.Variable(value=subjects)
        subjectsList = tk.Listbox(subjectsBox, listvariable=listVar, height=5, width= 30)
        subjectsList.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

        backButton = tk.Button(subjectsBox, text="Back", command=lambda: self.destroy())
        backButton.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
        
        def enrol():
            if len(student.getSubjects()) < 4:
                sub = Subject()
                student.enrol(sub)
                StudentController.updateStudent(student)
                self.destroy()
                SubjectsWindow(master,student)
            else:
                info = "Students are allowed to enrol in 4 subjects only"
                mb.showerror(title="Enrolment Error", message = info)
                self.focus()
            
        enrolButton = tk.Button(subjectsBox, text="Enrol", command=enrol)
        enrolButton.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

class LoginFrame(tk.LabelFrame):
    def __init__(self,master):
        super().__init__(master=master, text="Sign In", bg=GUI_BG, fg="white", padx=20, pady=20, font=GUI_FONT)
        
        self.emailLable = tk.Label(self, text="Email:", justify="left", bg=GUI_BG, fg=GUI_FONT_YELLOW, font=GUI_FONT)
        self.emailLable.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        
        self.passwordLabel = tk.Label(self, text="Password:", justify="left", bg=GUI_BG, fg=GUI_FONT_YELLOW, font=GUI_FONT)
        self.passwordLabel.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
        
        self.emailText = tk.StringVar()
        self.emailField = tk.Entry(self, textvariable=self.emailText)
        self.emailField.grid(column=1, row=0, padx=5, pady=5)
        self.emailField.focus()
        
        self.passwordText = tk.StringVar()
        self.passwordField = tk.Entry(self, textvariable=self.passwordText, show="*")
        self.passwordField.grid(column=1, row=1, padx=5, pady=5)
        
        self.cancelButton = tk.Button(self, text="Cancel", command=lambda: root.quit())
        self.cancelButton.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
        
        self.loginButton = tk.Button(self, text="Login", command=self.login)
        self.loginButton.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)
        
    def login(self):
        if self.emailText.get() == '':
            info = "Please enter Email Address"
            mb.showerror(title="Login Error", message = info)
            return
        
        if self.passwordText.get() == '':
            info = "Please enter Password"
            mb.showerror(title="Login Error", message = info)
            return

        studentToLogin = StudentController.validateCredentials(self.emailText.get(), self.passwordText.get())        

        #If successful login
        if studentToLogin:
            info = "Login Successful"
            mb.showinfo(title="Login Confirmation", message = info)
            root.unbind("<Return>")
            SubjectsWindow(root,studentToLogin)
            self.clear()
            
        else:
            info = "Login Failed"
            mb.showinfo(title="Login Confirmation", message = info)
            self.clear()
            
    def clear(self):
        self.emailField.delete(0,tk.END)
        self.passwordField.delete(0,tk.END)

#Starting the app
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x200")
    root.title("University App")
    root.configure(bg=GUI_BG)
    root.resizable(False,False)
    
    box = LoginFrame(root)
    box.columnconfigure(0, weight=1)
    box.columnconfigure(1, weight=3)
    box.place(rely=0.5, relx=0.5, anchor="center")
        
    root.mainloop()