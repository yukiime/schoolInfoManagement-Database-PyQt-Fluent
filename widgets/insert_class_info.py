import pymysql
from PyQt5.QtCore import Qt,QEasingCurve
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_insert_class_info import Ui_Inster_class_info

class inster_class_info(Ui_Inster_class_info):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()
        self.init_data()

    def init_widget_UI(self):
        self.Cno_LineEdit.setText("040821")
        # 设置不换行 
        self.Class_data_tableWidget.setWordWrap(False)
        self.Major_data_tableWidget.setWordWrap(False)
        # 隐藏垂直表头
        # self.data_tableWidget.verticalHeader().hide()
        # 自适应宽度
        # self.data_tableWidget.resizeColumnsToContents()
        # 水平表头的列宽自适应模式 / 关掉比较好看
        # self.data_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 自动排序功能
        self.Class_data_tableWidget.setSortingEnabled(True)
        self.Major_data_tableWidget.setSortingEnabled(True)
        # 禁止编辑
        # self.data_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(15, 40, 0, 0)

        # customize scroll animation
        self.Class_SmoothScrollArea.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.Class_SmoothScrollArea.horizontalScrollBar().setValue(1800)
        self.Class_SmoothScrollArea.setStyleSheet("QScrollArea {border: none;}")       
        self.Maior_SmoothScrollArea.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.Maior_SmoothScrollArea.horizontalScrollBar().setValue(1800)
        self.Maior_SmoothScrollArea.setStyleSheet("QScrollArea {border: none;}")

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.Class_data_tableWidget)
        ctd.set_index_num([0])
        self.Class_data_tableWidget.setItemDelegate(ctd)
        self.Major_data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.Major_select_pushButton.clicked.connect(self.change_Major_DataView)
        self.Class_select_PushButton.clicked.connect(self.select_class_info)
        self.insert_pushButton.clicked.connect(self.insertData)
        self.Major_data_tableWidget.cellClicked.connect(self.tableItems_set_Mno)

    def getCno(self):
        cno_str = self.Cno_LineEdit.text()
        if cno_str :
            try:
                Sno_number = int(cno_str)
                if(len(cno_str)!=8):
                    raise ValueError()
                return cno_str
            except ValueError:
            # 类型转换错误，弹窗提示用户
                createErrorInfoBar(self,"输入错误", "班级编号输入无效 请输入一个有效的8位整数。")

    def getData(self):
        name_str = self.Name_LineEdit.text()
        cno_str = self.getCno()
        mno_str = self.Mno_LineEdit.text()

        # 验证mno_str
        mno_isRight = False 
        for row in range(self.Major_data_tableWidget.rowCount()):
            item = self.Major_data_tableWidget.item(row, 0)  # 第0列的单元格
            if item is not None and item.text() == mno_str:
                mno_isRight = True
                break
        if not mno_isRight:
            mno_str = 0
            createErrorInfoBar(self,"专业编号输入无效", "不存在该专业")

        return cno_str,mno_str,name_str

    def insertData(self):
        try:
            cno_str,mno_str,name_str = self.getData()
            if mno_str != 0:
                db = DatabaseConnection()
                db.connect()
                query = "INSERT INTO sms_class VALUES(%s,%s,%s)"
                db.execute_query(query,(cno_str,mno_str,name_str))
                db.disconnect()
                createSuccessInfoBar(self,"添加成功","恭喜！！！")
        except pymysql.err.IntegrityError as e:
            # 捕获 pymysql.err.IntegrityError 异常
            createErrorInfoBar(self,"添加失败 班级编号冲突", str(e))
        except Exception as e:
            # 捕获其他继承自 Exception 的异常
            createErrorInfoBar(self,"添加失败 其他数值错误", str(e))

    def init_data(self):
        self.tableFlag = False
        db = DatabaseConnection()
        db.connect()
        query = "SELECT * FROM sms_major"
        result = db.execute_query(query)
        self.fill_Major_table(result)
        for row in range(self.Major_data_tableWidget.rowCount()):
            self.Major_data_tableWidget.hideRow(row)

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
        self.Major_data_tableWidget.resizeColumnToContents(1)

    # Major table点击事件
    def tableItems_set_Mno(self,row,colum):
        text = self.Major_data_tableWidget.item(row,0).text()
        self.Mno_LineEdit.setText(text)
        self.Mno_Cno_LineEdit.setText(text)
        self.Cno_LineEdit.setText(text[:4])

    def change_Major_DataView(self):
        # 当前是可以看的
        if self.tableFlag:
            for row in range(self.Major_data_tableWidget.rowCount()):
                self.Major_data_tableWidget.hideRow(row)
            self.Major_select_pushButton.setText("查看专业列表")
            self.Major_resultHint_label.setText("专业列表已关闭")
            self.tableFlag = False
            createSuccessInfoBar(self,"关闭表成功", "请正确输入专业编号")
        else:
            for row in range(self.Major_data_tableWidget.rowCount()):
                self.Major_data_tableWidget.showRow(row)
            self.Major_select_pushButton.setText("关闭专业列表")
            self.Major_resultHint_label.setText("专业列表如下")
            self.tableFlag = True
            createSuccessInfoBar(self,"打开表成功", "请参考专业表输入专业编号")

    def select_class_info(self):
        mno_str = self.Mno_Cno_LineEdit.text()
        if mno_str:
            db = DatabaseConnection()
            db.connect()
            query = "SELECT * FROM sms_class WHERE sms_class.Mno = %s"
            result = db.execute_query(query,mno_str)
            db.disconnect()
            
            if result:
                col_names = ['班级编号','专业编号','班级名称']
                index_num = len(result)
                col_num = 3
                self.Class_data_tableWidget.setRowCount(index_num)
                self.Class_data_tableWidget.setColumnCount(col_num)
                self.Class_data_tableWidget.setHorizontalHeaderLabels(col_names)
                for i, indexInfo in enumerate(result):
                    for j in range(col_num):
                        item = QTableWidgetItem(str(indexInfo[j]))
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.Class_data_tableWidget.setItem(i, j, item)

                self.Class_data_tableWidget.setColumnWidth(0,150)
                self.Class_data_tableWidget.setColumnWidth(1,100)
                self.Class_data_tableWidget.setColumnWidth(2,200)
                # self.Class_data_tableWidget.resizeColumnToContents(2)
                createSuccessInfoBar(self,"查询成功","恭喜！！！")
            else:
                createWarningInfoBar(self,"查询成功","该专业下暂无班级")
        else:
            createErrorInfoBar(self,"查询失败","请先输入专业编号")


