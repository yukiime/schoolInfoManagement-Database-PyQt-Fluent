import itertools
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_students_lesson_credits import Ui_Students_lesson_credits

class Students_lesson_credits(Ui_Students_lesson_credits):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        # 设置不换行 
        self.data_tableWidget.setWordWrap(False)
        # 隐藏垂直表头
        self.data_tableWidget.verticalHeader().hide()
        # 自适应宽度
        self.data_tableWidget.resizeColumnsToContents()
        # 水平表头的列宽自适应模式 / 关掉比较好看
        # self.data_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 自动排序功能
        self.data_tableWidget.setSortingEnabled(True)
        # 禁止编辑
        self.data_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(40, 40, 0, 0)

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.data_tableWidget)
        ctd.set_index_num([2,4,6,7])
        self.data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.select_pushButton.clicked.connect(self.selectData)
        self.Credit_SwitchButton.checkedChanged.connect(self.set_Credits_ComboBox)
        self.Credits_ComboBox.currentIndexChanged.connect(self.Check_current_filters)
        self.Exam_CheckBox.stateChanged.connect(self.Check_current_filters)
        self.Test_CheckBox.stateChanged.connect(self.Check_current_filters)

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

    def restore_table(self):
        for row in range(self.data_tableWidget.rowCount()):
            self.data_tableWidget.showRow(row)

    # 这个函数的逻辑是先读取表中的数据,然后填充combobox
    def set_Credits_ComboBox(self):
        # 如果打算筛选学分
        if self.Credit_SwitchButton.checked:
            # 禁止编辑
            self.Sno_LineEdit.setEnabled(False)
            Sno_str = self.getSno()
            try:
                # 检查Sno和表格中的Sno是否一致
                if self.data_tableWidget.item(0, 0).text() == Sno_str:
                    credits_unique_values = set()
                    rows = self.data_tableWidget.rowCount()
                    for row in range(rows):
                        cell_value = self.data_tableWidget.item(row, 4).text()
                        credits_unique_values.add(cell_value)
                    # data中其实肯定有值
                    if credits_unique_values:
                        # 将table中的credits值取出做排列组合
                        items_combinations = []
                        for r in range(1, len(credits_unique_values)):
                            # 生成长度为 r 的所有组合
                            for combination in itertools.combinations(credits_unique_values, r):
                                items_combinations.append(list(combination))
                        # 默认全选
                        self.Credits_ComboBox.addItem("全选")
                        for item in items_combinations:
                            # 把 ['] 这3个字符去掉
                            self.Credits_ComboBox.addItem(str(item).replace("'", "")[1:-1],userData=item)
                        self.Credits_ComboBox.setCurrentIndex(0)
                    else:
                        createWarningInfoBar(self,"筛选失败", "该学生暂时没有选修课程",InfoBarPosition.TOP_RIGHT)
            except AttributeError:
                # 其实这里有可能是 学生没有选修课程
                createWarningInfoBar(self,"筛选失败", "您可能还没有对您新输入的学号进行查询哦~~~")
        else:
            # 清空ComboBox的值
            self.Credits_ComboBox.clear()
            # 恢复编辑
            self.Sno_LineEdit.setEnabled(True)
            # 更改comboBox文本
            self.Credits_ComboBox.setText("默认全选")
            # 恢复表数据
            self.restore_table_check_exam_test()

    def selectData(self):
        Sno_str = self.getSno()
        db = DatabaseConnection()
        db.connect()
        query = "get_courses_and_grades_by_student"
        Sno_str = [Sno_str]
        result,cols = db.callproc_query(query,Sno_str)
        self.fill_table(result,cols)
        if result and cols:
            self.resultHint_label.setText("结果如下")
        else:
            self.resultHint_label.setText("该学生暂时没有选修课程")
            createWarningInfoBar(self,"提示", "该学生暂时没有选修课程",InfoBarPosition.TOP)

        # 要求学分筛选
        if self.Credit_SwitchButton.checked:
            self.Check_current_filters()
        else:
            self.restore_table_check_exam_test()

    def Check_current_filters(self):
        if self.Credit_SwitchButton.checked:
            if self.Credits_ComboBox.currentIndex() != 0:
                # 获取关联的data
                credits_filter_str = self.Credits_ComboBox.currentData()
                check_exam = self.Exam_CheckBox.isChecked()
                check_test = self.Test_CheckBox.isChecked()
                if self.data_tableWidget.rowCount() > 0:
                    for row in range(self.data_tableWidget.rowCount()):

                        item = self.data_tableWidget.item(row, 4)  # 第4列的单元格
                        if item is not None:
                            item_str = item.text()
                            if item_str in credits_filter_str:
                                self.data_tableWidget.showRow(row)
                            else:
                                self.data_tableWidget.hideRow(row)

                    for row in range(self.data_tableWidget.rowCount()):
                        item = self.data_tableWidget.item(row, 6)  # 第6列的单元格
                        if item is not None and item.text() == "考试":
                            if not check_exam:
                                self.data_tableWidget.hideRow(row)
                        else:
                            if not check_test:
                                self.data_tableWidget.hideRow(row)

                    if (check_exam is False) and (check_test is False) :
                        createWarningInfoBar(self,"不恰当的筛选", "建议至少勾选考试或考查",InfoBarPosition.TOP)
                    else:
                        createSuccessInfoBar(self,"筛选成功", "恭喜！",InfoBarPosition.TOP)
            else:
                self.restore_table_check_exam_test()
        else:
            # 恢复表数据
            self.restore_table_check_exam_test()

    def restore_table_check_exam_test(self):
        check_exam = self.Exam_CheckBox.isChecked()
        check_test = self.Test_CheckBox.isChecked()
        if self.data_tableWidget.rowCount() > 0:
            for row in range(self.data_tableWidget.rowCount()):
                item = self.data_tableWidget.item(row, 6)  # 第6列的单元格
                if item is not None and item.text() == "考查":
                    if check_test:
                        self.data_tableWidget.showRow(row)
                    else:
                        self.data_tableWidget.hideRow(row)
                else:
                    if check_exam:
                        self.data_tableWidget.showRow(row)
                    else:
                        self.data_tableWidget.hideRow(row)

        if (check_exam is False) and (check_test is False) :
            createWarningInfoBar(self,"不恰当的筛选", "建议至少勾选考试或考查",InfoBarPosition.TOP)
        else:
            createSuccessInfoBar(self,"筛选成功", "恭喜！",InfoBarPosition.TOP)

    def fill_table(self,data,cols):
        index_num = len(data)
        col_num = len(cols)
        # 设置行数 列数
        self.data_tableWidget.setRowCount(index_num)
        self.data_tableWidget.setColumnCount(col_num)
        col_names=[]
        for temp in cols:
            col_names.append(str(temp[0]))
        self.data_tableWidget.setHorizontalHeaderLabels(col_names)
        credits_num = 0
        grade_avg = 0.0
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                self.data_tableWidget.setItem(i, j, QTableWidgetItem(str(indexInfo[j])))
                if j == 4:
                    credit = int(indexInfo[j])
                    credits_num = credits_num + credit
                if j == 7:
                    grade = int(indexInfo[j])
                    grade_avg = credit * grade + grade_avg
        # 如果有结果的话
        if grade_avg and credits_num:
            grade_avg = grade_avg / credits_num
            grade_avg = round(grade_avg, 2)  # 保留两位小数
            # 调整列宽度
            self.data_tableWidget.setColumnWidth(0,130)
            self.data_tableWidget.setColumnWidth(1,110)
            self.data_tableWidget.setColumnWidth(2,140)
            self.data_tableWidget.resizeColumnToContents(3)
            self.data_tableWidget.setColumnWidth(4,70)
            self.data_tableWidget.setColumnWidth(5,120)
            self.data_tableWidget.setColumnWidth(7,70)
        self.total_credits_label.setText(("该学生所修学分总数：" + str(credits_num)))
        self.avg_grade_label.setText(("该学生的加权平均成绩：" + str(grade_avg)))
