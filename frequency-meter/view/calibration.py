#!/usr/bin/env python3
"""Calibration Window"""
# Standard libraries
import os
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
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

        #Initialize coarse calibration plots
        self.figure_coarse = plt.figure(figsize=(4, 3))
        self.figure_coarse.patch.set_alpha(0)
        self.canvas_coarse = FigureCanvas(self.figure_coarse)
        self.plotVLayout_coarse.addWidget(self.canvas_coarse)
        self.ax_coarse = self.figure_coarse.add_subplot(111)
        self.figure_coarse.subplots_adjust(top=0.85, bottom=0.10, left=0.1)
        self.ax_coarse.grid()
        self.ax_coarse.set_ylabel("F(Hz)", rotation= 'horizontal')
        self.ax_coarse.yaxis.set_label_coords(-0.05, 1.04)

        #Initialize fine calibration plots
        self.figure_fine = plt.figure(figsize=(5, 7))
        self.figure_fine.patch.set_alpha(0)
        self.canvas_fine = FigureCanvas(self.figure_fine)
        self.plotVLayout_fine.addWidget(self.canvas_fine)
        self.ax_fine_cdt = self.figure_fine.add_subplot(311)
        self.ax_fine_dnl = self.figure_fine.add_subplot(312)
        self.ax_fine_inl = self.figure_fine.add_subplot(313)
        self.figure_fine.subplots_adjust(top=0.85, bottom=0.10, left=0.1)
        self.ax_fine_cdt.grid()
        self.ax_fine_dnl.grid()
        self.ax_fine_inl.grid()


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
