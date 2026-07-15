# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel
from qfluentwidgets import Pivot
from widgets.students_grade_year_widget import students_grade_year_widget
from widgets.students_info_subWidgets import *


class students_info_pivot(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setObjectName("students_info_pivot_1")
        self.setup_UI()
        self.init_subInterFace()

    def setup_UI(self):
        # 创建一个垂直布局管理器
        self.vBoxLayout = QVBoxLayout(self)
        # 创建一个 Pivot 控件
        self.pivot = Pivot(self)
        # 创建一个 QStackedWidget 控件
        self.stackedWidget = QStackedWidget(self)
        # 将 Pivot 控件和 QStackedWidget 控件添加到垂直布局中
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 40, 0, 10)

        self.resize(910, 800)

    # # 设置自定义样式表
    # def init_stylesheet(self):
    #     self.setStyleSheet("""
    #         QLabel{
    #             font: 20px 'Segoe UI';
    #             background: rgb(242,242,242);
    # #           我觉得圆角好看一些 但是关系不大
    #             border-radius: 8px;
    #         }
    #     """)

    def init_subInterFace(self):
        self.SnoInterface = Students_info_Sno( self)
        self.AreaInterface = Students_info_Area(self)
        self.AgeInterface = Students_info_Age(self)
        self.CreditsInterface = Students_info_Credit(self)
        self.ClassInterface = Students_info_Class(self)                        

        # 添加子界面到 QStackedWidget
        # self.addSubInterface(self.ClassInterface, 'ClassInterface', '专业班级')
        self.addSubInterface(self.SnoInterface, 'SnoInterface', '学号')
        self.addSubInterface(self.AreaInterface, 'AreaInterface', '地区')
        self.addSubInterface(self.AgeInterface, 'AgeInterface', '年龄')
        self.addSubInterface(self.CreditsInterface, 'CreditsInterface', '学分')
        self.addSubInterface(self.ClassInterface, 'ClassInterface', '专业班级')

        # 当 QStackedWidget 的当前界面发生变化时，触发 onCurrentIndexChanged 方法
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        # 设置初始界面为 'songInterface'
        self.stackedWidget.setCurrentWidget(self.ClassInterface)
        self.pivot.setCurrentItem(self.ClassInterface.objectName())


    def addSubInterface(self, widget: QLabel, objectName, text):
        # 设置子界面的对象名称、文本和对齐方式
        widget.setObjectName(objectName)
        # 将子界面添加到 QStackedWidget 中
        self.stackedWidget.addWidget(widget)

        # 在 Pivot 控件中添加一个项目
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        # 当 QStackedWidget 的当前界面发生变化时，更新 Pivot 控件的当前项目
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())

