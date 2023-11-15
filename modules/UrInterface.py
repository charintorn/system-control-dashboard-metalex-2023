from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal


from modules.Logger import Logger
from modules.rich_setup import *

import time
import uuid
import threading

from pymodbus.client import ModbusTcpClient


class UrInterface(QObject):
    connectionChangedSignal = pyqtSignal(bool)
    inputsFetchedSignal = pyqtSignal(list)
    modbusLoopFrequencySignal = pyqtSignal(float)

    def __init__(
        self,
        name_="UR Interface",
        #
        ip_="",
        freq_=1,
        #
        input_types_=["DI", "DI", "DI", "DI"],
        input_NOs_=[0, 1, 2, 3],
    ):
        super().__init__()
        try:
            #
            self.NAME = name_
            #
            self.logger = Logger(self.NAME)
            self.logger.debug("Initilizing ...")

            ### local variables ###
            #
            self.ip = ip_
            self.freq = freq_
            #
            self.input_types = []
            self.input_NOs = []
            self.set_input_types(input_types_)
            self.set_input_NOs(input_NOs_)
            #
            self.client = None
            self.connected = False
            #
            self.read_thread = None
            self.read_thread_enable = None
            self.read_thread_working = False

            ### signal/slot ###

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Configuration ############################################################################# #
    # ########################################################################################### #
    def set_ip(self, ip_="127.0.0.1"):
        try:
            self.ip = ip_

        except Exception as err:
            console.print_exception()

    def set_frequency(self, frequency_=1):
        try:
            self.freq = frequency_

        except Exception as err:
            console.print_exception()

    def set_input_types(self, types_=["DI", "DI", "DI", "DI"]):
        try:
            self.input_types = types_

        except Exception as err:
            console.print_exception()

    def set_input_NOs(self, NOs_=[0, 1, 2, 3]):
        try:
            # self.logger.info(f"set_input_NOs: {NOs_}")
            self.input_NOs = NOs_

        except Exception as err:
            console.print_exception()

    def get_config(self):
        try:
            config_ = {
                "ip": self.ip,
                "types": self.input_types,
                "NO": self.input_NOs,
            }

            return config_

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Connection ################################################################################ #
    # ########################################################################################### #
    def connect_disconnect(self):
        #
        if not self.connected:
            self.connect()
        else:
            self.disconnect()
        #

    def connect(self):
        try:
            uri_ = f"{self.ip}"

            self.logger.info(f"connect(): to {self.NAME} : {uri_} ...")

            self.client = ModbusTcpClient(uri_)
            self.client.connect()

            self.connected = True
            self.read_thread_enable = True

            self.read_thread = threading.Thread(
                target=self.read_holding_registers_loop, daemon=True
            )
            self.read_thread.start()
            self.logger.info(f"connected to {self.NAME} already.")

            self.connectionChangedSignal.emit(self.connected)

        except Exception as err:
            console.print_exception()

    def disconnect(self):
        try:
            self.logger.info(f"disconnect(): from {self.NAME} ...")
            self.read_thread_enable = False

            while self.read_thread_working:
                self.logger.debug(
                    f"{self.NAME} waiting for self.read_thread_working = False : {self.read_thread_working} ..."
                )
                time.sleep(0.1)

            self.client.close()
            self.connected = False

            self.logger.warning(f"Disconnected from `{self.NAME}`.")

            self.connectionChangedSignal.emit(self.connected)

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # reading registers ######################################################################### #
    # ########################################################################################### #
    def read_single_register(self, reg_NO_=None):
        try:
            # self.logger.debug(f"read_single_register(reg_NO_ = {reg_NO_}) ...")
            qty_ = 1
            result_ = self.client.read_holding_registers(reg_NO_, qty_)
            # self.logger.debug(
            #     f"read_single_register(reg_NO_ = {reg_NO_}) :: => {result_.registers}"
            # )
            return result_.registers
        except Exception as err:
            console.print_exception()
            return None

    def read_holding_registers_loop(self):
        try:
            self.logger.info(
                f"read_holding_registers_loop(): has begun!, {self.freq} Hz"
            )
            #
            self.read_thread_working = True
            #
            # console.log(f"self.input_types: {self.input_types}")
            # console.log(f"self.input_NOs: {self.input_NOs}")
            #
            #
            time_ = 1 / self.freq
            #
            prev_time_ = None
            #
            while self.read_thread_enable:
                try:
                    #
                    start_time_ = time.time()
                    #
                    di_register_ = self.read_single_register(reg_NO_=0)[0]
                    ci_register_ = self.read_single_register(reg_NO_=30)[0]
                    # self.logger.debug(f"di_register_ = {di_register_}")
                    # self.logger.debug(f"ci_register_ = {ci_register_}")
                    #
                    input_bits_ = [None, None, None, None]

                    # Read feed-in and feed-out based on input type
                    for i in range(len(input_bits_)):
                        #

                        type_ = self.input_types[i]
                        NO_ = self.input_NOs[i]
                        #
                        # console.log(f"-> {i}: {type_}:{NO_}")

                        if type_ == "DI":
                            input_bits_[i] = ((di_register_ >> NO_) & 1) == 1
                        else:  # "CI"
                            input_bits_[i] = ((ci_register_ >> NO_) & 1) == 1
                    #
                    # console.print(f"input_bits_ => {input_bits_}")
                    self.inputsFetchedSignal.emit(input_bits_)
                    #
                    end_time_ = time.time()
                    if prev_time_ != None:
                        actual_freq_ = 1 / (end_time_ - prev_time_)
                        self.modbusLoopFrequencySignal.emit(actual_freq_)
                    prev_time_ = end_time_
                    #
                    period_ = end_time_ - start_time_
                    #
                    #
                    if period_ < time_:
                        time.sleep(time_ - period_)
                    #
                except Exception as err:
                    console.print_exception()

        except Exception as err:
            console.print_exception()
            # self.logger.error(f"read_holding_registers_loop():: {err.__str__()}")
        finally:
            self.read_thread_working = False
            self.logger.warning("read_holding_registers_loop has stopped!")
