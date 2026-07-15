from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QIcon
from qframelesswindow import FramelessWindow
from qfluentwidgets import Dialog
from ui.Ui_login import Ui_login_form
from general.infoBar import createErrorInfoBar
from interface_jump import *
from database import DatabaseConnection

class LoginWindow(FramelessWindow,Ui_login_form):
    def __init__(self,parent=None):
        super().__init__()
        self.setObjectName("login")
        self.setupUi(self)
        self.retranslateUi(self)
        self.load_ui_data()
        self.init_slots()
        self.connect_database()

    def load_ui_data(self):
        # 下拉框
        self.user_type_combo.addItem("学生")
        self.user_type_combo.addItem("教师")
        self.user_type_combo.addItem("管理员")
        self.user_type_combo.setCurrentIndex(0)
        # 头图
        image_path = "./img/title_img.jpg"  # 图片路径
        pixmap = QPixmap(image_path)
        width = 600  # 宽度
        height = 280  # 高度
        scaled_pixmap = pixmap.scaled(width, height)
        self.head_img_label.setPixmap(scaled_pixmap)

        # 密码不可见
        self.password_input.setEchoMode(QLineEdit.Password)

        self.setWindowIcon(QIcon('icon/bar.jpg'))
        self.setWindowTitle('登录界面')

        #居中显示
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    # 槽绑定
    def init_slots(self):
        self.login_button.clicked.connect(self.login)
        self.user_type_combo.currentIndexChanged.connect(self.on_combo_box_changed)    
    
    # 链接数据库
    def connect_database(self):
        # 数据库连接
        self.database = DatabaseConnection()
        self.database.connect()    
    
    # 关闭数据库
    def disconnect_database(self):
        self.database.disconnect()    
        
    # 下拉框改变事件
    def on_combo_box_changed(self):
        selected_text = self.user_type_combo.currentText()  # 获取当前选中的文本值
        hint = "请先使用下拉框选择用户类型"

        if selected_text == "学生":
            hint = "  您的账户及初始密码为 1 2 位学号,请及时修改密码"
        elif selected_text == "教师":
            hint = "  您的账户及初始密码为 8 位教师编号,请及时修改密码"
        elif selected_text == "管理员":
            hint = "  请不要泄露密码给无关人士"

        self.hint_label.setText("{}".format(hint))
    
    # 在对应的用户账户表查询账户
    def select_current_type_accountTabel_account(self,user_type,username):
        table,account,result = None,None,None
        if user_type == "学生":
            table = "sms_suser"
            account = "Saccount"
        elif user_type == "教师":
            table = "sms_tuser"
            account = "Taccount"
        elif user_type == "管理员":
            table = "sms_admin"
            account = "Aaccount"
        else:
            createErrorInfoBar(self,"错误", "未选择账户类型")

        if table and account :
            # 查询对应的账户表
            query = f"SELECT * FROM {table} WHERE {account} = %s"
            result = self.database.execute_query(query, username)

        return result
    
    # 在对应的用户账户表查询账户和密码
    def select_current_type_accountTabel_account_password(self,user_type,username, password):
        table,account,password_col,result = None,None,None,None
        if user_type == "学生":
            table = "sms_suser"
            account = "Saccount"
            password_col = "Spassword"
        elif user_type == "教师":
            table = "sms_tuser"
            account = "Taccount"
            password_col = "Tpassword"
        elif user_type == "管理员":
            table = "sms_admin"
            account = "Aaccount"
            password_col = "Apassword"
        else:
            createErrorInfoBar(self,"错误", "未选择账户类型")

        if table and account and password_col:
            # 查询对应的账户表
            query = f"SELECT * FROM {table} WHERE {account} = %s AND {password_col} = %s"
            result = self.database.execute_query(query, (username, password))

        return result

    # 在对应的表查询编号
    def select_current_type_dataTabel(self,user_type,username):
        result = None
        if user_type == "学生":
            table = "sms_students"
            select_no = "Sno"
        elif user_type == "教师":
            table = "sms_teacher"
            select_no = "Tno"

        # 查询对应的数据表
        if user_type and select_no:
            query = f"SELECT {table}.{select_no} FROM {table} WHERE {select_no}= %s"
            result = self.database.execute_query(query, username)

        return result
    
    # 在对应的用户账户表插入初始化账户和密码
    def insert_current_type_accountTabel(self,user_type,username):
        table,account,password_col = None,None,None
        if user_type == "学生":
            table = "sms_suser"
            account = "Saccount"
            password_col = "Spassword"
        elif user_type == "教师":
            table = "sms_tuser"
            account = "Taccount"
            password_col = "Tpassword"
        else:
            createErrorInfoBar(self,"未知错误", "login程序错误")
        if table and account and password_col:
            query = f"INSERT INTO {table} ({account},{password_col}) VALUE (%s,%s)"
            self.database.execute_query(query, (username, username))

    def jump_interface(self,type,username,password):
        self.disconnect_database()
        if type == "学生":
            self.username = username
            self.password = password
            open_student_window(self)
            self.close()  # 关闭login窗口 

        elif type == "教师":
            self.username = username
            self.password = password
            open_teacher_window(self)
            self.close()  # 关闭login窗口 
        elif type == "管理员":
            # open_admin_window(username,password)
            self.username = username
            self.password = password
            open_admin_window(self)
            self.close()  # 关闭login窗口 
            # self.hide()  # 关闭login窗口 
        else:
            createErrorInfoBar(self,"错误", "系统错误")

    def login(self):
        # 获取 用户类型 账号框内容 密码框内容
        user_type = self.user_type_combo.currentText()
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "":
            createErrorInfoBar(self,"输入错误", "账户输入不可为空")
        elif password == "":
            createErrorInfoBar(self,"输入错误", "密码输入不可为空")
        else:
            # 在对应的账户表获取查询账户的结果
            result = self.select_current_type_accountTabel_account(user_type,username)
            
            # 查到了账户
            if result:
                # 查询账号密码成功
                result = self.select_current_type_accountTabel_account_password(user_type,username, password)
                if result:
                    if len(result) == 1:
                        w = Dialog("登录成功", "登录成功！ 请确认OK跳转到下一界面", self)
                        if w.exec():
                            self.jump_interface(user_type,username,password)
                        else:
                            self.label.setText("          欢迎回来！")
                    # 查询主键返回多行值 数据库出现错误
                    else:
                        createErrorInfoBar(self,"未知错误", "数据库错误")
                else:
                    createErrorInfoBar(self,"登录失败", "账户或密码错误")
            # 没有查找到账户 
            elif((user_type == "学生" or user_type == "教师") and username == password) :
                # 可能是第一次登录
                result = self.select_current_type_dataTabel(user_type,username)
                if result:
                    # 返回唯一结果
                    if len(result) == 1:
                        # 第一次登录 插入账户密码
                        self.insert_current_type_accountTabel(user_type,username)
                        w = Dialog("登录成功", "登录成功！ 请确认OK跳转到下一界面", self)
                        if w.exec():
                            self.jump_interface(user_type,username,password)
                        else:
                            self.label.setText("          欢迎回来！")
                    # 查询主键返回多行值 数据库出现错误
                    else:
                        createErrorInfoBar(self,"未知错误", "数据库错误")
                else:
                    createErrorInfoBar(self,"登录失败", "不存在该人员账户 请尽快与管理员核对")
            else:
                createErrorInfoBar(self,"登录失败", "账户或密码错误")
