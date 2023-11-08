from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


from modules.Logger import Logger
from modules.rich_setup import *

from modules.MirInterface import MirInterface


class MirUiInterface(QObject):
    def __init__(self, MAINWINDOW_):
        super().__init__()
        #
        try:
            #
            self.MAINWINDOW = MAINWINDOW_
            self.NAME = "MirUiInterface"
            #
            self.logger = Logger(self.NAME)
            self.logger.debug("Initilizing ...")
            #

            ##### UIs #####
            self.input_ip = self.MAINWINDOW.lineEdit_setting_mir_ip
            self.input_username = self.MAINWINDOW.lineEdit_setting_mir_username
            self.input_password = self.MAINWINDOW.lineEdit_setting_mir_password
            self.input_auth_key = self.MAINWINDOW.lineEdit_setting_mir_auth_key
            self.input_freq = self.MAINWINDOW.lineEdit_setting_mir_freq

            self.btn_connect = self.MAINWINDOW.pushButton_setting_mir_connect

            self.lable_latency = self.MAINWINDOW.label_setting_mir_latency

            ##### Controllers #####
            self.mirInterface = MirInterface(
                ip_=self.input_ip.text(),
                username_=self.input_username.text(),
                password_=self.input_password.text(),
                auth_key_=self.input_auth_key.text(),
                frequency_=self.input_freq.text(),
            )

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
                self.setStyleSheet("{background-color: none;}")
            else:
                self.btn_connect.setText("Connect")
                self.setStyleSheet("{background-color: red;}")
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
            self.mirInterface.set_frequency(text)
        except Exception as err:
            console.print_exception()

    @pyqtSlot()
    def on_connect_btn_clicked(self):
        try:
            self.logger.debug("on_connect_btn_clicked() ...")
            self.mirInterface.connect()
        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Signal Slots ############################################################################## #
    # ########################################################################################### #
    @pyqtSlot(bool)
    def connectionStateUpdatedSlot(self, connected_):
        try:
            self.logger.debug("connectionStateUpdatedSlot(connected_={connected_}) ...")

        except Exception as err:
            console.print_exception()
