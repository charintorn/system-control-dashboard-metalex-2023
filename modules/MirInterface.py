from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


from modules.Logger import Logger
from modules.rich_setup import *

import requests
import time
import uuid
import threading
import base64

from pymodbus.client import ModbusTcpClient


class ApiInterface(QObject):
    def __init__(
        self, name_="API Interface", ip_="", username_="", password_="", auth_key_=""
    ):
        super().__init__()
        #
        try:
            self.NAME = name_
            self.logger = Logger(name_)
            self.logger.debug("Initilizing ...")

            ### local variables ###
            self.ip = ip_
            self.username = username_
            self.password = password_
            self.auth_key = auth_key_
            #
            self.credential = ""
            self.auth_header = "Basic "

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Credentials ############################################################################### #
    # ########################################################################################### #
    def set_username(self, username_=""):
        try:
            self.logger.debug(f"set_username(username_={username_}):: ...")

            self.username = username_

        except Exception as err:
            console.print_exception()

    def set_password(self, password_=""):
        try:
            self.logger.debug(f"set_password(password_={password_}):: ...")

            self.password = password_

        except Exception as err:
            console.print_exception()

    def set_auth_key(self, auth_key_=""):
        try:
            self.logger.debug(f"set_auth_key(auth_key_={auth_key_}):: ...")

            self.auth_key = auth_key_

            self.auth_header = self.auth_key

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # URL ####################################################################################### #
    # ########################################################################################### #
    def set_ip(self, set_ip_=""):
        try:
            self.logger.debug(f"set_ip(set_ip_={set_ip_}):: ...")

            self.ip = set_ip_

        except Exception as err:
            console.print_exception()

    def _get_req_header(self):
        try:
            headers = {
                "accept": "application/json",
                "Authorization": self.auth_header,
                "Accept-Language": "en_US",
            }

            return headers

        except Exception as err:
            console.print_exception()
            return None

    def _get_base_url(self):
        try:
            return f"http://{self.ip}/api/v2.0.0"

        except Exception as err:
            console.print_exception()
            return None

    # ########################################################################################### #
    # API Request ############################################################################### #
    # ########################################################################################### #
    def api_request(self, method_="get", uri_="", body_={}):
        try:
            #
            self.logger.debug(
                f"api_request(method_={method_}, uri_={uri_}, body_={body_}):: ..."
            )
            #
            if uri_[0] == "/":
                uri_ = uri_[1:]
            #
            url_ = f"{self._get_base_url()}/{uri_}"
            self.logger.debug(f"api_request():: url_={url_}")
            #
            headers_ = self._get_req_header()
            #
            res = None
            data = None
            status_code = None
            #
            if method_ == "get":
                res = requests.get(url_, headers=headers_, json=body_, timeout=5)
                status_code = res.status_code
                if status_code != 200:
                    raise Exception(f"Cannot make GET request")
            elif method_ == "post":
                res = requests.post(url_, headers=headers_, json=body_, timeout=5)
                status_code = res.status_code
                if status_code != 201:
                    raise Exception(f"Cannot POST/Created data in Fleet!")
            elif method_ == "delete":
                res = requests.delete(url_, headers=headers_, json=body_, timeout=5)
                status_code = res.status_code
                if status_code != 204:
                    raise Exception(f"Cannot DELETE/remove data from Fleet!")
                return {"status_code": res.status_code}

            #
            data = {
                "status_code": res.status_code,
                "text": res.text,
                "data": res.json(),
            }
            return data

        except Exception as err:
            console.print_exception()
            return None
            # self.main_wn.app_dialog_manager.error.show(err, LABEL)


class ModbusInterface(QObject):
    #
    connectionChangedSignal = pyqtSignal(bool)
    readModbusUpdatedSignal = pyqtSignal(list)
    readModbusActualFrequencySignal = pyqtSignal(float)

    #
    def __init__(
        self,
        name_="ModbusInterface",
        ip_="192.168.12.",
        frequency_=1,
        start_addr_=1000,
        qty_=24,
        #
        DATABASE_=None,
        #
        urInterfaceList_=[],
    ):
        super().__init__()
        #
        try:
            self.NAME = name_
            self.logger = Logger(name_)
            self.logger.debug("Initilizing ...")

            ### local variables ###
            self.ip = ip_
            self.frequency = frequency_
            #
            self.modbus_start_addr = start_addr_
            self.modbus_qty = qty_
            #
            self.DATABASE = DATABASE_
            #
            self.urInterfaceList = urInterfaceList_
            #
            self.config = {}
            #
            self.write_registers = [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ]
            #
            self.modbus_thread = threading.Thread(
                target=self.read_holding_registers, daemon=True
            )
            self.modbus_thread_enable = False
            self.modbus_thread_working = False
            #
            self.urInterface_1 = None
            self.urInterface_2 = None
            self.urInterface_3 = None
            #
            for i in range(len(self.urInterfaceList)):
                if i == 0:
                    self.urInterface_1 = self.urInterfaceList[i]
                elif i == 1:
                    self.urInterface_2 = self.urInterfaceList[i]
                elif i == 2:
                    self.urInterface_3 = self.urInterfaceList[i]
            #
            ##### Custom Signals/Slots #####
            self.DATABASE.settingLoadedSignal.connect(self.settingLoadedSlot)
            #
            self.urInterface_1.inputsFetchedSignal.connect(
                lambda input_bits: self.urInputsFetchedSlot(input_bits, (8 * 1) - 8)
            )
            self.urInterface_2.inputsFetchedSignal.connect(
                lambda input_bits: self.urInputsFetchedSlot(input_bits, (8 * 2) - 8)
            )
            self.urInterface_3.inputsFetchedSignal.connect(
                lambda input_bits: self.urInputsFetchedSlot(input_bits, (8 * 3) - 8)
            )
        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Configuration ############################################################################# #
    # ########################################################################################### #
    def set_ip(self, ip_=""):
        try:
            self.logger.debug(f"set_ip(set_ip_ = {ip_}):: ...")

            self.ip = ip_

        except Exception as err:
            console.print_exception()

    def set_frequency(self, frequency_=1):
        try:
            self.logger.debug(f"set_frequency(frequency_ = {frequency_}) :: ...")

            self.frequency = frequency_

        except Exception as err:
            console.print_exception()

    def set_start_address(self, addr_=1):
        try:
            self.logger.debug(f"set_start_address(addr_ = {addr_}) :: ...")

            self.modbus_start_addr = (
                addr_ + 999
            )  # mir address starts at reg NO 1000 (MiR reg 1 = reg 1000)

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Connection ################################################################################ #
    # ########################################################################################### #
    def connect(self):
        try:
            uri_ = f"{self.ip}"

            self.logger.info(
                f"connect(): to {self.ip}, {self.modbus_start_addr}, {self.modbus_qty}, {self.frequency} ..."
            )

            self.client = ModbusTcpClient(uri_)
            self.client.connect()

            self.connected = True
            self.modbus_thread_enable = True

            self.modbus_thread = threading.Thread(
                target=self.read_write_loop, daemon=True
            )
            self.modbus_thread.start()
            self.logger.info(f"connected to {self.NAME} already.")

            self.connectionChangedSignal.emit(self.connected)

        except Exception as err:
            console.print_exception()

    def disconnect(self):
        try:
            self.logger.info(f"disconnect(): from {self.NAME} ...")
            self.modbus_thread_enable = False

            while self.modbus_thread_working:
                self.logger.debug(
                    f"{self.NAME} waiting for self.modbus_thread_working = False : {self.modbus_thread_working} ..."
                )
                time.sleep(0.1)

            self.client.close()
            self.connected = False

            self.logger.warning(f"Disconnected from `{self.NAME}`.")

            self.connectionChangedSignal.emit(self.connected)

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # MODBUS #################################################################################### #
    # ########################################################################################### #
    def read_holding_registers(self, reg_NO_=1000, qty_=24):
        try:
            # self.logger.debug(f"read_holding_register(reg_NO_ = {reg_NO_}) ...")
            result_ = self.client.read_holding_registers(reg_NO_, qty_)
            registers_ = result_.registers
            # self.logger.debug(
            #     f"read_holding_register({reg_NO_}, {qty_}) :: => {registers_}"
            # )
            return registers_
        except Exception as err:
            console.print_exception()
            raise err

    def read_write_loop(self):
        try:
            self.logger.info(f"read_write_loop(): has begun!, {self.frequency} Hz")
            #
            self.modbus_thread_working = True
            #
            time_ = 1 / self.frequency
            #
            prev_time_ = None
            #
            while self.modbus_thread_enable:
                try:
                    #
                    start_time_ = time.time()
                    #
                    self.client.write_registers(
                        address=self.modbus_start_addr,
                        values=self.write_registers,
                        slave=255,
                    )
                    #
                    read_registers_ = self.read_holding_registers(
                        self.modbus_start_addr, self.modbus_qty
                    )
                    # console.log(f"read_registers_: {read_registers_}")
                    # console.print(f"input_bits_ => {input_bits_}")

                    if read_registers_ != None:
                        self.readModbusUpdatedSignal.emit(read_registers_)
                    #
                    end_time_ = time.time()
                    #
                    if prev_time_ != None:
                        actual_freq_ = 1 / (end_time_ - prev_time_)
                        self.readModbusActualFrequencySignal.emit(actual_freq_)
                        # console.log(f"actual_freq_: {actual_freq_}")
                    prev_time_ = end_time_
                    #
                    period_ = end_time_ - start_time_
                    #
                    if period_ < time_:
                        time.sleep(time_ - period_)
                    #

                except Exception as err:
                    console.print_exception()
                    self.readModbusActualFrequencySignal.emit(0.0)

        except Exception as err:
            console.print_exception()
            # self.logger.error(f"read_holding_registers_loop():: {err.__str__()}")
        finally:
            self.modbus_thread_working = False
            self.logger.warning("read_holding_registers_loop has stopped!")

    ##### Custom Signals/Slots #####
    @pyqtSlot(dict)
    def settingLoadedSlot(self, settings_):
        try:
            self.config = settings_["mir"]
            self.logger.info(f"settingLoadedSlot({self.config}) :: ...")
            #
            self.set_ip(ip_=self.config["ip"])
            self.set_start_address(addr_=self.config["start_addr"])

        except Exception as err:
            console.print_exception()

    ### UR
    @pyqtSlot(list, int)
    def urInputsFetchedSlot(self, input_bits_=[], reg_idx_=None):
        try:
            for i in range(len(input_bits_)):
                self.write_registers[reg_idx_ + 1] = 1 if input_bits_[i] else 0
                reg_idx_ += 2  # Increment reg_idx_ by 2 for each iteration

            self.logger.debug(
                f"urInputsFetchedSlot: {reg_idx_} : {input_bits_} => {self.write_registers}"
            )
        except Exception as err:
            console.print_exception()


class MirInterface(QObject):
    connectionStateUpdatedSignal = pyqtSignal(bool)
    robotStatusFetchedSignal = pyqtSignal(dict)

    def __init__(
        self,
        name_="MiR Interface",
        ip_="",
        username_="",
        password_="",
        auth_key_="",
        #
        frequency_=1,
        start_addr_=1000,
        #
        DATABASE_=None,
        #
        urInterfaceList_=[],
    ):
        super().__init__()
        try:
            #
            self.logger = Logger(name_)
            self.logger.debug("Initilizing ...")
            #
            self.DATABASE = DATABASE_
            #
            self.API_INTERFACE = ApiInterface()
            self.MODBUS_INTERFACE = ModbusInterface(
                DATABASE_=self.DATABASE, urInterfaceList_=urInterfaceList_
            )
            #
            self.set_ip(ip_)
            self.set_username(username_)
            self.set_password(password_)
            self.set_auth_key(auth_key_)
            self.set_frequency(frequency_)
            self.set_modbus_start_addr(start_addr_)

            ### local variables ###
            self.frequency = frequency_
            #
            self.client = None
            self.connected = False

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Configurations ############################################################################ #
    # ########################################################################################### #
    def set_ip(self, ip_):
        self.API_INTERFACE.set_ip(ip_)
        self.MODBUS_INTERFACE.set_ip(ip_)

    def set_username(self, username_):
        self.API_INTERFACE.set_username(username_)

    def set_password(self, password_):
        self.API_INTERFACE.set_password(password_)

    def set_auth_key(self, password_):
        self.API_INTERFACE.set_auth_key(password_)

    def set_frequency(self, frequency_):
        try:
            self.logger.debug(f"set_frequency(frequency_ = {frequency_}) :: ...")
            self.MODBUS_INTERFACE.set_frequency(frequency_)
        except Exception as err:
            console.print_exception()

    def set_modbus_start_addr(self, addr_=1000):
        try:
            self.MODBUS_INTERFACE.set_start_address(addr_)
        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Connect/Disconnect ######################################################################## #
    # ########################################################################################### #
    def connect_disconnect(self):
        pass
        if not self.connected:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        try:
            self.MODBUS_INTERFACE.connect()
            #
            self.connected = True
            self.connectionStateUpdatedSignal.emit(self.connected)
        except Exception as err:
            console.print_exception()

    def disconnect(self):
        try:
            self.MODBUS_INTERFACE.disconnect()
            #
            self.connected = False
            self.connectionStateUpdatedSignal.emit(self.connected)
        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # robot status ############################################################################## #
    # ########################################################################################### #
    def read_robot_status(self):
        try:
            self.logger.debug(f"read_robot_status() :: ...")
            res_ = self.API_INTERFACE.api_request("get", "/status", {})
            return res_
        except Exception as err:
            console.print_exception()

    def read_robot_status_loop(self):
        try:
            self.modbus_thread_working = True
            self.logger.info("read_robot_status_loop has begun!")
            #
            while self.modbus_thread_enable:
                res_ = self.read_robot_status()

                if res_:
                    self.robotStatusFetchedSignal.emit(res_["data"])

                time.sleep(1 / float(self.frequency.strip()))
            #
            self.modbus_thread_working = False
            self.logger.warning("read_robot_status_loop has stopped!")
        except Exception as err:
            console.print_exception()
        finally:
            self.modbus_thread_working = False
