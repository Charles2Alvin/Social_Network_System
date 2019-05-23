import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
import modelFile
from SignUpPage import *


class EntranceWindow(QWidget):
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
        self.label.setText("<font color=%s>%s</font>" % ('#F3EFEE', "快聊——中国最in的社交app"))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(100)

        font = QFont('微软雅黑', 36)
        font.setBold(True)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.label.setFont(font)

        self.vbox = QVBoxLayout()             #整体垂直布局
        self.vbox.addWidget(self.label, Qt.AlignHCenter)      #添加大标题
        self.setLayout(self.vbox)

        #表单
        self.formlayout = QFormLayout()
        font.setPixelSize(18)       #再次字体大小

        # Row 1 登陆按钮
        self.signInbtn = QPushButton("登陆")
        self.signInbtn.setFont(font)
        self.signInbtn.setFixedWidth(150)
        self.signInbtn.setFixedHeight(30)
        self.formlayout.addRow("", self.signInbtn)

        self.signUpbtn = QPushButton("注册")
        self.signUpbtn.setFont(font)
        self.signUpbtn.setFixedWidth(150)
        self.signUpbtn.setFixedHeight(30)
        self.formlayout.addRow("", self.signUpbtn)

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

