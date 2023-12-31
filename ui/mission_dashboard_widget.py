# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mission_dashboard_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MissionDashboardWidget(object):
    def setupUi(self, MissionDashboardWidget):
        MissionDashboardWidget.setObjectName("MissionDashboardWidget")
        MissionDashboardWidget.resize(373, 41)
        MissionDashboardWidget.setStyleSheet("QWidget {\n"
"    background-color: rgb(255, 255, 255);\n"
"    padding: 0px;\n"
"    border-radius: 5px;\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(MissionDashboardWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_mission_name = QtWidgets.QLabel(MissionDashboardWidget)
        self.label_mission_name.setObjectName("label_mission_name")
        self.horizontalLayout.addWidget(self.label_mission_name)
        spacerItem = QtWidgets.QSpacerItem(251, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_delete = QtWidgets.QPushButton(MissionDashboardWidget)
        self.pushButton_delete.setStyleSheet("/* Default style */\n"
"QPushButton {\n"
"    background-color: rgb(255, 200, 200); /* Light red background */\n"
"    color: rgb(255, 0, 0);\n"
"    padding: 5px 10px;\n"
"    border-radius: 5px; \n"
"}\n"
"\n"
"/* Hover style */\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 0, 0);\n"
"    color: rgb(255, 255, 255);\n"
"    border-radius: 5px;\n"
"}\n"
"")
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.horizontalLayout.addWidget(self.pushButton_delete)

        self.retranslateUi(MissionDashboardWidget)
        QtCore.QMetaObject.connectSlotsByName(MissionDashboardWidget)

    def retranslateUi(self, MissionDashboardWidget):
        _translate = QtCore.QCoreApplication.translate
        MissionDashboardWidget.setWindowTitle(_translate("MissionDashboardWidget", "MissionDashboardWidget"))
        self.label_mission_name.setText(_translate("MissionDashboardWidget", "Mission name"))
        self.pushButton_delete.setText(_translate("MissionDashboardWidget", "x"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MissionDashboardWidget = QtWidgets.QWidget()
    ui = Ui_MissionDashboardWidget()
    ui.setupUi(MissionDashboardWidget)
    MissionDashboardWidget.show()
    sys.exit(app.exec_())
