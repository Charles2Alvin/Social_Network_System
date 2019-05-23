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
from PyQt5.QtGui import *
import time
import pymysql


class Plaza_Window(QWidget):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.currentID = None
        self.initUI()

    #init方法里设置window的属性
    def initUI(self):
        # 设置窗口大小、居中、标题
        self.resize(1280, 720)
        self.center()

        """设置布局和部件"""
        self.grid = QGridLayout()

        self.headline = QLabel()
        self.headline.setText("<font color=%s>%s</font>" % ('#F3EFEE', "每一刻精彩都不容错过"))
        headfont = QFont('微软雅黑', 36)
        headfont.setBold(True)
        self.headline.setFont(headfont)
        self.headline.setFixedHeight(50)
        self.grid.addWidget(self.headline, 1, 1)
        self.setLayout(self.grid)


    def bottomDeGrp(self):
        grp_name, ok = QInputDialog.getText(
            self, "删除分组", "请输入删除的分组名:",
            QLineEdit.Normal, "这是默认值")
        if not ok:
            return
        if grp_name == "默认分组":
            return
        model = modelFile.Model()
        model.connect2db()
        status = model.chGrp(self.currentID, grp_name)
        if status == 1:
            QMessageBox.information(self, "分组信息", "没有这个分组诶",
                                    QMessageBox.Yes)
        if status == 0:
            QMessageBox.information(self, "分组信息", "修改成功",
                                    QMessageBox.Yes)
        self.showfriends()

    def bottomAddGrp(self):
        grp_name, ok = QInputDialog.getText(
            self, "新增分组", "请输入新的分组名:",
            QLineEdit.Normal, "这是默认值")
        if not ok:
            return
        model = modelFile.Model()
        model.connect2db()
        result = model.existGrp(grp_name)
        if len(result) != 0:
            QMessageBox.information(self, "分组信息", "这个分组已存在哦",
                                            QMessageBox.Yes)
            return
        model.addGrp(self.currentID, grp_name)
        self.showfriends()

    def refresh(self):
        model = modelFile.Model()
        model.connect2db()
        contents = model.get_fri_journal(self.currentID)
        self.row = 0
        self.record = []
        if len(contents) == 0:
            return
        for item in contents:
            name = item[0]
            email = item[1]
            title = item[2]
            body = item[3]
            time = item[4]
            content = name + "\n"
            content += "via (" + email + ")\n"
            content += "————————————————————<"
            content += title
            content += ">————————————————————\n"
            content += body
            content += "\n\n\n发布于*"
            content += str(time)

            t1 = QTextEdit()
            t1.setText(content)

            t2 = QPushButton("添加评论")
            t2.setObjectName(str(self.row))
            t2.setFixedWidth(100)
            t2.setFixedHeight(30)
            t2.clicked.connect(self.addComment)

            t3 = QPushButton("转载")
            t3.setObjectName(str(self.row))
            t3.setFixedWidth(100)
            t3.setFixedHeight(30)
            t3.clicked.connect(self.share)

            self.grid.addWidget(t1, self.row + 2, 1)
            self.grid.addWidget(t2, self.row + 2, 2)
            self.grid.addWidget(t3, self.row + 2, 3)
            self.row += 1
            self.record.append([t1, t2, t3])

    def share(self):
        sender = self.sender()
        row = int(sender.objectName())
        # 获取文本和好友名
        text = self.record[row][0].toPlainText()
        length = len(text)
        for i in range(length):
            if text[i] == '\n': break
        fri_name = text[0:i]

        # 获取用户评论
        comment, ok = QInputDialog.getMultiLineText(
            self, "动态转载", "写下这一刻的感受～", "")
        if not ok:
            return

        # 构建新日志
        title = "转载自 " + fri_name + " 的内容"
        body = "我的评论：\n"
        body += comment
        body += "\n————————————————————我是分隔线————————————————————\n"
        body += text

        now = int(round(time.time() * 1000))
        share_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
        model = modelFile.Model()
        model.connect2db()
        model.addJournal(self.currentID, title, body, share_time)
        QMessageBox.information(self, "提醒", "转载成功！",
                                QMessageBox.Yes)

    def addComment(self):
        sender = self.sender()
        row = int(sender.objectName())
        text = self.record[row][0].toPlainText()
        comment, ok = QInputDialog.getMultiLineText(
            self, "添加评论", "请在下方输入评论:", "")
        if not ok:
            return
        length = len(text)
        for i in range(length):
            if text[i] == '(':
                break
        for j in range(length):
            if text[j] == ')':
                break
        for p in range(length):
            if text[p] == '<':
                break
        for q in range(length):
            if text[q] == '>':
                break
        friMail = text[i+1:j]
        publish_time = text[length-19:]
        title = text[p+1:q]
        now = int(round(time.time() * 1000))
        comment_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
        model = modelFile.Model()
        model.connect2db()
        myname = model.usrinfo(self.currentID)
        myname = myname[0]
        raw = model.fetch_journal_time(friMail, publish_time)

        body = list(raw)[0]
        body += "\n\n\n————————————————————"
        body += "来自 "
        body += str(myname)
        body += " 的评论"
        body += "————————————————————\n"
        body += comment+"\n"
        body += comment_time
        try:
            model.deleteJournal(friMail, publish_time)
            model.addJournal(friMail, title, body, publish_time)
            model.conn.commit()
            QMessageBox.information(self, "提醒", "评论成功！",
                                    QMessageBox.Yes)
        except pymysql.Error:
            print("error")
            model.conn.rollback()
        self.refresh()

    def center(self):
        qr = self.frameGeometry()
        #获得中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动窗口的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())
