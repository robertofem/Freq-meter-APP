#!/usr/bin/env python3
"""Calibration Window"""
# Standard libraries
import glob
import logging
import os
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import math
import statistics
# Third party libraries
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QRegularExpression, QTimer
# Local libraries
from view import calibration_interface
from view import freqmeterdevice
from view import measurement_engine

logger = logging.getLogger('view')


class CalibWindow(QtWidgets.QDialog, calibration_interface.Ui_CalibWindow):
    """
    Class for defining the behaviour of the Device Manager Interface.
    """
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

        # Connect/Disconnect buttons
        self.target_device_connect.pressed.connect(
                lambda dev_type="target":
                self.__on_device_control_button_press(dev_type))
        self.reference_device_connect.pressed.connect(
                lambda dev_type="reference":
                self.__on_device_control_button_press(dev_type))
        # Measurement selector buttons
        self.__setup_measurement_selectors()

        # Start and Stop Buttons events
        self.button_start_coarse.clicked.connect(self.__start_coarse)
        self.button_stop_coarse.clicked.connect(self.__stop_coarse)
        self.button_start_fine.clicked.connect(self.__start_fine)
        self.button_stop_fine.clicked.connect(self.__stop_fine)

        # Button box events (accept/reject)
        self.buttonBox.clicked.connect(self.__handle_buttonBox_click)

        #Save in file Button event
        self.button_save_fine.clicked.connect(self.__save_fine)

        # Qt timer set-up for updating the plots.
        self.__plot_update = QTimer()
        # Measurement engine
        self.m_engine = measurement_engine.MeasurementEngine(threaded=False)

        # Initialize coarse calibration plots
        self.figure_coarse = plt.figure(figsize=(4.5, 3))
        self.figure_coarse.patch.set_alpha(0)
        self.canvas_coarse = FigureCanvas(self.figure_coarse)
        self.plotVLayout_coarse.addWidget(self.canvas_coarse)
        self.ax_coarse = self.figure_coarse.add_subplot(111)
        self.figure_coarse.subplots_adjust(top=0.65, bottom=0.10, left=0.1)
        self.ax_coarse.grid()
        self.ax_coarse.set_ylabel("F(Hz)", rotation= 'horizontal')
        self.ax_coarse.yaxis.set_label_coords(-0.05, 1.04)

        # Initialize fine calibration plots
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

        # populate target (to be calibrated) listbox with only FPGA freq meters
        self.__populate_target_combobox()
        # populate list with reference devices with all devices
        self.__populate_reference_combobox()

        #clean message labels
        self.label_coarse_mess.setText("")
        self.label_fine_mess.setText("")

        # create devices for target and reference
        self.target_device = None
        self.reference_device = None

        # define parameters to stop coarse calibration
        # define the resolution of the target device at 1MHz
        self.res_1MHz = 0.01 #Hz
        # define the number of measurements to calculate coarse calibration
        self.min_meas_coarse_calib = 10

    def __setup_measurement_selectors(self):
        channel_controls = self.findChildren(
                QtWidgets.QRadioButton,
                QRegularExpression("device_channel\\d"))
        for control in channel_controls:
            policy = control.sizePolicy()
            policy.setRetainSizeWhenHidden(True)
            control.setSizePolicy(policy)
            control.setEnabled(False)
            control.setVisible(False)

        impedance_controls = self.findChildren(
                QtWidgets.QRadioButton,
                QRegularExpression("device_impedance\\d"))
        for control in impedance_controls:
            policy = control.sizePolicy()
            policy.setRetainSizeWhenHidden(True)
            control.setSizePolicy(policy)
            control.setEnabled(False)
            control.setVisible(False)

    def __populate_target_combobox(self):
        # clear the combobox
        self.target_device_selector.clear()
        # open all files and add devices which vendor is "Uvigo"
        device_names_list = [os.path.basename(match)[:-4]
                             for match in glob.glob('resources/devices/*yml')]
        for device_name in device_names_list:
            dev_dir = "{}/resources/devices/".format(os.getcwd())
            dev_path = "{}{}.yml".format(dev_dir, device_name)
            new_device = freqmeterdevice.FreqMeter.get_freq_meter(dev_path)
            if new_device.get_vendor_name() == "Uvigo":
                self.target_device_selector.addItem(device_name)
        return

    def __populate_reference_combobox(self):
        # clear the combobox
        self.reference_device_selector.clear()
        # add all devices
        device_names_list = [os.path.basename(match)[:-4]
                             for match in glob.glob('resources/devices/*yml')]
        self.reference_device_selector.addItems(device_names_list)
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

    def __on_device_control_button_press(self, device):
        device_group = self.findChild(QtWidgets.QGroupBox,
                                      "{}_device_group".format(device))
        if device_group.property("name"):
            self.__disconnect_device(device)
        else:
            self.__connect_device(device)

    def __connect_device(self, device):
        device_group = self.findChild(QtWidgets.QGroupBox,
                                      "{}_device_group".format(device))
        name = device_group.findChild(QtWidgets.QComboBox).currentText()

        # check if the other device is the same and it is connected
        if device == "reference":
            other_device_group = self.target_device_group
        else:
            other_device_group = self.reference_device_group
        if name == other_device_group.property("name"):
            logger.warning("This device is already connected")
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
        if device == "reference":
            self.reference_device = new_device
        else:
            self.target_device = new_device

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

        device_group.setProperty("name", name)
        return

    def __disconnect_device(self, device):
        device_group = self.findChild(QtWidgets.QGroupBox,
                                      "{}_device_group".format(device))
        # Change the button text to Connect
        device_group.findChild(QtWidgets.QPushButton).setText("Connect")
        # Enable selector
        device_group.findChild(QtWidgets.QComboBox).setEnabled(True)
        # Disable signal and channel controls
        for control in device_group.findChildren(QtWidgets.QGroupBox):
            control.setEnabled(False)
        channel_controls = [
            channel for channel in device_group.findChildren(
                QtWidgets.QRadioButton,
                QRegularExpression("channel\\d"))]
        for control in channel_controls:
            control.setChecked(False)
            control.setEnabled(False)
            control.setVisible(False)
        impedance_controls = [
            impedance for impedance in device_group.findChildren(
                    QtWidgets.QRadioButton,
                    QRegularExpression("impedance\\d"))]
        for control in impedance_controls:
            control.setChecked(False)
            control.setEnabled(False)
            control.setVisible(False)

        logger.info("Disconnected from device {}".format(
                device_group.property("name")))

        device_group.setProperty("name", None)

        if device == "reference":
            self.reference_device.disconnect()
        else:
            self.target_device.disconnect()
        return

    def __start_coarse(self):
        """
        Start coarse calibration.
        """
        #Check that target and reference are connected
        if self.target_device == None or self.reference_device == None:
            logger.warning("Connect devices before start coarse calibration")
            return
        if (not self.target_device.is_connected() or not
        self.reference_device.is_connected()):
            logger.warning("Connect devices before start coarse calibration")
            return

        # Get general measuring parameters
        fetch_time = 1 #seconds
        sample_time = 1 #seconds
        plot_time = min(500, fetch_time*1000)

        #Initialize calibration variables
        self.M = 1.0 #uncalibrated value
        self.coarse_finished_correct  = 0

        #send the M to make the device uncalibrated
        self.target_device.coarse_calibration(self.M)

        # Block controls
        self.button_start_coarse.setEnabled(False)
        self.button_stop_coarse.setEnabled(True)
        self.button_start_fine.setEnabled(False)
        self.button_stop_fine.setEnabled(False)

        for dev_type in ["target", "reference"]:
            device_group = self.findChild(QtWidgets.QGroupBox,
                    "{}_device_group".format(dev_type))
            device_group.findChild(QtWidgets.QComboBox).setEnabled(False)
            device_group.findChild(QtWidgets.QPushButton).setEnabled(False)
            device_group.findChild(QtWidgets.QGroupBox,
                    "{}_device_channels".format(dev_type)).setEnabled(False)
            device_group.findChild(QtWidgets.QGroupBox,
                    "{}_device_impedances".format(dev_type)).setEnabled(False)

        #connect the timer to the coarse update
        self.__plot_update.timeout.connect(self.__update_coarse)

        # Start devices measurement
        for dev_type in ["target", "reference"]:
            # Obtain selected channel
            channel_controls = self.findChild(
                QtWidgets.QGroupBox, "{}_device_channels".format(dev_type))
            channel_controls = channel_controls.findChildren(
                QtWidgets.QRadioButton)
            selected_channel = [c for c in filter(
                lambda c: c.isChecked(), channel_controls)][0]
            chan = int(selected_channel.text()) - 1
            # Obtain selected impedance
            impedance_controls = self.findChild(
                QtWidgets.QGroupBox, "{}_device_impedances".format(dev_type))
            impedance_controls = impedance_controls.findChildren(
                QtWidgets.QRadioButton)
            selected_impedance = [c for c in filter(
                lambda c: c.isChecked(), impedance_controls)][0]
            imp = selected_impedance.text()
            # Start measurement
            if dev_type == "target":
                self.target_device.start_measurement(sample_time, chan, imp)
            else:
                self.reference_device.start_measurement(sample_time, chan, imp)

        # Start the measurement engine
        self.m_engine.start([self.target_device, self.reference_device],
        fetch_time)
        logger.debug("Measurement started")

        #Inform the user
        self.label_coarse_mess.setText("Coarse calibration started.")
        self.label_coarse_mess.setStyleSheet('color: black')
        logger.info("Coarse calibration started.")

        # Start the timer to update plots
        self.__plot_update.start(plot_time)
        logger.debug("Plotting started")
        return

    def __stop_coarse(self):
        """
        Stop coarse calibration.
        """
        self.m_engine.stop()
        logger.debug("Measurement stopped")
        self.__plot_update.stop()
        logger.debug("Plotting stopped")

        # Re-anable controls
        self.button_start_coarse.setEnabled(True)
        self.button_stop_coarse.setEnabled(False)
        self.button_start_fine.setEnabled(True)
        self.button_stop_fine.setEnabled(False)

        for dev_type in ["target", "reference"]:
            device_group = self.findChild(QtWidgets.QGroupBox,
                    "{}_device_group".format(dev_type))
            device_group.findChild(QtWidgets.QComboBox).setEnabled(True)
            device_group.findChild(QtWidgets.QPushButton).setEnabled(True)
            device_group.findChild(QtWidgets.QGroupBox,
                    "{}_device_channels".format(dev_type)).setEnabled(True)
            device_group.findChild(QtWidgets.QGroupBox,
                    "{}_device_impedances".format(dev_type)).setEnabled(True)

        #Inform the user if the calibration succeded
        if (self.coarse_finished_correct == 0):
            self.label_coarse_mess.setText(
            "Coarse calibration failed. {} is now uncalibrated.".format(
                self.target_device_selector.currentText()))
            self.label_coarse_mess.setStyleSheet('color: red')
            logger.info(
                "Coarse calibration failed. {} is now uncalibrated.".format(
                self.target_device_selector.currentText()))
        else:
            self.label_coarse_mess.setText(
                "Coarse calibration finished succesfully on {}.".format(
                self.target_device_selector.currentText()))
            self.label_coarse_mess.setStyleSheet('color: green')
            logger.info(
                "Coarse calibration finished succesfully on {}.".format(
                self.target_device_selector.currentText()))

    def __update_coarse(self):
        # Clear plot
        self.ax_coarse.cla()
        self.ax_coarse.grid()
        self.ax_coarse.set_ylabel("F(Hz)", rotation='horizontal')
        self.ax_coarse.yaxis.set_label_coords(-0.05, 1.04)
        # Remove exponential notation in y axis
        self.ax_coarse.get_yaxis().get_major_formatter().set_useOffset(False)

        #get measurements from devices
        target_data = self.target_device.get_measurement_data()
        reference_data = self.reference_device.get_measurement_data()

        #for the target select the coarse signal and plot
        for j, channel in enumerate(self.target_device_channels.findChildren(
                QtWidgets.QRadioButton)):
            if channel.isChecked():
                selected_channel = j
        channel_measurements = target_data[selected_channel]
        target_f = [measurement["coarse"]
            for measurement in channel_measurements.values()]
        self.ax_coarse.plot(target_f, label="Target: {} Ch-{}".format(
            self.target_device_selector.currentText(), selected_channel+1))

        #for the reference select the first (it doesnt matter coarse or fine)
        for j, channel in enumerate(self.reference_device_channels.findChildren(
                QtWidgets.QRadioButton)):
            if channel.isChecked():
                selected_channel = j
        channel_measurements = reference_data[selected_channel]
        reference_f = [measurement[self.reference_device.get_signals()[0]]
            for measurement in channel_measurements.values()]
        self.ax_coarse.plot(reference_f, label="Reference: {} Ch-{}".format(
            self.target_device_selector.currentText(), selected_channel+1))

        # Print legends in the plot
        handles, labels = self.ax_coarse.get_legend_handles_labels()
        plt.legend()

        self.canvas_coarse.draw()

        #calculate M
        mean_target_f = 0.0
        mean_reference_f = 0.0
        for i in range(len(target_f)):
            mean_target_f = mean_target_f + target_f[i]
            mean_reference_f = mean_reference_f + reference_f[i]
        if mean_target_f > 0.0:
            self.M = mean_reference_f/mean_target_f
            self.label_calib_const.setText("Coarse calibration constant(M)={}"
                .format(self.M))

        #check if the value of M is already correct and stop
        if len(target_f) > self.min_meas_coarse_calib:
            #calculate the standard deviation of the last target measurements
            standard_dev = statistics.pstdev(target_f[-self.min_meas_coarse_calib:])
            self.label_calib_const.setText(self.label_calib_const.text() + " (std dev ={})"
                .format(standard_dev))
            #if standard deviation smaller than resolution the source freq
            #was stable enough to produce a correct value of M
            if standard_dev < self.res_1MHz:
                self.coarse_finished_correct = 1
                #calibrate the device
                self.target_device.coarse_calibration(self.M)
                #stop the calibration process
                self.__stop_coarse()
        return

    def __start_fine(self):
        """
        Start fine calibration.
        """
        #Check that target and reference are connected
        if self.target_device == None:
            logger.warning("Connect devices before start fine calibration")
            return
        if (not self.target_device.is_connected()):
            logger.warning("Connect devices before start fine calibration")
            return

        #read the number of measurements to perform the cdt
        n_meas_fine_text = self.lineEditFineMeas.text()
        if (not n_meas_fine_text.isdigit()):
            logger.warning("Write an integer in Number of measurmenets for CDT")
            return
        self.n_meas_fine = int(n_meas_fine_text);

        #Initialize variables related with the fine calibration
        self.fine_finished_correct  = 0

        # Block controls
        self.button_start_coarse.setEnabled(False)
        self.button_stop_coarse.setEnabled(False)
        self.button_start_fine.setEnabled(False)
        self.button_stop_fine.setEnabled(True)
        self.button_save_fine.setEnabled(False)

        for dev_type in ["target", "reference"]:
            device_group = self.findChild(QtWidgets.QGroupBox,
                    "{}_device_group".format(dev_type))
            device_group.findChild(QtWidgets.QComboBox).setEnabled(False)
            device_group.findChild(QtWidgets.QPushButton).setEnabled(False)
            device_group.findChild(QtWidgets.QGroupBox,
                    "{}_device_channels".format(dev_type)).setEnabled(False)
            device_group.findChild(QtWidgets.QGroupBox,
                    "{}_device_impedances".format(dev_type)).setEnabled(False)


        #connect the timer to the fine update function
        self.__plot_update.timeout.connect(self.__update_fine)

        # Obtain selected channel
        channel_controls = self.findChild(
            QtWidgets.QGroupBox, "target_device_channels")
        channel_controls = channel_controls.findChildren(
            QtWidgets.QRadioButton)
        selected_channel = [c for c in filter(
            lambda c: c.isChecked(), channel_controls)][0]
        chan = int(selected_channel.text()) - 1

        #start code density test (CDT) gate time 1ms
        self.target_device.cdt_start(0.001, self.n_meas_fine, chan)

        #Inform the user
        self.label_fine_mess.setText("Fine calibration started.")
        self.label_fine_mess.setStyleSheet('color: black')
        logger.info("Fine calibration started.")

        # Start the timer to update plots
        self.__plot_update.start(2000) #2 seconds
        return

    def __stop_fine(self):
        """
        Stop fine calibration.
        """
        logger.debug("Fine calibration stopped")

        #Stop the timer that calls update
        self.__plot_update.stop()

        # Re-anable controls
        self.button_start_coarse.setEnabled(True)
        self.button_stop_coarse.setEnabled(False)
        self.button_start_fine.setEnabled(True)
        self.button_stop_fine.setEnabled(False)
        if (self.fine_finished_correct == 1):
            self.button_save_fine.setEnabled(True)

        for dev_type in ["target", "reference"]:
            device_group = self.findChild(QtWidgets.QGroupBox,
                    "{}_device_group".format(dev_type))
            device_group.findChild(QtWidgets.QComboBox).setEnabled(True)
            device_group.findChild(QtWidgets.QPushButton).setEnabled(True)
            device_group.findChild(QtWidgets.QGroupBox,
                    "{}_device_channels".format(dev_type)).setEnabled(True)
            device_group.findChild(QtWidgets.QGroupBox,
                    "{}_device_impedances".format(dev_type)).setEnabled(True)

        #Inform the user if the calibration succeded
        if (self.fine_finished_correct == 0):
            self.label_fine_mess.setText(
            "Fine calibration failed. {} is now uncalibrated.".format(
                self.target_device_selector.currentText()))
            self.label_fine_mess.setStyleSheet('color: red')
            logger.info(
                "Fine calibration failed. {} is now uncalibrated.".format(
                self.target_device_selector.currentText()))
        else:
            self.label_fine_mess.setText(
                "Fine calibration finished succesfully on {}.".format(
                self.target_device_selector.currentText()))
            self.label_fine_mess.setStyleSheet('color: green')
            logger.info(
                "Fine calibration finished succesfully on {}.".format(
                self.target_device_selector.currentText()))

        #Paint the results
        if (self.fine_finished_correct == 1):
            #Read CDT,DNL and INL from device
            values = self.target_device.cdt_get_values()

            #Clear plots
            for plot in [self.ax_fine_cdt, self.ax_fine_dnl, self.ax_fine_inl]:
                plot.cla()
                plot.grid()
                plot.yaxis.set_label_coords(-0.05, 1.04)
                # Remove exponential notation in y axis
                plot.get_yaxis().get_major_formatter().set_useOffset(False)
            self.ax_fine_cdt.set_ylabel("CDT", rotation='horizontal')
            self.ax_fine_dnl.set_ylabel("DNL", rotation='horizontal')
            self.ax_fine_inl.set_ylabel("INL", rotation='horizontal')

            # Obtain selected channel
            channel_controls = self.findChild(
                QtWidgets.QGroupBox, "target_device_channels")
            channel_controls = channel_controls.findChildren(
                QtWidgets.QRadioButton)
            selected_channel = [c for c in filter(
                lambda c: c.isChecked(), channel_controls)][0]
            chan = int(selected_channel.text()) - 1

            #plot CDT
            self.ax_fine_cdt.plot(values['cdt'], label="Target: {} Ch-{} CDT".format(
                self.target_device_selector.currentText(), chan+1))
            #plot DNL
            self.ax_fine_dnl.plot(values['dnl'], label="Target: {} Ch-{} DNL".format(
                self.target_device_selector.currentText(), chan+1))
            #plot INL
            self.ax_fine_inl.plot(values['inl'], label="Target: {} Ch-{} INL".format(
                self.target_device_selector.currentText(), chan+1))
            self.canvas_fine.draw()

            #save data in vectors so it can be later saved into file
            self.cdt = values['cdt']
            self.dnl = values['dnl']
            self.inl = values['inl']

    def __update_fine(self):
        #ask the fmeter if the CDT has already finished
        status = self.target_device.cdt_end()

        if status["end"]:
            self.fine_finished_correct = 1;
            self.__stop_fine()
        elif status["error"]:
            self.__stop_fine()
        else:
            self.label_fine_mess.setText("CDT will end in {}min {}s".format(
            status["time_left"]["minutes"],
            status["time_left"]["seconds"]
        ))
        return

    def __save_fine(self):
        #Create file header
        file_header="Code density test results\n"
        file_header+="Device: {}\n".format(self.target_device_selector.currentText())
        file_header+="\nCDT\tDNL\tINL\n"

        # Build measurement rows
        data_lines = [file_header]
        for i in range(len(self.cdt)):
            measurement=""
            measurement += str(self.cdt[i])
            measurement += "\t"
            measurement += str(self.dnl[i])
            measurement += "\t"
            measurement += str(self.inl[i])
            data_lines.append(measurement)

        # Obtain file to save the data
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", "")[0]
        if not file:
            logger.warning("No file selected")
            return
        with open(file, "w") as openfile:
            openfile.writelines("{}\n".format(l) for l in data_lines)
