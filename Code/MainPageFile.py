from EntrancePageFile import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
import modelFile
from SignUpPage import *
from SignInPage import *
from EntrancePageFile import *
from FunctionPage import *
from FriendPage import *
from Work_Exp_Page import *
from Edu_exp_page import *
from JournalPage import *
from PlazaPage import *

class MainPage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.entrance = EntranceWindow()
        self.entrance2 = EntranceWindow()
        self.signinpage = SignInWindow()
        self.signuppage = SignUpWindow()
        self.functionpage = functionWindow()
        self.personalpage = PersonalInfoWindow()
        self.friendpage = FriendInfoWindow()
        self.work_exp_page = Work_Exp_Window()
        self.edu_exp_page = Edu_Exp_Window()
        self.journal_page = Journal_Window()
        self.plaza_page = Plaza_Window()

        self.initUI()
        self.currentID = None

    def initUI(self):
        self.resize(900, 600)
        self.center()
        self.setWindowTitle("Haitao.com")

        self.setCentralWidget(self.entrance)
        self.signalBinding()

    def signalBinding(self):
        self.entrance.signInbtn.clicked.connect(self.showSignInPage)
        self.entrance.signUpbtn.clicked.connect(self.showSignUpPage)

        self.signinpage.signInbtn.clicked.connect(self.signin)

        self.functionpage.backbtn.clicked.connect(self.exit)

        # 显示个人信息
        self.functionpage.infobtn.clicked.connect(self.showinfo)

        # 显示工作经历信息
        self.functionpage.expbtn.clicked.connect(self.show_work_experience)

        # 显示教育经历信息
        self.functionpage.edubtn.clicked.connect(self.show_edu_experience)

        # 显示好友信息
        self.functionpage.fribtn.clicked.connect(self.showfri)

        # 我的日志页面
        self.functionpage.journalbtn.clicked.connect(self.show_journal)

        # 泡泡广场
        self.functionpage.plazabtn.clicked.connect(self.show_Plaza)

    def show_Plaza(self):
        self.plaza_page.currentID = self.currentID
        self.plaza_page.refresh()
        image = QPixmap()
        image.load(r"/Users/mohaitao/Desktop/pics/pic6.jpg")
        palette1 = QPalette()
        palette1.setBrush(self.plaza_page.backgroundRole(), QBrush(image))  # 背景图片
        self.plaza_page.setPalette(palette1)
        self.plaza_page.setAutoFillBackground(False)
        self.plaza_page.show()

    def show_journal(self):
        self.journal_page.currentID = self.currentID
        self.journal_page.fetch()
        self.journal_page.show()

    def show_edu_experience(self):
        self.edu_exp_page.currentID = self.currentID
        self.edu_exp_page.fetchexp()
        self.edu_exp_page.show()

    def show_work_experience(self):
        self.work_exp_page.currentID = self.currentID
        self.work_exp_page.fetchexp()
        image = QPixmap()
        image.load(r"/Users/mohaitao/Desktop/pics/pic6.jpg")
        palette1 = QPalette()
        palette1.setBrush(self.work_exp_page.backgroundRole(), QBrush(image))  # 背景图片
        self.work_exp_page.setPalette(palette1)
        self.work_exp_page.setAutoFillBackground(False)
        self.work_exp_page.show()

    def signin(self):
        self.currentID = self.signinpage.modelsignin()
        print(self.currentID)
        if self.currentID != None:
            self.showFunctionPage()

    def showinfo(self):
        self.personalpage.currentID = self.currentID
        self.personalpage.fetchinfo()
        self.personalpage.show()

    def showfri(self):
        print("working!")
        self.friendpage.currentID = self.currentID
        self.friendpage.showfriends()
        image = QPixmap()
        image.load(r"/Users/mohaitao/Desktop/pics/pic1.jpg")
        palette1 = QPalette()
        palette1.setBrush(self.friendpage.backgroundRole(), QBrush(image))  # 背景图片
        # self.friendpage.setPalette(palette1)
        self.friendpage.setAutoFillBackground(False)
        self.friendpage.show()

    def exit(self):
        exit(0)

    def showFunctionPage(self):
        self.setCentralWidget(self.functionpage)

    def showEntrancePage(self):
        self.setCentralWidget(self.entrance)

    def showSignInPage(self):
        self.setCentralWidget(self.signinpage)

    def showSignUpPage(self):
        self.setCentralWidget(self.signuppage)

    def center(self):
        qr = self.frameGeometry()
        #获得中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动窗口的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())

#
# impMenu = QMenu('Import', self)
#         impAct = QAction('Import mail', self)
#         impMenu.addAction(impAct)
#
#         newAct = QAction('基本资料', self)
#         newAct.triggered.connect(self.showEntrancePage)
#
#         fileMenu.addAction(newAct)
#         fileMenu.addMenu(impMenu)
# menubar = self.menuBar()
#         menubar.setNativeMenuBar(False)
#         fileMenu = menubar.addMenu('个人资料')
#         friendMenu = menubar.addMenu("好友列表")
#         journalMenu = menubar.addMenu("我的日志")
#         self.gobackMenu = menubar.addMenu("返回")