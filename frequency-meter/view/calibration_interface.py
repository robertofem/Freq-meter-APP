# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/resources/calibration_interface.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CalibWindow(object):
    def setupUi(self, CalibWindow):
        CalibWindow.setObjectName("CalibWindow")
        CalibWindow.resize(815, 602)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CalibWindow.sizePolicy().hasHeightForWidth())
        CalibWindow.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(CalibWindow)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.groupBox_coarse = QtWidgets.QGroupBox(CalibWindow)
        self.groupBox_coarse.setObjectName("groupBox_coarse")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_coarse)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.reference_device_group = QtWidgets.QGroupBox(self.groupBox_coarse)
        self.reference_device_group.setObjectName("reference_device_group")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.reference_device_group)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.reference_device_selector = QtWidgets.QComboBox(self.reference_device_group)
        self.reference_device_selector.setObjectName("reference_device_selector")
        self.verticalLayout_5.addWidget(self.reference_device_selector)
        self.reference_device_connect = QtWidgets.QPushButton(self.reference_device_group)
        self.reference_device_connect.setObjectName("reference_device_connect")
        self.verticalLayout_5.addWidget(self.reference_device_connect)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.reference_device_channels = QtWidgets.QGroupBox(self.reference_device_group)
        self.reference_device_channels.setEnabled(False)
        self.reference_device_channels.setMinimumSize(QtCore.QSize(100, 120))
        self.reference_device_channels.setObjectName("reference_device_channels")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.reference_device_channels)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.reference_device_channel0 = QtWidgets.QRadioButton(self.reference_device_channels)
        self.reference_device_channel0.setEnabled(False)
        self.reference_device_channel0.setObjectName("reference_device_channel0")
        self.verticalLayout_4.addWidget(self.reference_device_channel0)
        self.reference_device_channel1 = QtWidgets.QRadioButton(self.reference_device_channels)
        self.reference_device_channel1.setEnabled(False)
        self.reference_device_channel1.setObjectName("reference_device_channel1")
        self.verticalLayout_4.addWidget(self.reference_device_channel1)
        self.reference_device_channel2 = QtWidgets.QRadioButton(self.reference_device_channels)
        self.reference_device_channel2.setEnabled(False)
        self.reference_device_channel2.setObjectName("reference_device_channel2")
        self.verticalLayout_4.addWidget(self.reference_device_channel2)
        self.reference_device_channel3 = QtWidgets.QRadioButton(self.reference_device_channels)
        self.reference_device_channel3.setEnabled(False)
        self.reference_device_channel3.setObjectName("reference_device_channel3")
        self.verticalLayout_4.addWidget(self.reference_device_channel3)
        self.horizontalLayout_4.addWidget(self.reference_device_channels)
        self.reference_device_impedances = QtWidgets.QGroupBox(self.reference_device_group)
        self.reference_device_impedances.setEnabled(False)
        self.reference_device_impedances.setObjectName("reference_device_impedances")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.reference_device_impedances)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.reference_device_impedance0 = QtWidgets.QRadioButton(self.reference_device_impedances)
        self.reference_device_impedance0.setEnabled(False)
        self.reference_device_impedance0.setText("")
        self.reference_device_impedance0.setObjectName("reference_device_impedance0")
        self.verticalLayout_6.addWidget(self.reference_device_impedance0)
        self.reference_device_impedance1 = QtWidgets.QRadioButton(self.reference_device_impedances)
        self.reference_device_impedance1.setEnabled(False)
        self.reference_device_impedance1.setText("")
        self.reference_device_impedance1.setObjectName("reference_device_impedance1")
        self.verticalLayout_6.addWidget(self.reference_device_impedance1)
        self.reference_device_impedance2 = QtWidgets.QRadioButton(self.reference_device_impedances)
        self.reference_device_impedance2.setEnabled(False)
        self.reference_device_impedance2.setText("")
        self.reference_device_impedance2.setObjectName("reference_device_impedance2")
        self.verticalLayout_6.addWidget(self.reference_device_impedance2)
        self.reference_device_impedance3 = QtWidgets.QRadioButton(self.reference_device_impedances)
        self.reference_device_impedance3.setEnabled(False)
        self.reference_device_impedance3.setText("")
        self.reference_device_impedance3.setObjectName("reference_device_impedance3")
        self.verticalLayout_6.addWidget(self.reference_device_impedance3)
        self.horizontalLayout_4.addWidget(self.reference_device_impedances)
        self.verticalLayout_2.addWidget(self.reference_device_group)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.button_start_coarse = QtWidgets.QPushButton(self.groupBox_coarse)
        self.button_start_coarse.setObjectName("button_start_coarse")
        self.horizontalLayout_5.addWidget(self.button_start_coarse)
        self.button_stop_coarse = QtWidgets.QPushButton(self.groupBox_coarse)
        self.button_stop_coarse.setEnabled(False)
        self.button_stop_coarse.setObjectName("button_stop_coarse")
        self.horizontalLayout_5.addWidget(self.button_stop_coarse)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_calib_const = QtWidgets.QLabel(self.groupBox_coarse)
        self.label_calib_const.setObjectName("label_calib_const")
        self.horizontalLayout_6.addWidget(self.label_calib_const)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.label_coarse_mess = QtWidgets.QLabel(self.groupBox_coarse)
        self.label_coarse_mess.setObjectName("label_coarse_mess")
        self.verticalLayout_2.addWidget(self.label_coarse_mess)
        self.plotVLayout_coarse = QtWidgets.QVBoxLayout()
        self.plotVLayout_coarse.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.plotVLayout_coarse.setObjectName("plotVLayout_coarse")
        self.verticalLayout_2.addLayout(self.plotVLayout_coarse)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_8.addWidget(self.groupBox_coarse)
        self.groupBox_fine = QtWidgets.QGroupBox(CalibWindow)
        self.groupBox_fine.setObjectName("groupBox_fine")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_fine)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox_fine)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.lineEditFineMeas = QtWidgets.QLineEdit(self.groupBox_fine)
        self.lineEditFineMeas.setObjectName("lineEditFineMeas")
        self.horizontalLayout_3.addWidget(self.lineEditFineMeas)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.button_start_fine = QtWidgets.QPushButton(self.groupBox_fine)
        self.button_start_fine.setObjectName("button_start_fine")
        self.horizontalLayout_7.addWidget(self.button_start_fine)
        self.button_stop_fine = QtWidgets.QPushButton(self.groupBox_fine)
        self.button_stop_fine.setEnabled(False)
        self.button_stop_fine.setObjectName("button_stop_fine")
        self.horizontalLayout_7.addWidget(self.button_stop_fine)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.label_fine_mess = QtWidgets.QLabel(self.groupBox_fine)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_fine_mess.sizePolicy().hasHeightForWidth())
        self.label_fine_mess.setSizePolicy(sizePolicy)
        self.label_fine_mess.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_fine_mess.setObjectName("label_fine_mess")
        self.verticalLayout_3.addWidget(self.label_fine_mess)
        self.button_save_fine = QtWidgets.QPushButton(self.groupBox_fine)
        self.button_save_fine.setEnabled(False)
        self.button_save_fine.setObjectName("button_save_fine")
        self.verticalLayout_3.addWidget(self.button_save_fine)
        self.plotVLayout_fine = QtWidgets.QVBoxLayout()
        self.plotVLayout_fine.setObjectName("plotVLayout_fine")
        self.verticalLayout_3.addLayout(self.plotVLayout_fine)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_8.addWidget(self.groupBox_fine)
        self.gridLayout.addLayout(self.horizontalLayout_8, 2, 1, 1, 1)
        self.ErrorLabel = QtWidgets.QLabel(CalibWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ErrorLabel.sizePolicy().hasHeightForWidth())
        self.ErrorLabel.setSizePolicy(sizePolicy)
        self.ErrorLabel.setText("")
        self.ErrorLabel.setObjectName("ErrorLabel")
        self.gridLayout.addWidget(self.ErrorLabel, 4, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(CalibWindow)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)
        self.target_device_group = QtWidgets.QGroupBox(CalibWindow)
        self.target_device_group.setObjectName("target_device_group")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.target_device_group)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.target_device_selector = QtWidgets.QComboBox(self.target_device_group)
        self.target_device_selector.setObjectName("target_device_selector")
        self.verticalLayout.addWidget(self.target_device_selector)
        self.target_device_connect = QtWidgets.QPushButton(self.target_device_group)
        self.target_device_connect.setMinimumSize(QtCore.QSize(120, 0))
        self.target_device_connect.setObjectName("target_device_connect")
        self.verticalLayout.addWidget(self.target_device_connect)
        self.horizontalLayout_10.addLayout(self.verticalLayout)
        self.target_device_channels = QtWidgets.QGroupBox(self.target_device_group)
        self.target_device_channels.setEnabled(False)
        self.target_device_channels.setMinimumSize(QtCore.QSize(120, 120))
        self.target_device_channels.setObjectName("target_device_channels")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.target_device_channels)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.target_device_channel0 = QtWidgets.QRadioButton(self.target_device_channels)
        self.target_device_channel0.setEnabled(False)
        self.target_device_channel0.setObjectName("target_device_channel0")
        self.verticalLayout_7.addWidget(self.target_device_channel0)
        self.target_device_channel1 = QtWidgets.QRadioButton(self.target_device_channels)
        self.target_device_channel1.setEnabled(False)
        self.target_device_channel1.setObjectName("target_device_channel1")
        self.verticalLayout_7.addWidget(self.target_device_channel1)
        self.target_device_channel2 = QtWidgets.QRadioButton(self.target_device_channels)
        self.target_device_channel2.setEnabled(False)
        self.target_device_channel2.setObjectName("target_device_channel2")
        self.verticalLayout_7.addWidget(self.target_device_channel2)
        self.target_device_channel3 = QtWidgets.QRadioButton(self.target_device_channels)
        self.target_device_channel3.setEnabled(False)
        self.target_device_channel3.setObjectName("target_device_channel3")
        self.verticalLayout_7.addWidget(self.target_device_channel3)
        self.horizontalLayout_10.addWidget(self.target_device_channels)
        self.target_device_impedances = QtWidgets.QGroupBox(self.target_device_group)
        self.target_device_impedances.setEnabled(False)
        self.target_device_impedances.setMinimumSize(QtCore.QSize(120, 120))
        self.target_device_impedances.setObjectName("target_device_impedances")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.target_device_impedances)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.target_device_impedance0 = QtWidgets.QRadioButton(self.target_device_impedances)
        self.target_device_impedance0.setEnabled(False)
        self.target_device_impedance0.setText("")
        self.target_device_impedance0.setObjectName("target_device_impedance0")
        self.verticalLayout_8.addWidget(self.target_device_impedance0)
        self.target_device_impedance1 = QtWidgets.QRadioButton(self.target_device_impedances)
        self.target_device_impedance1.setEnabled(False)
        self.target_device_impedance1.setText("")
        self.target_device_impedance1.setObjectName("target_device_impedance1")
        self.verticalLayout_8.addWidget(self.target_device_impedance1)
        self.target_device_impedance2 = QtWidgets.QRadioButton(self.target_device_impedances)
        self.target_device_impedance2.setText("")
        self.target_device_impedance2.setObjectName("target_device_impedance2")
        self.verticalLayout_8.addWidget(self.target_device_impedance2)
        self.target_device_impedance3 = QtWidgets.QRadioButton(self.target_device_impedances)
        self.target_device_impedance3.setEnabled(False)
        self.target_device_impedance3.setText("")
        self.target_device_impedance3.setObjectName("target_device_impedance3")
        self.verticalLayout_8.addWidget(self.target_device_impedance3)
        self.horizontalLayout_10.addWidget(self.target_device_impedances)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.gridLayout.addWidget(self.target_device_group, 0, 1, 1, 1)

        self.retranslateUi(CalibWindow)
        QtCore.QMetaObject.connectSlotsByName(CalibWindow)
        CalibWindow.setTabOrder(self.target_device_selector, self.target_device_connect)
        CalibWindow.setTabOrder(self.target_device_connect, self.target_device_channel0)
        CalibWindow.setTabOrder(self.target_device_channel0, self.target_device_channel1)
        CalibWindow.setTabOrder(self.target_device_channel1, self.target_device_channel2)
        CalibWindow.setTabOrder(self.target_device_channel2, self.target_device_channel3)
        CalibWindow.setTabOrder(self.target_device_channel3, self.target_device_impedance0)
        CalibWindow.setTabOrder(self.target_device_impedance0, self.target_device_impedance1)
        CalibWindow.setTabOrder(self.target_device_impedance1, self.target_device_impedance2)
        CalibWindow.setTabOrder(self.target_device_impedance2, self.target_device_impedance3)
        CalibWindow.setTabOrder(self.target_device_impedance3, self.reference_device_selector)
        CalibWindow.setTabOrder(self.reference_device_selector, self.reference_device_connect)
        CalibWindow.setTabOrder(self.reference_device_connect, self.reference_device_channel0)
        CalibWindow.setTabOrder(self.reference_device_channel0, self.reference_device_channel1)
        CalibWindow.setTabOrder(self.reference_device_channel1, self.reference_device_channel2)
        CalibWindow.setTabOrder(self.reference_device_channel2, self.reference_device_channel3)
        CalibWindow.setTabOrder(self.reference_device_channel3, self.reference_device_impedance0)
        CalibWindow.setTabOrder(self.reference_device_impedance0, self.reference_device_impedance1)
        CalibWindow.setTabOrder(self.reference_device_impedance1, self.reference_device_impedance2)
        CalibWindow.setTabOrder(self.reference_device_impedance2, self.reference_device_impedance3)
        CalibWindow.setTabOrder(self.reference_device_impedance3, self.button_start_coarse)
        CalibWindow.setTabOrder(self.button_start_coarse, self.button_stop_coarse)
        CalibWindow.setTabOrder(self.button_stop_coarse, self.button_start_fine)
        CalibWindow.setTabOrder(self.button_start_fine, self.button_stop_fine)

    def retranslateUi(self, CalibWindow):
        _translate = QtCore.QCoreApplication.translate
        CalibWindow.setWindowTitle(_translate("CalibWindow", "FPGA Frequency Meter Calibration"))
        self.groupBox_coarse.setTitle(_translate("CalibWindow", "Coarse Calibration"))
        self.reference_device_group.setTitle(_translate("CalibWindow", "Reference device"))
        self.reference_device_connect.setText(_translate("CalibWindow", "Connect"))
        self.reference_device_channels.setTitle(_translate("CalibWindow", "Channels"))
        self.reference_device_channel0.setText(_translate("CalibWindow", "1"))
        self.reference_device_channel1.setText(_translate("CalibWindow", "2"))
        self.reference_device_channel2.setText(_translate("CalibWindow", "3"))
        self.reference_device_channel3.setText(_translate("CalibWindow", "4"))
        self.reference_device_impedances.setTitle(_translate("CalibWindow", "Impedance"))
        self.button_start_coarse.setText(_translate("CalibWindow", "Start"))
        self.button_stop_coarse.setText(_translate("CalibWindow", "Stop"))
        self.label_calib_const.setText(_translate("CalibWindow", "Coarse calibration constant:"))
        self.label_coarse_mess.setText(_translate("CalibWindow", "Coarse Calibration Messages"))
        self.groupBox_fine.setTitle(_translate("CalibWindow", "Fine Calibration"))
        self.label.setText(_translate("CalibWindow", "Number of measurments for the Code Density Test (CDT)"))
        self.lineEditFineMeas.setText(_translate("CalibWindow", "10000"))
        self.button_start_fine.setText(_translate("CalibWindow", "Start"))
        self.button_stop_fine.setText(_translate("CalibWindow", "Stop"))
        self.label_fine_mess.setText(_translate("CalibWindow", "Fine Calibration Messages"))
        self.button_save_fine.setText(_translate("CalibWindow", "Save in file"))
        self.target_device_group.setTitle(_translate("CalibWindow", "Target device (to be calibrated)"))
        self.target_device_connect.setText(_translate("CalibWindow", "Connect"))
        self.target_device_channels.setTitle(_translate("CalibWindow", "Channels"))
        self.target_device_channel0.setText(_translate("CalibWindow", "1"))
        self.target_device_channel1.setText(_translate("CalibWindow", "2"))
        self.target_device_channel2.setText(_translate("CalibWindow", "3"))
        self.target_device_channel3.setText(_translate("CalibWindow", "4"))
        self.target_device_impedances.setTitle(_translate("CalibWindow", "Impedance"))

