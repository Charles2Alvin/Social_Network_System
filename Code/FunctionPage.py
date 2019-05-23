import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
import modelFile
from SignUpPage import *
from PersonalInfo import *

class functionWindow(QWidget):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()
        self.state = 0

    #init方法里设置window的属性
    def initUI(self):
        #设置窗口大小、居中、标题
        self.resize(900, 600)
        self.center()

        self.label = QLabel()
        self.label.setText("<font color=%s>%s</font>" % ('#F3EFEE', "今天也是愉快的一天"))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(100)

        font = QFont('微软雅黑', 36)
        font.setBold(True)
        self.label.setFont(font)

        self.vbox = QVBoxLayout()             #整体垂直布局
        self.vbox.addWidget(self.label, Qt.AlignHCenter)      #添加大标题
        self.setLayout(self.vbox)

        #表单
        self.formlayout = QFormLayout()
        font.setPixelSize(18)       #再次字体大小

        # Row 1 登陆按钮
        self.infobtn = QPushButton("查看个人信息")
        self.infobtn.setFont(font)
        self.infobtn.setFixedWidth(150)
        self.infobtn.setFixedHeight(30)
        self.formlayout.addRow("", self.infobtn)

        self.expbtn = QPushButton("查看工作经历")
        self.expbtn.setFont(font)
        self.expbtn.setFixedWidth(150)
        self.expbtn.setFixedHeight(30)
        self.formlayout.addRow("", self.expbtn)

        self.edubtn = QPushButton("查看教育经历")
        self.edubtn.setFont(font)
        self.edubtn.setFixedWidth(150)
        self.edubtn.setFixedHeight(30)
        self.formlayout.addRow("", self.edubtn)

        self.fribtn = QPushButton("好友列表")
        self.fribtn.setFont(font)
        self.fribtn.setFixedWidth(150)
        self.fribtn.setFixedHeight(30)
        self.formlayout.addRow("", self.fribtn)

        self.journalbtn = QPushButton("我的空间")
        self.journalbtn.setFont(font)
        self.journalbtn.setFixedWidth(150)
        self.journalbtn.setFixedHeight(30)
        self.formlayout.addRow("", self.journalbtn)

        self.plazabtn = QPushButton("泡泡广场")
        self.plazabtn.setFont(font)
        self.plazabtn.setFixedWidth(150)
        self.plazabtn.setFixedHeight(30)
        self.formlayout.addRow("", self.plazabtn)

        self.backbtn = QPushButton("切换账号")
        self.backbtn.setFont(font)
        self.backbtn.setFixedWidth(150)
        self.backbtn.setFixedHeight(30)
        self.formlayout.addRow("", self.backbtn)

        ############################################################
        widget = QWidget()
        widget.setLayout(self.formlayout)
        widget.setFixedHeight(250)
        widget.setFixedWidth(300)

        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(widget, Qt.AlignCenter)

        self.bigwidget = QWidget()
        self.bigwidget.setLayout(self.Hlayout)                      #设置部件的布局为
        self.vbox.addWidget(self.bigwidget, Qt.AlignHCenter)      #在布局中增加部件，设为居中

        ################################################


    def center(self):
        qr = self.frameGeometry()
        #获得中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动窗口的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())

