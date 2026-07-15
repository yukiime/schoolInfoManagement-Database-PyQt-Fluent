# coding:utf-8
import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont
from PyQt5.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,setThemeColor,
                            isDarkTheme, setTheme, Theme, qrouter)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow
from general.AvatarWidget import AvatarWidget
from general.CustomTitleBar import CustomTitleBar
from widgets.students_grade_year_widget import students_grade_year_widget
from widgets.students_info_pivot import students_info_pivot
from widgets.students_lesson_credits import Students_lesson_credits
from widgets.insert_students_info import inster_students_info
from widgets.insert_class_info import inster_class_info
from widgets.insert_major_info import inster_major_info
from widgets.delete_student import delete_student
from widgets.insertAndUpdate_grade import insertAndUpdate_grade
from widgets.delete_grade import delete_grade
from widgets.schedule_student import schedule_student
from widgets.manipulate_lesson_grade import manipulate_lesson_grade
from widgets.setting_pivot import setting_pivot
from widgets.schedule_class import schedule_class
from widgets.schedule_teacher import schedule_teacher
from widgets.students_avgGrade_year_widget import students_avgGrade_year_widget
from widgets.students_lesson_credits_year import Students_lesson_credits_year

class AdminWindow(FramelessWindow):
    """主窗口类，继承自 FramelessWindow"""

    def __init__(self,parent=None):
        # super().__init__(parent=parent)
        super().__init__()
        # 使用浅色主题模式 qss会用到
        setTheme(Theme.LIGHT)
        # 改变导航栏 按钮 颜色 #d40078
        setThemeColor('#0078d4')
        # 标题栏
        self.setTitleBar(CustomTitleBar(self))

        self.setObjectName("ADMIN")
        self.username = parent.username
        self.password = parent.password
        print(parent.show())

        # 创建导航栏布局
        self.creat_Navigation_stack()
        # 初始化布局
        self.initLayout()
        # 添加导航项
        self.initNavigation()
        self.initWindow()


    def initLayout(self):
        self.hBoxLayout = QHBoxLayout(self)
        # 水平布局中的控件之间的间距为 0
        self.hBoxLayout.setSpacing(0)
        # 水平布局的边距为 0 即没有边距 
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        # 将导航界面部件加入布局
        self.hBoxLayout.addWidget(self.navigationInterface)
        # 将堆叠窗口部件加入布局
        self.hBoxLayout.addWidget(self.stackWidget)
        # 堆叠窗口部件在布局中的拉伸因子为 1 这意味着它会占据尽可能多的水平空间 
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)
        # 将标题栏置于窗口的最顶层 以确保它显示在其他部件的前面 
        self.titleBar.raise_()
        # 将导航界面的 displayModeChanged 信号连接到标题栏的 raise_ 槽函数 
        # 这样当导航界面的显示模式发生变化时 会启动槽函数 使标题栏会被置于最顶层 
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)
    
    def creat_Navigation_stack(self):
        # 导航栏 传入窗口作为父对象
        self.navigationInterface = NavigationInterface(self, showMenuButton=True, showReturnButton=True)
        # 堆叠窗口部件
        self.stackWidget = QStackedWidget(self)

        # 创建子界面
        self.students_info = students_info_pivot(self)
        self.insert_students_info = inster_students_info(self)
        self.insert_class_info = inster_class_info(self)
        self.inster_major_info = inster_major_info(self)
        self.delete_student = delete_student(self)
        self.insertAndUpdate_grade = insertAndUpdate_grade(self)
        self.delete_grade = delete_grade(self)
        self.schedule_student = schedule_student(self)
        self.manipulate_lesson_grade = manipulate_lesson_grade(self)
        self.schedule_class = schedule_class(self)
        self.schedule_teacher = schedule_teacher(self)
        self.students_avgGrade_year = students_avgGrade_year_widget(self)

        self.student_grade_byYear = students_grade_year_widget(self)
        # self.student_total_credits = Students_lesson_credits(self)
        self.Students_lesson_credits_year = Students_lesson_credits_year(self)

        self.settingInterface = setting_pivot(self)

    def createAvw_andAdd(self):

        # self.navigationInterface.addWidget(
        #     routeKey='temp',
        #     widget=AvatarWidget(),
        #     onClick=lambda: self.switchTo(self.searchInterface),
        #     position=NavigationItemPosition.SCROLL,
        #     tooltip="hello ha"
        # )

        avw = AvatarWidget()
        # if self.username == "000":
        #     avw.setName("Mio")
        # else:

        avw.setName("管理员" + str(self.username))
        avw.setAvatr("icon/admin.jpg")
        # 添加自定义小部件到底部
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=avw,
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM
        )

    def initNavigation(self):
        # 部件 图标 文本名
        self.addSubInterface(self.students_info, FIF.FEEDBACK, '学生信息查询', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.schedule_student, FIF.PASTE, '学生课程表', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.insert_students_info, FIF.EDIT, '添加学生信息', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.delete_student, FIF.DELETE, '删除学生', NavigationItemPosition.SCROLL)

        self.navigationInterface.addSeparator(NavigationItemPosition.SCROLL)

        self.addSubInterface(self.students_avgGrade_year, FIF.TRANSPARENT, '按学级进行学生学分成绩排名', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Students_lesson_credits_year, FIF.SEARCH, '学生课程成绩及学分学年统计', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.student_grade_byYear, FIF.SEARCH, '按学年统计学生成绩', NavigationItemPosition.SCROLL)

        self.navigationInterface.addSeparator(NavigationItemPosition.SCROLL)

        # self.addSubInterface(self.student_total_credits, FIF.SEARCH, '学生所学课程及学分统计', NavigationItemPosition.SCROLL)
        # self.addSubInterface(self.student_grade_byYear, FIF.SEARCH, '学生成绩按学年查询', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.insertAndUpdate_grade, FIF.EDIT, '添加或更新学生成绩记录', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.delete_grade, FIF.DELETE, '删除学生成绩记录', NavigationItemPosition.SCROLL)

        self.navigationInterface.addSeparator(NavigationItemPosition.SCROLL)

        # self.addSubInterface(self.lesson_info, FIF.SEARCH, '课程的基本信息', NavigationItemPosition.SCROLL)
        # self.addSubInterface(self.class_info, FIF.SEARCH, '班级的基本信息', NavigationItemPosition.SCROLL)
        # self.addSubInterface(self.class_students_info, FIF.SEARCH, '班级的学生信息', NavigationItemPosition.SCROLL)


        self.addSubInterface(self.manipulate_lesson_grade, FIF.PENCIL_INK, '课程成绩修改界面', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.schedule_teacher, FIF.PASTE, '教师任课表', NavigationItemPosition.SCROLL)
        
        self.navigationInterface.addSeparator(NavigationItemPosition.SCROLL)

        self.addSubInterface(self.insert_class_info, FIF.EDIT, '添加班级信息', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.inster_major_info, FIF.EDIT, '添加专业信息', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.schedule_class, FIF.PASTE, '班级课程表', NavigationItemPosition.SCROLL)
        self.navigationInterface.addSeparator(NavigationItemPosition.SCROLL)


        # self.navigationInterface.addSeparator(NavigationItemPosition.BOTTOM)

        self.createAvw_andAdd()
        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # !IMPORTANT: 不要忘记设置默认路由键
        # 设置默认的路由键 qrouter 是一个路由管理器 用于管理子界面的切换 该方法用于设置默认显示的子界面 
        # 接受两个参数：self.stackWidget 是子界面的容器对象 self.musicInterface.objectName() 是默认显示的子界面的对象名称 
        qrouter.setDefaultRouteKey(self.stackWidget, self.students_info.objectName())

        # 设置最大宽度
        self.navigationInterface.setExpandWidth(300)

        # 槽函数绑定 当currentChanged时
        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)

        # 设置堆叠窗口的当前显示界面的索引为 
        self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        self.resize(1000, 800)
        self.setWindowIcon(QIcon('icon/admin_bar.jpg'))
        self.setWindowTitle('管理员界面')
        # 设置标题栏的背景为样式化背景
        # Qt.WA_StyledBackground 是一个窗口属性 用于启用窗口或窗口部件使用样式表来绘制背景
        self.titleBar.setAttribute(Qt.WA_StyledBackground)
        
        # 窗口位置
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.setQss()

    # 部件 图标 文本名 默认加到上一层
    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP):
        """添加子界面"""
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            # 路由键
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            # 响应函数
            onClick=lambda: self.switchTo(interface),
            position=position,
            # 提示文本
            tooltip=text
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'img/{color}.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    # 切换子界面到顶部
    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    # 记录当前界面 以便回溯
    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackWidget, widget.objectName())

    def showMessageBox(self):
        message = str(self.username)
        w = MessageBox(
            '您好，管理员'+ message,
            '欢迎来到高校信息数据库管理系统 如需更改相关设置,请前往设置界面',
            self
        )
        w.exec()

    def setColor(self,color):
        setThemeColor(color)

    def getParent(self):
        print(self.parent())

    # 当窗口大小改变时 标题栏会根据新的窗口大小进行相应的位置调整和尺寸
    def resizeEvent(self, e):
        # 将标题栏移动到窗口的 (46, 0) 坐标
        self.titleBar.move(46, 0)
        # 大小设置为窗口宽度减去 46
        self.titleBar.resize(self.width()-46, self.titleBar.height())


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = AdminWindow()
    w.show()
    app.exec_()
