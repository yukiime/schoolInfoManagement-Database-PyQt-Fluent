from PyQt5.QtWidgets import QApplication
from login import LoginWindow
from admin_interface import AdminWindow
from student_interface import StudentWindow
from teacher_interface import TeacherWindow
from interface_jump import *

if __name__ == "__main__":
    app = QApplication([])
    login_window = LoginWindow()
    login_window.show()
    app.exec()
