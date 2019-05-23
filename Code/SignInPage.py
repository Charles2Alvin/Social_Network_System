import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
import modelFile
from SignUpPage import *


class SignInWindow(QWidget):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()

    #init方法里设置window的属性
    def initUI(self):
        #设置窗口大小、居中、标题
        self.resize(900, 600)
        self.center()

        self.label = QLabel()
        self.label.setText("<font color=%s>%s</font>" % ('#F3EFEE', "用户登陆"))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(100)
        font = QFont('微软雅黑', 36)
        font.setBold(True)
        self.label.setFont(font)

        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)

        self.vbox = QVBoxLayout()             #整体垂直布局
        self.vbox.addWidget(self.label, Qt.AlignHCenter)      #添加大标题
        self.setLayout(self.vbox)

        #表单
        self.formlayout = QFormLayout()
        font.setPixelSize(18)       #再次字体大小


        # Row 1
        self.emailLabel = QLabel("Email")  # 提示语
        self.emailLabel.setFont(font)  # 设置字体

        self.emailLineEdit = QLineEdit()  # 设置输入框
        self.emailLineEdit.setFixedWidth(180)  # 设置条形的大小
        self.emailLineEdit.setFixedHeight(32)
        self.emailLineEdit.setMaxLength(20)
        self.emailLineEdit.setFont(font)  # 设置字体
        self.formlayout.addRow(self.emailLabel, self.emailLineEdit)

        # Row 2
        self.passLabel = QLabel("密码")  # 提示语
        self.passLabel.setFont(font)  # 设置字体

        self.passLineEdit = QLineEdit()  # 设置输入框
        self.passLineEdit.setFixedWidth(180)  # 设置条形的大小
        self.passLineEdit.setFixedHeight(32)
        self.passLineEdit.setMaxLength(10)
        self.passLineEdit.setFont(font)  # 设置字体
        self.formlayout.addRow(self.passLabel, self.passLineEdit)

        # Row 3 登陆按钮
        self.signInbtn = QPushButton("登陆")
        self.signInbtn.setFont(font)
        self.signInbtn.setFixedWidth(120)
        self.signInbtn.setFixedHeight(30)
        self.formlayout.addRow("", self.signInbtn)

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

    def modelsignin(self):
        email = self.emailLineEdit.text()
        passwd = self.passLineEdit.text()

        model = modelFile.Model()
        model.connect2db()
        loginstatus = model.signin(email, passwd)
        #print("Checking!")
        if loginstatus == 1:
            #账号不存在
            print(QMessageBox.warning(
                     self, "警告", "账号不存在!", QMessageBox.Yes, QMessageBox.Yes))

        elif loginstatus == 2:
            #登陆成功
            print(QMessageBox.information(
                     self, "提醒", "登陆成功!", QMessageBox.Yes, QMessageBox.Yes))
            return email

        elif loginstatus == 3:
            #密码错误
            print(QMessageBox.warning(
                     self, "警告", "密码错误!", QMessageBox.Yes, QMessageBox.Yes))

    def clear(self):
        #原布局上的清除表单
        self.vbox.removeWidget(self.bigwidget)
        self.bigwidget.deleteLater()
        self.bigwidget = None

        #清除原布局上的标题
        self.vbox.removeWidget(self.label)
        self.label.deleteLater()
        self.label = None

        self.mainpage()

    def mainpage(self):
        """获取用户对应信息"""



    def publish(self):
        title = QLabel('Title')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(30)  # 设定部件之间的距离是30像素

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)  # 表示放到第3行第1列，占据5行和1列

        submitButton = QPushButton("发布")
        grid.addWidget(submitButton, 4, 1, 9, 1)  # 上面的部件占据5行，从第9行开始

        self.vbox.addLayout(grid)

    def center(self):
        qr = self.frameGeometry()
        #获得中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动窗口的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())





