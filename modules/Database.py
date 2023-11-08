from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal


from modules.Logger import Logger
from modules.rich_setup import *

import json
import os


class Database(QObject):
    settingLoadedSignal = pyqtSignal(dict)

    def __init__(self, name_="Database"):
        super().__init__()
        try:
            self.NAME = name_
            #
            self.logger = Logger(self.NAME)
            self.logger.debug("Initilizing ...")
            #
        except Exception as err:
            console.print_exception()

    def load_settings(self):
        try:
            settings_file_path = os.path.join(
                os.path.dirname(__file__), "../settings.json"
            )
            with open(settings_file_path, "r") as settings_file:
                settings = json.load(settings_file)
            return settings
        except Exception as err:
            console.print_exception()

    def load(self):
        try:
            #
            self.logger.debug("load")
            #
            settings_ = self.load_settings()
            self.settingLoadedSignal.emit(settings_)
            # console.log(f"{type(settings_)} settings_ = {settings_}")
        except Exception as err:
            console.print_exception()
