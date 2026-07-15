from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.student_ui.Ui_info import Ui_info
import pymysql

class Students_info(Ui_info):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        # self.init_slots()
        self.initData(parent.username)
        self.init_widget_UI()
    
    def initData(self,username):
        db = DatabaseConnection()
        db.connect()
        query = "select * from sms_students WHERE(Sno = %s)"
        result = db.execute_query(query,username)
        db.disconnect()
        # self.label_Sno.setText()
        print(result)

    def init_widget_UI(self):
        self.setContentsMargins(0, 80, 0, 0)

    