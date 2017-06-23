#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
import sys
# Third party libraries
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.initUI()

    def initUI(self):
    	# Button por quitting the program.
        quit_btn = QtGui.QPushButton('Quit', self)
        quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        quit_btn.setToolTip('This is a <b>QPushButton</b> widget')
        quit_btn.resize(quit_btn.sizeHint())
        quit_btn.move(50, 50)       
    	# Button por quitting the program.
        aux_btn = QtGui.QPushButton('Aux', self)
        aux_btn.setToolTip('This is a <b>QPushButton</b> widget')
        aux_btn.resize(aux_btn.sizeHint())
        aux_btn.move(200, 50)
        # UI config
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Tooltips')    
        self.show()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 

def run():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
