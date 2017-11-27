# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Wed Sep 02 20:32:46 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog,self).__init__(parent)
        #Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.lineEdit1 = QtGui.QLineEdit(Dialog)
        self.lineEdit1.setGeometry(QtCore.QRect(30, 230, 251, 22))
        self.lineEdit1.setObjectName(_fromUtf8("lineEdit1"))
        self.textBrowser1 = QtGui.QTextBrowser(Dialog)
        self.textBrowser1.setGeometry(QtCore.QRect(30, 20, 256, 192))
        self.textBrowser1.setObjectName(_fromUtf8("textBrowser1"))
        self.pushButton1 = QtGui.QPushButton(Dialog)
        self.pushButton1.setGeometry(QtCore.QRect(300, 230, 93, 28))
        self.pushButton1.setObjectName(_fromUtf8("pushButton1"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEdit1.clear)
        #QtCore.QObject.connect(self.pushButton1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.textBrowser1.show)
        QtCore.QObject.connect(self.lineEdit1, QtCore.SIGNAL(_fromUtf8("returnPressed()")), Dialog.slot1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton1.setText(_translate("Dialog", "anniu", None))

    def slot1(self):
        e = self.lineEdit1.text().ascii()
        self.textBrowser1.insertItem(e)
        self.lineEdit1.clear()
        

if __name__ == "__main__":  
    app = QApplication(sys.argv)  
    f = Dialog()  
    f.show()
    f.exec_()  
#     app.setMainWidget(f)  
#     app.exec_loop()

