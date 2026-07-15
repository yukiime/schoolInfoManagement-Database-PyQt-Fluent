from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.teacher_ui.Ui_info import Ui_info


class teacher_info(Ui_info):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        # self.init_slots()
        self.init_widget_UI()

    def init_widget_UI(self):
        self.setContentsMargins(0, 80, 0, 0)

    