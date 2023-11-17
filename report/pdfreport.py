from ..configs import PdfReportConfig, WebAppConfig
from ..constants import WebAppConstants
from ..logger import Logger
from base64 import b64decode
from selenium import webdriver
from selenium.webdriver.common.print_page_options import PrintOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import traceback

class PdfReport:
    driver: webdriver.Firefox
    _logger: Logger

    def __init__(self, log_file_path: str) -> None:          
        options = Options()
        options.add_argument("-headless")
        options.binary = FirefoxBinary(PdfReportConfig.FIREFOX_WEB_DRIVER_BINARY_ABS_PATH)
        self.driver = webdriver.Firefox(options=options)
        self.driver.set_window_size(3840, 2400)
        self._logger = Logger(log_file_path)
    
    def save_pdf(self, scan_id: str, image_id: int, dest_abs_path: str, timeout = 60) -> bool:
        retry_counter = 3
        while(retry_counter):
            self._logger.info(f"Generating pdf for image {image_id}")
            retry_counter = retry_counter - 1
            try:
                if type_filter is None:
                    type_filter = "Default"
                if image_filter is None:
                    image_filter = "Default"
                self.driver.get(f'{WebAppConfig.REPORT_DETAILS_PREFIX_URL}{WebAppConstants.SCAN_ID}={scan_id}&{WebAppConstants.IMAGE_ID}={image_id}')
                self.driver.maximize_window()
                try:
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.ID, 'processingDone'))
                    )
                except Exception:
                    self._logger.error(f"Timeout Occurred While Generating pdf for image {image_id}")
                    continue
                prntOptions = PrintOptions()
                prntOptions.orientation = "portrait"
                prntOptions.background = True
                prntOptions.margin_left = 0
                prntOptions.margin_right = 0
                prntOptions.margin_top = 0
                prntOptions.margin_bottom = 0
                prntOptions.shrink_to_fit = True
                prntOptions.page_width = 40
                prntOptions.page_height = 100
                pdf = b64decode(self.driver.print_page(prntOptions))
                with open(dest_abs_path, 'wb') as f:
                        f.write(pdf)
                self.driver.quit()
                self._logger.info(f"Generated pdf for image {image_id}")
                return True
            except Exception as ex:
                 self._logger.error(f"Exception {ex} occurred While Generating pdf for image {image_id}")
                 self._logger.error(traceback.format_exc())
        return False
