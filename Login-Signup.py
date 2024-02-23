import random
import time

import cv2
import numpy as np
import torch
from PyQt5.QtGui import QPixmap, QPainter, QPen, QPainterPath, QImage
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QGraphicsScene, \
    QGraphicsEllipseItem, QGraphicsView, QGraphicsProxyWidget, QGraphicsTextItem, QLineEdit
from PyQt5.QtCore import Qt, QFile,QLocale
from PyQt5 import QtCore
import matplotlib

from GenderClassification.app import Model

matplotlib.use('Qt5Agg')
from PyQt5.QtGui import QColor
import pyqtgraph as pg

import sys

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.ui = loadUi(r"C:\Users\PC\PycharmProjects\pythonProject2\GenderClassification\app\Login.ui", self)
        self.username = self.ui.username
        self.password = self.ui.password
        self.login_button = self.ui.login
        self.set_echo_button = self.ui.set_echo
        self.signup_button = self.ui.sign_up


        self.echo_password = True
        self.username.setReadOnly(True)
        self.password.setReadOnly(True)

        self.ui.frame.mousePressEvent = lambda event: self.set_line_edit_default()
        self.username.mousePressEvent = lambda event: self.line_edit_pressed(self.ui.username)
        self.password.mousePressEvent = lambda event: self.line_edit_pressed(self.ui.password)
        self.set_echo_button.clicked.connect(self.set_echo_mode)
        self.signup_button.clicked.connect(self.redirect_to_signup)


        self.show()

    def line_edit_pressed(self, lineEdit):
            lineEdit.setReadOnly(False)
            if lineEdit.text() == "   Password" or lineEdit.text() == "   Username":
             lineEdit.setText("")
            if lineEdit == self.password:
                if len(self.username.text()) == 0:
                 self.username.setText("   Username")
                self.username.setReadOnly(True)
            elif lineEdit == self.username:
                if len(self.password.text()) == 0:
                 self.password.setText("   Password")
                self.password.setReadOnly(True)
    def set_line_edit_default(self):
          if len(self.password.text()) == 0:
              self.password.setText("   Password")
          if len(self.username.text()) == 0:
              self.username.setText("   Username")

          self.username.setReadOnly(True)
          self.password.setReadOnly(True)

    def set_echo_mode(self):
        if self.echo_password == True:
          self.password.setEchoMode(QLineEdit.Password)
          self.echo_password = False
        else:
         self.password.setEchoMode(QLineEdit.Normal)
         self.echo_password = True
    def redirect_to_signup(self):
        signup = Signup()
        signup.show()
        self.window().destroy()

class Signup(QMainWindow):
    def __init__(self):
        super(Signup, self).__init__()
        self.ui = loadUi(r"C:\Users\PC\PycharmProjects\pythonProject2\GenderClassification\app\Signup.ui", self)
        self.username = self.ui.username
        self.password = self.ui.password
        self.signup = self.ui.signup_button
        self.set_echo_button = self.ui.setecho
        self.login_button = self.ui.redirect_login
        self.email = self.ui.email
        self.warn_label = self.findChild(QLabel, "warn")

        self.echo_password = True
        self.username.setReadOnly(True)
        self.password.setReadOnly(True)
        self.email.setReadOnly(True)
        self.ui.frame.mousePressEvent = lambda event: self.set_line_edit_default()
        self.username.mousePressEvent = lambda event: self.line_edit_pressed(self.username)
        self.password.mousePressEvent = lambda event: self.line_edit_pressed(self.password)
        self.email.mousePressEvent = lambda event: self.line_edit_pressed(self.email)
        self.set_echo_button.clicked.connect(self.set_echo_mode)
        self.login_button.clicked.connect(self.redirect_to_login)
        self.setTabOrder(self.username, self.email)
        self.warn_label.setVisible(False)

        self.show()

    def line_edit_pressed(self, lineEdit):
        lineEdit.setReadOnly(False)
        if lineEdit.text() == "   Password" or lineEdit.text() == "   Username" or  lineEdit.text() == "   Email":
            lineEdit.setText("")
        if lineEdit == self.password:
            if len(self.username.text()) == 0:
                self.username.setText("   Username")
            if len(self.email.text()) == 0:
                self.email.setText("   Email")
            self.username.setReadOnly(True)
            self.email.setReadOnly(True)
        elif lineEdit == self.username:
            if len(self.password.text()) == 0:
                self.password.setText("   Password")
            if len(self.email.text()) == 0:
                self.email.setText("   Email")
            self.password.setReadOnly(True)
            self.email.setReadOnly(True)
        elif lineEdit == self.email:
            if len(self.password.text()) == 0:
                self.password.setText("   Password")
            if len(self.username.text()) == 0:
                self.username.setText("   Username")
            self.password.setReadOnly(True)
            self.username.setReadOnly(True)

    def set_line_edit_default(self):
        if len(self.password.text()) == 0:
            self.password.setText("   Password")
        if len(self.username.text()) == 0:
            self.username.setText("   Username")
        if len(self.email.text()) == 0:
            self.email.setText("   Email")

        self.username.setReadOnly(True)
        self.password.setReadOnly(True)
        self.email.setReadOnly(True)

    def set_echo_mode(self):
        if self.echo_password == True:
            self.password.setEchoMode(QLineEdit.Password)
            self.echo_password = False
        else:
            self.password.setEchoMode(QLineEdit.Normal)
            self.echo_password = True

    def redirect_to_login(self):
        login = Login()
        login.show()
        self.window().destroy()




    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.setFocusPolicy(Qt.StrongFocus)
            self.username.setFocus()
            if (len(self.password.text()) == 0 or len(self.username.text()) == 0 or len(self.email.text()) == 0
                    or self.password.text() == "   Password" or self.username.text() == "   Username" or self.email.text() == "   Email"):
                self.warn_label.setVisible(True)
            else:
                self.warn_label.setVisible(False)


        else:
            super().keyPressEvent(qKeyEvent)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())