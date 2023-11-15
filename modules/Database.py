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
            self.base_path = ""

            if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
                # Running as a bundled executable
                self.base_path = sys._MEIPASS
            else:
                # Running in a normal Python environment
                self.base_path = os.path.abspath(".")
            #
            # Set the current working directory to the directory of the executable
            os.chdir(self.base_path)
            #
            self.logger.info(f"base_path: {self.base_path}")
            #
            self.settings_file_path = os.path.join(self.base_path, "settings.json")
            #
            self.get_mir_config = None
            self.get_ur_1_config = None
            self.get_ur_2_config = None
            self.get_ur_3_config = None
        except Exception as err:
            console.print_exception()

    def load_settings(self):
        try:
            with open(self.settings_file_path, "r") as settings_file:
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

    def save(self):
        try:
            #
            self.logger.debug("save() :: ...")
            #
            mir_config_ = self.get_mir_config()
            ur_1_config_ = self.get_ur_1_config()
            ur_2_config_ = self.get_ur_2_config()
            ur_3_config_ = self.get_ur_3_config()
            #
            # console.log(f"mir_config_: {mir_config_}")
            # console.log(f"ur_1_config_: {ur_1_config_}")
            #
            settings_ = {
                "mir": mir_config_,
                "ur": [ur_1_config_, ur_2_config_, ur_3_config_],
            }
            #
            self.logger.info(f"\t > settings: {settings_}")

            # Save the settings to a JSON file
            with open(self.settings_file_path, "w") as settings_file:
                json.dump(settings_, settings_file, indent=4)

            self.logger.info("Settings saved successfully.")
        except Exception as err:
            console.print_exception()
