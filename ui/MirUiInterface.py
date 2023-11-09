from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


from modules.Logger import Logger
from modules.rich_setup import *

from modules.MirInterface import MirInterface


class MirUiInterface(QObject):
    def __init__(
        self,
        name_="MirUiInterface",
        MAINWINDOW_=None,
        DATABASE_=None,
        mirInterface_=None,
    ):
        super().__init__()
        #
        try:
            #
            self.NAME = name_
            #
            self.logger = Logger(self.NAME)
            self.logger.debug("Initilizing ...")
            #
            self.MAINWINDOW = MAINWINDOW_
            self.DATABASE = DATABASE_
            self.mirInterface = mirInterface_

            ##### UIs #####
            self.input_ip = self.MAINWINDOW.lineEdit_setting_mir_ip
            self.input_username = self.MAINWINDOW.lineEdit_setting_mir_username
            self.input_password = self.MAINWINDOW.lineEdit_setting_mir_password
            self.input_auth_key = self.MAINWINDOW.lineEdit_setting_mir_auth_key
            self.input_freq = self.MAINWINDOW.lineEdit_setting_mir_freq
            self.input_start_addr = self.MAINWINDOW.lineEdit_mir_reg_NO_4

            self.btn_connect = self.MAINWINDOW.pushButton_setting_mir_connect

            self.label_latency = self.MAINWINDOW.label_setting_mir_latency
            self.label_actual_freq = self.MAINWINDOW.label_setting_mir_actual_freq

            #
            self.input_register_list = [
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_8,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_9,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_10,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_11,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_12,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_13,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_14,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_15,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_16,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_17,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_18,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_19,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_20,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_21,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_22,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_23,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_24,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_25,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_26,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_27,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_28,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_29,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_30,
                self.MAINWINDOW.lineEdit_mir_modbus_addr_NO_31,
            ]

            ##### Local variables #####
            self.connected = False

            self.initialize()

            ##### UI Signals/Slots #####
            self.input_ip.textChanged.connect(self.on_input_ip_changed)
            self.input_username.textChanged.connect(self.on_input_username_changed)
            self.input_password.textChanged.connect(self.on_input_password_changed)
            self.input_auth_key.textChanged.connect(self.on_input_auth_key_changed)
            self.input_freq.textChanged.connect(self.on_input_frequency_changed)

            self.btn_connect.clicked.connect(self.on_connect_btn_clicked)

            ##### Custom Signals/Slots #####
            self.mirInterface.connectionStateUpdatedSignal.connect(
                self.connectionStateUpdatedSlot
            )
            self.mirInterface.MODBUS_INTERFACE.readModbusUpdatedSignal.connect(
                self.readModbusUpdatedSlot
            )

            self.mirInterface.MODBUS_INTERFACE.readModbusActualFrequencySignal.connect(
                self.readModbusActualFrequencySignal
            )
            #
            self.DATABASE.settingLoadedSignal.connect(self.settingLoadedSlot)

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # UIs ####################################################################################### #
    # ########################################################################################### #
    def update_ui(self):
        try:
            ##### inputs #####
            enable_input_ = self.connected

            # text inputs
            self.input_ip.setEnabled(enable_input_)
            self.input_username.setEnabled(enable_input_)
            self.input_password.setEnabled(enable_input_)
            self.input_auth_key.setEnabled(enable_input_)
            self.input_freq.setEnabled(enable_input_)

            if self.connected:
                self.btn_connect.setText("Disconnect")
                self.btn_connect.setStyleSheet("background-color: red; color: white;")
            else:
                self.btn_connect.setText("Connect")
                self.btn_connect.setStyleSheet("background-color: none;")
                self.btn_connect.setStyleSheet("color: none;")
            pass

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Initialize ################################################################################ #
    # ########################################################################################### #
    def initialize(self):
        try:
            #
            # self.mirInterface.set_ip(self.input_ip.text())
            # self.mirInterface.input_username(self.input_ip.input_username())
            # self.mirInterface.set_password(self.input_ip.input_password())
            pass

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # UI Slots ################################################################################## #
    # ########################################################################################### #
    @pyqtSlot(str)
    def on_input_ip_changed(self, text):
        try:
            self.mirInterface.set_ip(text)
        except Exception as err:
            console.print_exception()

    @pyqtSlot(str)
    def on_input_username_changed(self, text):
        try:
            self.mirInterface.set_username(text)
        except Exception as err:
            console.print_exception()

    @pyqtSlot(str)
    def on_input_password_changed(self, text):
        try:
            self.mirInterface.set_password(text)
        except Exception as err:
            console.print_exception()

    @pyqtSlot(str)
    def on_input_auth_key_changed(self, text):
        try:
            self.mirInterface.set_auth_key(text)
        except Exception as err:
            console.print_exception()

    @pyqtSlot(str)
    def on_input_frequency_changed(self, text):
        try:
            self.mirInterface.set_frequency(float(text.strip()))
        except Exception as err:
            console.print_exception()

    @pyqtSlot()
    def on_connect_btn_clicked(self):
        try:
            self.logger.debug("on_connect_btn_clicked() :: ...")
            self.mirInterface.connect_disconnect()
        except Exception as err:
            console.print_exception()

    @pyqtSlot(str)
    def on_input_start_addr_changed(self, text):
        try:
            self.mirInterface.set_modbus_start_addr(int(text.strip()))
        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Custom Signal Slots ####################################################################### #
    # ########################################################################################### #
    @pyqtSlot(bool)
    def connectionStateUpdatedSlot(self, connected_):
        try:
            self.logger.debug(
                f"connectionStateUpdatedSlot(connected_={connected_}) ..."
            )

            self.connected = connected_

            self.update_ui()

        except Exception as err:
            console.print_exception()

    @pyqtSlot(list)
    def readModbusUpdatedSlot(self, registers_):
        try:
            self.logger.debug(f"readModbusUpdatedSlot(registers_ = {registers_}) ...")
            #
            for i in range(len(registers_)):
                reg_value_ = registers_[i]
                ui_input_register_ = self.input_register_list[i]
                #
                ui_input_register_.setText(str(reg_value_))

        except Exception as err:
            console.print_exception()

    @pyqtSlot(float)
    def readModbusActualFrequencySignal(self, actual_freq_):
        try:
            # self.logger.debug(
            #     f"readModbusActualFrequencySignal(actual_freq_ = {actual_freq_}) ..."
            # )
            self.label_actual_freq.setText(str("{:10.4f}".format(actual_freq_)))
            #
            if actual_freq_ > 0.0:
                self.label_actual_freq.setStyleSheet("background-color: #DCEDC8;")
            else:
                self.label_actual_freq.setStyleSheet("background-color: #FFCDD2;")
        except Exception as err:
            console.print_exception()

    ### Database
    @pyqtSlot(dict)
    def settingLoadedSlot(self, settings_):
        try:
            self.logger.debug(f"settingLoadedSlot(settings_) :: ...")
            #
            config_ = settings_["mir"]
            self.logger.debug(f"\t > config_: {config_}")
            #
            self.input_ip.setText(config_["ip"])

        except Exception as err:
            console.print_exception()
