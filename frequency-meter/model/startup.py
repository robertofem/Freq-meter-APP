#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
import sys
# Third party libraries
from PyQt4 import QtGui, QtCore
# Local libraries
from view import interface

class MainWindow(QtGui.QMainWindow, interface.Ui_MainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.left2rightButton_2.clicked.connect(self.left2right)

    def left2right(self):
        listItems=self.listWidget.selectedItems()
        for item in listItems:
            self.listWidget2.addItem(item)
            self.listWidget.takeItem(self.listWidget.row(item))

def run():
    app = QtGui.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
