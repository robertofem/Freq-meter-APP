# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created: Fri Jun 23 17:03:10 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(900, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(9, 9, 256, 361))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        self.listWidget_2 = QtGui.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(380, 10, 256, 361))
        self.listWidget_2.setObjectName(_fromUtf8("listWidget_2"))
        self.left2rightButton_2 = QtGui.QPushButton(self.centralwidget)
        self.left2rightButton_2.setGeometry(QtCore.QRect(280, 90, 85, 27))
        self.left2rightButton_2.setObjectName(_fromUtf8("left2rightButton_2"))
        self.right2leftButton = QtGui.QPushButton(self.centralwidget)
        self.right2leftButton.setGeometry(QtCore.QRect(280, 120, 85, 27))
        self.right2leftButton.setObjectName(_fromUtf8("right2leftButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Item1", None))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Item2", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.left2rightButton_2.setText(_translate("MainWindow", ">>>", None))
        self.right2leftButton.setText(_translate("MainWindow", "<<<", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

