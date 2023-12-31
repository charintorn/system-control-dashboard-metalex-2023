from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


from modules.Logger import Logger
from modules.rich_setup import *

from modules.UrInterface import UrInterface


class UrUiInterface(QObject):
    def __init__(
        self,
        #
        name_="UR UI Interface",
        station_NO_=0,
        urInterface_=None,
        #
        MAINWINDOW_=None,
        #
        input_ip_=None,
        input_freq_=None,
        btn_connect_=None,
        #
        comboBox_feed_in_type_8266_=None,
        comboBox_feed_in_type_32_=None,
        comboBox_feed_in_NO_8266_=None,
        comboBox_feed_in_NO_32_=None,
        comboBox_feed_out_type_8266_=None,
        comboBox_feed_out_type_32_=None,
        comboBox_feed_out_NO_8266_=None,
        comboBox_feed_out_NO_32_=None,
        #
        label_loop_freq_=None
        #
    ):
        super().__init__()
        #
        try:
            #
            self.NAME = name_
            self.station_NO = station_NO_
            self.urInterface = urInterface_
            #
            self.logger = Logger(self.NAME)
            self.logger.debug("Initilizing ...")

            ##### UIs #####
            self.MAINWINDOW = MAINWINDOW_
            #
            self.input_ip = input_ip_
            self.input_frequency = input_freq_
            self.btn_connect = btn_connect_
            #
            self.comboBox_feed_in_type_8266 = comboBox_feed_in_type_8266_
            self.comboBox_feed_in_type_32 = comboBox_feed_in_type_32_
            self.comboBox_feed_in_NO_8266 = comboBox_feed_in_NO_8266_
            self.comboBox_feed_in_NO_32 = comboBox_feed_in_NO_32_
            self.comboBox_feed_out_type_8266 = comboBox_feed_out_type_8266_
            self.comboBox_feed_out_type_32 = comboBox_feed_out_type_32_
            self.comboBox_feed_out_NO_8266 = comboBox_feed_out_NO_8266_
            self.comboBox_feed_out_NO_32 = comboBox_feed_out_NO_32_
            #
            self.label_loop_freq = label_loop_freq_

            ##### Local variables #####
            self.connected = False
            self.config = {}

            ##### UI Signals/Slots #####
            self.btn_connect.clicked.connect(self.on_connect_btn_clicked)
            self.input_ip.textChanged.connect(self.on_input_ip_changed)
            self.comboBox_feed_in_type_8266.currentIndexChanged.connect(
                self.on_input_type_changed
            )
            self.comboBox_feed_in_type_32.currentIndexChanged.connect(
                self.on_input_type_changed
            )
            self.comboBox_feed_out_type_8266.currentIndexChanged.connect(
                self.on_input_type_changed
            )
            self.comboBox_feed_out_type_32.currentIndexChanged.connect(
                self.on_input_type_changed
            )
            #
            self.comboBox_feed_in_NO_8266.currentIndexChanged.connect(
                self.on_input_NO_changed
            )
            self.comboBox_feed_in_NO_32.currentIndexChanged.connect(
                self.on_input_NO_changed
            )
            self.comboBox_feed_out_NO_8266.currentIndexChanged.connect(
                self.on_input_NO_changed
            )
            self.comboBox_feed_out_NO_32.currentIndexChanged.connect(
                self.on_input_NO_changed
            )
            ##### Custom Signals/Slots #####
            self.MAINWINDOW.DATABASE.settingLoadedSignal.connect(self.settingLoadedSlot)

            ##### Initialize #####
            self.urInterface.connectionChangedSignal.connect(self.connectionChangedSlot)
            self.urInterface.inputsFetchedSignal.connect(self.inputsFetchedSlot)
            self.urInterface.modbusLoopFrequencySignal.connect(
                self.modbusLoopFrequencySlot
            )

        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # UIs ####################################################################################### #
    # ########################################################################################### #
    def update_ui(self):
        try:
            # Inputs enable state
            enable_input = not self.connected

            # Text inputs
            self.input_ip.setEnabled(enable_input)
            self.comboBox_feed_in_type_8266.setEnabled(enable_input)
            self.comboBox_feed_in_type_32.setEnabled(enable_input)
            self.comboBox_feed_in_NO_8266.setEnabled(enable_input)
            self.comboBox_feed_in_NO_32.setEnabled(enable_input)
            self.comboBox_feed_out_type_8266.setEnabled(enable_input)
            self.comboBox_feed_out_type_32.setEnabled(enable_input)
            self.comboBox_feed_out_NO_8266.setEnabled(enable_input)
            self.comboBox_feed_out_NO_32.setEnabled(enable_input)

            # Button text and style
            if self.connected:
                self.btn_connect.setText("Disconnect")
                self.btn_connect.setStyleSheet("background-color: red; color: white;")
            else:
                self.btn_connect.setText("Connect")
                self.btn_connect.setStyleSheet("background-color: none; color: none;")

        except Exception as err:
            console.print_exception()

    def update_combobox_color(self, input_list_=[False, False, False, False]):
        try:
            comboBox_list_ = [
                self.comboBox_feed_in_NO_8266,
                self.comboBox_feed_in_NO_32,
                self.comboBox_feed_out_NO_8266,
                self.comboBox_feed_out_NO_32,
            ]

            for i in range(len(comboBox_list_)):
                input_on_ = input_list_[i]
                color_ = "green" if input_on_ else "none;"
                font_color_ = "white" if input_on_ else "none;"
                comboBox_list_[i].setStyleSheet(
                    f"background-color: {color_}; color: {font_color_}"
                )

        except Exception as err:
            console.print_exception()

    def update_actual_freq_label(self, actual_freq_=0.0):
        try:
            self.label_loop_freq.setText(str("{:10.4f}".format(actual_freq_)))
            #
            if actual_freq_ > 0.0:
                self.label_loop_freq.setStyleSheet("background-color: #DCEDC8;")
            else:
                self.label_loop_freq.setStyleSheet("background-color: #FFCDD2;")
        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # UI Slots ################################################################################## #
    # ########################################################################################### #
    @pyqtSlot()
    def on_connect_btn_clicked(self):
        try:
            self.logger.debug(
                f"on_connect_btn_clicked(): self.connected = {self.connected}..."
            )
            #
            #
            #
            if not self.connected:
                self.urInterface.set_frequency(
                    frequency_=float(self.input_frequency.text().strip())
                )
                #
                self.urInterface.connect()
            else:
                self.urInterface.disconnect()
            #
            #
            #
        except Exception as err:
            console.print_exception()

    @pyqtSlot(str)
    def on_input_ip_changed(self, text):
        try:
            self.urInterface.set_ip(ip_=self.input_ip.text().strip())
        except Exception as err:
            console.print_exception()

    @pyqtSlot(int)
    def on_input_type_changed(self, idx):
        try:
            # console.log(f"on_input_type_changed: {idx}")
            self.urInterface.set_input_types(
                [
                    self.comboBox_feed_in_type_8266.currentText().strip(),
                    self.comboBox_feed_in_type_32.currentText().strip(),
                    self.comboBox_feed_out_type_8266.currentText().strip(),
                    self.comboBox_feed_out_type_32.currentText().strip(),
                ]
            )
        except Exception as err:
            console.print_exception()

    @pyqtSlot(int)
    def on_input_NO_changed(self, idx):
        try:
            # console.log(f"on_input_NO_changed: {idx}")
            self.urInterface.set_input_NOs(
                [
                    int(self.comboBox_feed_in_NO_8266.currentText().strip()),
                    int(self.comboBox_feed_in_NO_32.currentText().strip()),
                    int(self.comboBox_feed_out_NO_8266.currentText().strip()),
                    int(self.comboBox_feed_out_NO_32.currentText().strip()),
                ]
            )
        except Exception as err:
            console.print_exception()

    # ########################################################################################### #
    # Signal Slots ############################################################################## #
    # ########################################################################################### #
    ### Settings
    @pyqtSlot(dict)
    def settingLoadedSlot(self, settings_):
        try:
            self.logger.debug(
                f"station {self.station_NO}, settingLoadedSlot(settings) ..."
            )
            #
            self.config = settings_["ur"][self.station_NO - 1]
            self.logger.debug(f"\t > config: {self.config} ...")
            #
            self.input_ip.setText(self.config["ip"])
            #
            self.comboBox_feed_in_type_8266.setCurrentText(self.config["types"][0])
            self.comboBox_feed_in_type_32.setCurrentText(self.config["types"][1])
            self.comboBox_feed_out_type_32.setCurrentText(self.config["types"][2])
            self.comboBox_feed_out_NO_8266.setCurrentText(self.config["types"][3])
            #
            self.comboBox_feed_in_NO_8266.setCurrentText(str(self.config["NO"][0]))
            self.comboBox_feed_in_NO_32.setCurrentText(str(self.config["NO"][1]))
            self.comboBox_feed_out_NO_8266.setCurrentText(str(self.config["NO"][2]))
            self.comboBox_feed_out_NO_32.setCurrentText(str(self.config["NO"][3]))
            #
            # Set the autual UR interface
            self.urInterface.set_ip(self.config["ip"])
            self.urInterface.set_input_types(self.config["types"])
            self.urInterface.set_input_NOs(self.config["NO"])
        except Exception as err:
            console.print_exception()

    ### Modbus
    @pyqtSlot(bool)
    def connectionChangedSlot(self, connected_):
        try:
            self.logger.debug(f"connectionChangedSlot(connected_={connected_}) ...")
            self.connected = connected_

            self.update_ui()
            self.inputsFetchedSlot([False, False, False, False])
        except Exception as err:
            console.print_exception()

    @pyqtSlot(list)
    def inputsFetchedSlot(self, input_list_):
        try:
            self.logger.debug(f"inputsFetchedSlot(input_list_={input_list_}) ...")
            self.update_combobox_color(input_list_)
            pass
        except Exception as err:
            console.print_exception()

    @pyqtSlot(float)
    def modbusLoopFrequencySlot(self, actual_freq_):
        try:
            # self.logger.debug(
            #     f"modbusLoopFrequencySlot(actual_freq_ = {actual_freq_}) ..."
            # )
            self.update_actual_freq_label(actual_freq_)
            pass
        except Exception as err:
            console.print_exception()
