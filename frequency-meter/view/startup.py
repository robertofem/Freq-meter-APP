#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
import glob
import logging
import os
import sys
# Third party libraries
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavTbar
import matplotlib.pyplot as plt
from PyQt5 import QtGui, QtCore, QtWidgets
import yaml
# Local libraries
from view import device_manager
from view import calibration
from view import freqmeterdevice
from view import measurement_engine
from view import instrument_data
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
        # Configure the Menu bar
        self.menuTools.triggered[QtWidgets.QAction].connect(self.tools_action)
        # Configure the logger, assigning an instance of AppLogHandler.
        self.log_handler = AppLogHandler(self.LoggerBrowser)
        logger.addHandler(self.log_handler)
        logger.info("Initialized the Frequency-Meter Application")
        # Log console level selection buttons
        self.DebugCheck.clicked.connect(self.update_logger_level)
        self.InfoCheck.clicked.connect(self.update_logger_level)
        self.WarnCheck.clicked.connect(self.update_logger_level)
        self.ErrorCheck.clicked.connect(self.update_logger_level)
        # Connect main buttons to its functions
        self.StartButton.clicked.connect(self.start_plot)
        self.StopButton.clicked.connect(self.stop_plot)
        self.DebugButton.clicked.connect(self.debug)
        self.ConnectDevButton1.clicked.connect(self.connect_device1)
        self.ConnectDevButton2.clicked.connect(self.connect_device2)
        # Lists containing graphical objects associated to different device
        self.device_scrollareas = [self.dev1_scrollarea, self.dev2_scrollarea]
        self.DevComboBox=[self.DeviceComboBox1, self.DeviceComboBox2]
        self.ConnectButton=[self.ConnectDevButton1, self.ConnectDevButton2]
        #Setup of the graphic elemnts in those Lists
        for slot in range(2):
            self.device_scrollareas[slot].setVisible(True)
            self.device_scrollareas[slot].setEnabled(False)
            self.device_scrollareas[slot].setFixedHeight(145)
            self.updateDevCombobox(self.DevComboBox[slot])
        #Make measurment times visible
        self.TimesgroupBox.setEnabled(True)
        # Instrument devices list.
        self.devices = [None, None]

        # Qt timer set-up for updating the plots.
        self.__plot_update = QtCore.QTimer()
        self.__plot_update.timeout.connect(self.update_plots)
        # Measurement engine
        self.m_engine = measurement_engine.MeasurementEngine(threaded=False)

        # plot layout set-up.
        self.figure = plt.figure()
        self.figure.patch.set_alpha(0)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavTbar(self.canvas, self)
        self.plotControlHLayout.addWidget(self.toolbar)
        spacer1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.plotControlHLayout.addItem(spacer1)
        self.plotVLayout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(top=0.9, bottom=0.1, left=0.13, right=0.95)
        self.ax.grid()
        self.ax.set_ylabel("F(Hz)", rotation='horizontal')
        self.ax.yaxis.set_label_coords(-0.05, 1.04)

        # Plot data
        # list of InstrumentData
        self.data = []
        # list (channel) of lists (signal)
        self.cboxes = [[], []]
        self.sample_counter = 0

    def connect_device1(self):
        if self.ConnectButton[0].text() == "Connect":
            self.connect_device(0)
        else:
            self.disconnect_device(0)
        return

    def connect_device2(self):
        if self.ConnectButton[1].text() == "Connect":
            self.connect_device(1)
        else:
            self.disconnect_device(1)
        return

    def connect_device(self, slot):
        """
        Load device in its corresponding slot and try to connect to it.
        """
        device_name = self.DevComboBox[slot].currentText()
        # Return if the ComboBox has not a valid item selected.
        if device_name == "<None>":
            logger.warning("No device selected")
            return
        else:
            if slot==0:
                other_slot = 1
            else:
                other_slot = 0
            if device_name == self.DevComboBox[other_slot].currentText():
                logger.warning(
                "Device {dev} is already selected in the other slot"
                .format(dev=device_name))
                return

        # Deal with the situation where the conf file is deleted since
        # the last time the list was refreshed.
        dev_dir = "{}/resources/devices/".format(os.getcwd())
        dev_path = "{dir}{dev}.yml".format(dir=dev_dir, dev=device_name)
        if not glob.glob(dev_path):
            logger.warning("Selected device does not longer exist")
            return

        #Disconnect and delete the old device in this slot
        if self.devices[slot] != None:
            #Disconnect first
            if self.devices[slot].is_connected():
                self.devices[slot].disconnect()
        self.devices[slot] = None
        #Disable the scroll
        self.device_scrollareas[slot].setEnabled(False)

        #Create a new device and try to connect to it
        new_device = freqmeterdevice.FreqMeter.get_freq_meter(dev_path)
        connected = new_device.connect()
        if connected:
            logger.info("Connected to device {dev}".format(dev=device_name))
            ready = new_device.is_ready()
            if not ready:
                logger.error("Device {dev} connected but not responding ACK"
                .format(dev=device_name))
                return
        else:
            logger.error("Unable to connect to device {dev}"
            .format(dev=device_name))

        #Add device to the list of available devices to do measurements
        self.devices[slot] = new_device

        # Measurement area items set-up
        self.device_scrollareas[slot].setEnabled(True)
        self.cboxes[slot] = self.items_setup(dev_path,slot+1)

        # Reset the ComboBox to the default value.
        #self.DevComboBox[slot].setCurrentIndex(0)

        #Change the button text to Disconnect
        self.ConnectButton[slot].setText("Disconnect")

        return

    def disconnect_device(self, slot):
        """
        Disconnect device and remove from slot.
        """
        #Disconnect and delete the old device in this slot
        if self.devices[slot] != None:
            #Disconnect first
            if self.devices[slot].is_connected():
                self.devices[slot].disconnect()
                device_name = self.DevComboBox[slot].currentText()
                logger.info("Disconnected from device {dev}"
                .format(dev=device_name))
        self.devices[slot] = None
        #Disable the scroll
        self.device_scrollareas[slot].setEnabled(False)
        #Change the button text to Disconnect
        self.ConnectButton[slot].setText("Connect")


    def tools_action(self,q):
        if q.text() == "Device manager":
            self.open_dev_mngr()
        elif q.text() == "FPGA frequency meter calibration":
            self.open_calib()

    def open_dev_mngr(self):
        logger.debug("Opening Device Manager pop-up window")
        self.popup = device_manager.DevManagerWindow()
        self.popup.exec_()
        self.popup = None;
        for slot in range(2):
            self.updateDevCombobox(self.DevComboBox[slot])
        logger.info("Updated devices list")
        return

    def open_calib(self):
        logger.debug("Opening FPGA device Calibration pop-up window")
        self.popup = calibration.CalibWindow()
        self.popup.exec_()
        self.popup = None
        return

    def updateDevCombobox(self, comboBox):
        devices_list = [os.path.basename(match)[:-4] for match in
                        glob.glob('resources/devices/*yml')]
        comboBox.clear()
        comboBox.addItem('<None>')
        comboBox.addItems(devices_list)
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
        self.LoadDeviceButton.setEnabled(True)
        self.DeviceComboBox.setEnabled(True)
        self.remove_buttons[dev-1].setEnabled(False)
        self.connect_buttons[dev-1].setEnabled(False)
        # Measurement area items set-up
        self.device_scrollareas[dev-1].setVisible(False)
        # Disable the times group box if any device is loaded.
        if all(dev is None for dev in self.devices):
            self.TimesgroupBox.setEnabled(False)
        return

    def start_plot(self):
        # Check which devices will be loaded and connected
        # They will be used to measure and plot
        self.measuring_devices = []
        for device in self.devices:
            if device:
                if not device.is_connected():
                    logger.warning("Some device is not connected")
                    return
                self.measuring_devices.append(device)

        # Generate data structure to store plotting values
        self.data = []
        for measuring_device in self.measuring_devices:
            self.data.append(instrument_data.InstrumentData(
                n_channels=1, n_signals=measuring_device.n_signals,
                sig_types=measuring_device.sig_types))
        logger.debug("Cleaning older stored data")

        # Start the measurement engine
        sample_time = self.SampleTimeBox.value()
        fetch_time = self.FetchTimeBox.value()
        self.m_engine.start(self.measuring_devices, fetch_time, sample_time)
        logger.debug("Measurement Starts")

        # Start the timer to update plots
        # 65ms=15 updates per second (enough for human eye)
        self.__plot_update.start(500)
        logger.debug("Plotting Starts")
        return

    def update_plots(self):
        # Get measurements
        self.ax.cla()
        self.ax.grid()
        self.ax.set_ylabel("F(Hz)", rotation='horizontal')
        self.ax.yaxis.set_label_coords(-0.03, 1.04)
        # Remove exponential notation in y axis
        self.ax.get_yaxis().get_major_formatter().set_useOffset(False)

        # TODO [floonone-20170904] Plot every device and every channel
        for device in self.measuring_devices:
            measurements = device.get_measurement_data()
            signals = device.get_signals()
            for sig in range(len(signals)):
                # If the corresponding checkbox is checked then plot
                sig_key = "S{}".format(sig+1)
                sig_type = signals[sig]
                if self.cboxes[0][0][sig_key].isChecked():
                    # Draw the plot
                    self.ax.plot(
                        list(measurements[0][sig_type].values()),
                        label="Dev-{} Ch-{} {}".format(1, 1, sig_type)
                    )

            # Print legends in the plot
            handles, labels = self.ax.get_legend_handles_labels()
            plt.legend(bbox_to_anchor=(0., 1.02, 1., 0.102), loc=0, ncol=3,
                       mode="expand", borderaxespad=0., fontsize='xx-small')

            # Update sample counter
            self.sample_counter = len(self.data[0].channel[0].signal[
                self.measuring_devices[0].sig_types['S1']])

            # If scroll mode selected then cut the signal
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
        self.__plot_update.stop()
        self.m_engine.stop()
        logger.debug("Pressed stop button")
        return

    def debug(self):
        print("debug")
        return

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
                    if sig_type:
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
