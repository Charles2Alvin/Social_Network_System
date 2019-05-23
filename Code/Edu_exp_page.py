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
import sip

class Edu_Exp_Window(QWidget):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.currentID = None
        self.initUI()

    #init方法里设置window的属性
    def initUI(self):
        # 设置窗口大小、居中、标题
        self.resize(1280, 960)
        self.center()

        """设置布局和部件"""
        headfont = QFont()
        headfont.setPixelSize(36)
        self.grid = QGridLayout()


        headlineLB = QLabel("教育经历")
        headlineLB.setFont(headfont)
        headlineLB.setFixedHeight(100)

        levelLB = QLabel("等级")
        levelLB.setFixedWidth(180)
        levelLB.setFixedHeight(32)

        schoolLB = QLabel("学校")
        schoolLB.setFixedWidth(180)
        schoolLB.setFixedHeight(32)

        degreeLB = QLabel("学位")
        degreeLB.setFixedWidth(180)
        degreeLB.setFixedHeight(32)

        startdateLB = QLabel("开始时间")
        startdateLB.setFixedWidth(180)
        startdateLB.setFixedHeight(32)

        enddateLB = QLabel("结束时间")
        enddateLB.setFixedWidth(180)
        enddateLB.setFixedHeight(32)

        self.grid.addWidget(headlineLB, 1, 1)
        self.grid.addWidget(levelLB, 2, 1)
        self.grid.addWidget(schoolLB, 2, 2)
        self.grid.addWidget(degreeLB, 2, 3)
        self.grid.addWidget(startdateLB, 2, 4)
        self.grid.addWidget(enddateLB, 2, 5)

        self.addBtn = QPushButton("录入新的教育经历")
        self.addBtn.setFixedWidth(180)
        self.addBtn.setFixedHeight(32)
        self.addBtn.clicked.connect(self.addtuple)

        self.setLayout(self.grid)

    def fetchexp(self):
        model = modelFile.Model()
        model.connect2db()
        result = model.show_edu_exp(self.currentID)
        self.rowindex = 0
        self.record = []
        if len(result) == 0:
            t1 = QLineEdit()
            t2 = QLineEdit()
            t3 = QLineEdit()
            t4 = QLineEdit()
            t5 = QLineEdit()

            t6 = QPushButton("添加")
            t6.setFixedWidth(150)
            t6.setFixedHeight(30)
            t6.setObjectName(str(self.rowindex))
            t6.clicked.connect(self.add2db)

            self.grid.addWidget(t1, self.rowindex+3, 1)
            self.grid.addWidget(t2, self.rowindex+3, 2)
            self.grid.addWidget(t3, self.rowindex+3, 3)
            self.grid.addWidget(t4, self.rowindex+3, 4)
            self.grid.addWidget(t5, self.rowindex+3, 5)
            self.grid.addWidget(t6, self.rowindex+3, 6)

            self.record.append([t1, t2, t3, t4, t5, t6])
            return

        for item in result:
            level = item[1]
            school = item[2]
            degree = item[3]
            start_day = str(item[4])
            end_day = str(item[5])

            t1 = QLineEdit(level)
            t2 = QLineEdit(school)
            t3 = QLineEdit(degree)
            t4 = QLineEdit(start_day)
            t5 = QLineEdit(end_day)

            t6 = QPushButton("更新")
            t6.setObjectName(str(self.rowindex))
            t6.setFixedWidth(100)
            t6.setFixedHeight(30)
            t6.clicked.connect(self.updateLine)

            t7 = QPushButton("删除")
            t7.setObjectName(str(self.rowindex))
            t7.setFixedWidth(100)
            t7.setFixedHeight(30)
            t7.clicked.connect(self.delete_tuple)

            self.grid.addWidget(t1, self.rowindex+3, 1)
            self.grid.addWidget(t2, self.rowindex+3, 2)
            self.grid.addWidget(t3, self.rowindex+3, 3)
            self.grid.addWidget(t4, self.rowindex+3, 4)
            self.grid.addWidget(t5, self.rowindex+3, 5)
            self.grid.addWidget(t6, self.rowindex+3, 6)
            self.grid.addWidget(t7, self.rowindex+3, 7)

            self.rowindex += 1
            self.record.append([t1, t2, t3, t4, t5, t6, t7])

        self.grid.addWidget(self.addBtn, self.rowindex+3, 1)

    def updateLine(self):
        model = modelFile.Model()
        model.connect2db()

        sender = self.sender()
        rowindex = sender.objectName()
        rowindex = int(rowindex)

        level = self.record[rowindex][0].text()
        school = self.record[rowindex][1].text()
        degree = self.record[rowindex][2].text()
        startdate = self.record[rowindex][3].text()
        enddate = self.record[rowindex][4].text()

        model.update_edu_exp(self.currentID, level, school, degree, startdate, enddate)
        self.fetchexp()

    def delete_tuple(self):
        # 删除的时候需要获取信号源的行坐标
        sender = self.sender()
        rowindex = sender.objectName()
        rowindex = int(rowindex)

        level = self.record[rowindex][0].text()

        model = modelFile.Model()
        model.connect2db()
        model.delete_edu_exp(self.currentID, level)

        # 删除所有控件！
        print("will delete", self.record[rowindex][0].text())
        for row in range(len(self.record)):
            for col in range(7):
                self.record[row][col].deleteLater()

        self.fetchexp()

    def add2db(self):
        sender = self.sender()
        rowindex = sender.objectName()
        rowindex = int(rowindex)

        level = self.record[rowindex][0].text()
        school = self.record[rowindex][1].text()
        degree = self.record[rowindex][2].text()
        startDate = self.record[rowindex][3].text()
        endDate = self.record[rowindex][4].text()

        model = modelFile.Model()
        model.connect2db()
        model.add_edu_work(self.currentID, level, school, degree, startDate, endDate)

        for row in range(len(self.record)-1):
            for col in range(7):
                print(row, col)
                self.record[row][col].deleteLater()
        for col in range(6):
            self.record[len(self.record)-1][col].deleteLater()

        self.fetchexp()

    def addtuple(self):
        self.t1 = QLineEdit()
        self.t2 = QLineEdit()
        self.t3 = QLineEdit()
        self.t4 = QLineEdit()
        self.t5 = QLineEdit()

        self.t6 = QPushButton("添加")
        self.t6.setFixedWidth(150)
        self.t6.setFixedHeight(30)
        self.t6.setObjectName(str(self.rowindex))
        self.t6.clicked.connect(self.add2db)

        self.grid.addWidget(self.t1, self.rowindex+3, 1)
        self.grid.addWidget(self.t2, self.rowindex+3, 2)
        self.grid.addWidget(self.t3, self.rowindex+3, 3)
        self.grid.addWidget(self.t4, self.rowindex+3, 4)
        self.grid.addWidget(self.t5, self.rowindex+3, 5)
        self.grid.addWidget(self.t6, self.rowindex+3, 6)

        self.record.append([self.t1, self.t2, self.t3, self.t4, self.t5, self.t6])
        self.rowindex += 1

    def center(self):
        qr = self.frameGeometry()
        #获得中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动窗口的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())
