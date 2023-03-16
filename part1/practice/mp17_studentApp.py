import sys
from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * #QIcon
from PyQt5 import uic
import pymysql
import os

class LoginApp(QWidget):
    conn = None
    curIdx = 0  # 현재 데이터 PK

    def __init__(self):
        super().__init__()
        uic.loadUi('./practice/login.ui', self)
        self.setWindowTitle('로그인 v0.5')

    def FindID(self):
        self.hide()
        self.FindIDApp = FindIDApp()

class FindIDApp(QWidget):
    def __init__(self):
        super(FindIDApp, self).__init__()
        uic.loadUi('./practice/findId.ui', self)
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginApp()
    ex.show()
    sys.exit(app.exec_())