from compliance import ComplianceManager
from configs import TwistlockClientConfig
from constants import CveConstants, GlobalConstants, ProcessedReportConstants, TwistlockClientConstants, TwistlockReportParserConstants
from cve import CveManager
from datetime import datetime, timedelta
from helpers.datetimeconverter import format_common_date_time, parse_twistlock_date_time
from logger import Logger
from package import PackageManager
from report import ProcessedReport
from time import sleep
from typing import Any, Dict, List, Optional

import json
import requests
import traceback

class TwistlockClient:
    _logger: Logger
    _token: str
    _username: str
    _password: str
    _token_expiry_date: datetime
    def __init__(self, log_file_location: str, username: str, password: str) -> None:
        self._username = username.replace('\\\\', '\\')
        self._password = password
        self._token = None
        self._token_expiry_date = None
        self._logger = Logger(log_file_location)
    
    def _generate_token(self) -> Optional[str]:
        try:
            payload = json.dumps({
                GlobalConstants.USERNAME: self._username,
                GlobalConstants.PASSWORD: self._password
            })
            headers = {
            GlobalConstants.CONTENT_TYPE: GlobalConstants.APPLICATION_JSON,
            GlobalConstants.ACCEPT: GlobalConstants.APPLICATION_JSON
            }
            self._token_expiry_date = datetime.now() + timedelta(minutes=TwistlockClientConfig.TOKEN_EXPIRY_SPAN)
            response = requests.request("POST", TwistlockClientConfig.AUTHENTICATE_API, headers=headers, data=payload, verify=TwistlockClientConfig.VERIFY_TWISTLOCK_SERVER_CERTIFICATE)
            self._logger.info(f"Twistlock Authenticate API status code: {response.status_code}")
            self._logger.info(f"Twistlock Authenticate API Response: {response.json()}")
            self._token = response.json()['token']
            self._logger.info(f"Generated Token: {self._token}")
            return self._token
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while generating token")
            self._logger.error(traceback.format_exc())
            return None
    
    def get_token(self) -> str:
        if self._token is None or self._token_expiry_date is None or self._token_expiry_date < datetime.now():
            self._logger.info("Generating New Twistlock Token...")
            return self._generate_token()
        else:
            self._logger.info("Using Already Generated Twistlock Token...")
            return self._token
    
    def _generate_auth_header(self) -> Dict[str, str]:
        token: str = self.get_token()
        if token:
            return {
                GlobalConstants.AUTHORIZATION: f"{GlobalConstants.BEARER} {token}",
                GlobalConstants.CONTENT_TYPE: GlobalConstants.APPLICATION_JSON,
                GlobalConstants.ACCEPT: GlobalConstants.APPLICATION_JSON
            }
        else:
            self._logger.error("Unable to generate auth token for twistlock. Exiting...")
            raise Exception("Unable to generate auth token for twistlock")
    
    def get_full_hostname_from_hostname(self, short_hostname: str, if_fail_on_non_existance: bool = True) -> Optional[str]:
        try:
            params = {
                TwistlockClientConstants.PROJECT: TwistlockClientConfig.PROJECT_VALUE,
                GlobalConstants.SEARCH: short_hostname,
                GlobalConstants.LIMIT: 1,
                GlobalConstants.FIELDS: [
                    GlobalConstants.HOSTNAME,
                ],
                "compact": True
            }
            response = requests.get(TwistlockClientConfig.HOST_INFO_API, params=params, headers=self._generate_auth_header(), verify=TwistlockClientConfig.VERIFY_TWISTLOCK_SERVER_CERTIFICATE)
            self._logger.info(f"Twistlock Host Info API Response: {response.text}")
            response_json = response.json()
            if response_json is None or len(response_json) != 1:
                self._logger.error(f"Unable to get hostname from Twistlock")
                if if_fail_on_non_existance:
                    raise Exception(f"Unable to get hostname from Twistlock")
                else:
                    return None
            else:
                self._logger.info(f"Full Hostname: {response.json()[0]['hostname']}")
                return response.json()[0][GlobalConstants.HOSTNAME]
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting hostname for: {short_hostname}")
            self._logger.error(traceback.format_exc())
            return None
    
    def get_host_report_from_host(self, short_hostname: str) -> Dict[str, Any]:
        try:
            hostname = self.get_full_hostname_from_hostname(short_hostname)
            params = {
                TwistlockClientConstants.PROJECT: TwistlockClientConfig.PROJECT_VALUE,
                GlobalConstants.HOSTNAME: hostname,
                GlobalConstants.LIMIT: 1
                
            }
            response = requests.get(TwistlockClientConfig.HOST_REPORT_API, params=params, headers=self._generate_auth_header(), verify=TwistlockClientConfig.VERIFY_TWISTLOCK_SERVER_CERTIFICATE)
            self._logger.info(f"Twistlock Host Report API Response: {response.text}")
            response_json = response.json()
            if response_json is None or len(response_json) != 1:
                self._logger.error(f"Unable to get host report from Twistlock")
                return {}
            else:
                return response.json()[0]
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting host report for: {short_hostname}")
            self._logger.error(traceback.format_exc())
            return {}
    
    def get_image_names_from_host(self, short_hostname: str) -> List[str]:
        image_names: List[str] = []
        try:
            hostname = self.get_full_hostname_from_hostname(short_hostname)
            offset = 0
            limit = 40
            results_returned = limit
            while(results_returned >= limit):
                offset = len(image_names)
                params = {
                    TwistlockClientConstants.PROJECT: TwistlockClientConfig.PROJECT_VALUE,
                    GlobalConstants.HOSTNAME: hostname,
                    GlobalConstants.OFFSET: offset,
                    GlobalConstants.LIMIT: limit
                }
                response = requests.get(TwistlockClientConfig.IMAGE_NAMES_API, params=params, headers=self._generate_auth_header(), verify=TwistlockClientConfig.VERIFY_TWISTLOCK_SERVER_CERTIFICATE)
                self._logger.info(f"Twistlock Image API Response: {response.text}")
                if response.json() is None:
                    return image_names
                results_returned = len(response.json())
                image_names = list(set(image_names + response.json()))
                sleep(2)
            return image_names
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting image names for: {short_hostname}")
            self._logger.error(traceback.format_exc())
            return image_names
    
    def get_image_results_from_host(self, short_hostname: str) -> List[Dict[Any, Any]]:
        image_data: List[Dict[Any, Any]] = []
        try:
            hostname = self.get_full_hostname_from_hostname(short_hostname)
            offset = 0
            limit = 10
            results_returned = limit
            while(results_returned >= limit):
                sleep(5)
                offset = len(image_data)
                params = {
                    TwistlockClientConstants.PROJECT: TwistlockClientConfig.PROJECT_VALUE,
                    GlobalConstants.HOSTNAME: hostname,
                    GlobalConstants.OFFSET: offset,
                    GlobalConstants.LIMIT: limit
                }
                response = requests.get(TwistlockClientConfig.IMAGE_REPORT_API, params=params, headers=self._generate_auth_header(), verify=TwistlockClientConfig.VERIFY_TWISTLOCK_SERVER_CERTIFICATE)
                self._logger.info(f"Image Report API Response: {response.text}")
                if response.json() is None:
                    return image_data
                results_returned = len(response.json())
                img_data: Dict[str, Any]
                for img_data in response.json():
                    filtered_img_data: Dict[str, Any] = {}
                    for key, value in img_data.items():
                        if key in [
                            TwistlockReportParserConstants.SECRETS,
                            TwistlockReportParserConstants.OSDISTRO,
                            TwistlockReportParserConstants.OSDISTROVERSION,
                            TwistlockReportParserConstants.OSDISTRORELEASE,
                            TwistlockReportParserConstants.DISTRO,
                            TwistlockReportParserConstants.PACKAGES,
                            TwistlockReportParserConstants.APPLICATIONS,
                            TwistlockReportParserConstants.ID,
                            TwistlockReportParserConstants.COMPLIANCEISSUES,
                            TwistlockReportParserConstants.VULNERABILITIES,
                            TwistlockReportParserConstants.REPOTAG,
                            TwistlockReportParserConstants.TAGS,
                            TwistlockReportParserConstants.NAMESPACES
                            ]:
                            filtered_img_data[key] = value
                    image_data.append(filtered_img_data)
            return image_data
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting images report for: {short_hostname}")
            self._logger.error(traceback.format_exc())
            return image_data


class TwistlockReportParser:
    _processed_report: ProcessedReport
    _logger: Logger

    def __init__(self, log_file_path: str, twistlock_json_report_result: Dict[str, Any]) -> None:
        self._logger = Logger(log_file_path)
        package_manager = PackageManager()
        cve_manager = CveManager(log_file_path)
        compliance_manager = ComplianceManager(log_file_path)
        id: str = twistlock_json_report_result.get(TwistlockReportParserConstants.ID)
        name: str = twistlock_json_report_result.get(ProcessedReportConstants.NAME)
        repo_tag: Dict[str, str] = twistlock_json_report_result.get(TwistlockReportParserConstants.REPOTAG)
        if repo_tag:
            name = f"{repo_tag.get('registry')}/{repo_tag.get('repo')}/{repo_tag.get('tag')}"
        distro: str = twistlock_json_report_result.get(ProcessedReportConstants.DISTRO)
        distro_version: str = twistlock_json_report_result.get(ProcessedReportConstants.DISTRORELEASE)
        distro_version = twistlock_json_report_result.get(TwistlockReportParserConstants.OSDISTROVERSION)
        digest: str = twistlock_json_report_result.get(ProcessedReportConstants.DIGEST)
        if not digest:
            digest = id
        namespaces = twistlock_json_report_result.get(TwistlockReportParserConstants.NAMESPACES)
        if type(namespaces) is list:
            namespaces = ", ".join(namespaces)
        secrets = twistlock_json_report_result.get(TwistlockReportParserConstants.SECRETS)
        if type(secrets) is list:
            secrets = ", ".join(secrets)
        if twistlock_json_report_result.get(TwistlockReportParserConstants.PACKAGES) and TwistlockReportParserConstants.PKGS in twistlock_json_report_result.get(TwistlockReportParserConstants.PACKAGES):
            package: Dict[str, Any]
            for package in twistlock_json_report_result.get(TwistlockReportParserConstants.PACKAGES):
                package_type: str = package.get(TwistlockReportParserConstants.PKGSTYPE)
                package = package.get(TwistlockReportParserConstants.PKGS)
                package_manager.add_package(package.get(ProcessedReportConstants.NAME), package.get(ProcessedReportConstants.VERSION), package_type, package.get(ProcessedReportConstants.PATH))
        else:
            package: Dict[str, Any]
            for package in twistlock_json_report_result.get(TwistlockReportParserConstants.PACKAGES):
                package_manager.add_package(package.get(ProcessedReportConstants.NAME), package.get(ProcessedReportConstants.VERSION), package.get(ProcessedReportConstants.TYPE), package.get(ProcessedReportConstants.PATH))
        if twistlock_json_report_result.get(TwistlockReportParserConstants.APPLICATIONS):
            application: Dict[str, Any]
            for application in twistlock_json_report_result.get(TwistlockReportParserConstants.APPLICATIONS):
                package_manager.add_package(application.get(ProcessedReportConstants.NAME), application.get(ProcessedReportConstants.VERSION), None, application.get(ProcessedReportConstants.PATH))
        if twistlock_json_report_result.get(TwistlockReportParserConstants.VULNERABILITIES):
            vulnerability: Dict[str, Any]
            for vulnerability in twistlock_json_report_result.get(TwistlockReportParserConstants.VULNERABILITIES):
                vulnerability[CveConstants.PUBLISHEDDATE] = parse_twistlock_date_time(vulnerability.get(CveConstants.PUBLISHEDDATE))
                if vulnerability[CveConstants.PUBLISHEDDATE] is None and type(vulnerability.get(CveConstants.PUBLISHEDDATE_KUBERNETES)) is int:
                   vulnerability[CveConstants.PUBLISHEDDATE] =  datetime.fromtimestamp(vulnerability.get(CveConstants.PUBLISHEDDATE_KUBERNETES))
                if vulnerability[CveConstants.PUBLISHEDDATE] is None and type(vulnerability.get(CveConstants.PUBLISHEDDATE_KUBERNETES)) is str:
                   vulnerability[CveConstants.PUBLISHEDDATE] =  parse_twistlock_date_time(vulnerability.get(CveConstants.PUBLISHEDDATE_KUBERNETES))
                vulnerability[CveConstants.PUBLISHEDDATE] = format_common_date_time(vulnerability[CveConstants.PUBLISHEDDATE])
                
                vulnerability[CveConstants.FIXEDDATE] = parse_twistlock_date_time(vulnerability.get(CveConstants.FIXEDDATE))
                if vulnerability[CveConstants.FIXEDDATE] is None and type(vulnerability.get(CveConstants.FIXEDDATE_KUBERNETES)) is int:
                   vulnerability[CveConstants.FIXEDDATE] =  datetime.fromtimestamp(vulnerability.get(CveConstants.FIXEDDATE_KUBERNETES))
                if vulnerability[CveConstants.FIXEDDATE] is None and type(vulnerability.get(CveConstants.FIXEDDATE_KUBERNETES)) is str:
                   vulnerability[CveConstants.FIXEDDATE] =  parse_twistlock_date_time(vulnerability.get(CveConstants.FIXEDDATE_KUBERNETES))
                vulnerability[CveConstants.FIXEDDATE] = format_common_date_time(vulnerability[CveConstants.FIXEDDATE])

                vulnerability[CveConstants.DISCOVEREDDATE] = parse_twistlock_date_time(vulnerability.get(CveConstants.DISCOVEREDDATE))
                if vulnerability[CveConstants.DISCOVEREDDATE] is None and type(vulnerability.get(CveConstants.DISCOVEREDDATE_KUBERNETES)) is int:
                   vulnerability[CveConstants.DISCOVEREDDATE] =  datetime.fromtimestamp(vulnerability.get(CveConstants.DISCOVEREDDATE_KUBERNETES))
                if vulnerability[CveConstants.DISCOVEREDDATE] is None and type(vulnerability.get(CveConstants.DISCOVEREDDATE_KUBERNETES)) is str:
                   vulnerability[CveConstants.DISCOVEREDDATE] =  parse_twistlock_date_time(vulnerability.get(CveConstants.DISCOVEREDDATE_KUBERNETES))
                vulnerability[CveConstants.DISCOVEREDDATE] = format_common_date_time(vulnerability[CveConstants.DISCOVEREDDATE])
                cve_manager.add_cve(json.dumps(vulnerability))
        
        if twistlock_json_report_result.get(TwistlockReportParserConstants.COMPLIANCEISSUES):
            compliance: Dict[str, Any]
            for compliance in twistlock_json_report_result.get(TwistlockReportParserConstants.COMPLIANCEISSUES):
                compliance_manager.add_compliance(json.dumps(compliance))
        
        if twistlock_json_report_result.get(TwistlockReportParserConstants.COMPLIANCES):
            compliance: Dict[str, Any]
            for compliance in twistlock_json_report_result.get(TwistlockReportParserConstants.COMPLIANCES):
                compliance_manager.add_compliance(json.dumps(compliance))
        self._processed_report = ProcessedReport(log_file_path=log_file_path,
                                                 id=id,
                                                 report_name=name,
                                                 distro=distro,
                                                 distro_release=distro_version,
                                                 digest=digest,
                                                 namespace=namespaces,
                                                 secrets=secrets,
                                                 cve_manager=cve_manager,
                                                 package_manager=package_manager,
                                                 compliance_manager=compliance_manager)
    def get_vulnerability_report_json(self) -> Dict[str, Any]:
        return self._processed_report.toJson()
    
    def save_vulnerability_report_json(self, abs_report_path: str) -> bool:
        return self._processed_report.save_report(abs_report_path)