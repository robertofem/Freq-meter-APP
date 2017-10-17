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
from PyQt5.QtCore import QRegularExpression, QTimer
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

        #Connect/Disconnect buttons
        self.target_dev_connect.pressed.connect(lambda dev_type="target_dev":
            self.__on_device_control_button_press(dev_type))
        self.ref_dev_connect.pressed.connect(lambda dev_type="ref_dev":
            self.__on_device_control_button_press(dev_type))
        # Start and Stop Buttons events
        self.button_start_coarse.clicked.connect(self.__start_coarse)
        self.button_stop_coarse.clicked.connect(self.__stop_coarse)
        self.button_start_fine.clicked.connect(self.__start_fine)
        self.button_stop_fine.clicked.connect(self.__stop_fine)
        # Button box events (accept/reject)
        self.buttonBox.clicked.connect(self.__handle_buttonBox_click)

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
        self.__populate_target_combobox()
        #populate list with reference devices with all devices
        self.__populate_reference_combobox()

        #create devices for target and reference
        self.target_dev = None
        self.ref_dev = None

    def __populate_target_combobox(self):
        #clear the combobox
        self.target_dev_selector.clear()
        #open all files and add devices which vendor is "Uvigo"
        device_names_list = [os.path.basename(match)[:-4]
                        for match in glob.glob('resources/devices/*yml')]
        for device_name in device_names_list:
            dev_dir = "{}/resources/devices/".format(os.getcwd())
            dev_path = "{}{}.yml".format(dev_dir, device_name)
            new_device = freqmeterdevice.FreqMeter.get_freq_meter(dev_path)
            if new_device.get_vendor_name() == "Uvigo":
                self.target_dev_selector.addItem(device_name)
        return

    def __populate_reference_combobox(self):
        #clear the combobox
        self.ref_dev_selector.clear()
        #add all devices
        device_names_list = [os.path.basename(match)[:-4]
                        for match in glob.glob('resources/devices/*yml')]
        self.ref_dev_selector.addItems(device_names_list)
        return

    def __handle_buttonBox_click(self, button):
        """
        Check which button was pressed and perform corresponding action.
        """
        clicked_button = self.buttonBox.standardButton(button)
        if clicked_button == QtWidgets.QDialogButtonBox.Close:
            self.__show_exit_dialog()
        return

    def __show_exit_dialog(self):
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

    def __on_device_control_button_press(self, dev_type):
        button_pressed = self.findChild(QtWidgets.QPushButton,
            "{}_connect".format(dev_type))
        if button_pressed.text()=="Disconnect":
            self.__disconnect_dev(dev_type)
        else:
            self.__connect_dev(dev_type)

    def __connect_dev(self, dev_type):
        device_group = self.findChild(QtWidgets.QGroupBox,
                                      "{}_group".format(dev_type))
        name = device_group.findChild(QtWidgets.QComboBox).currentText()

        # check if the other device is the same and it is connected
        if dev_type == "ref_dev":
            current_dev = self.ref_dev
            other_dev = self.ref_dev
            other_type = "target_dev"
        else:
            current_dev = self.target_dev
            other_dev = self.target_dev
            other_type = "ref_dev"
        other_group = self.findChild(QtWidgets.QGroupBox,
                                      "{}_group".format(other_type))
        other_name = other_group.findChild(QtWidgets.QComboBox).currentText()
        if other_dev != None:
            if other_dev.is_connected() and name == other_name:
                logger.warning("This device is already connected");
                return

        # path join
        dev_dir = "{}/resources/devices/".format(os.getcwd())
        dev_path = "{}{}.yml".format(dev_dir, name)
        if not glob.glob(dev_path):
            logger.warning("Selected device does not longer exist")
            return

        # Create a new device and try to connect to it
        new_device = freqmeterdevice.FreqMeter.get_freq_meter(dev_path)
        if not new_device.connect():
            logger.error("Unable to connect to device {}".format(name))
            return
        if not new_device.is_ready():
            logger.error("Device {} connected but not responding ACK".format(
                    name))
            return
        logger.info("Connected to device {}".format(name))
        current_dev = new_device

        # Change the button text to Disconnect
        device_group.findChild(QtWidgets.QPushButton).setText("Disconnect")
        # Disable selector
        device_group.findChild(QtWidgets.QComboBox).setEnabled(False)
        # Enable signal and channel controls
        for control in device_group.findChildren(QtWidgets.QGroupBox):
            control.setEnabled(True)
        # Show available channels
        channel_controls = [channel for channel in device_group.findChildren(
                QtWidgets.QRadioButton, QRegularExpression("channel\\d"))]
        print(channel_controls)
        channels = new_device.get_channels()
        for i in range(channels):
            channel_controls[i].setEnabled(True)
            channel_controls[i].setVisible(True)
        for i in range(channels, 4):
            channel_controls[i].setEnabled(False)
            channel_controls[i].setVisible(False)
        channel_controls[0].setChecked(True)
        # Show available impedances
        impedance_controls = [channel for channel in device_group.findChildren(
                QtWidgets.QRadioButton, QRegularExpression("impedance\\d"))]
        impedances = new_device.get_impedances()
        for i in range(len(impedances)):
            impedance_controls[i].setText(impedances[i])
            impedance_controls[i].setEnabled(True)
            impedance_controls[i].setVisible(True)
        for i in range(len(impedances), 4):
            impedance_controls[i].setText("")
            impedance_controls[i].setEnabled(False)
            impedance_controls[i].setVisible(False)
        impedance_controls[0].setChecked(True)


    def __disconnect_dev(self, dev_type):
        logger.info("disconnect {}".format(dev_type))
        # Change the button text to Disconnect
        # device_group.findChild(QtWidgets.QPushButton).setText("Connect")

    def __start_coarse(self):
        """
        Start coarse calibration.
        """
        ref_name = self.ref_dev_selector.currentText()

        #Check that target and reference devices are different
        if target_name == ref_name:
            logger.error("Target device and reference device are the same");
            return

        #Obtain the path of the target and reference devices


        ref_path = "{}{}.yml".format(dev_dir, ref_name)

        if not glob.glob(ref_path):
            logger.warning("Reference device does not longer exist")
            return

        #Create target and reference devices and try to connect to them



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

    def __stop_coarse(self):
        """
        Stop coarse calibration.
        """
        return

    def __start_fine(self):
        """
        Start fine calibration.
        """
        return
    def __stop_fine(self):
        """
        Stop fine calibration.
        """
        return
