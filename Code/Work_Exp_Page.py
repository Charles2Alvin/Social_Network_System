import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
import modelFile
from SignUpPage import *
import re
import copy
class Work_Exp_Window(QWidget):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.currentID = None
        self.initUI()

    #init方法里设置window的属性
    def initUI(self):
        # 设置窗口大小、居中、标题
        self.resize(1280, 1080)
        self.center()

        """设置布局和部件"""
        headfont = QFont('微软雅黑', 36)
        font = QFont('微软雅黑', 25)
        self.grid = QGridLayout()


        self.headline = QLabel()
        self.headline.setText("<font color=%s>%s</font>" % ('#F3EFEE', "工作经历"))
        self.headline.setFont(headfont)
        self.headline.setFixedHeight(100)

        self.workplace = QLabel()
        self.workplace.setText("<font color=%s>%s</font>" % ('#F3EFEE', "工作地点"))
        self.workplace.setFont(font)
        self.workplace.setFixedWidth(180)
        self.workplace.setFixedHeight(32)

        self.title = QLabel()
        self.title.setText("<font color=%s>%s</font>" % ('#F3EFEE', "职位"))
        self.title.setFont(font)
        self.title.setFixedWidth(180)
        self.title.setFixedHeight(32)

        self.startdate = QLabel()
        self.startdate.setText("<font color=%s>%s</font>" % ('#F3EFEE', "开始时间"))
        self.startdate.setFont(font)
        self.startdate.setFixedWidth(180)
        self.startdate.setFixedHeight(32)

        self.enddate = QLabel()
        self.enddate.setText("<font color=%s>%s</font>" % ('#F3EFEE', "结束时间"))
        self.enddate.setFont(font)
        self.enddate.setFixedWidth(180)
        self.enddate.setFixedHeight(32)

        self.text = QTextEdit()

        self.updateBtn = QPushButton("录入新的经历")
        self.updateBtn.setFixedWidth(180)
        self.updateBtn.setFixedHeight(32)
        self.updateBtn.clicked.connect(self.bottomAdd)

        self.grid.addWidget(self.headline, 1, 1)
        self.grid.addWidget(self.workplace, 2, 1)
        self.grid.addWidget(self.title, 2, 2)
        self.grid.addWidget(self.startdate, 2, 3)
        self.grid.addWidget(self.enddate, 2, 4)

        self.setLayout(self.grid)

    def fetchexp(self):
        model = modelFile.Model()
        model.connect2db()
        result = model.show_work_exp(self.currentID)
        self.rowindex = 0
        self.record = []
        if len(result) == 0:
            t1 = QLineEdit()
            t2 = QLineEdit()
            t3 = QLineEdit()
            t4 = QLineEdit()

            t5 = QPushButton("添加")
            t5.setFixedWidth(150)
            t5.setFixedHeight(30)
            t5.setObjectName(str(self.rowindex))
            t5.clicked.connect(self.add_exp_tuple)

            self.grid.addWidget(t1, self.rowindex+3, 1)
            self.grid.addWidget(t2, self.rowindex+3, 2)
            self.grid.addWidget(t3, self.rowindex+3, 3)
            self.grid.addWidget(t4, self.rowindex+3, 4)
            self.grid.addWidget(t5, self.rowindex+3, 5)

            self.record.append([t1, t2, t3, t4, t5])

            return

        for item in result:
            work_place = item[1]
            title = item[2]
            start_day = str(item[3])
            end_day = str(item[4])

            t1 = QLineEdit(work_place)
            t2 = QLineEdit(title)
            t3 = QLineEdit(start_day)
            t4 = QLineEdit(end_day)

            t5 = QPushButton("更新")
            t5.setObjectName(str(self.rowindex))
            t5.setFixedWidth(100)
            t5.setFixedHeight(30)
            t5.clicked.connect(self.updateLine)

            t6 = QPushButton("删除")
            t6.setObjectName(str(self.rowindex))
            t6.setFixedWidth(100)
            t6.setFixedHeight(30)
            t6.clicked.connect(self.delete_tuple)

            self.grid.addWidget(t1, self.rowindex+3, 1)
            self.grid.addWidget(t2, self.rowindex+3, 2)
            self.grid.addWidget(t3, self.rowindex+3, 3)
            self.grid.addWidget(t4, self.rowindex+3, 4)
            self.grid.addWidget(t5, self.rowindex+3, 5)
            self.grid.addWidget(t6, self.rowindex+3, 6)
            self.rowindex += 1
            self.record.append([t1, t2, t3, t4, t5, t6])
        self.grid.addWidget(self.updateBtn, self.rowindex+3, 1)

    def updateLine(self):
        model = modelFile.Model()
        model.connect2db()
        sender = self.sender()
        rowindex = sender.objectName()
        rowindex = int(rowindex)
        workplace = self.record[rowindex][0].text()
        title = self.record[rowindex][1].text()
        startdate = self.record[rowindex][2].text()
        enddate = self.record[rowindex][3].text()
        model.update_work_exp(self.currentID, workplace, title, startdate, enddate)
        self.fetchexp()

    def delete_tuple(self):
        model = modelFile.Model()
        model.connect2db()

        sender = self.sender()
        rowindex = sender.objectName()
        rowindex = int(rowindex)

        workplace = self.record[rowindex][0].text()
        title = self.record[rowindex][1].text()

        print("chosen", workplace)

        model.delete_work_exp(self.currentID, workplace, title)

        # 删除所有控件！
        print("will delete", self.record[rowindex][0].text())
        for row in range(len(self.record)):
            for col in range(6):
                self.record[row][col].deleteLater()

        self.fetchexp()

    def add_exp_tuple(self):
        sender = self.sender()
        rowindex = sender.objectName()
        rowindex = int(rowindex)

        workplace = self.record[rowindex][0].text()
        title = self.record[rowindex][1].text()
        startdate = self.record[rowindex][2].text()
        enddate = self.record[rowindex][3].text()

        model = modelFile.Model()
        model.connect2db()
        model.add_work_exp(self.currentID, workplace, title, startdate, enddate)

        # 删除所有控件！

        for row in range(len(self.record)-1):
            for col in range(6):
                print(row, col)
                self.record[row][col].deleteLater()
        for col in range(5):
            self.record[len(self.record)-1][col].deleteLater()
        self.fetchexp()

    def bottomAdd(self):
        model = modelFile.Model()
        model.connect2db()
        self.t1 = QLineEdit()
        self.t2 = QLineEdit()
        self.t3 = QLineEdit()
        self.t4 = QLineEdit()

        self.t5 = QPushButton("添加")
        self.t5.setFixedWidth(150)
        self.t5.setFixedHeight(30)
        self.t5.setObjectName(str(self.rowindex))
        self.t5.clicked.connect(self.add_exp_tuple)

        self.grid.addWidget(self.t1, self.rowindex+3, 1)
        self.grid.addWidget(self.t2, self.rowindex+3, 2)
        self.grid.addWidget(self.t3, self.rowindex+3, 3)
        self.grid.addWidget(self.t4, self.rowindex+3, 4)
        self.grid.addWidget(self.t5, self.rowindex+3, 5)

        self.record.append([self.t1, self.t2, self.t3, self.t4, self.t5])
        self.rowindex += 1

    def center(self):
        qr = self.frameGeometry()
        #获得中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动窗口的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())
