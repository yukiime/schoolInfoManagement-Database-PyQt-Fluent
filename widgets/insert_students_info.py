import itertools
import pymysql
from PyQt5.QtCore import Qt,QEasingCurve
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_insert_students_info import Ui_Inster_students_info

class inster_students_info(Ui_Inster_students_info):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()
        self.init_data()

    def init_widget_UI(self):
        self.Sno_LineEdit.setText("2021033402")
        self.Sex_ComboBox.addItems(["男","女"])
        self.Sex_ComboBox.setCurrentIndex(0)
        # 设置不换行 
        self.data_tableWidget.setWordWrap(False)
        self.students_data_tableWidget.setWordWrap(False)
        # 隐藏垂直表头
        # self.data_tableWidget.verticalHeader().hide()
        # 自适应宽度
        # self.data_tableWidget.resizeColumnsToContents()
        # 水平表头的列宽自适应模式 / 关掉比较好看
        # self.data_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 自动排序功能
        self.data_tableWidget.setSortingEnabled(True)
        self.students_data_tableWidget.setSortingEnabled(True)
        # 禁止编辑
        # self.data_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(15, 20, 0, 0)

        # customize scroll animation
        self.SmoothScrollArea.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.SmoothScrollArea.horizontalScrollBar().setValue(1800)
        self.SmoothScrollArea.setStyleSheet("QScrollArea {border: none;}")       
        self.SmoothScrollArea_2.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.SmoothScrollArea_2.horizontalScrollBar().setValue(1800)
        self.SmoothScrollArea_2.setStyleSheet("QScrollArea {border: none;}")

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.data_tableWidget)
        ctd.set_index_num([0,1])
        self.data_tableWidget.setItemDelegate(ctd)
        self.students_data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.select_pushButton.clicked.connect(self.change_DataView)
        self.insert_pushButton.clicked.connect(self.insertData)
        self.Major_ComboBox.currentIndexChanged.connect(self.major_comboBox_changed)
        self.data_tableWidget.cellClicked.connect(self.tableItems_set_Cno)
        self.students_select_PushButton.clicked.connect(self.select_student_info)

    def getSno(self):
        Sno_str = self.Sno_LineEdit.text()
        if Sno_str :
            try:
                Sno_number = int(Sno_str)
                if(len(Sno_str)!=12):
                    raise ValueError()
                return Sno_str
            except ValueError:
            # 类型转换错误，弹窗提示用户
                createErrorInfoBar(self,"输入错误", "学号输入无效，请输入一个有效的十二位整数。")

    def getData(self):
        name_str = self.Name_LineEdit.text()
        sex_str = self.Sex_ComboBox.currentText()
        age_str = self.Age_SpinBox.text()
        area_str = self.Area_LineEdit.text()
        cno_str = self.Class_LineEdit.text()

        # 验证cno_str
        cno_isRight = False 
        for row in range(self.data_tableWidget.rowCount()):
            item = self.data_tableWidget.item(row, 0)  # 第3列的单元格
            if item is not None and item.text() == cno_str:
                cno_isRight = True
                break
        if not cno_isRight:
            cno_str = 0
            createErrorInfoBar(self,"班级编号输入无效", "不存在该班级")

        return name_str,sex_str,age_str,area_str,cno_str

    def insertData(self):
        try:
            sno_str = self.getSno()
            name_str,sex_str,age_str,area_str,cno_str = self.getData()
            if cno_str != 0:
                db = DatabaseConnection()
                db.connect()
                query = "INSERT INTO sms_students VALUES(%s,%s,%s,%s,%s,%s,'0')"
                db.execute_query(query,(sno_str,cno_str,name_str,sex_str,age_str,area_str))
                db.disconnect()
                createSuccessInfoBar(self,"添加成功","恭喜！！！")
        except pymysql.err.IntegrityError as e:
            # 捕获 pymysql.err.IntegrityError 异常
            createErrorInfoBar(self,"添加失败 学号冲突", str(e))
        except Exception as e:
            # 捕获其他继承自 Exception 的异常
            createErrorInfoBar(self,"添加失败 其他数值错误", str(e))

    def init_data(self):
        self.tableFlag = False
        db = DatabaseConnection()
        db.connect()
        query = "SELECT sms_class.Cno,sms_class.Cname,sms_major.*FROM sms_class,sms_major WHERE ( sms_class.Mno = sms_major.Mno )"
        result = db.execute_query(query)
        self.fill_table(result)
        for row in range(self.data_tableWidget.rowCount()):
            self.data_tableWidget.hideRow(row)

    # 这个函数的逻辑是先读取表中的数据,然后填充combobox
    def set_Major_ComboBox(self):
        # 因为是有筛选完数据之后调用的 所以一定有数据
        credits_unique_values = set()
        rows = self.data_tableWidget.rowCount()
        for row in range(rows):
            cell_value = self.data_tableWidget.item(row, 3).text()
            credits_unique_values.add(cell_value)
        
        # 默认全选
        self.Major_ComboBox.addItem("全选")
        for item in credits_unique_values:
            self.Major_ComboBox.addItem(item)
        self.Major_ComboBox.setCurrentIndex(0)

    def change_DataView(self):
        # 当前是可以看的
        if self.tableFlag:
            for row in range(self.data_tableWidget.rowCount()):
                self.data_tableWidget.hideRow(row)
            self.Major_ComboBox.clear()
            self.Major_ComboBox.setText("默认全选")
            self.select_pushButton.setText("查看专业班级列表")
            self.tableFlag = False
            createSuccessInfoBar(self,"关闭表成功", "请正确输入班级编号")
        else:
            for row in range(self.data_tableWidget.rowCount()):
                self.data_tableWidget.showRow(row)
            self.select_pushButton.setText("关闭专业班级列表")
            self.set_Major_ComboBox()
            self.tableFlag = True
            createSuccessInfoBar(self,"打开表成功", "请参考班级表输入班级编号")

    def fill_table(self,data):
        index_num = len(data)
        col_num = 4
        # 设置行数 列数
        self.data_tableWidget.setRowCount(index_num)
        self.data_tableWidget.setColumnCount(col_num)
        col_names=['班级编号','班级名','专业编号','专业名称']
        self.data_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                item = QTableWidgetItem(str(indexInfo[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.data_tableWidget.setItem(i, j, item)
               
        # 调整列宽度
        self.data_tableWidget.resizeColumnToContents(0)
        self.data_tableWidget.resizeColumnToContents(1)
        self.data_tableWidget.resizeColumnToContents(2)
        self.data_tableWidget.resizeColumnToContents(3)

    # 获取comboBox的值筛选table
    def major_comboBox_changed(self):
        major_str = self.Major_ComboBox.currentText()
        for row in range(self.data_tableWidget.rowCount()):
            item = self.data_tableWidget.item(row, 3)  # 第3列的单元格
            if item is not None and item.text() == major_str:
                self.data_tableWidget.showRow(row)
            else:
                self.data_tableWidget.hideRow(row)
    
    # table点击事件
    def tableItems_set_Cno(self,row,colum):
        text = self.data_tableWidget.item(row,0).text()
        self.Class_LineEdit.setText(text)
        sno_text = '20' + text[4:6] + text[:4] + text[-2:]
        self.Sno_LineEdit.setText(sno_text)
        self.students_Cno_LineEdit.setText(text)

    def select_student_info(self):
        cno_str = self.students_Cno_LineEdit.text()
        if cno_str:
            db = DatabaseConnection()
            db.connect()
            query = "SELECT sms_students.Cno,sms_students.Sno,sms_students.Sname FROM sms_students WHERE sms_students.Cno = %s"
            result = db.execute_query(query,cno_str)
            db.disconnect()
            
            if result:
                col_names = ['班级编号','学号','姓名']
                index_num = len(result)
                col_num = 3
                self.students_data_tableWidget.setRowCount(index_num)
                self.students_data_tableWidget.setColumnCount(col_num)
                self.students_data_tableWidget.setHorizontalHeaderLabels(col_names)
                for i, indexInfo in enumerate(result):
                    for j in range(col_num):
                        item = QTableWidgetItem(str(indexInfo[j]))
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.students_data_tableWidget.setItem(i, j, item)

                self.students_data_tableWidget.resizeColumnToContents(0)
                self.students_data_tableWidget.resizeColumnToContents(1)
                self.students_data_tableWidget.resizeColumnToContents(2)
                createSuccessInfoBar(self,"查询成功","恭喜！！！")
            else:
                createWarningInfoBar(self,"查询成功","该班级下暂无学生")
        else:
            createErrorInfoBar(self,"查询失败","请先输入班级编号")


