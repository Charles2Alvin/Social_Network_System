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

class FriendInfoWindow(QWidget):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.currentID = None
        self.initUI()

    #init方法里设置window的属性
    def initUI(self):
        # 设置窗口大小、居中、标题
        self.resize(1080, 720)
        self.center()

        """设置布局和部件"""
        headfont = QFont()
        headfont.setPixelSize(36)
        self.grid = QGridLayout()

        self.headline = QLabel("好友都在这里！")
        self.headline.setFont(headfont)
        self.headline.setFixedHeight(100)

        self.nameLB = QLabel("姓名")
        self.nameLB.setFixedWidth(180)
        self.nameLB.setFixedHeight(32)

        self.mailLB = QLabel("邮箱")
        self.mailLB.setFixedWidth(180)
        self.mailLB.setFixedHeight(32)

        self.addrLB = QLabel("地址")
        self.addrLB.setFixedWidth(180)
        self.addrLB.setFixedHeight(32)

        self.grpLB = QLabel("分组")
        self.grpLB.setFixedWidth(180)
        self.grpLB.setFixedHeight(32)

        self.searchBtn = QPushButton("添加关注")
        self.searchBtn.setFixedWidth(150)
        self.searchBtn.setFixedHeight(32)
        self.searchBtn.clicked.connect(self.bottomAdd)

        self.addGrpBtn = QPushButton("新增分组")
        self.addGrpBtn.setFixedWidth(150)
        self.addGrpBtn.setFixedHeight(32)
        self.addGrpBtn.clicked.connect(self.bottomAddGrp)

        self.deGrpBtn = QPushButton("删除分组")
        self.deGrpBtn.setFixedWidth(150)
        self.deGrpBtn.setFixedHeight(32)
        self.deGrpBtn.clicked.connect(self.bottomDeGrp)

        self.grid.addWidget(self.headline, 1, 1)
        self.grid.addWidget(self.nameLB, 2, 1)
        self.grid.addWidget(self.mailLB, 2, 2)
        self.grid.addWidget(self.addrLB, 2, 3)
        self.grid.addWidget(self.grpLB, 2, 4)

        self.setLayout(self.grid)

    def setBackGround(self):
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("")))
        self.setPalette(window_pale)

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

    def showfriends(self):
        model = modelFile.Model()
        model.connect2db()
        friends = model.showfriends(self.currentID)
        self.row = 0
        self.record = []
        if len(friends) == 0:
            self.grid.addWidget(self.searchBtn, self.row + 3, 1)
            self.grid.addWidget(self.addGrpBtn, self.row + 3, 2)
            return

        for item in friends:
            fri_email = item[1]
            grp_name = item[2]

            fri_info = model.usrinfo(fri_email)
            fri_name = fri_info[0]
            fri_addr = fri_info[4]

            t1 = QLabel(fri_name)
            t2 = QLabel(fri_email)
            t3 = QLabel(fri_addr)
            t4 = QLineEdit(grp_name)

            t5 = QPushButton("修改分组")
            t5.setObjectName(str(self.row))
            t5.setFixedWidth(100)
            t5.setFixedHeight(30)
            t5.clicked.connect(self.updateGrp)

            t6 = QPushButton("删除")
            t6.setObjectName(str(self.row))
            t6.setFixedWidth(100)
            t6.setFixedHeight(30)
            t6.clicked.connect(self.deleteFri)

            self.grid.addWidget(t1, self.row + 3, 1)
            self.grid.addWidget(t2, self.row + 3, 2)
            self.grid.addWidget(t3, self.row + 3, 3)
            self.grid.addWidget(t4, self.row + 3, 4)
            self.grid.addWidget(t5, self.row + 3, 5)
            self.grid.addWidget(t6, self.row + 3, 6)
            self.row += 1
            self.record.append([t1, t2, t3, t4, t5, t6])
        self.grid.addWidget(self.searchBtn, self.row + 3, 1)
        self.grid.addWidget(self.addGrpBtn, self.row + 3, 2)
        self.grid.addWidget(self.deGrpBtn, self.row + 3, 3)

    def updateGrp(self):
        sender = self.sender()
        rowindex = int(sender.objectName())
        fri_mail = self.record[rowindex][1].text()
        grp_name = self.record[rowindex][3].text()

        print(fri_mail, grp_name)
        model = modelFile.Model()
        model.connect2db()
        model.updateGrp(self.currentID, fri_mail, grp_name)
        self.showfriends()

    def deleteFri(self):
        model = modelFile.Model()
        model.connect2db()

        sender = self.sender()
        rowindex = sender.objectName()
        rowindex = int(rowindex)
        name = self.record[rowindex][0].text()
        fri_email = self.record[rowindex][1].text()

        reply = QMessageBox.warning(self,
                                    "取消关注",
                                    "确定取消关注{}吗？".format(name),
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == 65536:
            return
        model.deleteFriend(self.currentID, fri_email)

        # 删除所有控件！
        for row in range(len(self.record)):
            for col in range(6):
                self.record[row][col].deleteLater()

        self.showfriends()

    def bottomAdd(self):
        fri_email, ok = QInputDialog.getText(self, "搜索好友", "请输入好友的email", QLineEdit.Normal, "abc@gmail.com")
        if not ok:
            return
        if fri_email == self.currentID:
            QMessageBox.information(self, "提醒", "你输入了自己的email...",
                                    QMessageBox.Yes)
            return
        model = modelFile.Model()
        model.connect2db()
        grp = model.findGrp(self.currentID, fri_email)
        if len(grp) != 0:
            QMessageBox.information(self, "提醒", "ta已经是你的好友啦",
                                    QMessageBox.Yes)
            return
        fri_info = model.usrinfo(fri_email)
        if len(fri_info) == 0:
            QMessageBox.information(self, "没有诶", "该用户还未注册哦",
                                            QMessageBox.Yes)
            return
        model.addFriend(self.currentID, fri_email)
        self.showfriends()

    def center(self):
        qr = self.frameGeometry()
        #获得中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动窗口的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())
