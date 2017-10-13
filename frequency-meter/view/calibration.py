#!/usr/bin/env python3
"""Calibration Window"""
# Standard libraries
import glob
import logging
import os
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
# Third party libraries
from PyQt5 import QtGui, QtCore, QtWidgets
# Local libraries
from view import calibration_interface
from view import freqmeterdevice

logger = logging.getLogger('view')

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
        self.figure_coarse = plt.figure(figsize=(4.5, 3))
        self.figure_coarse.patch.set_alpha(0)
        self.canvas_coarse = FigureCanvas(self.figure_coarse)
        self.plotVLayout_coarse.addWidget(self.canvas_coarse)
        self.ax_coarse = self.figure_coarse.add_subplot(111)
        self.figure_coarse.subplots_adjust(top=0.85, bottom=0.10, left=0.1)
        self.ax_coarse.grid()
        self.ax_coarse.set_ylabel("F(Hz)", rotation= 'horizontal')
        self.ax_coarse.yaxis.set_label_coords(-0.05, 1.04)

        #Initialize fine calibration plots
        self.figure_fine = plt.figure(figsize=(4.5, 4.5))
        self.figure_fine.patch.set_alpha(0)
        self.canvas_fine = FigureCanvas(self.figure_fine)
        self.plotVLayout_fine.addWidget(self.canvas_fine)
        self.ax_fine_cdt = self.figure_fine.add_subplot(311)
        self.ax_fine_dnl = self.figure_fine.add_subplot(312)
        self.ax_fine_inl = self.figure_fine.add_subplot(313)
        self.figure_fine.subplots_adjust(top=0.95, bottom=0.1, left=0.1)
        self.ax_fine_cdt.grid()
        self.ax_fine_dnl.grid()
        self.ax_fine_inl.grid()

        #populate target (to be calibrated) listbox with only FPGA freq meters
        self.populate_target_combobox()
        #populate list with reference devices with all devices
        self.populate_reference_combobox()

    def populate_target_combobox(self):
        #clear the combobox
        self.cBoxTargetDev.clear()
        #open all files and add devices which vendor is "Uvigo"
        device_names_list = [os.path.basename(match)[:-4]
                        for match in glob.glob('resources/devices/*yml')]
        for device_name in device_names_list:
            dev_dir = "{}/resources/devices/".format(os.getcwd())
            dev_path = "{}{}.yml".format(dev_dir, device_name)
            new_device = freqmeterdevice.FreqMeter.get_freq_meter(dev_path)
            if new_device.get_vendor_name() == "Uvigo":
                self.cBoxTargetDev.addItem(device_name)
        return

    def populate_reference_combobox(self):
        #clear the combobox
        self.cBoxRefDev.clear()
        #add all devices
        device_names_list = [os.path.basename(match)[:-4]
                        for match in glob.glob('resources/devices/*yml')]
        self.cBoxRefDev.addItems(device_names_list)
        return

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
        target_name = self.cBoxTargetDev.currentText()
        ref_name = self.cBoxRefDev.currentText()

        #Check that target and reference devices are different
        if target_name == ref_name:
            logger.error("Target device and reference device are the same");
            return

        #Obtain the path of the target and reference devices
        dev_dir = "{}/resources/devices/".format(os.getcwd())
        target_path = "{}{}.yml".format(dev_dir, target_name)
        ref_path = "{}{}.yml".format(dev_dir, ref_name)
        if not glob.glob(target_path):
            logger.warning("Target device does not longer exist")
            return
        if not glob.glob(ref_path):
            logger.warning("Reference device does not longer exist")
            return

        #Create target and reference devices and try to connect to them
        self.target_dev = freqmeterdevice.FreqMeter.get_freq_meter(target_path)
        if not self.target_dev.connect():
            logger.error("Unable to connect to device {}".format(target_name))
            return
        if not self.target_dev.is_ready():
            logger.error("Device {} connected but not responding ACK".format(
                    target_name))
            return
        logger.info("Connected to device {}".format(target_name))

        self.ref_dev = freqmeterdevice.FreqMeter.get_freq_meter(ref_path)
        if not self.ref_dev.connect():
            logger.error("Unable to connect to device {}".format(ref_name))
            return
        if not self.ref_dev.is_ready():
            logger.error("Device {} connected but not responding ACK".format(
                    ref_name))
            return
        logger.info("Connected to device {}".format(ref_name))

        #Delete the old coarse calibration writing M=1.0
        self.target_dev.set_coarse_calib(1.0)

        #Start the coarse calibration reading values from target and ref devices


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
