#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
import glob
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavTbar
import matplotlib.pyplot as plt
import logging
import os
import sys
import yaml
# Third party libraries
from PyQt4 import QtGui, QtCore
# Local libraries
from view import device_manager
from view import freqmeterdevice
from view import interface
# Test library
import random

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
        # Run the windows initialization routines.
        self.setupUi(self)
        self.popup = None
        self.update_devices_list()
        # Configure the logger, assigning an instance of AppLogHandler.
        self.log_handler = AppLogHandler(self.LoggerBrowser)
        logger.addHandler(self.log_handler)
        logger.info("Initialized the Frequency-Metter Application")
        # Test buttons
        self.StartButton.clicked.connect(self.start_plot)
        self.StopButton.clicked.connect(self.stop_plot)
        self.ClearButton.clicked.connect(self.clear_plot)
        # Log console level selection buttons
        self.DebugCheck.clicked.connect(self.update_logger_level)
        self.InfoCheck.clicked.connect(self.update_logger_level)
        self.WarnCheck.clicked.connect(self.update_logger_level)
        self.ErrorCheck.clicked.connect(self.update_logger_level)
        # Status labels initial configuration
        self.Status1Label_1.setVisible(False)
        self.Status1Label_2.setVisible(False)
        self.Status2Label_1.setVisible(False)
        self.Status2Label_2.setVisible(False)
        self.devnamelabel_1.setVisible(False)
        self.devnamelabel_2.setVisible(False)
        # Measurements channels labels initial configuration
        self.dev1_scrollarea.setVisible(False)
        self.dev2_scrollarea.setVisible(False)
        self.dev1label.setVisible(False)
        self.dev2label.setVisible(False)
        # Device manager buttons
        self.LoadDeviceButton.clicked.connect(self.load_device)
        self.DeviceMngButton.clicked.connect(self.new_device)
        # Devices buttons
        self.RemoveDevice1Button.clicked.connect(self.remove_device1)
        self.RemoveDevice2Button.clicked.connect(self.remove_device2)
        self.connectButton_1.clicked.connect(self.connect_device1)
        self.connectButton_2.clicked.connect(self.connect_device2)
        # Instrument devices list.
        self.devices = [None, None]
        # Qt timer set-up for updating the plots.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        # plot layout set-up.
        self.figure = plt.figure()
        self.figure.patch.set_alpha(0)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavTbar(self.canvas, self)
        self.plotVLayout.addWidget(self.toolbar)
        self.plotVLayout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(top=0.9, bottom=0.13, left=0.1)
        self.ax.grid()
        # Plot data
        self.data = {'1': [], '2': []}

    def update_logger_level(self):
        """Evaluate the check boxes states and update logger level."""
        self.log_handler.enabled[logging.DEBUG] = self.DebugCheck.isChecked()
        self.log_handler.enabled[logging.INFO] = self.InfoCheck.isChecked()
        self.log_handler.enabled[logging.WARN] = self.WarnCheck.isChecked()
        self.log_handler.enabled[logging.ERROR] = self.ErrorCheck.isChecked()
        return

    def load_device(self):
        """
        Load the selected device to the first available slot.
        """
        device_name = self.DeviceComboBox.currentText()
        if device_name == "<None>":
            logger.warn("No device selected")
        elif device_name in (self.Device1NameLabel.text(),
                             self.Device2NameLabel.text()):
            logger.warn("Selected device is already loaded")
        else:
            # Deal with the situation where the conf file is deleted since 
            # the last time the list was refreshed.
            dev_dir = "{}/resources/devices/".format(os.getcwd())
            dev_path = "{dir}{dev}.yml".format(dir=dev_dir, dev=device_name)
            if not glob.glob(dev_path):
                logger.warn("Selected device does not longer exist")
                return
            if self.devices[0] is None:
                self.devices[0] = freqmeterdevice.FreqMeterDevice(dev_path,
                                                                  logger)
                logger.info("Loaded the device {dev}".format(dev=device_name))
                # Measurement area items set-up
                self.dev1_scrollarea.setVisible(True)
                self.dev1label.setVisible(True)
                self.dev1label.setText(device_name)
                # measurement_items_setup()
                # Devices manager area items set-up
                self.Status1Label_1.setVisible(True)
                self.Status1Label_2.setVisible(True)
                self.devnamelabel_1.setVisible(True)
                self.Status1Label_2.setText("<font color='red'>not connected"
                                           "</font>")
                self.Device1NameLabel.setText(self.DeviceComboBox.currentText())
                self.DeviceComboBox.setCurrentIndex(0)
                # If a device is already loaded at the other section, disable
                # the load button.
                if self.RemoveDevice2Button.isEnabled():
                    self.LoadDeviceButton.setEnabled(False)
                    self.DeviceComboBox.setEnabled(False)
                self.RemoveDevice1Button.setEnabled(True)
                self.connectButton_1.setEnabled(True)
            elif self.devices[1] is None:
                self.devices[1] = freqmeterdevice.FreqMeterDevice(dev_path,
                                                                  logger)
                logger.info("Loaded the device {dev}".format(dev=device_name))
                # Measurement area items set-up
                self.dev2_scrollarea.setVisible(True)
                self.dev2label.setVisible(True)
                self.dev2label.setText(device_name)
                self.Status2Label_1.setVisible(True)
                self.Status2Label_2.setVisible(True)
                self.devnamelabel_2.setVisible(True)
                self.Status2Label_2.setText("<font color='red'>not connected"
                                           "</font>")
                self.Device2NameLabel.setText(self.DeviceComboBox.currentText())
                self.DeviceComboBox.setCurrentIndex(0)
                self.LoadDeviceButton.setEnabled(False)
                self.DeviceComboBox.setEnabled(False)
                self.RemoveDevice2Button.setEnabled(True)
                self.connectButton_2.setEnabled(True)
            else:
                logger.warn("There are 2 devices already loaded!")
        return

    def remove_device1(self):
        self.devices[0].disconnect()
        self.devices[0] = None
        logger.info("Device 1 removed")
        self.Status1Label_1.setVisible(False)
        self.Status1Label_2.setVisible(False)
        self.devnamelabel_1.setVisible(False)
        self.Device1NameLabel.setText("")
        self.LoadDeviceButton.setEnabled(True)
        self.DeviceComboBox.setEnabled(True)
        self.RemoveDevice1Button.setEnabled(False)
        self.connectButton_1.setEnabled(False)
        # Measurement area items set-up
        self.dev1_scrollarea.setVisible(False)
        self.dev1label.setVisible(False)
        return

    def remove_device2(self):
        self.devices[1].disconnect()
        self.devices[1] = None
        logger.info("Device 2 removed")
        self.Status2Label_1.setVisible(False)
        self.Status2Label_2.setVisible(False)
        self.devnamelabel_2.setVisible(False)
        self.Device2NameLabel.setText("")
        self.LoadDeviceButton.setEnabled(True)
        self.DeviceComboBox.setEnabled(True)
        self.RemoveDevice2Button.setEnabled(False)
        self.connectButton_2.setEnabled(False)
        # Measurement area items set-up
        self.dev1_scrollarea.setVisible(False)
        self.dev1label.setVisible(False)
        return

    def connect_device1(self):
        self.devices[0].connect()
        if self.devices[0].is_connected():
            self.Status1Label_2.setText("<font color='green'>connected</font>")
        else:
            self.Status1Label_2.setText("<font color='red'>not connected"
                                        "</font>")
        return

    def connect_device2(self):
        self.devices[1].connect()
        if self.devices[0].is_connected():
            self.Status2Label_2.setText("<font color='green'>connected</font>")
        else:
            self.Status2Label_2.setText("<font color='red'>not connected"
                                        "</font>")
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

    def update_plots(self):
        # Sample values for X and Y axis
        # for i in range(10):
        self.data['1'].append(random.gauss(10, 0.5))
        self.data['2'].append(random.gauss(10, 0.1))
        # Discard old graph
        self.ax.cla()
        # Draw the plot
        self.ax.grid()
        self.ax.plot(self.data['1'], 'r-')
        self.ax.plot(self.data['2'], 'b-')
        # Set the visible area
        if self.scrollcheckBox.isChecked():
            if len(self.data['1']) > 100:
                self.ax.set_xlim(len(self.data['1']) - 100, len(self.data['1']))
        # Refresh canvas
        self.canvas.draw()
        logger.debug("Plot debugging")
        return

    def start_plot(self):
        # Sample values for X and Y axis
        self.timer.start(1000)
        logger.debug("Start plotting")
        return

    def stop_plot(self):
        self.timer.stop()
        logger.debug("Pressed stop button")
        return

    def clear_plot(self):
        logger.debug("Pressed clear button")
        return


def measurement_items_setup(conf_file, dev=1):
    """
    Reads the info from a conf_file and prepares the scroll area items.
    """
    # with open(conf_file, 'r') as read_file:
    #         dev_data = yaml.load(read_file)
    # channels = int(dev_data['chanels']['Quantity'])
    # for channel in range(1, channels+1):
    #     pass
    return

def run():
    # The QApplication object manages the application control flow and settings.
    app = QtGui.QApplication(sys.argv)
    # Set to a GTK allowed style in order to avoid annoying erros on Ubuntu.
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
