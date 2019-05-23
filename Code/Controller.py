import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
from dialog import *
from SignUpPage import *
import modelFile
from SignInPage import *
from MainPageFile import *
from EntrancePageFile import *

class Controller:
    def __init__(self):
        self.model = modelFile.Model()


    def signup(self):
        app = QApplication(sys.argv)
        # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        window = MainPage()

        image = QPixmap()
        image.load(r"/Users/mohaitao/Desktop/pics/pic3.jpg")
        palette1 = QPalette()
        palette1.setBrush(window.backgroundRole(), QBrush(image))  # 背景图片
        window.setPalette(palette1)
        window.setAutoFillBackground(True)

        window.show()
        sys.exit(app.exec_())
        # btn = window.signInBtn
        # btn.clicked.connect(childWindow.show)


controller = Controller()
controller.signup()
