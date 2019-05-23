#!/usr/bin/python3
# -*- coding: utf-8 -*-import sys
from PyQt5.QtWidgets import (QApplication, QWidget,QPushButton,
    QLineEdit)
from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QColor

import sys
from PyQt5.QtWidgets import QApplication, QWidget
app = QApplication(sys.argv)     #这里提供一个重要的进口，基本小部件位于Pyqt5.QtWidgets
w = QWidget()       #窗口小部件
w.resize(250, 250)       #调整部件大小
w.move(300, 300)         #移动部件位置   坐标为（300， 300）
w.setWindowTitle('The first Program')
image = QtGui.QPixmap()
image.load(r"/Users/mohaitao/Desktop/pic1.jpg")
palette1 = QtGui.QPalette()
palette1.setBrush(w.backgroundRole(), QtGui.QBrush(image)) #背景图片
w.setPalette(palette1)
w.setAutoFillBackground(True)

w.show()
sys.exit(app.exec_())
