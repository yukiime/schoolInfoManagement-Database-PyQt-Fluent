import pymysql
from PyQt5.QtCore import Qt,QEasingCurve
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_insert_major_info import Ui_Inster_major_info

class inster_major_info(Ui_Inster_major_info):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        # 设置不换行 
        self.Major_data_tableWidget.setWordWrap(False)
        # 隐藏垂直表头
        # self.data_tableWidget.verticalHeader().hide()
        # 自适应宽度
        # self.data_tableWidget.resizeColumnsToContents()
        # 水平表头的列宽自适应模式 / 关掉比较好看
        # self.data_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 自动排序功能
        self.Major_data_tableWidget.setSortingEnabled(True)
        # 禁止编辑
        # self.data_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(15, 60, 0, 0)

        # customize scroll animation
        self.SmoothScrollArea.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.SmoothScrollArea.horizontalScrollBar().setValue(1800)
        self.SmoothScrollArea.setStyleSheet("QScrollArea {border: none;}")       

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.Major_data_tableWidget)
        ctd.set_index_num([0])
        self.Major_data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.select_pushButton.clicked.connect(self.change_Major_DataView)
        self.insert_pushButton.clicked.connect(self.insertData)

    def getMno(self):
        mno_str = self.Mno_LineEdit.text()
        if mno_str :
            try:
                Sno_number = int(mno_str)
                if(len(mno_str)!=4):
                    raise ValueError()
                return mno_str
            except ValueError:
            # 类型转换错误，弹窗提示用户
                createErrorInfoBar(self,"输入错误", "专业编号输入无效 请输入一个有效的4位整数。")

    def getData(self):
        name_str = self.Name_LineEdit.text()
        mno_str = self.getMno()

        return mno_str,name_str

    def insertData(self):
        try:
            mno_str,name_str = self.getData()
            if mno_str != 0:
                db = DatabaseConnection()
                db.connect()
                query = "INSERT INTO sms_major VALUES(%s,%s)"
                db.execute_query(query,(mno_str,name_str))
                db.disconnect()
                createSuccessInfoBar(self,"添加成功","恭喜！！！")
                self.select_pushButton.setText("刷新专业列表")
        except pymysql.err.IntegrityError as e:
            # 捕获 pymysql.err.IntegrityError 异常
            createErrorInfoBar(self,"添加失败 专业编号冲突", str(e))
        except Exception as e:
            # 捕获其他继承自 Exception 的异常
            createErrorInfoBar(self,"添加失败 其他数值错误", str(e))

    def fill_Major_table(self,data):
        index_num = len(data)
        col_num = 2
        # 设置行数 列数
        self.Major_data_tableWidget.setRowCount(index_num)
        self.Major_data_tableWidget.setColumnCount(col_num)
        col_names=['专业编号','专业名称']
        self.Major_data_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                item = QTableWidgetItem(str(indexInfo[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.Major_data_tableWidget.setItem(i, j, item)
               
        # 调整列宽度
        self.Major_data_tableWidget.setColumnWidth(0,150)
        self.Major_data_tableWidget.setColumnWidth(1,300)
        # self.Major_data_tableWidget.resizeColumnToContents(300)

    def change_Major_DataView(self):
        db = DatabaseConnection()
        db.connect()
        query = "SELECT * FROM sms_major"
        result = db.execute_query(query)
        self.fill_Major_table(result)
        if self.select_pushButton.text() == "刷新专业列表":
            self.select_pushButton.setText("查看专业列表")
            createSuccessInfoBar(self,"刷新表成功", "请参考专业表输入专业编号")
        else:
            createSuccessInfoBar(self,"查看表成功", "请参考专业表输入专业编号")



import sys
if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = inster_major_info()
    w.show()
    app.exec_()