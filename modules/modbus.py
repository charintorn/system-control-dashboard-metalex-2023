from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal


from modules.Logger import Logger
from modules.rich_setup import *

import time
import uuid
import threading

from pymodbus.client import ModbusTcpClient


class Modbus(QObject):
    connectionUpdatedSignal = pyqtSignal(bool)
    registersUpdatedSignal = pyqtSignal(list)

    def __init__(self, MAINWINDOW_):
        super().__init__()
        try:
            self.logger = Logger("Modbus")
            self.logger.debug("Initilizing ...")

            self.MAINWINDOW = MAINWINDOW_
            # self.ERROR_INDICATION = self.MAINWINDOW.ERROR_INDICATION

            ### UIs ###
            self.lineEdit_ip = self.MAINWINDOW.lineEdit_ip
            self.lineEdit_port = self.MAINWINDOW.lineEdit_port
            self.lineEdit_freq = self.MAINWINDOW.lineEdit_freq
            self.pushButton_connect = self.MAINWINDOW.pushButton_connect

            self.lineEdit_reg_NO_1 = self.MAINWINDOW.lineEdit_reg_NO_1

            ### local variables ###
            self.ip = ""
            self.port = None
            self.freq = None

            self.client = None

            self.connected = False

            self.read_thread = None
            self.is_read_treadd_working = False

            ### signal/slot ###
            self.pushButton_connect.clicked.connect(self.connect_disconnect)

        except Exception as err:
            console.print_exception()

    # def update_ui(self):
    #     pass

    def connect_disconnect(self):
        if not self.connected:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        try:
            self.ip = self.lineEdit_ip.text().strip().lower()
            self.port = self.lineEdit_port.text().strip().lower()

            uri = f"{self.ip}"

            self.logger.info(f"connecting to : {uri} ...")

            self.client = ModbusTcpClient(uri)
            self.client.connect()

            self.connected = True

            self.read_thread = threading.Thread(
                target=self.read_holding_registers_loop, daemon=True
            )
            self.read_thread.start()

        except Exception as err:
            console.print_exception()
        finally:
            self.connectionUpdatedSignal.emit(self.connected)

    def disconnect(self):
        try:
            self.client.close()
            self.connected = False

            while self.is_read_treadd_working:
                time.sleep(0.1)

            self.logger.warning(f"Disconnected from the MODBUS server already!")

        except Exception as err:
            console.print_exception()
        finally:
            self.connectionUpdatedSignal.emit(self.connected)

    def read_holding_registers(self):
        try:
            # self.logger.debug("read_holding_registers ...")
            first_reg_NO_ = int(self.lineEdit_reg_NO_1.text().strip())
            qty_ = 14
            result_ = self.client.read_holding_registers(first_reg_NO_, qty_)
            return result_.registers
        except Exception as err:
            console.print_exception()
            return []

    def read_holding_registers_loop(self):
        try:
            self.logger.info("read_holding_registers_loop has begun!")

            self.is_read_treadd_working = True
            self.freq = int(self.lineEdit_freq.text().strip())
            time_ = 1 / self.freq

            while self.connected:
                registers_ = self.read_holding_registers()
                self.registersUpdatedSignal.emit(registers_)
                # self.logger.debug(f"registers: {registers_}")
                time.sleep(time_)

            self.is_read_treadd_working = False

            self.logger.info("read_holding_registers_loop has stopped!")

        except Exception as err:
            console.print_exception()
