import sys

from ui.mainwindow import Ui_MainWindow
from ui.station_ur_widget import Ui_StationUrWidget
from ui.mir_dashboard_widget import Ui_MirDashboardWidget
from ui.mission_dashboard_widget import Ui_MissionDashboardWidget

from ui.MirUiInterface import MirUiInterface
from ui.UrUiInterface import UrUiInterface

# from ui.resources import resources_rc

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from modules.Logger import Logger
from modules.rich_setup import *

from modules.Database import Database
from modules.MirInterface import MirInterface
from modules.UrInterface import UrInterface


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # ############################## #

        ##### Logger #####
        self.logger = Logger("mainwindow")
        self.logger.debug("Initialzing ...")

        ##### Mainwindow #####
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.setGeometry(0, 25, self.width(), self.height())

        ##### Modules #####
        self.DATABASE = Database()
        #
        self.urInterface_1 = UrInterface(name_="urInterface_1")
        self.urInterface_2 = UrInterface(name_="urInterface_2")
        self.urInterface_3 = UrInterface(name_="urInterface_3")
        #
        self.mirInterface = MirInterface(
            name_="mirInterface",
            DATABASE_=self.DATABASE,
            urInterfaceList_=[
                self.urInterface_1,
                self.urInterface_2,
                self.urInterface_3,
            ],
        )

        ##### Actions #####
        self.actionFile_load.triggered.connect(self.DATABASE.load)
        self.actionFile_exit.triggered.connect(QApplication.instance().quit)

        ##### UIs #####
        ## Dashboard
        # Station 0
        self.stationUrWidget_0 = QWidget()
        ui_stationUrWidget_0 = Ui_StationUrWidget()
        ui_stationUrWidget_0.setupUi(self.stationUrWidget_0)
        self.verticalLayout_groupBox_station_0.addWidget(self.stationUrWidget_0)

        # Station 1
        self.stationUrWidget_1 = QWidget()
        ui_stationUrWidget_1 = Ui_StationUrWidget()
        ui_stationUrWidget_1.setupUi(self.stationUrWidget_1)
        self.verticalLayout_groupBox_station_1.addWidget(self.stationUrWidget_1)

        # Station 2
        self.stationUrWidget_2 = QWidget()
        ui_stationUrWidget_2 = Ui_StationUrWidget()
        ui_stationUrWidget_2.setupUi(self.stationUrWidget_2)
        self.verticalLayout_groupBox_station_2.addWidget(self.stationUrWidget_2)

        # Station 3
        self.stationUrWidget_3 = QWidget()
        ui_stationUrWidget_3 = Ui_StationUrWidget()
        ui_stationUrWidget_3.setupUi(self.stationUrWidget_3)
        self.verticalLayout_groupBox_station_3.addWidget(self.stationUrWidget_3)

        # MiR Dashboard
        self.mirDashboardWidget = QWidget()
        ui_mirDashboardWidget = Ui_MirDashboardWidget()
        ui_mirDashboardWidget.setupUi(self.mirDashboardWidget)
        self.verticalLayout_groupBox_mir.addWidget(self.mirDashboardWidget)

        ## Setting
        self.mirUiInterface = MirUiInterface(
            MAINWINDOW_=self, DATABASE_=self.DATABASE, mirInterface_=self.mirInterface
        )
        self.urUiInterfaceStation_1 = UrUiInterface(
            #
            name_="UR UI Interface #1",
            station_NO_=1,
            urInterface_=self.urInterface_1,
            #
            MAINWINDOW_=self,
            #
            input_ip_=self.lineEdit_ur_station_1_ip,
            input_freq_=self.lineEdit_setting_ur_freq,
            btn_connect_=self.pushButton_ur_station_1_connect,
            #
            comboBox_feed_in_type_8266_=self.comboBox_station_1_feed_in_sensor_type_8266,
            comboBox_feed_in_type_32_=self.comboBox_station_1_feed_in_sensor_type_32,
            comboBox_feed_in_NO_8266_=self.comboBox_station_1_feed_in_sensor_NO_8266,
            comboBox_feed_in_NO_32_=self.comboBox_station_1_feed_in_sensor_NO_32,
            comboBox_feed_out_type_8266_=self.comboBox_station_1_feed_out_sensor_type_8266,
            comboBox_feed_out_type_32_=self.comboBox_station_1_feed_out_sensor_type_32,
            comboBox_feed_out_NO_8266_=self.comboBox_station_1_feed_out_sensor_NO_8266,
            comboBox_feed_out_NO_32_=self.comboBox_station_1_feed_out_sensor_NO_32,
            #
            label_loop_freq_=self.label_setting_ur_modbus_loop_freq_1,
        )
        self.urUiInterfaceStation_2 = UrUiInterface(
            #
            name_="UR UI Interface #2",
            station_NO_=2,
            urInterface_=self.urInterface_2,
            #
            MAINWINDOW_=self,
            #
            input_ip_=self.lineEdit_ur_station_2_ip,
            input_freq_=self.lineEdit_setting_ur_freq,
            btn_connect_=self.pushButton_ur_station_2_connect,
            #
            comboBox_feed_in_type_8266_=self.comboBox_station_2_feed_in_sensor_type_8266,
            comboBox_feed_in_type_32_=self.comboBox_station_2_feed_in_sensor_type_32,
            comboBox_feed_in_NO_8266_=self.comboBox_station_2_feed_in_sensor_NO_8266,
            comboBox_feed_in_NO_32_=self.comboBox_station_2_feed_in_sensor_NO_32,
            comboBox_feed_out_type_8266_=self.comboBox_station_2_feed_out_sensor_type_8266,
            comboBox_feed_out_type_32_=self.comboBox_station_2_feed_out_sensor_type_32,
            comboBox_feed_out_NO_8266_=self.comboBox_station_2_feed_out_sensor_NO_8266,
            comboBox_feed_out_NO_32_=self.comboBox_station_2_feed_out_sensor_NO_32,
            #
            label_loop_freq_=self.label_setting_ur_modbus_loop_freq_2,
        )
        self.urUiInterfaceStation_3 = UrUiInterface(
            #
            name_="UR UI Interface #3",
            station_NO_=3,
            urInterface_=self.urInterface_3,
            #
            MAINWINDOW_=self,
            #
            input_ip_=self.lineEdit_ur_station_3_ip,
            input_freq_=self.lineEdit_setting_ur_freq,
            btn_connect_=self.pushButton_ur_station_3_connect,
            #
            comboBox_feed_in_type_8266_=self.comboBox_station_3_feed_in_sensor_type_8266,
            comboBox_feed_in_type_32_=self.comboBox_station_3_feed_in_sensor_type_32,
            comboBox_feed_in_NO_8266_=self.comboBox_station_3_feed_in_sensor_NO_8266,
            comboBox_feed_in_NO_32_=self.comboBox_station_3_feed_in_sensor_NO_32,
            comboBox_feed_out_type_8266_=self.comboBox_station_3_feed_out_sensor_type_8266,
            comboBox_feed_out_type_32_=self.comboBox_station_3_feed_out_sensor_type_32,
            comboBox_feed_out_NO_8266_=self.comboBox_station_3_feed_out_sensor_NO_8266,
            comboBox_feed_out_NO_32_=self.comboBox_station_3_feed_out_sensor_NO_32,
            #
            label_loop_freq_=self.label_setting_ur_modbus_loop_freq_3,
        )
        self.DATABASE.load()
        ### Modules ###

        ### Signal/SLot ###

    ### Update UIs ###


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
