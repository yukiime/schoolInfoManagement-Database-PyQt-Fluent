from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont
from PyQt5.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,setThemeColor,isDarkTheme )
from qfluentwidgets import FluentIcon as FIF

class AvatarWidget(NavigationWidget):
    """自定义的 Avatar 小部件类，继承自 NavigationWidget"""

    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
    
    def setAvatr(self,icon_str):
        self.avatar = QImage(icon_str).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def setName(self,name):
        self.name = name

    def paintEvent(self, e):
        painter = QPainter(self)
        # 平滑变换 抗锯齿
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        # 绘制背景 鼠标进入区域
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # 绘制头像
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            font = QFont('Segoe UI')
            font.setPixelSize(14)
            painter.setFont(font)
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, self.name)

