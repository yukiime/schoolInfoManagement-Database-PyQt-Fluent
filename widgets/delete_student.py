import pymysql
from PyQt5.QtCore import Qt,QEasingCurve
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_delete_student import Ui_delete_student

class delete_student(Ui_delete_student):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        self.Sno_LineEdit.setText("202203050101")
        # 设置不换行 
        self.lesson_data_tableWidget.setWordWrap(False)
        self.Student_info_tableWidget.setWordWrap(False)
        # 隐藏垂直表头
        self.lesson_data_tableWidget.verticalHeader().hide()
        self.Student_info_tableWidget.verticalHeader().hide()
        # 自适应宽度
        # self.data_tableWidget.resizeColumnsToContents()
        # 水平表头的列宽自适应模式 / 关掉比较好看
        # self.data_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 自动排序功能
        self.lesson_data_tableWidget.setSortingEnabled(True)
        self.Student_info_tableWidget.setSortingEnabled(True)
        # 禁止编辑
        # self.lesson_data_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Student_info_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(40, 40, 0, 0)

        # customize scroll animation
        self.SmoothScrollArea.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.SmoothScrollArea.horizontalScrollBar().setValue(1800)
        self.SmoothScrollArea.setStyleSheet("QScrollArea {border: none;}")       

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.lesson_data_tableWidget)
        ctd.set_index_num([2,3])
        self.lesson_data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.delete_pushButton.clicked.connect(self.deletetData)
        self.select_pushButton.clicked.connect(self.select_student)

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
                createErrorInfoBar(self,"输入错误", "学号输入无效，请输入一个有效的十二位整数。",InfoBarPosition.TOP)

    def deletetData(self):
        try:
            sno_str = self.getSno()
            if sno_str:
                db = DatabaseConnection()
                db.connect()
                query = "DELETE FROM sms_students WHERE Sno = %s"
                db.execute_query(query,sno_str)
                db.disconnect()
                createSuccessInfoBar(self,"删除成功","恭喜！！！")
        except pymysql.err.IntegrityError as e:
            # 捕获 pymysql.err.IntegrityError 异常
            createErrorInfoBar(self,"删除失败 学号冲突", str(e))
        except Exception as e:
            # 捕获其他继承自 Exception 的异常
            createErrorInfoBar(self,"删除失败 其他数值错误", str(e))

    def select_student(self):
        sno_str = self.getSno()
        if sno_str:
            db = DatabaseConnection()
            db.connect()
            query = "SELECT sms_major.Mname,sms_class.Cname,sms_students.* FROM sms_class,sms_major,sms_students WHERE ( sms_students.Sno = %s AND sms_students.Cno = sms_class.Cno AND sms_class.Mno = sms_major.Mno )"
            result = db.execute_query(query,sno_str)
            if result:
                self.fill_student_info_table(result)
                query = "get_courses_and_grades_by_student"
                sno_str = [sno_str]
                result,cols = db.callproc_query(query,sno_str)
                if result and cols:
                    self.fill_student_lesson_table(result,cols)
                else:
                    for row in range(self.lesson_data_tableWidget.rowCount()):
                        self.lesson_data_tableWidget.hideRow(row)
                    createWarningInfoBar(self,"提示", "该学生未选修课程",InfoBarPosition.TOP)
            else:
                createErrorInfoBar(self,"查看失败", "不存在该学生",InfoBarPosition.TOP)
            db.disconnect()
        

    def fill_student_info_table(self,data):
        col_names=["所属专业","所属班级名","学号","所属班级编号","姓名","性别","年龄","生源地","已修学分"]
        index_num = len(data)
        col_num = 9
        # 设置行数 列数
        self.Student_info_tableWidget.setRowCount(index_num)
        self.Student_info_tableWidget.setColumnCount(col_num)
        self.Student_info_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                item = QTableWidgetItem(str(indexInfo[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.Student_info_tableWidget.setItem(i, j, item)
        # 调整列宽度
        # self.Student_info_tableWidget.setColumnWidth(0,150)
        self.Student_info_tableWidget.resizeColumnToContents(0)
        self.Student_info_tableWidget.resizeColumnToContents(1)
        self.Student_info_tableWidget.resizeColumnToContents(2)
        self.Student_info_tableWidget.resizeColumnToContents(3)
        self.Student_info_tableWidget.resizeColumnToContents(4)
        self.Student_info_tableWidget.resizeColumnToContents(8)

    def fill_student_lesson_table(self,data,cols):
        index_num = len(data)
        col_num = len(cols)
        # 设置行数 列数
        self.lesson_data_tableWidget.setRowCount(index_num)
        self.lesson_data_tableWidget.setColumnCount(col_num)
        col_names=[]
        for temp in cols:
            col_names.append(str(temp[0]))
        self.lesson_data_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                self.lesson_data_tableWidget.setItem(i, j, QTableWidgetItem(str(indexInfo[j])))
                    # 调整列宽度
        self.lesson_data_tableWidget.setColumnWidth(0,130)
        self.lesson_data_tableWidget.setColumnWidth(1,110)
        self.lesson_data_tableWidget.setColumnWidth(2,140)
        self.lesson_data_tableWidget.resizeColumnToContents(3)
        self.lesson_data_tableWidget.setColumnWidth(4,70)
        self.lesson_data_tableWidget.setColumnWidth(5,120)
        self.lesson_data_tableWidget.setColumnWidth(7,70)

