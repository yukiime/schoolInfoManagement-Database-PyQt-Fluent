from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView,QHeaderView
from qfluentwidgets import InfoBarPosition
from database import DatabaseConnection
from general.CustomTableItemDelegate import CustomTableItemDelegate
from general.infoBar import *
from ui.Ui_students_info_Sno import Ui_Students_info_Sno
from ui.Ui_students_info_Area import Ui_Students_info_Area
from ui.Ui_students_info_Age import Ui_Students_info_Age
from ui.Ui_students_info_Credit import Ui_Students_info_Credit
from ui.Ui_students_info_class import Ui_Students_info_Class


class Students_info_Sno(Ui_Students_info_Sno):
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
        self.setContentsMargins(15, 0, 0, 0)

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.data_tableWidget)
        ctd.set_index_num([0,2])
        self.data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.select_pushButton.clicked.connect(self.selectData)

    def get_Sno(self):
        Sno_text = self.Sno_lineEdit.text()
        try:
            Sno_number = int(Sno_text)
            if(len(Sno_text)!=12):
                raise ValueError()
            return Sno_text
        except ValueError:
        # 类型转换错误，弹窗提示用户
            createErrorInfoBar(self,"输入错误", "学号输入无效，请输入一个有效的十二位整数。",InfoBarPosition.TOP_RIGHT)

    def selectData(self):
        Sno_text = self.get_Sno()
        if Sno_text:
            db = DatabaseConnection()
            db.connect()
            query = "SELECT * FROM sms_students WHERE Sno = %s"
            result = db.execute_query(query,Sno_text)
            self.fill_table(result)
            if result:
                self.resultHint_label.setText("结果如下")
                createSuccessInfoBar(self,"查询成功", "恭喜！",InfoBarPosition.TOP_RIGHT)
            else:
                self.resultHint_label.setText("无满足查询条件的结果")
                createWarningInfoBar(self,"查询失败", "没有满足条件的学生",InfoBarPosition.TOP_RIGHT)

    def fill_table(self,data):
        col_names=["学号","班级编号","姓名","性别","年龄","生源地","已修学分"]
        index_num = len(data)
        col_num = len(col_names)
        # 设置行数 列数
        self.data_tableWidget.setRowCount(index_num)
        self.data_tableWidget.setColumnCount(col_num)
        self.data_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                self.data_tableWidget.setItem(i, j, QTableWidgetItem(str(indexInfo[j])))
        # 调整列宽度
        self.data_tableWidget.setColumnWidth(0,130)
        self.data_tableWidget.setColumnWidth(1,110)
        self.data_tableWidget.setColumnWidth(2,110)

class Students_info_Area(Ui_Students_info_Area):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        self.Area_lineEdit.setText("浙江省")
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
        self.setContentsMargins(15, 0, 0, 0)

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.data_tableWidget)
        ctd.set_index_num([0,2,5])
        self.data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.select_pushButton.clicked.connect(self.selectData)

    def selectData(self):
        Area_text = self.Area_lineEdit.text()
        if Area_text:
            db = DatabaseConnection()
            db.connect()
            query = "SELECT * FROM sms_students WHERE Sarea = %s"
            result = db.execute_query(query,Area_text)
            self.fill_table(result)
            num = len(result)
            if result:
                self.resultHint_label.setText(("结果如下, 该地区总人数为 " + str(num)))
                createSuccessInfoBar(self,"查询成功", "恭喜！",InfoBarPosition.TOP_RIGHT)
            else:
                self.resultHint_label.setText("无满足查询条件的结果")
                createWarningInfoBar(self,"查询失败", "没有满足条件的学生",InfoBarPosition.TOP_RIGHT)

    def fill_table(self,data):
        col_names=["学号","班级编号","姓名","性别","年龄","生源地","已修学分"]
        index_num = len(data)
        col_num = len(col_names)
        # 设置行数 列数
        self.data_tableWidget.setRowCount(index_num)
        self.data_tableWidget.setColumnCount(col_num)
        self.data_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                self.data_tableWidget.setItem(i, j, QTableWidgetItem(str(indexInfo[j])))
        # 调整列宽度
        self.data_tableWidget.setColumnWidth(0,130)
        self.data_tableWidget.setColumnWidth(1,110)
        self.data_tableWidget.setColumnWidth(2,110)

class Students_info_Age(Ui_Students_info_Age):
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
        self.setContentsMargins(15, 0, 0, 0)

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.data_tableWidget)
        ctd.set_index_num([0,2,4])
        self.data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.select_pushButton.clicked.connect(self.selectData)
        self.Male_CheckBox.stateChanged.connect(self.Male_CheckBoxStateChanged)
        self.female_CheckBox.stateChanged.connect(self.Female_CheckBoxStateChanged)

    def getFilterConditions(self):
        Age_min = self.Age_Minimum_SpinBox.text()
        Age_max = self.Age_Maxmum_SpinBox.text()
        if Age_min and Age_max:
            Age_min = int(Age_min)
            Age_max = int(Age_max)
            if Age_max >= Age_min:
                check_male = self.Male_CheckBox.isChecked()
                check_female = self.female_CheckBox.isChecked()
                if (check_male is False) and (check_female is False) :
                    createErrorInfoBar(self,"输入错误", "必须至少勾选一个男或女的复选框",InfoBarPosition.TOP_RIGHT)
                    return None,None,None,None
                else:
                    return Age_min,Age_max,check_male,check_female
            else:
                createErrorInfoBar(self,"输入错误", "年龄上限不得小于年龄下限",InfoBarPosition.TOP_RIGHT)
                return None,None,None,None
        else:
            createErrorInfoBar(self,"输入错误", "没有给出合法的年龄数值",InfoBarPosition.TOP_RIGHT)
            return None,None,None,None

    def selectData(self):
        Age_min,Age_max,check_male,check_female = self.getFilterConditions()
        if Age_min and Age_max:
            db = DatabaseConnection()
            db.connect()

            if check_male and check_female :
                query = "SELECT * FROM sms_students WHERE ( Sage >= %s AND Sage <= %s )"
            elif check_male :
                query = "SELECT * FROM sms_students WHERE ( Sage >= %s AND Sage <= %s AND Ssex =  \"男\" )"
            elif check_female :
                query = "SELECT * FROM sms_students WHERE ( Sage >= %s AND Sage <= %s AND Ssex =  \"女\")"
            else:
                createErrorInfoBar(self,"输入错误", "必须至少勾选一个男或女的复选框",InfoBarPosition.TOP_RIGHT)

            result = db.execute_query(query,(Age_min,Age_max))
            self.fill_table(result)
            num = len(result)

            if result:
                self.resultHint_label.setText(("结果如下, 该年龄区间总人数为 " + str(num)))
                createSuccessInfoBar(self,"查询成功", "恭喜！",InfoBarPosition.TOP_RIGHT)
            else:
                self.resultHint_label.setText("无满足查询条件的结果")
                createWarningInfoBar(self,"查询失败", "没有满足条件的学生",InfoBarPosition.TOP_RIGHT)

    def Male_CheckBoxStateChanged(self):
        check_female = self.female_CheckBox.isChecked()
        check_male = self.Male_CheckBox.isChecked()
        if self.data_tableWidget.rowCount() > 0:
            for row in range(self.data_tableWidget.rowCount()):
                item = self.data_tableWidget.item(row, 3)  # 第4列的单元格
                if item is not None and item.text() == "男":
                    if check_male:
                        self.data_tableWidget.showRow(row)
                    else:
                        self.data_tableWidget.hideRow(row)
            if (check_male is False) and (check_female is False) :
                createWarningInfoBar(self,"不恰当的筛选", "建议至少勾选男或女",InfoBarPosition.BOTTOM_RIGHT)
            else:
                createSuccessInfoBar(self,"筛选成功", "恭喜！",InfoBarPosition.BOTTOM_RIGHT)

    def Female_CheckBoxStateChanged(self):
        check_male = self.Male_CheckBox.isChecked()
        check_female = self.female_CheckBox.isChecked()
        if self.data_tableWidget.rowCount() > 0:
            for row in range(self.data_tableWidget.rowCount()):
                item = self.data_tableWidget.item(row, 3)  # 第4列的单元格
                if item is not None and item.text() == "女":
                    if check_female:
                        self.data_tableWidget.showRow(row)
                    else:
                        self.data_tableWidget.hideRow(row)
            
            if (check_male is False) and (check_female is False) :
                createWarningInfoBar(self,"不恰当的筛选", "建议至少勾选男或女",InfoBarPosition.BOTTOM_RIGHT)
            else:
                createSuccessInfoBar(self,"筛选成功", "恭喜！",InfoBarPosition.BOTTOM_RIGHT)

    def fill_table(self,data):
        col_names=["学号","班级编号","姓名","性别","年龄","生源地","已修学分"]
        index_num = len(data)
        col_num = len(col_names)
        # 设置行数 列数
        self.data_tableWidget.setRowCount(index_num)
        self.data_tableWidget.setColumnCount(col_num)
        self.data_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                self.data_tableWidget.setItem(i, j, QTableWidgetItem(str(indexInfo[j])))
        # 调整列宽度
        self.data_tableWidget.setColumnWidth(0,130)
        self.data_tableWidget.setColumnWidth(1,110)
        self.data_tableWidget.setColumnWidth(2,110)

class Students_info_Credit(Ui_Students_info_Credit):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        self.Credit_Maxmum_SpinBox.setRange(0,300)
        self.Credit_Minimum_SpinBox.setRange(0,300)
        self.Credit_Minimum_SpinBox.setValue(6)
        self.Credit_Maxmum_SpinBox.setValue(25)
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
        self.setContentsMargins(15, 0, 0, 0)

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.data_tableWidget)
        ctd.set_index_num([0,2,6])
        self.data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.select_pushButton.clicked.connect(self.selectData)
        self.Male_CheckBox.stateChanged.connect(self.Male_CheckBoxStateChanged)
        self.Female_CheckBox.stateChanged.connect(self.Female_CheckBoxStateChanged)

    def getFilterConditions(self):
        Credit_min = self.Credit_Minimum_SpinBox.text()
        Credit_max = self.Credit_Maxmum_SpinBox.text()
        if Credit_min and Credit_max:
            Credit_min = int(Credit_min)
            Credit_max = int(Credit_max)
            if Credit_max >= Credit_min:
                check_male = self.Male_CheckBox.isChecked()
                check_female = self.Female_CheckBox.isChecked()
                if (check_male is False) and (check_female is False) :
                    createErrorInfoBar(self,"输入错误", "必须至少勾选一个男或女的复选框",InfoBarPosition.TOP_RIGHT)
                    return None,None,None,None
                else:
                    return Credit_min,Credit_max,check_male,check_female
            else:
                createErrorInfoBar(self,"输入错误", "已修学分数目的上限不得小于其下限",InfoBarPosition.TOP_RIGHT)
                return None,None,None,None
        else:
            createErrorInfoBar(self,"输入错误", "没有给出合法的学分数值",InfoBarPosition.TOP_RIGHT)
            return None,None,None,None

    def selectData(self):
        Credit_min,Credit_max,check_male,check_female = self.getFilterConditions()
        if Credit_max:
            db = DatabaseConnection()
            db.connect()

            if check_male and check_female :
                query = "SELECT * FROM sms_students WHERE ( Scredits >= %s AND Scredits <= %s )"
            elif check_male :
                query = "SELECT * FROM sms_students WHERE ( Scredits >= %s AND Scredits <= %s AND Ssex =  \"男\" )"
            elif check_female :
                query = "SELECT * FROM sms_students WHERE ( Scredits >= %s AND Scredits <= %s AND Ssex =  \"女\")"
            else:
                createErrorInfoBar(self,"输入错误", "必须至少勾选一个男或女的复选框",InfoBarPosition.TOP_RIGHT)

            result = db.execute_query(query,(Credit_min,Credit_max))
            self.fill_table(result)
            num = len(result)

            if result:
                self.resultHint_label.setText(("结果如下, 该已修学分数目区间总人数为 " + str(num)))
                createSuccessInfoBar(self,"查询成功", "恭喜！",InfoBarPosition.TOP_RIGHT)
            else:
                self.resultHint_label.setText("无满足查询条件的结果")
                createWarningInfoBar(self,"查询失败", "没有满足条件的学生",InfoBarPosition.TOP_RIGHT)

    def Male_CheckBoxStateChanged(self):
        check_female = self.Female_CheckBox.isChecked()
        check_male = self.Male_CheckBox.isChecked()
        if self.data_tableWidget.rowCount() > 0:
            for row in range(self.data_tableWidget.rowCount()):
                item = self.data_tableWidget.item(row, 3)  # 第4列的单元格
                if item is not None and item.text() == "男":
                    if check_male:
                        self.data_tableWidget.showRow(row)
                    else:
                        self.data_tableWidget.hideRow(row)
            if (check_male is False) and (check_female is False) :
                createWarningInfoBar(self,"不恰当的筛选", "建议至少勾选男或女",InfoBarPosition.BOTTOM_RIGHT)
            else:
                createSuccessInfoBar(self,"筛选成功", "恭喜！",InfoBarPosition.BOTTOM_RIGHT)

    def Female_CheckBoxStateChanged(self):
        check_male = self.Male_CheckBox.isChecked()
        check_female = self.Female_CheckBox.isChecked()
        if self.data_tableWidget.rowCount() > 0:
            for row in range(self.data_tableWidget.rowCount()):
                item = self.data_tableWidget.item(row, 3)  # 第4列的单元格
                if item is not None and item.text() == "女":
                    if check_female:
                        self.data_tableWidget.showRow(row)
                    else:
                        self.data_tableWidget.hideRow(row)
            
            if (check_male is False) and (check_female is False) :
                createWarningInfoBar(self,"不恰当的筛选", "建议至少勾选男或女",InfoBarPosition.BOTTOM_RIGHT)
            else:
                createSuccessInfoBar(self,"筛选成功", "恭喜！",InfoBarPosition.BOTTOM_RIGHT)

    def fill_table(self,data):
        self.data_tableWidget.clearContents()
        self.data_tableWidget.setRowCount(0)
        col_names=["学号","班级编号","姓名","性别","年龄","生源地","已修学分"]
        index_num = len(data)
        col_num = len(col_names)
        # 设置行数 列数
        self.data_tableWidget.setRowCount(index_num)
        self.data_tableWidget.setColumnCount(col_num)
        self.data_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                self.data_tableWidget.setItem(i, j, QTableWidgetItem(str(indexInfo[j])))
        # 调整列宽度
        self.data_tableWidget.setColumnWidth(0,130)
        self.data_tableWidget.setColumnWidth(1,110)
        self.data_tableWidget.setColumnWidth(2,110)

class Students_info_Class(Ui_Students_info_Class):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_slots()
        self.init_widget_UI()
        self.set_customTableItemDelegate()

    def init_widget_UI(self):
        self.Major_LineEdit.setText("0334")
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
        self.setContentsMargins(15, 0, 0, 0)

    def set_customTableItemDelegate(self):
        # NOTE: use custom item delegate
        ctd = CustomTableItemDelegate(self.data_tableWidget)
        ctd.set_index_num([0,2])
        self.data_tableWidget.setItemDelegate(ctd)

    def init_slots(self):
        self.select_pushButton.clicked.connect(self.selectData)
        self.Class_SwitchButton.checkedChanged.connect(self.set_Major_Class_ComboBox)
        self.Male_CheckBox.stateChanged.connect(self.Male_CheckBoxStateChanged)
        self.Female_CheckBox.stateChanged.connect(self.Female_CheckBoxStateChanged)

    def set_Major_Class_ComboBox(self):
        Major_str = self.Major_LineEdit.text()
        # 如果打算筛选班级
        if self.Class_SwitchButton.checked:
            # 禁止编辑
            self.Major_LineEdit.setEnabled(False)
            self.select_pushButton.setText("查询班级")
            if Major_str :
                try:
                    Major_int = int(Major_str)
                    if(len(Major_str)!=4):
                        raise ValueError()
                except ValueError:
                # 类型转换错误，弹窗提示用户
                    createErrorInfoBar(self,"输入错误", "专业编号输入无效，请输入一个有效的四位整数。",InfoBarPosition.TOP_LEFT)
            # 查询        
            query = "SELECT Cno FROM sms_class WHERE ( Mno = %s )"
            db = DatabaseConnection()
            db.connect()
            result = db.execute_query(query,Major_str)
            if result:
                # 将保存的LineEdit的值添加到ComboBox中
                for item in result:
                    self.Class_ComboBox.addItem(item[0])
                self.Class_ComboBox.setCurrentIndex(0)
            else:
                createWarningInfoBar(self,"筛选失败", "该专业下暂无班级",InfoBarPosition.TOP_RIGHT)
        else:
            # 恢复编辑
            self.Major_LineEdit.setEnabled(True)
            # 清空ComboBox的值
            self.Class_ComboBox.clear()
            # 更改按钮文本
            self.select_pushButton.setText("查询专业")

    def selectData(self):
        self.data_tableWidget.clearContents()
        self.data_tableWidget.setRowCount(0)
        # 要求班级筛选
        if self.Class_SwitchButton.checked:
            class_str = self.Class_ComboBox.currentText()
            if class_str:
                query = "SELECT sms_major.Mname,sms_class.Cname,sms_students.* FROM sms_class,sms_major,sms_students WHERE ( sms_students.Cno = %s AND sms_students.Cno = sms_class.Cno AND sms_class.Mno = sms_major.Mno )"
                db = DatabaseConnection()
                db.connect() 
                result = db.execute_query(query,class_str)
                self.fill_table(result)
                if result:
                    num = len(result)
                    self.resultHint_label.setText(("结果如下, 该班级总人数为 " + str(num)))
                    createSuccessInfoBar(self,"查询成功", "恭喜！",InfoBarPosition.TOP_RIGHT)
                else:
                    self.resultHint_label.setText("无满足查询条件的结果")
                    createWarningInfoBar(self,"查询失败", "没有满足条件的学生",InfoBarPosition.TOP_RIGHT)
            else:
                createErrorInfoBar(self,"筛选错误", "未选择班级编号",InfoBarPosition.TOP_RIGHT)
        # 筛选专业
        else:
            major_str = self.Major_LineEdit.text()
            if major_str:
                try:
                    Major_int = int(major_str)
                    if(len(major_str)!=4):
                        raise ValueError()
                except ValueError:
                # 类型转换错误，弹窗提示用户
                    createErrorInfoBar(self,"输入错误", "专业编号输入无效，请输入一个有效的四位整数。",InfoBarPosition.TOP_LEFT)
                # 查询        
                query = "SELECT sms_major.Mname,sms_class.Cname,sms_students.* FROM sms_class,sms_major,sms_students WHERE ( sms_class.Mno = %s AND sms_students.Cno = sms_class.Cno AND sms_class.Mno = sms_major.Mno )"
                db = DatabaseConnection()
                db.connect() 
                result = db.execute_query(query,major_str)
                self.fill_table(result)
                if result:
                    num = len(result)
                    self.resultHint_label.setText(("结果如下, 该专业总人数为 " + str(num)))
                    createSuccessInfoBar(self,"查询成功", "恭喜！",InfoBarPosition.TOP_RIGHT)
                else:
                    self.resultHint_label.setText("无满足查询条件的结果")
                    createWarningInfoBar(self,"查询失败", "可能该专业暂时没有招收学生",InfoBarPosition.TOP_RIGHT)
            else:
                createErrorInfoBar(self,"输入错误", "未输入专业编号",InfoBarPosition.TOP_RIGHT)

        check_male,check_female = self.Male_CheckBox.isChecked(),self.Female_CheckBox.isChecked()
        if check_male and check_female :
            pass
        elif not check_male :
            self.Male_CheckBoxStateChanged()
        elif not check_female :
            self.Male_CheckBoxStateChanged()

    def Male_CheckBoxStateChanged(self):
        check_female = self.Female_CheckBox.isChecked()
        check_male = self.Male_CheckBox.isChecked()
        if self.data_tableWidget.rowCount() > 0:
            for row in range(self.data_tableWidget.rowCount()):
                item = self.data_tableWidget.item(row, 5)  # 第4列的单元格
                if item is not None and item.text() == "男":
                    if check_male:
                        self.data_tableWidget.showRow(row)
                    else:
                        self.data_tableWidget.hideRow(row)
            if (check_male is False) and (check_female is False) :
                createWarningInfoBar(self,"不恰当的筛选", "建议至少勾选男或女",InfoBarPosition.BOTTOM_RIGHT)
            else:
                createSuccessInfoBar(self,"筛选成功", "恭喜！",InfoBarPosition.BOTTOM_RIGHT)

    def Female_CheckBoxStateChanged(self):
        check_male = self.Male_CheckBox.isChecked()
        check_female = self.Female_CheckBox.isChecked()
        if self.data_tableWidget.rowCount() > 0:
            for row in range(self.data_tableWidget.rowCount()):
                item = self.data_tableWidget.item(row, 5)  # 第4列的单元格
                if item is not None and item.text() == "女":
                    if check_female:
                        self.data_tableWidget.showRow(row)
                    else:
                        self.data_tableWidget.hideRow(row)
            
            if (check_male is False) and (check_female is False) :
                createWarningInfoBar(self,"不恰当的筛选", "建议至少勾选男或女",InfoBarPosition.BOTTOM_RIGHT)
            else:
                createSuccessInfoBar(self,"筛选成功", "恭喜！",InfoBarPosition.BOTTOM_RIGHT)

    def fill_table(self,data):
        col_names=["专业名称","班级名称","学号","班级编号","姓名","性别","年龄","生源地","已修学分"]
        index_num = len(data)
        col_num = len(col_names)
        # 设置行数 列数
        self.data_tableWidget.setRowCount(index_num)
        self.data_tableWidget.setColumnCount(col_num)
        self.data_tableWidget.setHorizontalHeaderLabels(col_names)
        for i, indexInfo in enumerate(data):
            for j in range(col_num):
                self.data_tableWidget.setItem(i, j, QTableWidgetItem(str(indexInfo[j])))
        # 调整列宽度
        for i in range(col_num):
            self.data_tableWidget.resizeColumnToContents(i)
        
        # self.data_tableWidget.resizeColumnToContents(1)
        # self.data_tableWidget.setColumnWidth(0,130)
        # self.data_tableWidget.setColumnWidth(1,110)
        # self.data_tableWidget.setColumnWidth(2,110)
