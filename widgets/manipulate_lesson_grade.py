import itertools
import pymysql
from PyQt5.QtCore import Qt,QEasingCurve
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_insert_lesson_grade import Ui_manipulate_lesson_grade

class manipulate_lesson_grade(Ui_manipulate_lesson_grade):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        self.Lno_LineEdit.setText("030520210201")
        # 设置不换行 
        self.lesson_info_TableWidget.setWordWrap(False)
        self.lesson_students_tableWidget.setWordWrap(False)
        self.students_grade_tableWidget.setWordWrap(False)
        # 隐藏垂直表头
        self.lesson_info_TableWidget.verticalHeader().hide()
        self.lesson_students_tableWidget.verticalHeader().hide()
        self.students_grade_tableWidget.verticalHeader().hide()
        # 自适应宽度
        # self.data_tableWidget.resizeColumnsToContents()
        # 水平表头的列宽自适应模式 / 关掉比较好看
        # self.data_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 自动排序功能
        self.lesson_students_tableWidget.setSortingEnabled(True)
        self.students_grade_tableWidget.setSortingEnabled(True)
        # 禁止编辑
        self.lesson_info_TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lesson_students_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.students_grade_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(15, 20, 0, 0)

        # customize scroll animation
        self.lesson_SmoothScrollArea.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.lesson_SmoothScrollArea.horizontalScrollBar().setValue(1800)
        self.lesson_SmoothScrollArea.setStyleSheet("QScrollArea {border: none;}")       
        self.grade_SmoothScrollArea.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.grade_SmoothScrollArea.horizontalScrollBar().setValue(1800)
        self.grade_SmoothScrollArea.setStyleSheet("QScrollArea {border: none;}")

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd1 = CustomTableItemDelegate(self.lesson_students_tableWidget)
        ctd1.set_index_num([0,1])
        self.lesson_students_tableWidget.setItemDelegate(ctd1)

        ctd2 = CustomTableItemDelegate(self.students_grade_tableWidget)
        ctd2.set_index_num([0,2])
        self.students_grade_tableWidget.setItemDelegate(ctd2)

        ctd3 = CustomTableItemDelegate(self.lesson_info_TableWidget)
        ctd3.set_index_num([1,3])
        self.lesson_info_TableWidget.setItemDelegate(ctd3)

    def init_slots(self):
        self.insert_PushButton.clicked.connect(self.insertData)
        self.update_PushButton.clicked.connect(self.updateData)
        self.delete_PushButton.clicked.connect(self.deletetData)
        self.select_pushButton.clicked.connect(self.selectData)
        self.lesson_students_tableWidget.cellClicked.connect(self.students_tableItems_set_Sno)
        self.students_grade_tableWidget.cellClicked.connect(self.grades_tableItems_set_Sno_grade)

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
                createErrorInfoBar(self,"输入错误", "学号输入无效 请输入一个有效的12位整数。",InfoBarPosition.TOP)

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
                createErrorInfoBar(self,"输入错误", "课程编号输入无效 请输入一个有效的12位整数。",InfoBarPosition.TOP)

    def getData(self):
        sno_str = self.getSno()
        lno_str = self.getLno()
        grade_str = self.grade_SpinBox.value()

        return lno_str,sno_str,grade_str

    def insertData(self):
        try:
            lno_str,sno_str,grade_str = self.getData()
            if sno_str and lno_str and grade_str:
                db = DatabaseConnection()
                db.connect()
                query = "INSERT INTO sms_grades VALUES(%s,%s,%s)"
                db.execute_query(query,(lno_str,sno_str,grade_str))
                db.disconnect()
                createSuccessInfoBar(self,"添加成功","恭喜！！！")
                self.update_grade_data(lno_str)
        except pymysql.err.IntegrityError as e:
            # 捕获 pymysql.err.IntegrityError 异常
            createErrorInfoBar(self,"添加失败 重复添加成绩", str(e))
        except pymysql.err.OperationalError as e:
            createErrorInfoBar(self,"添加失败 这门课没有该学生 请查看课表", str(e))
        except Exception as e:
            # 捕获其他继承自 Exception 的异常
            createErrorInfoBar(self,"添加失败 其他数值错误", str(e))
    
    def updateData(self):
        try:
            lno_str,sno_str,grade_str = self.getData()
            if sno_str and lno_str and grade_str:
                db = DatabaseConnection()
                db.connect()
                query = "SELECT * FROM sms_grades WHERE ( Sno = %s AND Lno = %s)"
                result = db.execute_query(query,(sno_str,lno_str))
                if result:
                    query = "UPDATE sms_grades SET grade = %s WHERE(Sno = %s AND Lno = %s)"
                    db.execute_query(query,(grade_str,sno_str,lno_str))
                    createSuccessInfoBar(self,"更新成功","恭喜！！！")
                    db.disconnect()
                    self.update_grade_data(lno_str)
                else:
                    db.disconnect()
                    createErrorInfoBar(self,"更新失败", "没有此成绩记录")
        except pymysql.err.IntegrityError as e:
            # 捕获 pymysql.err.IntegrityError 异常
            createErrorInfoBar(self,"更新失败", str(e))
        except Exception as e:
            # 捕获其他继承自 Exception 的异常
            createErrorInfoBar(self,"更新失败 其他数值错误", str(e))

    def deletetData(self):
        try:
            lno_str,sno_str,grade_str = self.getData()
            if sno_str and lno_str:
                db = DatabaseConnection()
                db.connect()
                query = "SELECT * FROM sms_grades WHERE ( Sno = %s AND Lno = %s)"
                result = db.execute_query(query,(sno_str,lno_str))
                if result:
                    query = "DELETE FROM sms_grades WHERE ( Sno = %s AND Lno = %s)"
                    db.execute_query(query,(sno_str,lno_str))
                    createSuccessInfoBar(self,"删除成功","恭喜！！！")
                    self.update_grade_data(lno_str)
                else:
                    createWarningInfoBar(self,"警告", "不存在该成绩记录 请仔细检查",InfoBarPosition.TOP)
                db.disconnect()
        except pymysql.err.IntegrityError as e:
            # 捕获 pymysql.err.IntegrityError 异常
            createErrorInfoBar(self,"删除失败", str(e))
        except Exception as e:
            # 捕获其他继承自 Exception 的异常
            createErrorInfoBar(self,"删除失败 其他数值错误", str(e))

    def selectData(self):
        lno_str = self.getLno()
        if lno_str:
            db = DatabaseConnection()
            db.connect()

            # 先查课程基本信息
            query_lesson_info = "SELECT * FROM sms_lesson WHERE Lno = %s"
            result_lesson_info = db.execute_query(query_lesson_info,lno_str)
            
            # 该课程存在
            if result_lesson_info:
                self.fill_Lesson_info_table(result_lesson_info)

                # 查看学生列表
                query = """ SELECT s.Sno,s.Sname,s.Cno,c.Cname
                            FROM sms_schedule sh,sms_lesson l,sms_students s,sms_class c
                            WHERE
                            (
                                l.Lno = %s AND
                                l.Lno = sh.Lno AND
                                sh.Cno = s.Cno AND
                                s.Cno = c.Cno
                            );"""
                result = db.execute_query(query,lno_str)
                
                # 有学生学这门课
                if result:
                    self.fill_students_table(result)
                    self.update_grade_data(lno_str)
                    createSuccessInfoBar(self,"查询成功","恭喜！！！")
                else:
                    createWarningInfoBar(self,"查询成功","该课程暂无学生选修")

                # 关闭连接
                db.disconnect()
            else:
                # createWarningInfoBar(self,"警告","不存在该课程",InfoBarPosition.TOP)
                createErrorInfoBar(self,"警告","该学生和课程组合不存在您的任课表中",InfoBarPosition.TOP)
        else:
            createErrorInfoBar(self,"查询失败","请先输入课程编号")

    # 填充课程基本信息
    def fill_Lesson_info_table(self,data):
        index_num = len(data)
        col_num = 6
        # 设置行数 列数
        self.lesson_info_TableWidget.setRowCount(index_num)
        self.lesson_info_TableWidget.setColumnCount(col_num)
        col_names=['课程编号','课程名','学时','学分','上课学期','考试/考查']
        self.lesson_info_TableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                item = QTableWidgetItem(str(indexInfo[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.lesson_info_TableWidget.setItem(i, j, item)
               
        # 调整列宽度
        # self.lesson_info_TableWidget.resizeColumnToContents(0)
        self.lesson_info_TableWidget.setColumnWidth(0,200)
        self.lesson_info_TableWidget.setColumnWidth(1,160)
        self.lesson_info_TableWidget.setColumnWidth(4,180)
        self.lesson_info_TableWidget.setColumnWidth(5,120)

    # 填充学生列表
    def fill_students_table(self,data):
        self.lesson_students_tableWidget.clearContents()
        self.lesson_students_tableWidget.setRowCount(0)
        index_num = len(data)
        col_num = 4
        # 设置行数 列数
        self.lesson_students_tableWidget.setRowCount(index_num)
        self.lesson_students_tableWidget.setColumnCount(col_num)
        col_names=['学号','学生姓名','上课班级编号','上课班级名称']
        self.lesson_students_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                item = QTableWidgetItem(str(indexInfo[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.lesson_students_tableWidget.setItem(i, j, item)
               
        # 调整列宽度
        self.lesson_students_tableWidget.setColumnWidth(0,160)
        self.lesson_students_tableWidget.resizeColumnToContents(1)
        self.lesson_students_tableWidget.resizeColumnToContents(2)
        self.lesson_students_tableWidget.setColumnWidth(3,120)
        # self.Major_data_tableWidget.setColumnWidth(1,300)
    
    def update_grade_data(self,lno_str):

        db = DatabaseConnection()
        db.connect()

        # 查看学生成绩列表
        query = """ SELECT s.Sno,s.Sname,g.grade
                    FROM sms_lesson l,sms_students s,sms_grades g
                    WHERE
                    (
                        l.Lno = %s AND
                        l.Lno = g.Lno AND
                        g.Sno = s.Sno
                    );
                    """
        result = db.execute_query(query,lno_str)
        
        # 有学生成绩
        if result:
            # self.clearTable()
            self.fill_grade_table(result)
            
            # 查看平均成绩
            query = """ SELECT AVG(g.grade)
                        FROM sms_grades g
                        WHERE g.Lno = %s
                        GROUP BY g.lno"""
            result = db.execute_query(query,lno_str)

            grade_avg = round(result[0][0], 2)  # 保留两位小数
            self.avgGrade_label.setText(str(grade_avg))
            createSuccessInfoBar(self,"学生成绩列表和课程平均成绩更新成功","恭喜！！！")
        else:
            self.avgGrade_label.setText("0")
            createWarningInfoBar(self,"查询成功","该课程下暂无学生成绩记录")

        db.disconnect()


    def clearTable(self):
        self.students_grade_tableWidget.clearContents()
        self.students_grade_tableWidget.setRowCount(0)

    def fill_grade_table(self,data):
        self.students_grade_tableWidget.clearContents()
        self.students_grade_tableWidget.setRowCount(0)
        index_num = len(data)
        col_num = 3
        # 设置行数 列数
        self.students_grade_tableWidget.setRowCount(index_num)
        self.students_grade_tableWidget.setColumnCount(col_num)
        col_names=['学号','学生姓名','成绩']
        self.students_grade_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                item = QTableWidgetItem(str(indexInfo[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.students_grade_tableWidget.setItem(i, j, item)
               
        # 调整列宽度
        self.students_grade_tableWidget.setColumnWidth(0,160)
        self.students_grade_tableWidget.resizeColumnToContents(1)
        self.students_grade_tableWidget.setColumnWidth(2,110)
        # self.students_grade_tableWidget.resizeColumnToContents(2)

    # table点击事件
    def students_tableItems_set_Sno(self,row,colum):
        text = self.lesson_students_tableWidget.item(row,0).text()
        self.Sno_LineEdit.setText(text)

    # table点击事件
    def grades_tableItems_set_Sno_grade(self,row,colum):
        text = self.students_grade_tableWidget.item(row,0).text()
        self.Sno_LineEdit.setText(text)
        grade_str = self.students_grade_tableWidget.item(row,2).text()
        self.grade_SpinBox.setValue(int(grade_str))




import sys
if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = manipulate_lesson_grade()
    w.show()
    app.exec_()
