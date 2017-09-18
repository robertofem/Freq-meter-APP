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
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRegularExpression, QTimer
# Local libraries
from view import device_manager
from view import calibration
from view import freqmeterdevice
from view import measurement_engine
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
        # Instrument devices list.
        self.__devices = {}
        self.popup = None
        # Configure the logger, assigning an instance of AppLogHandler.
        self.log_handler = AppLogHandler(self.LoggerBrowser)
        logger.addHandler(self.log_handler)
        logger.info("Initialized the Frequency-Meter Application")
        # Setup menu
        self.__setup_menu()
        # Setup device control area
        self.__setup_device_controls()

        # Log console level selection buttons
        self.DebugCheck.clicked.connect(self.update_logger_level)
        self.InfoCheck.clicked.connect(self.update_logger_level)
        self.WarnCheck.clicked.connect(self.update_logger_level)
        self.ErrorCheck.clicked.connect(self.update_logger_level)

        self.__setup_plot()
        # Qt timer set-up for updating the plots.
        self.__plot_update = QTimer()
        self.__plot_update.timeout.connect(self.__update_plot)
        # Measurement engine
        self.m_engine = measurement_engine.MeasurementEngine(threaded=False)

        # plot layout set-up.
        self.figure = plt.figure()
        self.figure.patch.set_alpha(0)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavTbar(self.canvas, self)
        self.plot_control.addWidget(self.toolbar)
        spacer1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
        self.plot_control.addItem(spacer1)
        self.plot.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(top=0.9, bottom=0.1, left=0.13, right=0.95)
        self.ax.grid()
        self.ax.set_ylabel("F(Hz)", rotation='horizontal')
        self.ax.yaxis.set_label_coords(-0.01, 1.04)

        # Plot data
        # list of InstrumentData
        self.data = []
        # list (channel) of lists (signal)
        self.cboxes = [[], []]
        self.sample_counter = 0

    def __setup_menu(self):
        # File
        # TODO [floonone-20170906] file actions
        # Tools
        self.device_manager.triggered.connect(self.__open_device_manager)
        self.fpga_calibration.triggered.connect(self.__open_calibration_window)
        # Help
        # TODO [floonone-20170906] help actions
        return

    def __open_device_manager(self):
        logger.debug("Opening Device Manager pop-up window")
        self.popup = device_manager.DevManagerWindow()
        self.popup.exec_()
        self.popup = None
        for slot in range(2):
            self.updateDevCombobox(self.DevComboBox[slot])
        logger.info("Updated devices list")
        return

    def __open_calibration_window(self):
        logger.debug("Opening FPGA device Calibration pop-up window")
        self.popup = calibration.CalibWindow()
        self.popup.exec_()
        self.popup = None
        return

    def __setup_device_controls(self):
        self.__fill_device_selectors()
        self.__setup_signal_channel_controls()
        self.__setup_device_control_button()

    def __fill_device_selectors(self):
        devices_list = [os.path.basename(match)[:-4]
                        for match in glob.glob('resources/devices/*yml')]
        device_selectors = self.findChildren(
                QtWidgets.QComboBox, QRegularExpression("\\d_selector"))
        for selector in device_selectors:
            selector.clear()
            selector.addItems(devices_list)
        return

    def __setup_signal_channel_controls(self):
        channel_controls = self.findChildren(
                QtWidgets.QRadioButton,
                QRegularExpression("device\\d_channel\\d"))
        for control in channel_controls:
            policy = control.sizePolicy()
            policy.setRetainSizeWhenHidden(True)
            control.setSizePolicy(policy)
            control.setEnabled(False)
            control.setVisible(False)

        signal_controls = self.findChildren(
                QtWidgets.QCheckBox,
                QRegularExpression("device\\d_signal\\d"))
        for control in signal_controls:
            policy = control.sizePolicy()
            policy.setRetainSizeWhenHidden(True)
            control.setSizePolicy(policy)
            control.setEnabled(False)
            control.setVisible(False)

    def __setup_device_control_button(self):
        device_connects = self.findChildren(
                QtWidgets.QPushButton, QRegularExpression("\\d_connect"))
        for i, connect in enumerate(device_connects):
            connect.pressed.connect(
                    lambda slot=i: self.__on_device_control_button_press(slot))
        return

    def __on_device_control_button_press(self, slot):
        device_group = self.findChild(QtWidgets.QGroupBox,
                                      "device{}".format(slot))
        if device_group.property("name"):
            self.__disconnect_device(slot)
        else:
            self.__connect_device(slot)

    def __connect_device(self, slot):
        device_group = self.findChild(QtWidgets.QGroupBox,
                                      "device{}".format(slot))
        name = device_group.findChild(QtWidgets.QComboBox).currentText()
        # Check rest of slots to see if device is already loaded
        checks = [checked for checked in filter(
                lambda child: child.property("name") == name,
                self.findChildren(QtWidgets.QGroupBox,
                                  QRegularExpression("device\\d$")))]
        if len(checks):
            logger.warning("Device {} is already selected in the other slot"
                           "".format(name))
            return False
        # FIXME [floonone-20170906] path join
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

        # Add device to the list of available devices to do measurements
        self.__devices[slot] = new_device

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
        channels = new_device.get_channels()
        # FIXME [floonone-20170906] don't use static method
        for i in range(channels):
            channel_controls[i].setEnabled(True)
            channel_controls[i].setVisible(True)
        for i in range(channels, 4):
            channel_controls[i].setEnabled(False)
            channel_controls[i].setVisible(False)
        # Select the first channel by default
        channel_controls[0].setChecked(True)
        # Show available signals
        signal_controls = [signal for signal in device_group.findChildren(
                QtWidgets.QCheckBox)]
        signals = new_device.get_signals()
        # FIXME [floonone-20170906] don't use static method
        for i in range(len(signals)):
            signal_controls[i].setText(signals[i])
            signal_controls[i].setEnabled(True)
            signal_controls[i].setVisible(True)
        for i in range(len(signals), 4):
            signal_controls[i].setText("")
            signal_controls[i].setEnabled(False)
            signal_controls[i].setVisible(False)

        device_group.setProperty("name", name)
        return

    def __disconnect_device(self, slot):
        device_group = self.findChild(QtWidgets.QGroupBox,
                                      "device{}".format(slot))
        # Remove device from the list of available devices
        del self.__devices[slot]
        # Change the button text to Connect
        device_group.findChild(QtWidgets.QPushButton).setText("Connect")
        # Enable selector
        device_group.findChild(QtWidgets.QComboBox).setEnabled(True)
        # Disable signal and channel controls
        for control in device_group.findChildren(QtWidgets.QGroupBox):
            control.setEnabled(False)
        channel_controls = [channel for channel in device_group.findChildren(
                QtWidgets.QRadioButton)]
        for control in channel_controls:
            control.setChecked(False)
            control.setEnabled(False)
            control.setVisible(False)
        signal_controls = [signal for signal in device_group.findChildren(
                QtWidgets.QCheckBox)]
        for control in signal_controls:
            control.setChecked(False)
            control.setEnabled(False)
            control.setVisible(False)
            control.setText("")

        logger.info("Disconnected from device {}".format(
                device_group.property("name")))

        device_group.setProperty("name", None)
        return

    def __setup_plot(self):
        self.start.pressed.connect(self.__start_plot)
        self.stop.pressed.connect(self.__stop_plot)
        # TODO [floonone-20170907] save button
        self.save.setEnabled(False)

    def __start_plot(self):
        # Block controls
        self.start.setEnabled(False)
        self.stop.setEnabled(True)
        self.save.setEnabled(False)
        self.measurement_configuration.setEnabled(False)

        for i, device in enumerate(self.findChildren(
                QtWidgets.QGroupBox, QRegularExpression("device\\d$"))):
            device.findChild(QtWidgets.QComboBox).setEnabled(False)
            device.findChild(QtWidgets.QPushButton).setEnabled(False)
            device.findChild(QtWidgets.QGroupBox,
                             "device{}_channels".format(i)).setEnabled(False)

        fetch_time = self.fetch_time.value()
        sample_time = self.fetch_time.value()
        plot_time = min(500, fetch_time*1000)
        # Start the measurement engine
        self.m_engine.start(self.__devices.values(), fetch_time, sample_time)
        logger.debug("Measurement started")

        # Start the timer to update plots
        self.__plot_update.start(plot_time)
        logger.debug("Plotting started")
        return

    def __stop_plot(self):
        self.m_engine.stop()
        logger.debug("Measurement stopped")
        self.__plot_update.stop()
        logger.debug("Plotting stopped")

        # Unlock controls
        self.start.setEnabled(True)
        self.stop.setEnabled(False)
        self.save.setEnabled(True)
        self.measurement_configuration.setEnabled(True)

        for i, device in enumerate(self.findChildren(
                QtWidgets.QGroupBox, QRegularExpression("device\\d$"))):
            device.findChild(QtWidgets.QPushButton).setEnabled(True)
            device.findChild(QtWidgets.QGroupBox,
                             "device{}_channels".format(i)).setEnabled(True)
            if not device.property("name"):
                device.findChild(QtWidgets.QComboBox).setEnabled(True)

    def __update_plot(self):
        # Clear plot
        self.ax.cla()
        self.ax.grid()
        self.ax.set_ylabel("F(Hz)", rotation='horizontal')
        self.ax.yaxis.set_label_coords(-0.01, 1.04)
        # Remove exponential notation in y axis
        self.ax.get_yaxis().get_major_formatter().set_useOffset(False)
        measurement_size = 0
        for i, device in self.__devices.items():
            measurements = device.get_measurement_data()
            device_control = self.findChild(
                    QtWidgets.QGroupBox, "device{}".format(i))
            name = device_control.property("name")
            selected_channel = None
            for j, channel in enumerate(device_control.findChildren(
                    QtWidgets.QRadioButton)):
                if channel.isChecked():
                    selected_channel = j
            channel_measurements = measurements[selected_channel]
            for signal in filter(
                    lambda x: x.isChecked(),
                    device_control.findChildren(QtWidgets.QCheckBox)):
                signal_values = [measurement[signal.text()]
                    for measurement in channel_measurements.values()]
                # Draw the plot
                self.ax.plot(signal_values, label="{} Ch-{} {}".format(
                        name, selected_channel+1, signal.text()))

        if self.autoscroll.isChecked() and measurement_size > 100:
            self.ax.set_xlim(measurement_size - 100, measurement_size)

        # Print legends in the plot
        plt.legend(bbox_to_anchor=(0., 1.02, 1., 0.102), loc=0, ncol=3,
                   mode="expand", borderaxespad=0., fontsize='xx-small')

        self.canvas.draw()
        return

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
