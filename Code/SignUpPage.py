import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
import modelFile


class SignUpWindow(QWidget):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()

    #init方法里设置window的属性
    def initUI(self):
        #设置窗口大小、居中、标题
        self.resize(900, 600)
        self.center()
        self.setWindowTitle('最in的社交app')

        self.label = QLabel("新用户注册")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(100)

        font = QFont()
        font.setPixelSize(36)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.label.setFont(font)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label, Qt.AlignHCenter)
        self.setLayout(self.layout)

        #表单
        self.formlayout = QFormLayout()
        font.setPixelSize(18)       #再次字体大小

        # Row 1
        self.nameLabel = QLabel("姓名")                  #提示语
        self.nameLabel.setFont(font)                    #设置字体

        self.nameLineEdit = QLineEdit()                 #设置输入框
        self.nameLineEdit.setFixedWidth(180)            #设置条形的大小
        self.nameLineEdit.setFixedHeight(32)
        self.nameLineEdit.setMaxLength(10)
        self.nameLineEdit.setFont(font)                 #设置字体
        self.formlayout.addRow(self.nameLabel, self.nameLineEdit)


        # Row 2
        self.emailLabel = QLabel("Email")  # 提示语
        self.emailLabel.setFont(font)  # 设置字体

        self.emailLineEdit = QLineEdit()  # 设置输入框
        self.emailLineEdit.setFixedWidth(180)  # 设置条形的大小
        self.emailLineEdit.setFixedHeight(32)
        self.emailLineEdit.setMaxLength(20)
        self.emailLineEdit.setFont(font)  # 设置字体
        self.formlayout.addRow(self.emailLabel, self.emailLineEdit)

        # Row 3
        self.passLabel = QLabel("密码")  # 提示语
        self.passLabel.setFont(font)  # 设置字体

        self.passLineEdit = QLineEdit()  # 设置输入框
        self.passLineEdit.setFixedWidth(180)  # 设置条形的大小
        self.passLineEdit.setFixedHeight(32)
        self.passLineEdit.setMaxLength(10)
        self.passLineEdit.setFont(font)  # 设置字体
        self.formlayout.addRow(self.passLabel, self.passLineEdit)

        # Row 4 注册按钮
        self.signUpbtn = QPushButton("注册")
        self.signUpbtn.setFont(font)
        self.signUpbtn.setFixedWidth(120)
        self.signUpbtn.setFixedHeight(30)
        self.formlayout.addRow("", self.signUpbtn)

        ############################################################
        widget = QWidget()
        widget.setLayout(self.formlayout)
        widget.setFixedHeight(250)
        widget.setFixedWidth(300)

        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(widget, Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(self.Hlayout)                      #设置部件的布局为
        self.layout.addWidget(widget, Qt.AlignHCenter)      #在布局中增加部件，设为居中

        ################################################

        self.signUpbtn.clicked.connect(self.modelsignup)

    def modelsignup(self):
        name = self.nameLineEdit.text()
        email = self.emailLineEdit.text()
        passwd = self.passLineEdit.text()

        model = modelFile.Model()
        model.connect2db()
        if model.checkemail(email):
            model.signup(name, None, None, email, None, passwd)
            print(QMessageBox.information(
                self, "提醒", "您已成功注册账号!", QMessageBox.Yes, QMessageBox.Yes))
            self.signal.emit(name)
        else:
            print(QMessageBox.warning(
                self, "警告", "该账号已存在,请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            print("该邮箱已被注册")

    def center(self):
        qr = self.frameGeometry()
        #获得中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动窗口的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())





