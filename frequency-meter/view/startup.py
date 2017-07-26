#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
import glob
import logging
import os
import sys
# Third party libraries
from PyQt4 import QtGui, QtCore
# Local libraries
from view import device_manager
from view import interface


# Create the application logger, with a previously defined configuration.
logger = logging.getLogger('view')

class AppLogHandler(logging.Handler):
    """
    Customized logging handler class, for printing on a PyQt Widget.
    """
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.widget = widget
        self.setLevel(logging.DEBUG)
        formatter = logging.Formatter(" %(asctime)s.%(msecs)03d %(levelname)8s:"
                                      " %(message)s", "%H:%M:%S")
        self.setFormatter(formatter)
        # Log messages colours.
        self.levelcolours = {
            logging.DEBUG: 'black',
            logging.INFO: 'blue',
            logging.WARN: 'orange',
            logging.ERROR: 'red',
        }
        # Paths to the log icons.
        parent_path = os.path.dirname(__file__)
        self.logsymbols = {
            logging.DEBUG: "{}/icons/debug.png".format(parent_path),
            logging.INFO: "{}/icons//info.png".format(parent_path),
            logging.WARN: "{}/icons//warning.png".format(parent_path),
            logging.ERROR: "{}/icons//error.png".format(parent_path),
        }
        # The True levels are the ones that are printed on the log.
        self.enabled = {
            logging.DEBUG: False,
            logging.INFO: True,
            logging.WARN: True,
            logging.ERROR: True,
        }

    def emit(self, record):
        """Override the logging.Handler.emit method.

        The received log message will be printed on the specified
        widget, tipically a TextBox.
        """
        # Only print on the log the enabled log levels.
        if not self.enabled[record.levelno]:
            return
        new_log = self.format(record)
        self.widget.insertHtml('<img src={img} height="14" width="14"/>'
                               '<font color="{colour}">{log_msg}</font><br />'
                               .format(img=self.logsymbols[record.levelno],
                                       colour=self.levelcolours[record.levelno],
                                       log_msg=new_log))
        self.widget.moveCursor(QtGui.QTextCursor.End)
        return


class MainWindow(QtGui.QMainWindow, interface.Ui_MainWindow):
    """
    Class for defining the behaviour of the User Interface main window.
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.popup = None
        self.update_devices_list()
        # Test buttons
        self.DebugButton.clicked.connect(self.debug)
        self.ErrorButton.clicked.connect(self.error)
        self.WarnButton.clicked.connect(self.warn)
        # Log console level selection buttons
        self.DebugCheck.clicked.connect(self.update_logger_level)
        self.InfoCheck.clicked.connect(self.update_logger_level)
        self.WarnCheck.clicked.connect(self.update_logger_level)
        self.ErrorCheck.clicked.connect(self.update_logger_level)
        # Status labels initial configuration
        self.Status1Label_1.setVisible(False)
        self.Status1Label_2.setVisible(False)
        self.Status1Label_2.setText("<font color='green'>connected</font>")
        self.Status2Label_1.setVisible(False)
        self.Status2Label_2.setVisible(False)
        self.Status2Label_2.setText("<font color='green'>connected</font>")
        # Device manager buttons
        self.LoadDeviceButton.clicked.connect(self.load_device)
        self.RemoveDevice1Button.clicked.connect(self.remove_device1)
        self.RemoveDevice2Button.clicked.connect(self.remove_device2)
        self.DeviceMngButton.clicked.connect(self.new_device)
        # Configure the logger, assigning an instance of AppLogHandler.
        self.log_handler = AppLogHandler(self.LoggerBrowser)
        # log_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(self.log_handler)
        logger.info("Initialized the Frequency-Metter Application")

    def update_logger_level(self):
        """Evaluate the check boxes states and update logger level."""
        self.log_handler.enabled[logging.DEBUG] = self.DebugCheck.isChecked()
        self.log_handler.enabled[logging.INFO] = self.InfoCheck.isChecked()
        self.log_handler.enabled[logging.WARN] = self.WarnCheck.isChecked()
        self.log_handler.enabled[logging.ERROR] = self.ErrorCheck.isChecked()
        return

    def load_device(self):
        device_name = self.DeviceComboBox.currentText()
        if device_name == "<None>":
            logger.warn("No device selected")
        else:
            if not self.RemoveDevice1Button.isEnabled():
                logger.info("Loaded the device {dev}".format(dev=device_name))
                self.Status1Label_1.setVisible(True)
                self.Status1Label_2.setVisible(True)
                self.Status1Label_2.setText("<font color='red'>disconnected"
                                           "</font>")
                self.Device1NameLabel.setText(self.DeviceComboBox.currentText())
                self.DeviceComboBox.setCurrentIndex(0)
                # If a device is already loaded at the other section, disable
                # the load button.
                if self.RemoveDevice2Button.isEnabled():
                    self.LoadDeviceButton.setEnabled(False)
                    self.DeviceComboBox.setEnabled(False)
                self.RemoveDevice1Button.setEnabled(True)
            elif not self.RemoveDevice2Button.isEnabled():
                logger.info("Loaded the device {dev}".format(dev=device_name))
                self.Status2Label_1.setVisible(True)
                self.Status2Label_2.setVisible(True)
                self.Status2Label_2.setText("<font color='red'>disconnected"
                                           "</font>")
                self.Device2NameLabel.setText(self.DeviceComboBox.currentText())
                self.DeviceComboBox.setCurrentIndex(0)
                self.LoadDeviceButton.setEnabled(False)
                self.DeviceComboBox.setEnabled(False)
                self.RemoveDevice2Button.setEnabled(True)
            else:
                logger.warn("There are 2 devices already loaded!")
        return

    def remove_device1(self):
        logger.info("Device removed")
        self.Status1Label_1.setVisible(False)
        self.Status1Label_2.setVisible(False)
        self.Device1NameLabel.setText("")
        self.LoadDeviceButton.setEnabled(True)
        self.DeviceComboBox.setEnabled(True)
        self.RemoveDevice1Button.setEnabled(False)
        return

    def remove_device2(self):
        logger.info("Device removed")
        self.Status2Label_1.setVisible(False)
        self.Status2Label_2.setVisible(False)
        self.Device2NameLabel.setText("")
        self.LoadDeviceButton.setEnabled(True)
        self.DeviceComboBox.setEnabled(True)
        self.RemoveDevice2Button.setEnabled(False)
        return

    def new_device(self):
        logger.debug("Opening Device Manager pop-up window")
        self.popup = device_manager.DevManagerWindow()
        self.popup.exec_()
        self.update_devices_list()
        return

    def update_devices_list(self):
        devices_list = [os.path.basename(match)[:-4] for match in
                        glob.glob('resources/devices/*yml')]
        self.DeviceComboBox.clear()
        self.DeviceComboBox.addItem('<None>')
        self.DeviceComboBox.addItems(devices_list)
        logger.info("Updated devices list")
        return        

    def debug(self):
        logger.debug("Pressed debug button")
        return

    def error(self):
        logger.error("Pressed error button")
        return

    def warn(self):
        logger.warn("Pressed error button")
        return


def run():
    # The QApplication object manages the application control flow and settings.
    app = QtGui.QApplication(sys.argv)
    # Set to a GTK allowed style in order to avoid annoying erros on Ubuntu.
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
