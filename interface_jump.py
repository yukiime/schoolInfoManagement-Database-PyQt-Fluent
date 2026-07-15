from admin_interface import AdminWindow
from student_interface import StudentWindow
from teacher_interface import TeacherWindow

def open_student_window(login):
    sd = StudentWindow(login)
    sd.show()

def open_teacher_window(login):
    tw = TeacherWindow(login)
    tw.show()

def open_admin_window(login):
    admin_window = AdminWindow(login)
    admin_window.show()
