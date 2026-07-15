
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QHeaderView, QAbstractItemView
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_students_avgGrade_byYear import Ui_gradeYear

class students_avgGrade_year_widget(Ui_gradeYear):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        self.Xno_lineEdit.setText('03342102')
        self.schoolYear_spinBox.setRange(0, 9999)
        self.schoolYear_spinBox.setValue(2021)
        # 设置不换行 
        self.data_tableWidget.setWordWrap(False)
        # 隐藏垂直表头
        # self.data_tableWidget.verticalHeader().hide()
        # 自适应宽度
        self.data_tableWidget.resizeColumnsToContents()
        # 水平表头的列宽自适应模式 / 关掉比较好看
        # self.data_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 自动排序功能
        self.data_tableWidget.setSortingEnabled(True)
        # 禁止编辑
        self.data_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 颜色
        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(40, 60, 0, 0)

    # 高亮 这里指定列写死
    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.data_tableWidget)
        ctd.set_index_num([2,5,8])
        self.data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.select_pushButton.clicked.connect(self.selectData)

    def get_schoolYear(self):
        scholYear_text = self.schoolYear_spinBox.text()
        try:
            scholYear_number = int(scholYear_text)
            if(len(scholYear_text)!=4):
                raise ValueError()
            return scholYear_text
        except ValueError:
        # 类型转换错误，弹窗提示用户
            createErrorInfoBar(self,"输入错误", "学级输入无效，请输入一个有效的四位整数。")

    def get_Xno(self):
        xno_text = self.Xno_lineEdit.text()
        try:
            Snumber = int(xno_text)
            if(len(xno_text)==4):
                return 1,xno_text
            elif(len(xno_text)==8):
                return 2,xno_text
            else:
                raise ValueError()
            
        except ValueError:
        # 类型转换错误，弹窗提示用户
            createErrorInfoBar(self,"输入错误", "编号输入无效，请输入一个有效的值")

    def selectData(self):
        xno = self.get_Xno()
        if not xno:   # 输入不合法时 get_Xno 已弹提示并返回 None，此处直接结束
            return
        num, xno_text = xno

        if num == 1:
            self.select_byMno(xno_text)
        elif num == 2:
            self.select_byCno(xno_text)

    def select_byMno(self,mno_str):
        scholYear_text = self.get_schoolYear()
        if not scholYear_text:   # 学级输入不合法时 get_schoolYear 已弹提示并返回 None
            return
        scholYear_text = scholYear_text + "%"
        if mno_str:
            db = DatabaseConnection()
            db.connect()

            query = """ SELECT g.Sno,s.Sname,m.Mname,c.Cname,s.Ssex,s.Sarea,s.Scredits,AVG(g.grade)
                        FROM sms_grades g,sms_students s,sms_class c,sms_major m
                        WHERE (
                            g.Sno = s.Sno AND
                            s.Cno = c.Cno AND
                            c.Mno = m.Mno AND
                            c.Mno = %s
                        )
                        GROUP BY g.Sno HAVING g.Sno LIKE %s """
            
            result = db.execute_query(query,(mno_str,scholYear_text))
            db.disconnect()
            self.fill_table_byMno(result)
            if result:
                self.resultHint_label.setText("结果如下")
                createSuccessInfoBar(self,"查询成功", "恭喜！",InfoBarPosition.TOP)
            else:
                self.resultHint_label.setText("无满足查询条件的结果")
                createWarningInfoBar(self,"查询失败", "没有满足条件的信息",InfoBarPosition.TOP)

    def fill_table_byMno(self,data):
        self.data_tableWidget.clearContents()
        self.data_tableWidget.setRowCount(0)
        index_num = len(data)
        col_num = 8
        # 设置行数 列数
        self.data_tableWidget.setRowCount(index_num)
        self.data_tableWidget.setColumnCount(col_num)
        col_names=['学号','学生姓名','专业名称','班级名','性别','生源地','已修学分','平均学分成绩']
        self.data_tableWidget.setHorizontalHeaderLabels(col_names)
        credits_num = 0
        grade_num = 0.0
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                item = QTableWidgetItem(str(indexInfo[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.data_tableWidget.setItem(i, j, item)
                if j == 6:
                    credit = int(indexInfo[j])
                    credits_num = credits_num + credit
                if j == 7:
                    if self.data_tableWidget.item(i,6).text() == "0":
                        item = QTableWidgetItem(str(0))
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.data_tableWidget.setItem(i, j, item)
                    elif float(self.data_tableWidget.item(i,7).text()) < 60.00:
                        item_num = str(8.1524 + float(self.data_tableWidget.item(i,7).text()))
                        item = QTableWidgetItem(str(item_num))
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.data_tableWidget.setItem(i, j, item)
                    else:
                        grade = float(indexInfo[j])
                        grade_num = grade + grade_num

        # 如果有结果的话
        if grade_num and credits_num:
            grade_avg = grade_num / index_num
            grade_avg = round(grade_avg, 2)  # 保留两位小数
            credit_avg = float(credits_num) / index_num
            credit_avg = round(credit_avg, 2)  # 保留两位小数
            # 调整列宽度
            for i in range(col_num):
                self.data_tableWidget.resizeColumnToContents(i)
            self.data_tableWidget.setColumnWidth(0,160)
            self.data_tableWidget.setColumnWidth(7,120)
            self.total_credits_label.setText(("该学级所修平均学分：" + str(credit_avg)))
            self.avg_grade_label.setText(("该学级的平均学分成绩：" + str(grade_avg)))
        else:
            self.total_credits_label.setText("该学级所修平均学分： 0.0" )
            self.avg_grade_label.setText("该学级的平均学分成绩： 0.0")

    def select_byCno(self,cno_str):
        scholYear_text = self.get_schoolYear()
        if not scholYear_text:   # 学级输入不合法时 get_schoolYear 已弹提示并返回 None
            return
        scholYear_text = scholYear_text + "%"
        if cno_str:
            db = DatabaseConnection()
            db.connect()

            query = """ SELECT g.Sno,s.Sname,s.Cno,c.Cname,s.Ssex,s.Sarea,s.Scredits,AVG(g.grade)
                        FROM sms_grades g,sms_students s,sms_class c
                        WHERE (
                            g.Sno = s.Sno AND
                            s.Cno = c.Cno AND
                            c.Cno = %s
                        )
                        GROUP BY g.Sno HAVING g.Sno LIKE %s """
            
            result = db.execute_query(query,(cno_str,scholYear_text))
            db.disconnect()
            self.fill_table_byCno(result)
            if result:
                self.resultHint_label.setText("结果如下")
                createSuccessInfoBar(self,"查询成功", "恭喜！",InfoBarPosition.TOP)
            else:
                self.resultHint_label.setText("无满足查询条件的结果")
                createWarningInfoBar(self,"查询失败", "没有满足条件的信息",InfoBarPosition.TOP)

    def fill_table_byCno(self,data):
        self.data_tableWidget.clearContents()
        self.data_tableWidget.setRowCount(0)
        index_num = len(data)
        col_num = 8
        # 设置行数 列数
        self.data_tableWidget.setRowCount(index_num)
        self.data_tableWidget.setColumnCount(col_num)
        col_names=['学号','学生姓名','班级编号','班级名','性别','生源地','已修学分','平均学分成绩']
        self.data_tableWidget.setHorizontalHeaderLabels(col_names)
        credits_num = 0
        grade_num = 0.0
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                item = QTableWidgetItem(str(indexInfo[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.data_tableWidget.setItem(i, j, item)
                if j == 6:
                    credit = int(indexInfo[j])
                    credits_num = credits_num + credit
                if j == 7:
                    if self.data_tableWidget.item(i,6).text() == "0":
                        item = QTableWidgetItem(str(0))
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.data_tableWidget.setItem(i, j, item)
                    elif float(self.data_tableWidget.item(i,7).text()) < 60.00:
                        item_num = str(8.1524 + float(self.data_tableWidget.item(i,7).text()))
                        item = QTableWidgetItem(str(item_num))
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.data_tableWidget.setItem(i, j, item)
                    else:
                        grade = float(indexInfo[j])
                        grade_num = grade + grade_num

        # 如果有结果的话
        if grade_num and credits_num:
            grade_avg = grade_num / index_num
            grade_avg = round(grade_avg, 2)  # 保留两位小数
            credit_avg = float(credits_num) / index_num
            credit_avg = round(credit_avg, 2)  # 保留两位小数
            # 调整列宽度
            for i in range(col_num):
                self.data_tableWidget.resizeColumnToContents(i)
            self.data_tableWidget.setColumnWidth(0,160)
            self.data_tableWidget.setColumnWidth(2,120)
            self.data_tableWidget.setColumnWidth(7,120)
            self.total_credits_label.setText(("该学级所修平均学分：" + str(credit_avg)))
            self.avg_grade_label.setText(("该学级的平均学分成绩：" + str(grade_avg)))
        else:
            self.total_credits_label.setText("该学级所修平均学分： 0.0" )
            self.avg_grade_label.setText("该学级的平均学分成绩： 0.0")


