#!/usr/bin/env python3
"""Device manager"""
# Standard libraries
import glob
import os
import yaml
# Third party libraries
from PyQt5 import QtGui, QtCore, QtWidgets
# Local libraries
from view import device_interface
from view import freqmeterdevice


class DevManagerWindow(QtWidgets.QDialog, device_interface.Ui_DevManagerWindow):
    """
    Class for defining the behaviour of the Device Manager Interface.
    """
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.__signal_number_labels = [self.S1label, self.S2label,
                                       self.S3label, self.S4label]
        self.__signal_type_labels = [self.signal1_type, self.signal2_type,
                                     self.signal3_type, self.signal4_type]
        # Vendor change event
        self.VendorSelector.currentIndexChanged.connect(self.__on_vendor_change)
        # Protocol change event
        self.CommProtocolBox.currentIndexChanged.connect(
                self.__on_protocol_change)
        # Read only impedance checkboxes
        self.impedance_50.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.impedance_1m.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        # Fill vendor combo
        self.__fill_vendor_selector()
        # Button box events (accept/reject)
        self.buttonBox.clicked.connect(self.handle_buttonBox_click)

    def __fill_vendor_selector(self):
        self.VendorSelector.addItems(
                sorted(freqmeterdevice.FreqMeter.get_vendors().keys()))

    def __on_vendor_change(self):
        # Obtain vendor data
        vendor_data = freqmeterdevice.FreqMeter.get_vendors()[
            self.VendorSelector.currentText()]
        # Set channel number
        self.channel_number.setText(str(vendor_data["channels"]))
        # Set signal number
        signal_number = len(vendor_data["signals"])
        self.signal_number.setText(str(signal_number))
        # Set signal types
        for i in range(signal_number):
            self.__signal_number_labels[i].setVisible(True)
            self.__signal_type_labels[i].setText(vendor_data["signals"][i])
            self.__signal_type_labels[i].setVisible(True)
        for i in range(signal_number, 4):
            self.__signal_number_labels[i].setVisible(False)
            self.__signal_type_labels[i].setVisible(False)
        # Set impedances
        if "50" in vendor_data["impedances"]:
            self.impedance_50.setChecked(True)
        else:
            self.impedance_50.setChecked(False)
        if "1M" in vendor_data["impedances"]:
            self.impedance_1m.setChecked(True)
        else:
            self.impedance_1m.setChecked(False)
        # Set protocol options
        self.CommProtocolBox.clear()
        self.CommProtocolBox.addItems(sorted(vendor_data["protocols"]))

    def handle_buttonBox_click(self, button):
        """
        Check which button was pressed and perform corresponding action.
        """
        clicked_button = self.buttonBox.standardButton(button)
        if clicked_button == QtWidgets.QDialogButtonBox.Save:
            self.save_device()
        elif clicked_button == QtWidgets.QDialogButtonBox.Open:
            self.open_device()
        elif clicked_button == QtWidgets.QDialogButtonBox.Cancel:
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

    def open_device(self):
        """
        Open a Qt file dialog and load a .yml configuration

        After loading the configuration, it is shown in the user
        interface, allowing the user to watch and modify it.
        """
        path = "{}/resources/devices/".format(os.getcwd())
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', path)[0]
        # If cancel button is pressed, return from function.
        if file == "":
            return
        # Open the specified file and parse it with yaml.
        with open(file, 'r') as conf_file:
            try:
                dev_data = yaml.load(conf_file)
            except yaml.parser.ParserError:
                err_text = "<font color='red'>Can open only 'YML' files!</font>"
                self.ErrorLabel.setText(err_text)
                return
        # Load general properties to interface.
        self.DevNameText.setText(dev_data['general']['Name'])
        v_index = self.VendorSelector.findText(dev_data['Vendor'])
        self.VendorSelector.setCurrentIndex(v_index)
        self.DevModelText.setText(dev_data['general']['Model'])
        self.DevSerialNText.setText(dev_data['general']['Serial_N'])
        self.DevFirmVersionText.setText(dev_data['general']['FirmVersion'])
        # Load channel properties to interface.
        self.NChannelsBox.setValue(int(dev_data['channels']['Quantity']))
        self.NSignalsBox.setValue(int(dev_data['channels']['Signals']))
        indx1 = self.S1comboBox.findText(dev_data['channels']['SigTypes']['S1'])
        indx2 = self.S2comboBox.findText(dev_data['channels']['SigTypes']['S2'])
        indx3 = self.S3comboBox.findText(dev_data['channels']['SigTypes']['S3'])
        indx4 = self.S4comboBox.findText(dev_data['channels']['SigTypes']['S4'])
        self.S1comboBox.setCurrentIndex(indx1)
        self.S2comboBox.setCurrentIndex(indx2)
        self.S3comboBox.setCurrentIndex(indx3)
        self.S4comboBox.setCurrentIndex(indx4)
        # Load communication properties to interface.
        c_index = self.CommProtocolBox.findText(dev_data['communications']
                                                        ['Protocol'])
        self.CommProtocolBox.setCurrentIndex(c_index)
        self.CommText_1.setText(dev_data['communications']
                                        ['Properties']['CommProp1'])
        self.CommText_2.setText(dev_data['communications']
                                        ['Properties']['CommProp2'])
        self.CommText_3.setText(dev_data['communications']
                                        ['Properties']['CommProp3'])
        self.CommText_4.setText(dev_data['communications']
                                        ['Properties']['CommProp4'])
        # Load impedance properties to interface.
        self.Ohm50checkBox.setChecked(dev_data['impedance']['R50Ohm'] == 'True')
        self.MegaOhmcheckBox.setChecked(dev_data['impedance']['R1MOhm']
                                        == 'True')
        return

    def save_device(self):
        """Read the whole form and save data to yaml file."""
        # Check that device name is not empty.
        dev_name = self.DevNameText.text()
        if dev_name == "":
            err_text = "<font color='red'>'Name' field cannot be empty!</font>"
            self.ErrorLabel.setText(err_text)
            return
        # Check that at least one impedance configuration is checked.
        elif (not self.Ohm50checkBox.isChecked()
                and not self.MegaOhmcheckBox.isChecked()):
            err_text = ("<font color='red'>At least one impedance"
                        " must be selected!</font>")
            self.ErrorLabel.setText(err_text)
            return
        # Check if the device already exists and ask user for overwriting it.
        elif glob.glob("resources/devices/{}.yml".format(dev_name)):
            question = ("It already exists a device configuration with the name"
                        " {}. Do you want to overwrite it?".format(dev_name))
            reply = QtWidgets.QMessageBox.question(self, 'Message', question,
                                                   QtWidgets.QMessageBox.Yes,
                                                   QtWidgets.QMessageBox.No)
            err_text = ""
            self.ErrorLabel.setText(err_text)
            if reply == QtWidgets.QMessageBox.No:
                return
        else:
            err_text = ""
        self.ErrorLabel.setText(err_text)
        # Construct a dictionary with the whole form information.
        dev_data = dict(
            general=dict(
                Name=str(self.DevNameText.text()),
                Vendor=str(self.VendorSelector.currentText()),
                Model=str(self.DevModelText.text()),
                Serial_N=str(self.DevSerialNText.text()),
                FirmVersion=str(self.DevFirmVersionText.text()),
                ),
            communications=dict(
                Protocol=str(self.CommProtocolBox.currentText()),
                Properties=dict(
                    CommProp1=str(self.CommText_1.text()),
                    CommProp2=str(self.CommText_2.text()),
                    CommProp3=str(self.CommText_3.text()),
                    CommProp4=str(self.CommText_4.text()),
                    ),
                ),
            channels=dict(
                Quantity=str(self.NChannelsBox.value()),
                Signals=str(self.NSignalsBox.value()),
                SigTypes=dict(
                    S1=str(self.S1comboBox.currentText()),
                    S2=str(self.S2comboBox.currentText()),
                    S3=str(self.S3comboBox.currentText()),
                    S4=str(self.S4comboBox.currentText()),
                    ),
                ),
            impedance=dict(
                R50Ohm=str(self.Ohm50checkBox.isChecked()),
                R1MOhm=str(self.MegaOhmcheckBox.isChecked()),
                ),
            )
        # If the file already exists, remove and create it again with the
        # form data.
        try:
            os.remove('resources/devices/{}.yml'.format(dev_name))
        except FileNotFoundError:
            pass
        with open('resources/devices/{}.yml'.format(self.DevNameText.text()),
                  'w') as outfile:
            yaml.dump(dev_data, outfile, default_flow_style=False)
        self.close()
        return

    def __on_protocol_change(self):
        """
        Update the communication labels/boxes texts and visible status.
        """
        if self.CommProtocolBox.currentText() == "TCP/IP":
            self.CommPropertiesgroupBox.setVisible(True)
            # Property 1 settings.
            self.CommLabel_1.setVisible(True)
            self.CommLabel_1.setText("IP:")
            self.CommText_1.setVisible(True)
            # Property 2 settings.
            self.CommLabel_2.setVisible(True)
            self.CommLabel_2.setText("Port:")
            self.CommText_2.setVisible(True)
            # Property 3 settings.
            self.CommLabel_3.setVisible(False)
            self.CommText_3.setVisible(False)
            # Property 4 settings.
            self.CommLabel_4.setVisible(False)
            self.CommText_4.setVisible(False)
        elif self.CommProtocolBox.currentText() == "Serial":
            self.CommPropertiesgroupBox.setVisible(True)
            # Property 1 settings.
            self.CommLabel_1.setVisible(True)
            self.CommLabel_1.setText("Port:")
            self.CommText_1.setVisible(True)
            # Property 2 settings.
            self.CommLabel_2.setVisible(True)
            self.CommLabel_2.setText("Speed:")
            self.CommText_2.setVisible(True)
            # Property 3 settings.
            self.CommLabel_3.setVisible(False)
            self.CommText_3.setVisible(False)
            # Property 4 settings.
            self.CommLabel_4.setVisible(False)
            self.CommText_4.setVisible(False)
        elif self.CommProtocolBox.currentText() == "USB":
            self.CommPropertiesgroupBox.setVisible(True)
            # Property 1 settings.
            self.CommLabel_1.setVisible(True)
            self.CommLabel_1.setText("Port:")
            self.CommText_1.setVisible(True)
            # Property 2 settings.
            self.CommLabel_2.setVisible(False)
            self.CommText_2.setVisible(False)
            # Property 3 settings.
            self.CommLabel_3.setVisible(False)
            self.CommText_3.setVisible(False)
            # Property 4 settings.
            self.CommLabel_4.setVisible(False)
            self.CommText_4.setVisible(False)
        elif self.CommProtocolBox.currentText() == "VISA":
            self.CommPropertiesgroupBox.setVisible(True)
            # Property 1 settings.
            self.CommLabel_1.setVisible(True)
            self.CommLabel_1.setText("VISA ID:")
            self.CommText_1.setVisible(True)
            # Property 2 settings.
            self.CommLabel_2.setVisible(False)
            self.CommText_2.setVisible(False)
            # Property 3 settings.
            self.CommLabel_3.setVisible(False)
            self.CommText_3.setVisible(False)
            # Property 4 settings.
            self.CommLabel_4.setVisible(False)
            self.CommText_4.setVisible(False)
        elif self.CommProtocolBox.currentText() == "Test":
            self.CommPropertiesgroupBox.setVisible(False)
            # Property 1 settings.
            self.CommLabel_1.setVisible(False)
            self.CommText_1.setVisible(False)
            # Property 2 settings.
            self.CommLabel_2.setVisible(False)
            self.CommText_2.setVisible(False)
            # Property 3 settings.
            self.CommLabel_3.setVisible(False)
            self.CommText_3.setVisible(False)
            # Property 4 settings.
            self.CommLabel_4.setVisible(False)
            self.CommText_4.setVisible(False)
        else:
            self.CommPropertiesgroupBox.setVisible(False)
        return
