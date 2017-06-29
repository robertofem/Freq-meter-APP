# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created: Thu Jun 29 17:07:35 2017
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
        MainWindow.resize(769, 424)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(48, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.LoggerBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.LoggerBrowser.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.LoggerBrowser.setAutoFillBackground(False)
        self.LoggerBrowser.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.LoggerBrowser.setObjectName(_fromUtf8("LoggerBrowser"))
        self.gridLayout.addWidget(self.LoggerBrowser, 4, 0, 1, 4)
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.WarnButton = QtGui.QPushButton(self.centralwidget)
        self.WarnButton.setObjectName(_fromUtf8("WarnButton"))
        self.gridLayout.addWidget(self.WarnButton, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.DebugButton = QtGui.QPushButton(self.centralwidget)
        self.DebugButton.setObjectName(_fromUtf8("DebugButton"))
        self.gridLayout.addWidget(self.DebugButton, 0, 0, 1, 1)
        self.ErrorButton = QtGui.QPushButton(self.centralwidget)
        self.ErrorButton.setObjectName(_fromUtf8("ErrorButton"))
        self.gridLayout.addWidget(self.ErrorButton, 0, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
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
        self.label.setText(_translate("MainWindow", "Log messages:", None))
        self.WarnButton.setText(_translate("MainWindow", "Warning", None))
        self.DebugButton.setText(_translate("MainWindow", "Debug", None))
        self.ErrorButton.setText(_translate("MainWindow", "ERROR", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

