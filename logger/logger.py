from constants.gloobal import GlobalConstants
from datetime import datetime
from helpers.datetimeconverter import format_common_date_time

import traceback

class Logger:
    log_file_path: str = None

    def __init__(self, log_file_path: str) -> None:
        self.log_file_path = log_file_path

    def _write_log_print(self, log: str, marker: str, write_output_to_screen: bool) -> None:
        try:
            log = f"[{marker}] [{format_common_date_time(datetime.now())}]: {log}"
            if write_output_to_screen:
                print(log)
            log = f"{log}\n"
            with open(self.log_file_path, "a") as log_file:
                log_file.write(log)
        except Exception as ex:
                print(f"{GlobalConstants.ERROR_CAPS}: Exception ({ex}) occured while writing logs")
                print(traceback.format_exc())
    
    def info(self, log: str, write_output_to_screen: bool = True) -> None:
        self._write_log_print(log, GlobalConstants.INFO_CAPS, write_output_to_screen)
    
    def error(self, log: str, write_output_to_screen: bool = True) -> None:
        self._write_log_print(log, GlobalConstants.ERROR_CAPS, write_output_to_screen)