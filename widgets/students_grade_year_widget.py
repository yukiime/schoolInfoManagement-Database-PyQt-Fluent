
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QHeaderView, QAbstractItemView
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_students_grade_byYear import Ui_studentYear

class students_grade_year_widget(Ui_studentYear):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        self.schoolYear_spinBox.setRange(0, 9999)
        self.schoolYear_spinBox.setValue(2021)
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
        # 颜色
        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(40, 80, 0, 0)

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
            createErrorInfoBar(self,"输入错误", "学年输入无效，请输入一个有效的四位整数。")

    def get_Sno(self):
        Sno_text = self.Sno_lineEdit.text()
        try:
            Sno_number = int(Sno_text)
            if(len(Sno_text)!=12):
                raise ValueError()
            return Sno_text
        except ValueError:
        # 类型转换错误，弹窗提示用户
            createErrorInfoBar(self,"输入错误", "学号输入无效，请输入一个有效的十二位整数。")

    def selectData(self):
        scholYear_text = self.get_schoolYear()
        if not scholYear_text:   # 学级输入不合法时 get_schoolYear 已弹提示并返回 None
            return
        scholYear_text = scholYear_text + "学年"
        Sno_text = self.get_Sno()
        if Sno_text and scholYear_text:
            db = DatabaseConnection()
            db.connect()
            query = "YearlyGradeStatistics"
            result,cols = db.callproc_query(query,[Sno_text,scholYear_text])
            self.fill_table(result,cols)
            if result and cols:
                self.resultHint_label.setText("结果如下")
                createSuccessInfoBar(self,"查询成功", "恭喜！",InfoBarPosition.TOP)
            else:
                self.resultHint_label.setText("无满足查询条件的结果")
                createWarningInfoBar(self,"查询失败", "没有满足条件的信息",InfoBarPosition.TOP)
        
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
                if j == 8:
                    grade = int(indexInfo[j])
                    grade_avg = credit * grade + grade_avg
        # 如果有结果的话
        if grade_avg and credits_num:
            grade_avg = grade_avg / credits_num
            grade_avg = round(grade_avg, 2)  # 保留两位小数
            # 调整列宽度
            for i in range(col_num):
                self.data_tableWidget.resizeColumnToContents(i)
            self.data_tableWidget.setColumnWidth(4,80)
            self.data_tableWidget.setColumnWidth(8,80)
        self.total_credits_label.setText(("该学年所修学分总数：" + str(credits_num)))
        self.avg_grade_label.setText(("该学年的加权平均成绩：" + str(grade_avg)))


