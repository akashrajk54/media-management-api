from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os


class DateRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, base_filename, **kwargs):
        self.base_filename = base_filename
        super().__init__(self.get_current_filename(), **kwargs)

    def get_current_filename(self):
        date_str = datetime.now().strftime("%d%m%Y")
        return os.path.join(
            os.path.dirname(self.base_filename), f"{date_str}_{os.path.basename(self.base_filename)}.log"
        )

    def doRollover(self):
        self.baseFilename = self.get_current_filename()
        super().doRollover()

    def emit(self, record):
        self.baseFilename = self.get_current_filename()
        super().emit(record)
