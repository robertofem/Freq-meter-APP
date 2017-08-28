#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
import glob
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavTbar
#from matplotlib import ticker
import matplotlib.pyplot as plt
import logging
import os
import sys
import time
import yaml
# Third party libraries
from PyQt5 import QtGui, QtCore, QtWidgets
# Local libraries
from view import device_manager
from view import calibration
from view import freqmeterdevice
from view import measurement_engine
from view import instrument_data
from view import interface
# library for testing
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
        widget, typically a TextBox.
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


class MainWindow(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    """
    Class for defining the behaviour of the User Interface main window.
    """
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        # Run the windows initialization routines.
        self.setupUi(self)
        self.popup = None
        self.update_devices_list()
        # Configure the Menu bar actionSave
        self.menuTools.triggered[QtWidgets.QAction].connect(self.open_calib)

        # Configure the logger, assigning an instance of AppLogHandler.
        self.log_handler = AppLogHandler(self.LoggerBrowser)
        logger.addHandler(self.log_handler)
        logger.info("Initialized the Frequency-Meter Application")
        # Test buttons
        self.StartButton.clicked.connect(self.start_plot)
        self.StopButton.clicked.connect(self.stop_plot)
        self.DebugButton.clicked.connect(self.debug)
        # Log console level selection buttons
        self.DebugCheck.clicked.connect(self.update_logger_level)
        self.InfoCheck.clicked.connect(self.update_logger_level)
        self.WarnCheck.clicked.connect(self.update_logger_level)
        self.ErrorCheck.clicked.connect(self.update_logger_level)
        # Status labels initial configuration
        self.status_label_1.setVisible(False)
        self.status_label_2.setVisible(False)
        self.connected_label_1.setVisible(False)
        self.connected_label_2.setVisible(False)
        self.devname_label_l_1.setVisible(False)
        self.devname_label_l_2.setVisible(False)
        # Measurements channels labels initial configuration
        self.dev1_scrollarea.setVisible(False)
        self.dev2_scrollarea.setVisible(False)
        self.dev_label_1.setVisible(False)
        self.dev_label_2.setVisible(False)
        # Device manager buttons
        self.LoadDeviceButton.clicked.connect(self.load_device)
        self.DeviceMngButton.clicked.connect(self.new_device)
        # Devices buttons
        self.removeButton_1.clicked.connect(lambda: self.remove_device(dev=1))
        self.removeButton_2.clicked.connect(lambda: self.remove_device(dev=2))
        self.connectButton_1.clicked.connect(lambda: self.connect_device(dev=1))
        self.connectButton_2.clicked.connect(lambda: self.connect_device(dev=2))
        # Lists containing objects manipulated at connect and remove events.
        self.connect_buttons = [self.connectButton_1, self.connectButton_2]
        self.remove_buttons = [self.removeButton_1, self.removeButton_2]
        self.devname_labels_l = [self.devname_label_l_1, self.devname_label_l_2]
        self.devname_labels_r = [self.devname_label_r_1, self.devname_label_r_2]
        self.status_labels = [self.status_label_1, self.status_label_2]
        self.connected_labels = [self.connected_label_1, self.connected_label_2]
        self.device_labels = [self.dev_label_1, self.dev_label_2]
        self.device_scrollareas = [self.dev1_scrollarea, self.dev2_scrollarea]
        # Instrument devices list.
        self.devices = [None, None]
        # Qt timer set-up for updating the plots.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        #Measuremnt engine
        self.m_engine = measurement_engine.MeasurementEngine(logger)
        # plot layout set-up.
        self.figure = plt.figure()
        self.figure.patch.set_alpha(0)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavTbar(self.canvas, self)
        self.plotVLayout.addWidget(self.toolbar)
        self.plotVLayout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(top=0.85, bottom=0.10, left=0.1)
        self.ax.grid()
        self.ax.set_ylabel("F(Hz)", rotation= 'horizontal')
        self.ax.yaxis.set_label_coords(-0.05, 1.04)
        # Plot data
        self.data = [] #list of InstrumentData
        self.cboxes = [[], []] #list (channel) of lists (signal)
        self.sample_counter = 0

    def load_device(self):
        """
        Load the selected device to the first available slot.
        """
        device_name = self.DeviceComboBox.currentText()
        # Return if the ComboBox has not a valid item selected.
        if device_name == "<None>":
            logger.warning("No device selected")
            return
        elif device_name in (self.device_labels[0].text(),
                             self.device_labels[1].text()):
            logger.warning("Selected device is already loaded")
            return
        # Deal with the situation where the conf file is deleted since
        # the last time the list was refreshed.
        dev_dir = "{}/resources/devices/".format(os.getcwd())
        dev_path = "{dir}{dev}.yml".format(dir=dev_dir, dev=device_name)
        if not glob.glob(dev_path):
            logger.warning("Selected device does not longer exist")
            return
        self.TimesgroupBox.setEnabled(True)
        # Look for the first available slot. Return if both are being used.
        if self.devices[0] is None:
            dev = 1
        elif self.devices[1] is None:
            dev = 2
        else:
            logger.warning("There are 2 devices already loaded!")
            return
        self.devices[dev-1] = freqmeterdevice.FreqMeter.get_freq_meter(dev_path)

        if self.devices[0] is None:
            logger.debug("self.device[0] is None")

        logger.info("Loaded the device {dev}".format(dev=device_name))
        # Measurement area items set-up
        self.device_scrollareas[dev-1].setVisible(True)
        self.device_labels[dev-1].setVisible(True)
        self.device_labels[dev-1].setText(device_name)
        self.cboxes[dev-1] = self.items_setup(dev_path,dev)
        # Devices manager area items set-up
        self.devname_labels_l[dev-1].setVisible(True)
        self.devname_labels_r[dev-1].setText(device_name)
        self.status_labels[dev-1].setVisible(True)
        self.connected_labels[dev-1].setVisible(True)
        self.connected_labels[dev-1].setText("<font color='red'>"
                                             "not connected</font>")
        # Reset the ComboBox to the default value.
        self.DeviceComboBox.setCurrentIndex(0)
        # If a device is already loaded at every slot, disable
        # the load button.
        if all(dev is not None for dev in self.devices):
            self.LoadDeviceButton.setEnabled(False)
            self.DeviceComboBox.setEnabled(False)
        self.remove_buttons[dev-1].setEnabled(True)
        self.connect_buttons[dev-1].setEnabled(True)
        return

    def new_device(self):
        logger.debug("Opening Device Manager pop-up window")
        self.popup = device_manager.DevManagerWindow()
        self.popup.exec_()
        self.popup = None;
        self.update_devices_list()
        return

    def open_calib(self):
        logger.debug("Opening FPGA device Calibration pop-up window")
        self.popup = calibration.CalibWindow()
        self.popup.exec_()
        self.popup = None;
        return

    def update_devices_list(self):
        devices_list = [os.path.basename(match)[:-4] for match in
                        glob.glob('resources/devices/*yml')]
        self.DeviceComboBox.clear()
        self.DeviceComboBox.addItem('<None>')
        self.DeviceComboBox.addItems(devices_list)
        logger.info("Updated devices list")
        return

    def connect_device(self, dev):
        """
        Connect or disconnect a device depending on its previous state.

        :param int dev: number of the target device. its corresponding
        list index is one value smaller, as it is 0-indexed.
        """
        if self.devices[dev-1].is_connected():
            # disconnect device.
            connected = self.devices[dev-1].disconnect()
            if not connected:
                self.connect_buttons[dev-1].setText("connect")
                self.connected_labels[dev-1].setText(
                        "<font color='red'>not connected</font>")
        else:
            # Try a connection and update status label and connect button text.
            connected = self.devices[dev-1].connect()
            if connected:
                ready = self.devices[dev - 1].is_ready()
                if ready:
                    self.connected_labels[dev-1].setText(
                            "<font color='green'>connected</font>")
                    self.connect_buttons[dev-1].setText("disconnect")
                else:
                    self.connected_labels[dev-1].setText(
                            "<font color='orange'>connected. No ACK</font>")
                    self.connect_buttons[dev-1].setText("disconnect")
            else:
                self.connected_labels[dev-1].setText(
                        "<font color='red'>not connected</font>")
        return

    def remove_device(self, dev):
        if self.devices[dev-1].is_connected():
            self.connect_device(dev=dev)
        self.devices[dev-1] = None
        logger.info("Device {} removed".format(dev))
        # Update the text of corresponding labels and buttons.
        self.status_labels[dev-1].setVisible(False)
        self.connected_labels[dev-1].setVisible(False)
        self.devname_labels_l[dev-1].setVisible(False)
        self.devname_labels_r[dev-1].setText("")
        self.device_labels[dev-1].setText("")
        self.LoadDeviceButton.setEnabled(True)
        self.DeviceComboBox.setEnabled(True)
        self.remove_buttons[dev-1].setEnabled(False)
        self.connect_buttons[dev-1].setEnabled(False)
        # Measurement area items set-up
        self.device_scrollareas[dev-1].setVisible(False)
        self.device_labels[dev-1].setVisible(False)
        # Disable the times group box if any device is loaded.
        if all(dev is None for dev in self.devices):
            self.TimesgroupBox.setEnabled(False)
        return

    def start_plot(self):
        #check which devices will be loaded and connected
        #they will be used to measure and plot
        self.dev_measure = []
        for device in self.devices:
            if device != None:
                if not device.is_connected():
                    logger.warning("Some device is not connected")
                    return
                self.dev_measure.append(device)

        # Generate data structure to store plotting values
        self.data = []
        for index in range(len(self.dev_measure)):
            self.data.append( instrument_data.InstrumentData(
                n_channels = 1,
                n_signals = self.dev_measure[index].n_signals,
                sig_types = self.dev_measure[index].sig_types
            ))
        logger.debug("Cleaning older stored data")

        # Start the measurement engine
        sample_time = self.SampleTimeBox.value()
        fetch_time = self.FetchTimeBox.value()
        self.m_engine.start(self.dev_measure, fetch_time, sample_time)
        logger.debug("Measurement Starts")

        #Start the timer to update plots
        self.timer.start(1000) #65ms=15 updates per second (enough for human eye)
        logger.debug("Plotting Starts")
        return

    def update_plots(self):
        # Get measuremnts from measurement engine
        new_samples = self.m_engine.get_values()

        #if the 1st signal of the 1st channel of the 1st device is not empty
        if len(new_samples[0].channel[0].signal[
            self.dev_measure[0].sig_types['S1']]) > 0:

            # Discard old graph and reset basic properties
            self.ax.cla()
            self.ax.grid()
            self.ax.set_ylabel("F(Hz)", rotation= 'horizontal')
            self.ax.yaxis.set_label_coords(-0.03, 1.04)
            # Remove exponential notation in y axis
            self.ax.get_yaxis().get_major_formatter().set_useOffset(False)

            #For each device
            for dev in range(len(self.dev_measure)):
                # Append new measurements to data historic
                self.data[dev].append(new_samples[dev])
                #For each signal in each channel
                for ch in range(1):
                    for sig in range (self.dev_measure[dev].n_signals):
                        #if the corresponding checkbox is checked then plot
                        sig_key = "S{}".format(sig+1)
                        sig_type = self.dev_measure[dev].sig_types[sig_key]
                        if self.cboxes[dev][ch][sig_key].isChecked():
                            # Draw the plot
                            self.ax.plot(
                                self.data[dev].channel[ch].signal[sig_type],
                                label="Dev-{dev} Ch-{chan} {signal}"
                                .format(dev=dev+1, chan=ch+1,signal=sig_type)
                            )

            #print legends in the plot
            handles, labels = self.ax.get_legend_handles_labels()
            plt.legend(bbox_to_anchor=(0., 1.02, 1., 0.102), loc=0, ncol=3,
                       mode="expand", borderaxespad=0., fontsize='xx-small')

            #Update sample counter
            self.sample_counter = len(self.data[0].channel[0].signal[
            self.dev_measure[0].sig_types['S1']])

            #If scroll mode selected then cut the signal
            if self.scrollcheckBox.isChecked():
                if self.sample_counter > 100:
                    self.ax.set_xlim(
                        self.sample_counter - 100,
                        self.sample_counter
                    )

            # Refresh canvas
            self.canvas.draw()
        return

    def stop_plot(self):
        self.timer.stop()
        self.m_engine.stop()
        logger.debug("Pressed stop button")
        return

    def debug(self):
        sample_time = self.SampleTimeBox.value()
        self.timer.start(sample_time * 1000)
        logger.debug("Start sampling every {} seconds".format(sample_time))
        return

    def debug_plot(self):
        # Discard old graph and reset basic properties
        self.ax.cla()
        self.ax.grid()
        self.ax.set_ylabel("F(Hz)", rotation= 'horizontal')
        self.ax.yaxis.set_label_coords(-0.05, 1.04)
        n_channels = int(self.devices[0]._dev_data['channels']['Quantity'])
        n_signals = int(self.devices[0]._dev_data['channels']['Signals'])
        sig_types = self.devices[0]._dev_data['channels']['SigTypes']
        # Go over every device channel
        for ch_index in range(n_channels):
            # Go over every Signal in the channel and plot its value if it is
            # specified in the corresponding CheckBox.
            for signal_index in range(n_signals):
                dic_index = "S{}".format(signal_index+1)
                sig_type = sig_types[dic_index]
                # Get new value and append it to data set.
                value = random.gauss(10, 1+signal_index)
                self.data['1'][ch_index][dic_index].append(value)
                if self.cboxes[0][ch_index][dic_index].isChecked():
                    # Draw the plot
                    self.ax.plot(self.data['1'][ch_index][dic_index],
                                 label="Dev-{dev} Ch-{channel} {signal}"
                                       "".format(dev=1, channel=ch_index+1,
                                                 signal=sig_type)
                                )
        handles, labels = self.ax.get_legend_handles_labels()
        plt.legend(bbox_to_anchor=(0., 1.02, 1., 0.102), loc=3, ncol=3,
                   mode="expand", borderaxespad=0., fontsize='xx-small')
        if self.scrollcheckBox.isChecked():
            if len(self.data['1']) > 100:
                self.ax.set_xlim(len(self.data['1']) - 100, len(self.data['1']))
        # Refresh canvas
        self.canvas.draw()
        logger.debug("Plot new sample: {}".format(value))

    def items_setup(self, conf_file, dev):
        """
        Reads the info from a conf_file and prepares the GUI items.

        There is a GroupBox for each device channel, with a maximum of
        four. Each GroupBox is visible or invisible depending on the
        amount of channels specified in the configuration file.

        Also, the ComboBoxes representing the signals from every channel
        are enabled or disabled depending if they have any function
        specified in the configuration file.

        Finally, the method returns a dictionary with every configured
        device signal.
        """
        # Find the scroll area corresponding to the input device.
        scrollarea_name = "dev{}_scrollarea".format(dev)
        dev_sa = ""
        # Find the ScrollArea corresponding to the input device number.
        for sa in self.measurement_groupBox.findChildren(QtWidgets.QScrollArea):
            if sa.objectName() == scrollarea_name:
                dev_sa = sa
        if dev_sa == "":
            logger.debug("No ScrollArea detected with name {}".format(dev_sa))
            return (0, 0)
        # Open and load the input device configuration file.
        with open(conf_file, 'r') as read_file:
            dev_data = yaml.load(read_file)
        active_checkboxes = []
        # Go over every group in the device area, representing each possible
        # channel, and set the GUI configuration according to the conf file.
        for g_idx, group in enumerate(dev_sa.findChildren(QtWidgets.QGroupBox)):
            if g_idx < int(dev_data['channels']['Quantity']):
                group.setVisible(True)
                active_checkboxes.append(dict())
                # Go over every CheckBox in the channel GroupBox and enable it
                # if it is specified in the configuration file.
                for c_idx, checkbox in enumerate(
                        group.findChildren(QtWidgets.QCheckBox)):
                    dic_index = "S{}".format(c_idx+1)
                    sig_type = dev_data['channels']['SigTypes'][dic_index]
                    checkbox.setText(sig_type)
                    if sig_type != "<None>":
                        active_checkboxes[g_idx][dic_index] = checkbox
                        checkbox.setEnabled(True)
                    else:
                        checkbox.setEnabled(False)
            # Hide the GroupBox if is not specified at the configuration file.
            else:
                group.setVisible(False)
        return (active_checkboxes)

    def update_logger_level(self):
        """Evaluate the check boxes states and update logger level."""
        self.log_handler.enabled[logging.DEBUG] = self.DebugCheck.isChecked()
        self.log_handler.enabled[logging.INFO] = self.InfoCheck.isChecked()
        self.log_handler.enabled[logging.WARN] = self.WarnCheck.isChecked()
        self.log_handler.enabled[logging.ERROR] = self.ErrorCheck.isChecked()
        return


def run():
    # The QApplication object manages the application control flow and settings.
    app = QtWidgets.QApplication(sys.argv)
    # Set to a GTK allowed style in order to avoid annoying errors on Ubuntu.
    app.setStyle(QtWidgets.QStyleFactory.create("plastique"))
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
