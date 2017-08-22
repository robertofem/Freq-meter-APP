#!/usr/bin/env python3
"""Calibration Window"""
# Standard libraries
import os
import sys
# Third party libraries
from PyQt5 import QtGui, QtCore, QtWidgets
# Local libraries
from view import calibration_interface


class CalibWindow(QtWidgets.QDialog, calibration_interface.Ui_CalibWindow):
    """
    Class for defining the behaviour of the Device Manager Interface.
    """
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

        # Start and Stop Buttons events
        self.button_start_coarse.clicked.connect(self.start_coarse)
        self.button_stop_coarse.clicked.connect(self.stop_coarse)
        self.button_start_fine.clicked.connect(self.start_fine)
        self.button_stop_fine.clicked.connect(self.stop_fine)
        # Button box events (accept/reject)
        self.buttonBox.clicked.connect(self.handle_buttonBox_click)

    def handle_buttonBox_click(self, button):
        """
        Check which button was pressed and perform corresponding action.
        """
        clicked_button = self.buttonBox.standardButton(button)
        if clicked_button == QtWidgets.QDialogButtonBox.Close:
            self.show_exit_dialog()
        return

    def show_exit_dialog(self):
        """
        Ask the user if he/she wants to exit the DevManager window.
        """
        reply = QtWidgets.QMessageBox.question(self, 'Exit message',
                                           "Do you want to exit?",
                                           QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.close()
        return


    def start_coarse(self):
        """
        Start coarse calibration.
        """
        return

    def stop_coarse(self):
        """
        Stop coarse calibration.
        """
        return

    def start_fine(self):
        """
        Start fine calibration.
        """
        return
    def stop_fine(self):
        """
        Stop fine calibration.
        """
        return
