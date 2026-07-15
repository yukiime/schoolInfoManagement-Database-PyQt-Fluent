# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget
from qfluentwidgets import Pivot
from widgets.student_widgets.setting_subWidgets import *

class setting_pivot(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.username = parent.username
        self.password = parent.password
        self.setObjectName("setting_pivot")
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
        self.title_label = QLabel()
        self.setTitleLabel()
        self.vBoxLayout.addWidget(self.title_label, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 40, 0, 10)

        self.resize(910, 800)

    def init_subInterFace(self):
        self.setting_updatePassword = setting_updatePassword(self)
        self.setting_return_login = setting_return_login(self)
        self.setting_setColor = setting_setColor(self)
                 

        # 添加子界面到 QStackedWidget
        # self.addSubInterface(self.ClassInterface, 'ClassInterface', '专业班级')
        self.addSubInterface(self.setting_updatePassword, 'setting_updatePassword', '修改密码')
        self.addSubInterface(self.setting_return_login, 'setting_return_login', '返回登录界面')
        self.addSubInterface(self.setting_setColor, 'setting_setColor', '更改主题颜色')

        # 当 QStackedWidget 的当前界面发生变化时，触发 onCurrentIndexChanged 方法
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        # 设置初始界面为 'songInterface'
        self.stackedWidget.setCurrentWidget(self.setting_updatePassword)
        self.pivot.setCurrentItem(self.setting_updatePassword.objectName())
        self.title_label.setText("你好!   学生用户" + str(self.username))

    def setTitleLabel(self):
        self.title_label = QtWidgets.QLabel()
        self.title_label.setGeometry(QtCore.QRect(180, 160, 520, 35))
        self.title_label.setMinimumSize(QtCore.QSize(320, 30))
        self.title_label.setMaximumSize(QtCore.QSize(520, 35))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(18)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")

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

if __name__ == "__main__":
    # enable dpi scale
    # 启用 DPI 缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 创建应用程序实例
    app = QApplication(sys.argv)
    # 创建 Demo 窗口
    w = setting_pivot()
    # 显示 Demo 窗口
    w.show()
    # 运行应用程序事件循环
    app.exec_()