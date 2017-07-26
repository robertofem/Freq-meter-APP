#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
import glob
import os
import sys
import yaml
# Third party libraries
from PyQt4 import QtGui, QtCore
# Local libraries
from view import device_interface


class DevManagerWindow(QtGui.QDialog, device_interface.Ui_DevManagerWindow):
    """
    Class for defining the behaviour of the Device Manager Interface.
    """
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        # Default group visibility
        self.CommPropertiesgroupBox.setVisible(False)
        # Combo boxes change events
        self.CommProtocolBox.currentIndexChanged.connect(self.protocol_change)
        self.NSignalsBox.valueChanged.connect(self.nsignals_change)
        # Button box events (accept/reject)
        self.buttonBox.clicked.connect(self.handle_buttonBox_click)

    def handle_buttonBox_click(self, button):
        """
        Check which button was pressed and perform corresponding action.
        """
        clicked_button = self.buttonBox.standardButton(button)
        if clicked_button == QtGui.QDialogButtonBox.Save:
            self.save_device()
        elif clicked_button == QtGui.QDialogButtonBox.Open:
            self.open_device()
        elif clicked_button == QtGui.QDialogButtonBox.Cancel:
            self.show_exit_dialog()
        return

    def show_exit_dialog(self):
        """
        Ask the user if he/she wants to exit the DevManager window.
        """
        reply = QtGui.QMessageBox.question(self, 'Exit message',
                                           "Do you want to exit?", 
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.close()
        return

    def open_device(self):
        """
        Open a Qt file dialog and load a .yml configuration
        
        After loading the configuration, it is shown in the user
        interface, allowing the user to watch and modify it.
        """
        dev_dir = "{}/resources/devices/".format(os.getcwd())
        file = QtGui.QFileDialog.getOpenFileName(self, 'Open file', dev_dir)
        with open(file, 'r') as conf_file:
            try:
                dev_data = yaml.load(conf_file)
            except yaml.parser.ParserError:
                err_text = "<font color='red'>Can open only '.yml' files!</font>"
                self.ErrorLabel.setText(err_text)
                return
        # Load general properties to interface.
        self.DevNameText.setText(dev_data['general']['Name'])
        self.DevVendorText.setText(dev_data['general']['Vendor'])
        self.DevModelText.setText(dev_data['general']['Model'])
        self.DevSerialNText.setText(dev_data['general']['Serial_N'])
        self.DevFirmVersionText.setText(dev_data['general']['FirmVersion'])
        # Load channel properties to interface.
        self.NChannelsBox.setValue(int(dev_data['chanels']['Quantity']))
        self.NSignalsBox.setValue(int(dev_data['chanels']['Signals']))
        index1 = self.S1comboBox.findText(dev_data['chanels']['SigTypes']['S1'])
        index2 = self.S2comboBox.findText(dev_data['chanels']['SigTypes']['S2'])
        index3 = self.S3comboBox.findText(dev_data['chanels']['SigTypes']['S3'])
        index4 = self.S4comboBox.findText(dev_data['chanels']['SigTypes']['S4'])
        self.S1comboBox.setCurrentIndex(index1)
        self.S2comboBox.setCurrentIndex(index2)
        self.S3comboBox.setCurrentIndex(index3)
        self.S4comboBox.setCurrentIndex(index4)
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
        self.Ohm50checkBox.setChecked(dev_data['impedance']['R50Ohm']=='True')
        self.MegaOhmcheckBox.setChecked(dev_data['impedance']['R1MOhm']=='True')
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
            reply = QtGui.QMessageBox.question(self, 'Message', question,
                                               QtGui.QMessageBox.Yes,
                                               QtGui.QMessageBox.No)
            err_text = ""
            self.ErrorLabel.setText(err_text)
            if reply == QtGui.QMessageBox.No:
                return
        else:
            err_text = ""
        self.ErrorLabel.setText(err_text)
        # Construct a dictionary with the whole form information.
        dev_data = dict(
            general = dict(
                Name = str(self.DevNameText.text()),
                Vendor = str(self.DevVendorText.text()),
                Model = str(self.DevModelText.text()),
                Serial_N = str(self.DevSerialNText.text()),
                FirmVersion = str(self.DevFirmVersionText.text()),
                ),
            communications = dict(
                Protocol = str(self.CommProtocolBox.currentText()),
                Properties = dict(
                    CommProp1 = str(self.CommText_1.text()),
                    CommProp2 = str(self.CommText_2.text()),
                    CommProp3 = str(self.CommText_3.text()),
                    CommProp4 = str(self.CommText_4.text()),
                    ),
                ),
            chanels = dict(
                Quantity = str(self.NChannelsBox.value()),
                Signals = str(self.NSignalsBox.value()),
                SigTypes = dict(
                    S1 = str(self.S1comboBox.currentText()),
                    S2 = str(self.S2comboBox.currentText()),
                    S3 = str(self.S3comboBox.currentText()),
                    S4 = str(self.S4comboBox.currentText()),
                    ),
                ),
            impedance = dict(
                R50Ohm = str(self.Ohm50checkBox.isChecked()),
                R1MOhm = str(self.MegaOhmcheckBox.isChecked()),
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

    def nsignals_change(self):
        """
        Enable/disable the signal elements depending on spin box value.
        """
        self.S2label.setEnabled(self.NSignalsBox.value() > 1)
        self.S2comboBox.setEnabled(self.NSignalsBox.value() > 1)
        self.S3label.setEnabled(self.NSignalsBox.value() > 2)
        self.S3comboBox.setEnabled(self.NSignalsBox.value() > 2)
        self.S4label.setEnabled(self.NSignalsBox.value() > 3)
        self.S4comboBox.setEnabled(self.NSignalsBox.value() > 3)
        # Reset the combo boxes values to default when signals are disabled.
        if self.NSignalsBox.value() < 4:
            self.S4comboBox.setCurrentIndex(0)
        if self.NSignalsBox.value() < 3:
            self.S3comboBox.setCurrentIndex(0)
        if self.NSignalsBox.value() < 2:
            self.S2comboBox.setCurrentIndex(0)

    def protocol_change(self):
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
        else:
            self.CommPropertiesgroupBox.setVisible(False)
        return
