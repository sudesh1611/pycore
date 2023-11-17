from configs import WebAppConfig
from constants import WebAppConstants
from logger import Logger
from report import ScanReport
from requests import post, get
from requests.auth import HTTPBasicAuth
from typing import Dict, List, Optional

import json
import traceback

class WebAppClient:
    _username: str
    _password: str
    _logger: Logger

    def __init__(self, log_file_path: str, username: str, password: str) -> None:
        self._logger = Logger(log_file_path)
        self._username = username
        self._password = password
    
    def get_all_scan_reports(self) -> List[ScanReport]:
        to_return: List[ScanReport] = []
        try:
            basic_auth = HTTPBasicAuth(self._username, self._password)
            self._logger.info(f"Getting scan reports from WebApp")
            headers = {
                "Content-Type":"application/json"
            }
            response = get(WebAppConfig.SCAN_REPORT_REST_API, auth=basic_auth, headers=headers, verify=WebAppConfig.VERIFY_WEBAPP_SERVER_CERTIFICATE)
            self._logger.info(f"Response Code: {response.status_code}")
            self._logger.info(f"Response: {response.json()}")
            if response.status_code == 200:
                item: Dict[str, str]
                for item in response.json():
                    to_return.append(ScanReport().fromJsonString(item))
            return to_return
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting all scan reports")
            self._logger.error(traceback.format_exc())
            return to_return
    
    def get_all_cve_and_jiras(self) -> Dict[str, List[List[str]]]:
        to_return = {}
        try:
            basic_auth = HTTPBasicAuth(self._username, self._password)
            self._logger.info(f"Getting CVE and Jira from WebApp")
            headers = {
                "Content-Type":"application/json"
            }
            response = get(WebAppConfig.CVE_JIRA_API, auth=basic_auth, headers=headers, verify=WebAppConfig.VERIFY_WEBAPP_SERVER_CERTIFICATE)
            self._logger.info(f"Response Code: {response.status_code}")
            self._logger.info(f"Response: {response.json()}")
            if response.status_code == 200:
                item: List[Dict[str, str]]
                for item in response.json():
                    to_return[item['cve_id']] = json.loads(item['jiras'])    
            return to_return
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting all cve and jiras")
            self._logger.error(traceback.format_exc())
            return to_return
    
    def add_cve_and_jira(self, cve_id: str, jira_id: str, status: str, summary: str) -> bool:
        try:
            self._logger.info(f"Adding CVE ID: {cve_id}, Jira ID: {jira_id}, Status: {status}, Summary: {summary}")
            basic_auth = HTTPBasicAuth(self._username, self._password)
            headers = {
                "Content-Type":"application/json"
            }
            response = post(
                WebAppConfig.CVE_JIRA_API,
                json={
                    WebAppConstants.CVE_ID: cve_id.upper(),
                    WebAppConstants.JIRAS: jira_id.upper(),
                    WebAppConstants.JIRA_STATUS: status,
                    WebAppConstants.JIRA_SUMMARY: summary
                },
                auth=basic_auth, headers=headers, verify=WebAppConfig.VERIFY_WEBAPP_SERVER_CERTIFICATE
            )
            self._logger.info(f"CVE, Jira Addition Response: {response.status_code}")
            if response.status_code!=200:
                self._logger.error(f"Error Response: {response.content}")
                return False
            return True
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while adding cve and jira")
            self._logger.error(traceback.format_exc())
            return False
    
    def save_scan_report_to_db(self, scan_report: ScanReport) -> Optional[str]:
        try:
            basic_auth = HTTPBasicAuth(self._username, self._password)
            self._logger.info(f"Saving scan report to database: {json.dumps(scan_report.toJson())}")
            headers = {
                "Content-Type":"application/json"
            }
            response = post(WebAppConfig.SCAN_REPORT_REST_API, json=scan_report.toJson(), auth=basic_auth, headers=headers, verify=WebAppConfig.VERIFY_WEBAPP_SERVER_CERTIFICATE)
            self._logger.info(f"Response Code: {response.status_code}")
            self._logger.info(f"Response: {response.text}")
            if response.status_code == 200:
                return response.json()['id']
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while saving scan report to db")
            self._logger.error(traceback.format_exc())