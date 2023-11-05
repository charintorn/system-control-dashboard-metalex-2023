import logging
import colorlog


class ColoredFormatter(logging.Formatter):
    """Custom Formatter to add colors to log messages"""

    def format(self, record):
        log_colors = {
            "DEBUG": "cyan",
            "INFO": "white",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        }
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)s] %(name)s :: %(message)s",
            log_colors=log_colors,
        )
        return formatter.format(record)


class Logger:
    def __init__(self, name=""):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)

        # Apply the colored formatter to the console handler
        formatter = ColoredFormatter()
        self.console_handler.setFormatter(formatter)

        self.logger.addHandler(self.console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == "__main__":
    # Example usage
    my_logger = Logger("example")
    my_logger.debug("This is a debug message")
    my_logger.info("This is an info message")
    my_logger.warning("This is a warning message")
    my_logger.error("This is an error message")
    my_logger.critical("This is a critical message")
