# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/device_interface.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DevManagerWindow(object):
    def setupUi(self, DevManagerWindow):
        DevManagerWindow.setObjectName("DevManagerWindow")
        DevManagerWindow.resize(714, 538)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DevManagerWindow.sizePolicy().hasHeightForWidth())
        DevManagerWindow.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(DevManagerWindow)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setObjectName("gridLayout")
        self.ErrorLabel = QtWidgets.QLabel(DevManagerWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ErrorLabel.sizePolicy().hasHeightForWidth())
        self.ErrorLabel.setSizePolicy(sizePolicy)
        self.ErrorLabel.setText("")
        self.ErrorLabel.setObjectName("ErrorLabel")
        self.gridLayout.addWidget(self.ErrorLabel, 8, 0, 1, 3)
        self.GeneralPropertiesgroupBox = QtWidgets.QGroupBox(DevManagerWindow)
        self.GeneralPropertiesgroupBox.setObjectName("GeneralPropertiesgroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.GeneralPropertiesgroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.GeneralPropertiesgroupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.GeneralPropertiesgroupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.GeneralPropertiesgroupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.GeneralPropertiesgroupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.GeneralPropertiesgroupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.DevNameText = QtWidgets.QLineEdit(self.GeneralPropertiesgroupBox)
        self.DevNameText.setObjectName("DevNameText")
        self.gridLayout_2.addWidget(self.DevNameText, 0, 1, 1, 1)
        self.DevModelText = QtWidgets.QLineEdit(self.GeneralPropertiesgroupBox)
        self.DevModelText.setObjectName("DevModelText")
        self.gridLayout_2.addWidget(self.DevModelText, 2, 1, 1, 1)
        self.DevSerialNText = QtWidgets.QLineEdit(self.GeneralPropertiesgroupBox)
        self.DevSerialNText.setObjectName("DevSerialNText")
        self.gridLayout_2.addWidget(self.DevSerialNText, 3, 1, 1, 1)
        self.DevFirmVersionText = QtWidgets.QLineEdit(self.GeneralPropertiesgroupBox)
        self.DevFirmVersionText.setObjectName("DevFirmVersionText")
        self.gridLayout_2.addWidget(self.DevFirmVersionText, 4, 1, 1, 1)
        self.VendorSelector = QtWidgets.QComboBox(self.GeneralPropertiesgroupBox)
        self.VendorSelector.setObjectName("VendorSelector")
        self.gridLayout_2.addWidget(self.VendorSelector, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.GeneralPropertiesgroupBox, 1, 0, 3, 1)
        self.CommSettingsgroupBox_2 = QtWidgets.QGroupBox(DevManagerWindow)
        self.CommSettingsgroupBox_2.setObjectName("CommSettingsgroupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.CommSettingsgroupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_8 = QtWidgets.QLabel(self.CommSettingsgroupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)
        self.CommProtocolBox = QtWidgets.QComboBox(self.CommSettingsgroupBox_2)
        self.CommProtocolBox.setObjectName("CommProtocolBox")
        self.gridLayout_4.addWidget(self.CommProtocolBox, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.CommSettingsgroupBox_2, 1, 2, 1, 1)
        self.CommPropertiesgroupBox = QtWidgets.QGroupBox(DevManagerWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CommPropertiesgroupBox.sizePolicy().hasHeightForWidth())
        self.CommPropertiesgroupBox.setSizePolicy(sizePolicy)
        self.CommPropertiesgroupBox.setObjectName("CommPropertiesgroupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.CommPropertiesgroupBox)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.CommLabel_1 = QtWidgets.QLabel(self.CommPropertiesgroupBox)
        self.CommLabel_1.setObjectName("CommLabel_1")
        self.gridLayout_3.addWidget(self.CommLabel_1, 1, 0, 1, 1)
        self.CommText_1 = QtWidgets.QLineEdit(self.CommPropertiesgroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CommText_1.sizePolicy().hasHeightForWidth())
        self.CommText_1.setSizePolicy(sizePolicy)
        self.CommText_1.setObjectName("CommText_1")
        self.gridLayout_3.addWidget(self.CommText_1, 1, 1, 1, 1)
        self.CommText_2 = QtWidgets.QLineEdit(self.CommPropertiesgroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CommText_2.sizePolicy().hasHeightForWidth())
        self.CommText_2.setSizePolicy(sizePolicy)
        self.CommText_2.setObjectName("CommText_2")
        self.gridLayout_3.addWidget(self.CommText_2, 2, 1, 1, 1)
        self.CommLabel_2 = QtWidgets.QLabel(self.CommPropertiesgroupBox)
        self.CommLabel_2.setObjectName("CommLabel_2")
        self.gridLayout_3.addWidget(self.CommLabel_2, 2, 0, 1, 1)
        self.CommLabel_3 = QtWidgets.QLabel(self.CommPropertiesgroupBox)
        self.CommLabel_3.setObjectName("CommLabel_3")
        self.gridLayout_3.addWidget(self.CommLabel_3, 3, 0, 1, 1)
        self.CommText_3 = QtWidgets.QLineEdit(self.CommPropertiesgroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CommText_3.sizePolicy().hasHeightForWidth())
        self.CommText_3.setSizePolicy(sizePolicy)
        self.CommText_3.setObjectName("CommText_3")
        self.gridLayout_3.addWidget(self.CommText_3, 3, 1, 1, 1)
        self.CommLabel_4 = QtWidgets.QLabel(self.CommPropertiesgroupBox)
        self.CommLabel_4.setObjectName("CommLabel_4")
        self.gridLayout_3.addWidget(self.CommLabel_4, 4, 0, 1, 1)
        self.CommText_4 = QtWidgets.QLineEdit(self.CommPropertiesgroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CommText_4.sizePolicy().hasHeightForWidth())
        self.CommText_4.setSizePolicy(sizePolicy)
        self.CommText_4.setObjectName("CommText_4")
        self.gridLayout_3.addWidget(self.CommText_4, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.CommPropertiesgroupBox, 2, 2, 2, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DevManagerWindow)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Open|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 9, 2, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(DevManagerWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)
        self.channel_number = QtWidgets.QLabel(self.groupBox)
        self.channel_number.setText("")
        self.channel_number.setObjectName("channel_number")
        self.gridLayout_5.addWidget(self.channel_number, 0, 1, 1, 1)
        self.signal_number = QtWidgets.QLabel(self.groupBox)
        self.signal_number.setText("")
        self.signal_number.setObjectName("signal_number")
        self.gridLayout_5.addWidget(self.signal_number, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 4, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(DevManagerWindow)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.Ohm50checkBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.Ohm50checkBox.setCheckable(False)
        self.Ohm50checkBox.setAutoExclusive(False)
        self.Ohm50checkBox.setObjectName("Ohm50checkBox")
        self.gridLayout_7.addWidget(self.Ohm50checkBox, 0, 0, 1, 1)
        self.MegaOhmcheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.MegaOhmcheckBox.setCheckable(False)
        self.MegaOhmcheckBox.setAutoExclusive(False)
        self.MegaOhmcheckBox.setObjectName("MegaOhmcheckBox")
        self.gridLayout_7.addWidget(self.MegaOhmcheckBox, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 7, 0, 1, 1)
        self.line = QtWidgets.QFrame(DevManagerWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 1, 7, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(DevManagerWindow)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.S3label = QtWidgets.QLabel(self.groupBox_2)
        self.S3label.setEnabled(True)
        self.S3label.setObjectName("S3label")
        self.gridLayout_6.addWidget(self.S3label, 2, 0, 1, 1)
        self.S1label = QtWidgets.QLabel(self.groupBox_2)
        self.S1label.setObjectName("S1label")
        self.gridLayout_6.addWidget(self.S1label, 0, 0, 1, 1)
        self.signal1_type = QtWidgets.QLabel(self.groupBox_2)
        self.signal1_type.setText("")
        self.signal1_type.setObjectName("signal1_type")
        self.gridLayout_6.addWidget(self.signal1_type, 0, 1, 1, 1)
        self.signal3_type = QtWidgets.QLabel(self.groupBox_2)
        self.signal3_type.setText("")
        self.signal3_type.setObjectName("signal3_type")
        self.gridLayout_6.addWidget(self.signal3_type, 2, 1, 1, 1)
        self.signal2_type = QtWidgets.QLabel(self.groupBox_2)
        self.signal2_type.setText("")
        self.signal2_type.setObjectName("signal2_type")
        self.gridLayout_6.addWidget(self.signal2_type, 1, 1, 1, 1)
        self.S2label = QtWidgets.QLabel(self.groupBox_2)
        self.S2label.setEnabled(True)
        self.S2label.setObjectName("S2label")
        self.gridLayout_6.addWidget(self.S2label, 1, 0, 1, 1)
        self.S4label = QtWidgets.QLabel(self.groupBox_2)
        self.S4label.setEnabled(True)
        self.S4label.setObjectName("S4label")
        self.gridLayout_6.addWidget(self.S4label, 4, 0, 1, 1)
        self.signal4_type = QtWidgets.QLabel(self.groupBox_2)
        self.signal4_type.setText("")
        self.signal4_type.setObjectName("signal4_type")
        self.gridLayout_6.addWidget(self.signal4_type, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 5, 0, 2, 1)

        self.retranslateUi(DevManagerWindow)
        QtCore.QMetaObject.connectSlotsByName(DevManagerWindow)

    def retranslateUi(self, DevManagerWindow):
        _translate = QtCore.QCoreApplication.translate
        DevManagerWindow.setWindowTitle(_translate("DevManagerWindow", "Device manager"))
        self.GeneralPropertiesgroupBox.setTitle(_translate("DevManagerWindow", "General properties"))
        self.label_2.setText(_translate("DevManagerWindow", "Vendor:"))
        self.label_3.setText(_translate("DevManagerWindow", "Model:"))
        self.label_4.setText(_translate("DevManagerWindow", "Serial Nº:"))
        self.label_7.setText(_translate("DevManagerWindow", "Firmware version:"))
        self.label.setText(_translate("DevManagerWindow", "Name:"))
        self.CommSettingsgroupBox_2.setTitle(_translate("DevManagerWindow", "Communication settings"))
        self.label_8.setText(_translate("DevManagerWindow", "Protocol"))
        self.CommPropertiesgroupBox.setTitle(_translate("DevManagerWindow", "Communication properties"))
        self.CommLabel_1.setText(_translate("DevManagerWindow", "Prop1:"))
        self.CommLabel_2.setText(_translate("DevManagerWindow", "Prop2:"))
        self.CommLabel_3.setText(_translate("DevManagerWindow", "Prop3:"))
        self.CommLabel_4.setText(_translate("DevManagerWindow", "Prop4:"))
        self.groupBox.setTitle(_translate("DevManagerWindow", "Chanels properties"))
        self.label_6.setText(_translate("DevManagerWindow", "Signals per ch.: "))
        self.label_5.setText(_translate("DevManagerWindow", "Nº of channels:"))
        self.groupBox_3.setTitle(_translate("DevManagerWindow", "Available impedances"))
        self.Ohm50checkBox.setText(_translate("DevManagerWindow", "50 Ω"))
        self.MegaOhmcheckBox.setText(_translate("DevManagerWindow", "1 MΩ"))
        self.groupBox_2.setTitle(_translate("DevManagerWindow", "Signal types"))
        self.S3label.setText(_translate("DevManagerWindow", "Signal 3:"))
        self.S1label.setText(_translate("DevManagerWindow", "Signal 1:"))
        self.S2label.setText(_translate("DevManagerWindow", "Signal 2:"))
        self.S4label.setText(_translate("DevManagerWindow", "Signal 4:"))

