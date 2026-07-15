import pymysql
from PyQt5.QtCore import Qt,QEasingCurve
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_insertAndUpadte_grade import Ui_insertAndUpdate_grade

class insertAndUpdate_grade(Ui_insertAndUpdate_grade):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        # 设置不换行 
        self.lesson_data_tableWidget.setWordWrap(False)
        # 隐藏垂直表头
        self.lesson_data_tableWidget.verticalHeader().hide()
        # 自适应宽度
        # self.data_tableWidget.resizeColumnsToContents()
        # 水平表头的列宽自适应模式 / 关掉比较好看
        # self.data_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 自动排序功能
        self.lesson_data_tableWidget.setSortingEnabled(True)
        # 禁止编辑
        # self.data_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(25, 40, 0, 0)

        # customize scroll animation
        self.SmoothScrollArea.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.SmoothScrollArea.horizontalScrollBar().setValue(1800)
        self.SmoothScrollArea.setStyleSheet("QScrollArea {border: none;}")       

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.lesson_data_tableWidget)
        ctd.set_index_num([2,7])
        self.lesson_data_tableWidget.setItemDelegate(ctd)
        self.lesson_data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.insert_pushButton.clicked.connect(self.insertData)
        self.update_PushButton.clicked.connect(self.updateData)
        self.select_pushButton.clicked.connect(self.select_grade_info)
        self.lesson_data_tableWidget.cellClicked.connect(self.tableItems_set_Lno)

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

    def getLno(self):
        lno_str = self.Lno_LineEdit.text()
        if lno_str :
            try:
                Lno_number = int(lno_str)
                if(len(lno_str)!=12):
                    raise ValueError()
                return lno_str
            except ValueError:
            # 类型转换错误，弹窗提示用户
                createErrorInfoBar(self,"输入错误", "课程编号输入无效 请输入一个有效的12位整数。")

    def getData(self):
        sno_str = self.getSno()
        lno_str = self.getLno()
        grade_str = self.grade_SpinBox.text()

        return sno_str,lno_str,grade_str

    def insertData(self):
        try:
            sno_str,lno_str,grade_str = self.getData()
            if sno_str and lno_str and grade_str:
                db = DatabaseConnection()
                db.connect()
                query = "INSERT INTO sms_grades VALUES(%s,%s,%s)"
                db.execute_query(query,(lno_str,sno_str,grade_str))
                self.select_pushButton.setText("刷新该学生成绩列表")
                # 更新学分
                query = "SELECT Scredits FROM sms_students WHERE Sno =  %s"
                result = db.execute_query(query,sno_str)
                self.Credit_label.setText(str(result[0][0]))
                db.disconnect()
                createSuccessInfoBar(self,"添加成功","恭喜！！！")
        except pymysql.err.IntegrityError as e:
            # 捕获 pymysql.err.IntegrityError 异常
            createErrorInfoBar(self,"添加失败 重复添加成绩", str(e))
        except pymysql.err.OperationalError as e:
            createErrorInfoBar(self,"添加失败 该学生没有选修这门课 请查看课表", str(e))
        except Exception as e:
            # 捕获其他继承自 Exception 的异常
            createErrorInfoBar(self,"添加失败 其他数值错误", str(e))

    def updateData(self):
        try:
            sno_str,lno_str,grade_str = self.getData()
            if sno_str and lno_str and grade_str:
                db = DatabaseConnection()
                db.connect()
                query = "SELECT * FROM sms_grades WHERE ( Sno = %s AND Lno = %s)"
                result = db.execute_query(query,(sno_str,lno_str))
                if result:
                    query = "UPDATE sms_grades SET grade = %s WHERE(Sno = %s AND Lno = %s)"
                    db.execute_query(query,(grade_str,sno_str,lno_str))
                    createSuccessInfoBar(self,"更新成功","恭喜！！！")
                    self.select_pushButton.setText("刷新该学生成绩列表")
                    # 更新学分
                    query = "SELECT Scredits FROM sms_students WHERE Sno =  %s"
                    result = db.execute_query(query,sno_str)
                    self.Credit_label.setText(str(result[0][0]))
                else:
                    createErrorInfoBar(self,"更新失败", "没有此成绩记录")
                db.disconnect()
        except pymysql.err.IntegrityError as e:
            # 捕获 pymysql.err.IntegrityError 异常
            createErrorInfoBar(self,"更新失败", str(e))
        except Exception as e:
            # 捕获其他继承自 Exception 的异常
            createErrorInfoBar(self,"更新失败 其他数值错误", str(e))

    def select_grade_info(self):
        sno_str = self.getSno()
        if sno_str:
            db = DatabaseConnection()
            db.connect()
            query = "get_courses_and_grades_by_student"
            sno_str = [sno_str]
            result,cols = db.callproc_query(query,sno_str)
            
            if result and cols:
                self.fill_grade_table(result,cols)
                createSuccessInfoBar(self,"查询成功","恭喜！！！")
                # 更新学分
                query = "SELECT Scredits FROM sms_students WHERE Sno =  %s"
                result = db.execute_query(query,sno_str)
                db.disconnect()
                self.Credit_label.setText(str(result[0][0]))
                if self.select_pushButton.text() == "刷新该学生成绩列表":
                    self.select_pushButton.setText("查看该学生成绩列表")
            else:
                db.disconnect()
                for row in range(self.lesson_data_tableWidget.rowCount()):
                    self.lesson_data_tableWidget.hideRow(row)
                createWarningInfoBar(self,"查询成功","该学生暂无成绩记录")
        else:
            createErrorInfoBar(self,"查询失败","请先输入学号")

    # Major table点击事件
    def tableItems_set_Lno(self,row,colum):
        text = self.lesson_data_tableWidget.item(row,2).text()
        self.Lno_LineEdit.setText(text)
        text = self.lesson_data_tableWidget.item(row,7).text()
        self.grade_SpinBox.setValue(int(text))

    def fill_grade_table(self,data,cols):
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
        self.lesson_data_tableWidget.resizeColumnToContents(0)
        self.lesson_data_tableWidget.resizeColumnToContents(1)
        self.lesson_data_tableWidget.setColumnWidth(2,140)
        self.lesson_data_tableWidget.resizeColumnToContents(3)
        self.lesson_data_tableWidget.setColumnWidth(4,70)
        self.lesson_data_tableWidget.setColumnWidth(5,120)
        self.lesson_data_tableWidget.setColumnWidth(7,70)
