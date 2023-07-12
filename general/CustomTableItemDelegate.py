from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtWidgets import QApplication, QStyleOptionViewItem

from qfluentwidgets import isDarkTheme, TableItemDelegate

class CustomTableItemDelegate(TableItemDelegate):
    """ Custom table item delegate """

    # 给某一列加上高亮
    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)

        # self.num可能是int也可能是list 
        # 需要判断index.column() 的值是否和self.num不相同
        if isinstance(self.num, int):
            if index.column() != self.num:
                return
        elif isinstance(self.num, list):
            if index.column() not in self.num:
                return
        else:
            return

        if isDarkTheme():
            option.palette.setColor(QPalette.Text, Qt.yellow)
            option.palette.setColor(QPalette.HighlightedText,  QColor("#FFAEB9"))
        else:
            # 普通高亮
            option.palette.setColor(QPalette.Text, Qt.red)
            # 选中高亮
            option.palette.setColor(QPalette.HighlightedText, Qt.blue)
    
    # 设置高亮列
    def set_index_num(self,num):
        self.num = num