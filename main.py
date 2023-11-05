import sys

from ui.mainwindow import Ui_MainWindow
from ui.station_ur_widget import Ui_StationUrWidget
from ui.mir_dashboard_widget import Ui_MirDashboardWidget
from ui.mission_dashboard_widget import Ui_MissionDashboardWidget

# from ui.resources import resources_rc

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from modules.Logger import Logger
from modules.rich_setup import *

from modules.modbus import Modbus


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # ############################## #

        ### Logger ###
        self.logger = Logger("mainwindow")
        self.logger.debug("Initialzing ...")

        ### Mainwindow ###
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.setGeometry(0, 25, self.width(), self.height())

        ### Actions ###
        self.actionFile_exit.triggered.connect(QApplication.instance().quit)

        ### UIs ###
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

        # Test mission queue
        # self.missionDashboardWidget = QWidget()
        # ui_missionDashboardWidget = Ui_MissionDashboardWidget()
        # ui_missionDashboardWidget.setupUi(self.missionDashboardWidget)
        # # self.missionQueueSrollArea = (
        # ui_mirDashboardWidget.scrollArea_mission_queue_layout.addWidget(
        #     self.missionDashboardWidget
        # )

        ### Modules ###

        ### Signal/SLot ###

    ### Update UIs ###


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
