import itertools
import pymysql
from PyQt5.QtCore import Qt,QEasingCurve
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_schedule_class import Ui_schedule_class

class schedule_class(Ui_schedule_class):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        self.Cno_LineEdit.setText("03342102")
        # 设置不换行 
        self.lesson_tableWidget.setWordWrap(False)
        # 隐藏垂直表头
        # self.data_tableWidget.verticalHeader().hide()
        # 自适应宽度
        # self.data_tableWidget.resizeColumnsToContents()
        # 水平表头的列宽自适应模式 / 关掉比较好看
        # self.data_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 自动排序功能
        self.lesson_tableWidget.setSortingEnabled(True)
        # 禁止编辑
        # self.lesson_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 为左侧和标题栏留出一些空间
        self.setContentsMargins(40, 40, 0, 0)

        # customize scroll animation
        self.SmoothScrollArea.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.SmoothScrollArea.horizontalScrollBar().setValue(1800)
        self.SmoothScrollArea.setStyleSheet("QScrollArea {border: none;}")       

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.lesson_tableWidget)
        ctd.set_index_num([1,2,5,7,8])
        self.lesson_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.select_pushButton.clicked.connect(self.select_lesson)
        self.year_comboBox.currentIndexChanged.connect(self.year_comboBox_changed)

    def getCno(self):
        cno_str = self.Cno_LineEdit.text()
        if cno_str :
            try:
                Cno_number = int(cno_str)
                if(len(cno_str)!=8):
                    raise ValueError()
                return cno_str
            except ValueError:
            # 类型转换错误，弹窗提示用户
                createErrorInfoBar(self,"输入错误", "班级编号输入无效 请输入一个有效的8位整数。")

    def select_lesson(self):
        cno_str = self.getCno()
        if cno_str:
            db = DatabaseConnection()
            db.connect()
            # 先查询所属班级
            query = """ SELECT m.Mname, m.Mno
                        FROM sms_class c, sms_major m
                        WHERE
                        (
                            c.Cno = %s AND
                            c.Mno = m.Mno
                        );"""
            result = db.execute_query(query,cno_str)
            
            # 存在该班级
            if result:
                self.set_major_label(result)
                query = """ SELECT c.Cname,l.Lno,l.Lname,l.Lhours,l.Lsemester,l.Lcredits,l.Lexam,sh.Tno,t.Tname
                            FROM sms_schedule sh, sms_lesson l,sms_teacher t,sms_class c
                            WHERE
                            (
                            c.Cno = %s AND
                            c.Cno = sh.Cno AND
                            sh.Lno = l.Lno AND
                            sh.Tno = t.Tno
                            )"""
                
                result = db.execute_query(query,cno_str)

                if result:
                    self.fill_table(result)
                    self.set_Year_ComboBox()
                    createSuccessInfoBar(self,"查询成功","恭喜！！！")
                else:
                    createWarningInfoBar(self,"提示", "该班级的课表为空",InfoBarPosition.TOP)
            else:
                createWarningInfoBar(self,"警告", "不存在该班级",InfoBarPosition.TOP)
            db.disconnect()     
        else:
            createErrorInfoBar(self,"查看失败", "请先输入班级编号",InfoBarPosition.TOP)

    def set_major_label(self,data):
        self.Major_label.setText(data[0][0])
        self.Mno_label.setText(data[0][1])

    # 获取comboBox的值筛选table
    def year_comboBox_changed(self):
        year_str = self.year_comboBox.currentText()
        if year_str != "全选":
            for row in range(self.lesson_tableWidget.rowCount()):
                item = self.lesson_tableWidget.item(row, 4) 
                if item is not None and item.text() == year_str:
                    self.lesson_tableWidget.showRow(row)
                else:
                    self.lesson_tableWidget.hideRow(row)
        else:
            for row in range(self.lesson_tableWidget.rowCount()):
                self.lesson_tableWidget.showRow(row)

    def fill_table(self,data):
        index_num = len(data)
        col_num = 9
        # 设置行数 列数
        self.lesson_tableWidget.setRowCount(index_num)
        self.lesson_tableWidget.setColumnCount(col_num)
        col_names=['班级名称','课程编号',"课程名称",'学时','学期','学分','考试/考查','教师编号',"教师姓名"]
        self.lesson_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                item = QTableWidgetItem(str(indexInfo[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                # if j == 2:
                #     item.setFlags(item.flags() | Qt.ItemIsEditable)  # 设置为可编辑
                self.lesson_tableWidget.setItem(i, j, item)

        # 调整列宽度
        for i in range(10):
            self.lesson_tableWidget.resizeColumnToContents(i)

    # 这个函数的逻辑是先读取表中的数据,然后填充combobox
    def set_Year_ComboBox(self):
        # 因为是有筛选完数据之后调用的 所以一定有数据
        credits_unique_values = set()
        rows = self.lesson_tableWidget.rowCount()
        for row in range(rows):
            cell_value = self.lesson_tableWidget.item(row, 4).text()
            credits_unique_values.add(cell_value)
        
        # 默认全选
        self.year_comboBox.addItem("全选")
        for item in credits_unique_values:
            self.year_comboBox.addItem(item)
        self.year_comboBox.setCurrentIndex(0)
