import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
import modelFile
from SignUpPage import *
import time

class Journal_Window(QWidget):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.currentID = "3"
        self.initUI()

    #init方法里设置window的属性
    def initUI(self):
        # 设置窗口大小、居中、标题
        self.resize(1280, 720)
        self.center()

        """设置布局和部件"""
        headfont = QFont()
        headfont.setPixelSize(36)
        self.grid = QGridLayout()

        headline = QLabel("我的日志")
        headline.setFont(headfont)
        headline.setFixedHeight(100)

        self.grid.addWidget(headline, 1, 1)
        self.setLayout(self.grid)

    def fetch(self):
        model = modelFile.Model()
        model.connect2db()
        jourals = model.fetch_journal(self.currentID)
        self.row = 0
        self.record = []
        if len(jourals) == 0:
            self.addBtn = QPushButton("写日志")
            self.addBtn.setFixedWidth(180)
            self.addBtn.setFixedHeight(32)
            self.addBtn.clicked.connect(self.bottomAdd)
            self.grid.addWidget(self.addBtn, self.row + 2, 1)

        for item in jourals:
            title = item[1]
            content = item[2]
            publish_time = str(item[3])

            t1 = QTextEdit()
            display = str(title)+"\n"+str(content)+"\n"


            # 提取这篇日志的所有评论
            comments = model.fetch_comment(self.currentID, publish_time)
            if len(comments) != 0:
                display += "\n\n\n\n\n-------------以下为好友评论-------------\n"
                for comment in comments:
                    replier = comment[0]
                    reply_content = comment[1]
                    reply_time = str(comment[2])
                    display += "来自好友：" + replier + "\n"
                    display += "评论内容：" + reply_content + "\n"
                    display += "回复时间：" + reply_time + "\n"
            display += "\n-------------最新更新时间（请勿修改）-------------\n"
            display += publish_time

            t1.setText(display)

            self.grid.addWidget(t1, self.row+2, 1)
            self.row += 1
            self.record.append([t1])
        # 底部添加新增按钮
        self.addBtn = QPushButton("写日志")
        self.addBtn.setFixedWidth(180)
        self.addBtn.setFixedHeight(32)
        self.addBtn.clicked.connect(self.bottomAdd)
        self.grid.addWidget(self.addBtn, self.row+2, 1)
        # 同理，新增编辑按钮，按下后每篇日志旁边出现修改和删除按钮
        self.editBtn = QPushButton("编辑")
        self.editBtn.setObjectName(str(self.row+2))
        self.editBtn.setFixedWidth(180)
        self.editBtn.setFixedHeight(32)
        self.editBtn.clicked.connect(self.bottomEdit)
        self.grid.addWidget(self.editBtn, self.row + 2, 2)

    def bottomEdit(self):
        rows = len(self.record)
        for row in range(rows):
            t1 = QPushButton("再次发布")
            t1.setFixedWidth(100)
            t1.clicked.connect(self.update_slot)
            t1.setFixedHeight(30)
            t1.setObjectName(str(row))

            t2 = QPushButton("删除")
            t2.clicked.connect(self.delete_slot)
            t2.setFixedWidth(100)
            t2.setFixedHeight(30)
            t2.setObjectName(str(row))

            self.record[row].append(t1)
            self.record[row].append(t2)
            self.grid.addWidget(t1, row+2, 2)
            self.grid.addWidget(t2, row+2, 3)
        self.editBtn.deleteLater()
        row = self.editBtn.objectName()
        self.cancelBtn = QPushButton("取消")
        self.cancelBtn.clicked.connect(self.cancel_slot)
        self.cancelBtn.setFixedWidth(180)
        self.cancelBtn.setFixedHeight(30)
        self.grid.addWidget(self.cancelBtn, int(row), 3)

    def cancel_slot(self):
        # 删除所有组件
        rows = len(self.record)
        for row in range(rows):
            for col in range(3):
                self.record[row][col].deleteLater()
        self.record[-1][1].deleteLater()
        # 删除底部按钮
        self.addBtn.deleteLater()
        self.cancelBtn.deleteLater()

        # 重新渲染页面
        self.fetch()

    def update_slot(self):
        sender = self.sender()
        row = int(sender.objectName())
        # 提取内容
        content = self.record[row][0].toPlainText()
        length = len(content)
        if content[-1] == '\n':
            content = content[:length]
        # 提取标题
        index1 = 0
        for i in range(length):
            if content[i] == '\n':
                index1 = i
                break
        title = content[0:index1]
        # 提取时间
        index2 = 0
        for i in range(length):
            if content[i] == '\n':
                index2 = i
        lastLine = content[index2 + 1:]
        # 提取主体
        body = content[index1+1:index2]
        length = len(body)
        body = body[0:length-39]
        model = modelFile.Model()
        model.connect2db()
        model.deleteJournal(self.currentID, str(lastLine))
        model.addJournal(self.currentID, title, body, lastLine)
        self.fetch()

    def delete_slot(self):
        sender = self.sender()
        row = int(sender.objectName())
        content = self.record[row][0].toPlainText()
        length = len(content)
        if content[-1] == '\n':
            content = content[:length]
        index = 0
        for i in range(length):
            if content[i] == '\n':
                index = i
        lastLine = content[index+1:]

        model = modelFile.Model()
        model.connect2db()
        model.deleteJournal(self.currentID, str(lastLine))

        # 删除所有组件
        rows = len(self.record)
        for row in range(rows):
            for col in range(3):
                self.record[row][col].deleteLater()
        self.record[-1][1].deleteLater()
        # 删除底部按钮
        self.addBtn.deleteLater()
        #self.editBtn.setVisible(False)
        # 重新渲染页面
        self.fetch()

    # 新增一个文本框，以及一个发表按钮，这时隐藏编辑按钮
    def bottomAdd(self):
        t1 = QTextEdit()
        t2 = QPushButton("发表")
        t2.setFixedWidth(180)
        t2.setFixedHeight(30)
        t2.setObjectName(str(self.row))
        t2.clicked.connect(self.addJournal)
        self.editBtn.setVisible(False)

        self.grid.addWidget(t1, self.row+2, 1)
        self.grid.addWidget(t2, self.row+2, 2)
        self.record.append([t1, t2])

    def addJournal(self):
        sender = self.sender()
        row = int(sender.objectName())
        content = self.record[row][0].toPlainText()
        for i in range(len(content)):
            if content[i] == '\n':
                break
        title = content[0:i]
        body = content[i+1:]
        now = int(round(time.time() * 1000))
        publish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))

        model = modelFile.Model()
        model.connect2db()
        model.addJournal(self.currentID, title, body, publish_time)
        # 添加完成后，删除所有组件
        rows = len(self.record)
        print(self.record)
        for row in range(rows):
            self.record[row][0].deleteLater()
        self.record[-1][1].deleteLater()
        self.addBtn.deleteLater()
        self.editBtn.deleteLater()
        # 重新加载页面
        self.fetch()


    def center(self):
        qr = self.frameGeometry()
        #获得中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动窗口的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())
