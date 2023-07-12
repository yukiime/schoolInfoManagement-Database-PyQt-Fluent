from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QAction
from PyQt5.QtWidgets import QMenuBar, QMenu

from qframelesswindow import TitleBar


class CustomTitleBar(TitleBar):
    """自定义的带图标和标题的标题栏类，继承自 TitleBar"""

    def __init__(self, parent):
        super().__init__(parent)
        
        # 添加窗口图标
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18) # 固定大小为 18x18 像素
        # 添加标题标签
        self.titleLabel = QLabel(self)
        self.titleLabel.setObjectName('titleLabel')
        # 菜单栏
        # self.menuBar = QMenuBar(self)
        
        self.insertWidget_ALL()
        self.init_window_slots()
    
    # 槽函数
    def init_window_slots(self):
        # 槽函数 在窗口图标发生变化时更新自定义标题栏的图标
        self.window().windowIconChanged.connect(self.setIcon)
        self.window().windowTitleChanged.connect(self.setTitle)
        # self.setmenubar()

    # 插入布局
    def insertWidget_ALL(self):
        # self.hBoxLayout是一个 QHBoxLayout 对象 超类中self.hBoxLayout = QHBoxLayout(self)
        # 插入间距 第二个参数是和同级的另一个部件之间的距离
        self.hBoxLayout.insertSpacing(0, 10)  
        # 插入到指定位置 
        # 第一个参数是插入布局位置 
        # 第二个是插入部件 
        # 第三个是拉伸因子 
        # 左对齐和底部对齐
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        # self.hBoxLayout.insertWidget(3, self.menuBar, 0, Qt.AlignLeft | Qt.AlignBottom)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))
    
    # TODO:改成传入fileMenu的list
    def setmenubar(self):
        pass
        # # 创建一个菜单
        # fileMenu = QMenu("文件", self)

        # # 创建两个菜单项
        # openAction = QAction("打开", self)
        # saveAction = QAction("保存", self)

        # # 将菜单项添加到菜单中
        # fileMenu.addAction(openAction)
        # fileMenu.addAction(saveAction)

        # # 将菜单添加到菜单栏中
        # self.menuBar.addMenu(fileMenu)