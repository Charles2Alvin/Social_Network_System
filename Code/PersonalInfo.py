import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
import modelFile
from SignUpPage import *


class PersonalInfoWindow(QWidget):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.currentID = None
        self.initUI()

    #init方法里设置window的属性
    def initUI(self):
        # 设置窗口大小、居中、标题
        self.resize(900, 600)
        self.center()

        """设置布局和部件"""
        self.grid = QGridLayout()
        self.grid.setSpacing(30)
        font = QFont('微软雅黑', 16)
        font.setBold(True)
        self.nametxt, self.gendertxt, self.birthtxt, self.emailtxt, self.addresstxt = \
            QLineEdit(), QComboBox(), QDateEdit(), QLabel(), QLineEdit()
        items = ['male', 'female']
        self.gendertxt.addItems(items)

        self.nametxt.setFixedWidth(180)
        self.nametxt.setFixedHeight(32)
        self.nametxt.setFont(font)

        self.gendertxt.setFixedWidth(180)
        self.gendertxt.setFixedHeight(32)
        self.gendertxt.setFont(font)

        self.birthtxt.setFixedWidth(180)
        self.birthtxt.setFixedHeight(32)
        self.birthtxt.setFont(font)

        self.emailtxt.setFixedWidth(180)
        self.emailtxt.setFixedHeight(32)
        self.emailtxt.setFont(font)

        self.addresstxt.setFixedWidth(180)
        self.addresstxt.setFixedHeight(32)
        self.addresstxt.setFont(font)

        self.imgLB = QPushButton()
        self.imgLB.setFixedWidth(280)
        self.imgLB.setFixedHeight(280)
        self.imgLB.clicked.connect(self.upload)

        nameLB = QLabel("姓名")
        nameLB.setFixedWidth(150)
        nameLB.setFixedHeight(30)
        nameLB.setFont(font)
        self.grid.addWidget(nameLB, 1, 1)
        self.grid.addWidget(self.nametxt, 1, 2)

        genderLB = QLabel("性别")
        genderLB.setFont(font)
        self.grid.addWidget(genderLB, 2, 1)
        self.grid.addWidget(self.gendertxt, 2, 2)

        birthLB = QLabel("生日")
        birthLB.setFont(font)
        self.grid.addWidget(birthLB, 3, 1)
        self.grid.addWidget(self.birthtxt, 3, 2)

        emailLB = QLabel("邮箱")
        emailLB.setFont(font)
        self.grid.addWidget(emailLB, 4, 1)
        self.grid.addWidget(self.emailtxt, 4, 2)

        addrLB = QLabel("地址")
        addrLB.setFont(font)
        self.grid.addWidget(addrLB, 5, 1)
        self.grid.addWidget(self.addresstxt, 5, 2)

        self.modifyBtn = QPushButton("修改")
        self.modifyBtn.setFixedWidth(180)
        self.modifyBtn.setFixedHeight(32)
        self.modifyBtn.setFont(font)
        self.modifyBtn.clicked.connect(self.modifyinfo)
        self.grid.addWidget(self.modifyBtn, 6, 2)

        Hbox = QHBoxLayout()
        Hbox.addWidget(self.imgLB)

        forImg = QWidget()
        forImg.setLayout(Hbox)

        forTxt = QWidget()
        forTxt.setLayout(self.grid)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(forImg)
        mainLayout.addWidget(forTxt)
        self.setLayout(mainLayout)

    def upload(self):
        # 参数二是默认的打开路径设置文件扩展名过滤,注意用双分号间隔
        file_, filetype = QFileDialog.getOpenFileName(self, "选取文件",
        "/Users/mohaitao/Desktop/pics", "All Files (*);;Image Files (*.jpg)")
        print(file_)
        model = modelFile.Model()
        model.connect2db()
        model.updatePortrait(self.currentID, file_)
        QMessageBox.information(
            self, "提醒", "头像修改成功!", QMessageBox.Yes)
        self.fetchinfo()


    def showfriends(self):
        model = modelFile.Model()
        model.connect2db()
        model.showfriends(self.currentID)

    def modifyinfo(self):
        # 邮箱是不能修改的，通过邮箱定位tuple，进行更新
        name, gender, birth, address = \
            self.nametxt.text(), self.gendertxt.currentText(), \
            self.birthtxt.text(), self.addresstxt.text()
        print(name, gender, birth, address)
        model = modelFile.Model()
        model.connect2db()
        status = model.modifyinfo(name, gender, birth, address, str(self.currentID))
        if status == 0:
            QMessageBox.information(
                self,"提醒", "修改成功!", QMessageBox.Yes, QMessageBox.Yes)
            self.fetchinfo()

    def fetchinfo(self):
        model = modelFile.Model()
        model.connect2db()
        info = model.usrinfo(self.currentID)
        name, gender, birth, email, address, imgPath = \
            info[0], info[1], info[2], info[3], info[4], info[6]
        """设置部件的文本内容"""
        self.nametxt.setText(name)
        self.gendertxt.setCurrentText(gender)
        self.birthtxt.setDate(QDate.fromString(str(birth),1))
        self.emailtxt.setText(email)
        self.addresstxt.setText(address)
        pix = QPixmap(imgPath)
        icon = QIcon()
        icon.addPixmap(pix, QIcon.Normal, QIcon.Off)
        self.imgLB.setIcon(icon)
        self.imgLB.setIconSize(QSize(240, 240))

    def center(self):
        qr = self.frameGeometry()
        #获得中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动窗口的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())

