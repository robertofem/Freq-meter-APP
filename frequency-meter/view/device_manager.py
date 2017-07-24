#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
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
        self.buttonBox.accepted.connect(self.save_device)
        self.buttonBox.rejected.connect(self.close)

    def save_device(self):
        """Read the whole form and save data to yaml file."""
        # Check that device name is not empty.
        if self.DevNameText.text() == "":
            self.ErrorLabel.setText("<font color='red'>"
                                    "'Name' field cannot be empty!</font>")
            return
        # Check that at least one impedance configuration is checked.
        elif (not self.Ohm50checkBox.isChecked()
                and not self.MegaOhmcheckBox.isChecked()):
            self.ErrorLabel.setText("<font color='red'>At least one impedance"
                                    " must be selected!</font>")
            return
        else:
            self.ErrorLabel.setText("")
        device_data = dict(
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
        with open('resources/devices/{}.yml'.format(self.DevNameText.text()),
                  'w') as outfile:
            yaml.dump(device_data, outfile, default_flow_style=False)
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
