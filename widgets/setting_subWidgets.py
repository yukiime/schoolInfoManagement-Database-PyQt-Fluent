import pymysql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView, QLineEdit
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_setting_update_password import Ui_setting_update_password
from ui.Ui_setting_return_login import Ui_setting_return_login
from ui.Ui_setting_setColor import Ui_Form

class setting_updatePassword(Ui_setting_update_password):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.username = parent.username
        self.password = parent.password
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()

    def init_widget_UI(self):
        # 密码不可见
        self.old_LineEdit.setEchoMode(QLineEdit.Password)
        self.new_LineEdit.setEchoMode(QLineEdit.Password)
        self.new_LineEdit_2.setEchoMode(QLineEdit.Password)

        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(15, 0, 0, 0)

    def init_slots(self):
        self.update_pushButton.clicked.connect(self.update_password)

    def get_username(self):
        username = self.username_LineEdit.text()
        if username:
            return username
        else:
            createErrorInfoBar(self,"输入错误","没有输入用户名")

    def get_old_password(self):
        old = self.old_LineEdit.text()
        if old:
            return old
        else:
            createErrorInfoBar(self,"输入错误","没有输入密码")

    def check_old(self):
        username = self.get_username()
        old = self.get_old_password()
        
        db = DatabaseConnection()
        db.connect()
        query = "select * from sms_admin WHERE(Aaccount = %s AND Apassword = %s)"
        result = db.execute_query(query,(username,old))
        db.disconnect()
        if result:
            return True
        else:
            createErrorInfoBar(self,"密码错误","原账户密码错误")
            return False
        
    def get_new(self):
        new = self.new_LineEdit.text()
        if new:
            return new
        else:
            createErrorInfoBar(self,"输入错误","新密码不能为空")
    
    def check_new(self):
        new = self.get_new()
        if new:
            if new == self.new_LineEdit_2.text():
                return new
            else:
                createErrorInfoBar(self,"输入错误","两次新密码不相同")
                return None

    def update_password(self):
        if self.check_old():
            new = self.check_new()
            if new:
                try:
                    db = DatabaseConnection()
                    db.connect()
                    query = "UPDATE sms_admin SET Apassword = %s WHERE(Aaccount = %s)"
                    db.execute_query(query,(new,self.username))
                    db.disconnect()
                    createSuccessInfoBar(self,"修改成功","恭喜！！！")
                except pymysql.err.IntegrityError as e:
                    createErrorInfoBar(self,"修改失败", str(e))
                except Exception as e:
                    createErrorInfoBar(self,"修改失败 其他数值错误", str(e))

                
class setting_return_login(Ui_setting_return_login):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()

    def init_widget_UI(self):

        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(15, 0, 0, 0)

    def init_slots(self):
        self.return_pushButton.clicked.connect(self.return_login)

    def return_login(self):
        # print(self.parent().parent().parent().parent().parent().show())
        self.parent().parent().parent().parent().close()

class setting_setColor(Ui_Form):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_widget_UI()
        self.init_slots()

    def init_widget_UI(self):
        self.ComboBox.addItem("蓝色")
        self.ComboBox.addItem("粉色")
        self.ComboBox.addItem("红色")
        self.ComboBox.addItem("绿色")
        self.ComboBox.addItem("褐色")
        
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(15, 0, 0, 0)

    def init_slots(self):
        self.ComboBox.currentIndexChanged.connect(self.set_current_color)

    def set_current_color(self):
        color_map = {
            "蓝色": '#0078d4',
            "粉色": '#d40078',
            "红色": '#d40700',
            "绿色": '#14d94f',
            "褐色": '#d4ab08',
        }
        hex_color = color_map.get(self.ComboBox.currentText())
        if not hex_color:
            return
        # 向上查找拥有 setColor 方法的顶层界面窗口，避免写死父窗口层级
        target = self.parent()
        while target is not None and not hasattr(target, 'setColor'):
            target = target.parent()
        if target is not None:
            target.setColor(hex_color)



