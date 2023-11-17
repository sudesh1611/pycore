from .blackduckproject import BlackDuckProject
from .blackduckversion import BlackDuckVersion
from ..cve import CveManager
from ..configs import BlackDuckClientConfig
from ..constants import BlackDuckClientConstants, BlackduckReportParserConstants, CveConstants, GlobalConstants
from ..helpers.datetimeconverter import format_common_date_time, parse_bduck_date_time
from ..logger import Logger
from ..package import PackageManager
from ..report import ProcessedReport
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import json
import requests
import sys
import traceback

class BlackDuckClient:
    _token: str = None
    _api_token: str = None
    _token_expiry_date: datetime
    _logger: Logger
    _raw_json = None

    def __init__(self, log_file_path: str, api_token: str) -> None:
        self._logger = Logger(log_file_path)
        self._api_token = api_token
    
    def _generate_token(self) -> str:
        try:
            headers = {
                GlobalConstants.ACCEPT: 'application/vnd.blackducksoftware.user-4+json',
                GlobalConstants.AUTHORIZATION: f'token {self._api_token}'
            }
            
            response = requests.request("POST", BlackDuckClientConfig.BDUCK_AUTHENTICATE_API, headers=headers, verify=BlackDuckClientConfig.VERIFY_BDUCK_SERVER_CERTIFICATE)
            self._logger.info(f"Blackduck authenticate API response: {response.text}")
            self._token = response.json()['bearerToken']
            self._logger.info(f"Generated blackduck bearer token: {self._token}")
            expire_in_miliseconds = response.json()['expiresInMilliseconds']
            expire_in_miliseconds = expire_in_miliseconds - 5000
            self._token_expiry_date = datetime.now() + timedelta(milliseconds=expire_in_miliseconds)
            self._logger.info(f"Token will expire on {self._token_expiry_date.isoformat(timespec='milliseconds')}")
            return self._token
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while generating blackduck bearer token")
            self._logger.error(traceback.format_exc())
            sys.exit(1)
    
    def get_token(self) -> str:
        if self._token is None or self._token_expiry_date is None or self._token_expiry_date < datetime.now():
            self._logger.info("Generating new blackduck bearer token...")
            return self._generate_token()
        else:
            self._logger.info("Using already generated blackduck bearer token...")
            return self._token
    
    def get_all_projects(self) -> List[BlackDuckProject]:
        all_projects: List[BlackDuckProject] = []
        try:
            headers = {
                GlobalConstants.ACCEPT: 'application/vnd.blackducksoftware.project-detail-6+json',
                GlobalConstants.AUTHORIZATION: f'{GlobalConstants.BEARER} {self.get_token()}'
            }
            params = {
                GlobalConstants.OFFSET: 0,
                GlobalConstants.LIMIT: 500
            }
            self._logger.info("Fetching all blackduck projects")
            response = requests.request("GET", BlackDuckClientConfig.BDUCK_PROJECTS_API, headers=headers, params=params,verify=False)
            self._logger.info(f"Blackduck get all projects API response: {response.status_code}")
            for item in response.json().get(BlackDuckClientConstants.ITEMS, []):
                project = BlackDuckProject(item[BlackDuckClientConstants.META][BlackDuckClientConstants.HREF].strip().split('/')[-1].strip(), item[BlackDuckClientConstants.NAME])
                all_projects.append(project)
                self._logger.info(f"Project ID: {project.id} and Project Name: {project.name}")
            return all_projects
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting all blackduck projects")
            self._logger.error(traceback.format_exc())
            return all_projects
    
    def get_all_versions_of_project(self, project_id: str) -> Dict[str, BlackDuckVersion]:
        versions_info: Dict[str, BlackDuckVersion] = {}
        try:
            BDUCK_VERSIONS_API = f"{BlackDuckClientConfig.BDUCK_PROJECTS_API}/{project_id}/versions"
            offset = 0
            limit = 200
            count = 1
            self._logger.info(f"Fetching all versions of project: {project_id}")
            while(offset < count):
                self._logger.info(f"Count: {count} and Offset:{offset}")
                headers = {
                    GlobalConstants.ACCEPT: 'application/vnd.blackducksoftware.project-detail-5+json',
                    GlobalConstants.AUTHORIZATION: f'{GlobalConstants.BEARER} {self.get_token()}'
                }
                params = {
                    GlobalConstants.OFFSET: offset,
                    GlobalConstants.LIMIT: limit
                }
                response = requests.request("GET", BDUCK_VERSIONS_API, headers=headers, params=params, verify=False)
                self._logger.info(f"Blackduck get all versions of project {project_id} API response: {response.status_code}")
                count = response.json()['totalCount']
                for item in response.json().get(BlackDuckClientConstants.ITEMS, []):
                    version_id = item[BlackDuckClientConstants.META][BlackDuckClientConstants.HREF].strip().split('/')[-1].strip()
                    versions_info[version_id] = BlackDuckVersion(version_id,
                                                                 item.get('versionName'),
                                                                 item.get("branch"),
                                                                 item.get("createdAt"),
                                                                 item.get("settingUpdatedAt"))
                    self._logger.info(f"Version ID: {version_id} and Version Name: {versions_info[version_id].name}")
                offset = offset + limit
            return versions_info
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting all versions of blackduck project: {project_id}")
            self._logger.error(traceback.format_exc())
            return versions_info
    
    def get_upgrade_resolution(self, component_id: str, component_version_id: str, origin_id: str) -> Optional[str]:
        upgrade_guidance: str = ""
        try:
            BDUCK_UPGRADE_GUIDE_API = f"{BlackDuckClientConfig.BDUCK_BASE_URL}/api/components/{component_id}/versions/{component_version_id}/origins/{origin_id}/upgrade-guidance"
            headers = {
                GlobalConstants.ACCEPT: 'application/vnd.blackducksoftware.component-detail-5+json',
                GlobalConstants.AUTHORIZATION: f'{GlobalConstants.BEARER} {self.get_token()}'
            }
            params = {
                GlobalConstants.OFFSET: 0,
                GlobalConstants.LIMIT: 500
            }
            self._logger.info(f"Fetching upgrade guidance of component: {component_id}, component version: {component_version_id} and origin: {origin_id}")
            response = requests.request("GET", BDUCK_UPGRADE_GUIDE_API, headers=headers, params=params, verify=False)
            self._logger.info(f"Blackduck upgrade guidance of component: {component_id}, component version: {component_version_id} and origin: {origin_id} API response: {response.status_code}")
            if "shortTerm" in response.json():
                short_term = response.json()["shortTerm"]
                if short_term.get("originName", "") != "":
                    upgrade_guidance = f"Short Term: {short_term['originName']},"
                elif short_term.get("versionName", "") != "":
                    upgrade_guidance = f"Short Term: {short_term['versionName']},"
            if "longTerm" in response.json():
                long_term = response.json()["longTerm"]
                if long_term.get("originName", "") != "":
                    upgrade_guidance += f"Long Term: {long_term['originName']}"
                elif long_term.get("versionName", "") != "":
                    upgrade_guidance += f"Long Term: {long_term['versionName']}"
            self._logger.info(f"Upgrade guidance of component: {component_id}, component version: {component_version_id} and origin: {origin_id} is {upgrade_guidance}")
            return upgrade_guidance
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting upgrade ")
            self._logger.error(traceback.format_exc())
            return upgrade_guidance
    
    def generate_vulnerabilities_processed_report(self, project_id: str, version_id: str, version_name: str) -> Optional[ProcessedReport]:
        try:
            BDUCK_VULNEBS_API = f"{BlackDuckClientConfig.BDUCK_PROJECTS_API}/{project_id}/versions/{version_id}/vulnerable-bom-components"
            offset = 0
            limit = 500
            count = 1
            self._logger.info(f"Fetching all vulnebs of project: {project_id} and version: {version_id}")
            cve_json_results: List[Dict[str, Any]] = []
            while(offset < count):
                self._logger.info(f"Count: {count} and Offset:{offset}")
                headers = {
                    GlobalConstants.ACCEPT: 'application/vnd.blackducksoftware.bill-of-materials-6+json',
                    GlobalConstants.AUTHORIZATION: f'{GlobalConstants.BEARER} {self.get_token()}'
                }
                params = {
                    GlobalConstants.OFFSET: offset,
                    GlobalConstants.LIMIT: limit
                }
                response = requests.request("GET", BDUCK_VULNEBS_API, headers=headers, params=params,verify=False)
                self._logger.info(f"Blackduck get all vulnebs of project {project_id} and version {version_id} API response: {response.status_code}")
                count = response.json()['totalCount']
                [cve_json_results.append(item) for item in response.json().get(BlackDuckClientConstants.ITEMS, [])]
                offset = offset + limit
            self._raw_json = cve_json_results
            blackduck_report_parser = BlackduckReportParser(self._logger.log_file_path, cve_json_results, version_id, version_name, self)
            self._logger.info(f"Successfully parsed the vulneb results of project: {project_id} and version: {version_id}")
            return blackduck_report_parser.get_vulnerability_processed_report()
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting all vulnebs of blackduck project: {project_id} and version: {version_id}")
            self._logger.error(traceback.format_exc())
            return None
    
    def save_unprocessed_json(self, abs_report_path: str) -> bool:
        try:
            with open(abs_report_path, "w", encoding='utf8') as fl:
                json.dump(self._raw_json, fl, indent=4, sort_keys=True)
            self._logger.info(f"Successfully saved the raw results in `{abs_report_path}`")
            return True
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while saving raw json to file: {abs_report_path}")
            self._logger.error(traceback.format_exc())
            return False

class BlackduckReportParser:
    _processed_report: ProcessedReport
    _logger: Logger

    def __init__(self, log_file_path: str, blackduck_result_json: Dict[str, Any], version_id: str, version_name: str, blackduck_client: BlackDuckClient) -> None:
        self._logger = Logger(log_file_path)
        package_manager = PackageManager()
        cve_manager = CveManager(log_file_path)
        for item in blackduck_result_json:
            try:
                href_str :str = item[BlackDuckClientConstants.META][BlackDuckClientConstants.HREF]
                component_id = href_str.strip().split("components/")[1].strip().split("/")[0].strip()
                component_version_id = href_str.strip().split("/origins")[0].strip().split("/")[-1].strip()
                origin_id = href_str.strip().split("origins/")[1].strip().split("/")[0].strip() if "origins" in href_str else None
                vulneb_json = {
                    CveConstants.ID: item[BlackduckReportParserConstants.VULNEB_WITH_REMEDIATION].get("vulnerabilityName"),
                    CveConstants.CVE: item[BlackduckReportParserConstants.VULNEB_WITH_REMEDIATION].get("vulnerabilityName"),
                    CveConstants.DESCRIPTION: item[BlackduckReportParserConstants.VULNEB_WITH_REMEDIATION].get("description"),
                    CveConstants.CVSS: item[BlackduckReportParserConstants.VULNEB_WITH_REMEDIATION].get("overallScore"),
                    CveConstants.STATUS: blackduck_client.get_upgrade_resolution(component_id, component_version_id, origin_id),
                    CveConstants.SEVERITY: item[BlackduckReportParserConstants.VULNEB_WITH_REMEDIATION].get("severity"),
                    CveConstants.PACKAGENAME: item["componentName"],
                    CveConstants.PACKAGEVERSION: item["componentVersionName"],
                    CveConstants.VENDOR_LINK_KEY: href_str,
                    CveConstants.PUBLISHEDDATE: format_common_date_time(parse_bduck_date_time(item[BlackduckReportParserConstants.VULNEB_WITH_REMEDIATION].get("vulnerabilityPublishedDate"))),
                    CveConstants.FIXEDDATE: format_common_date_time(parse_bduck_date_time(item[BlackduckReportParserConstants.VULNEB_WITH_REMEDIATION].get("remediationUpdatedAt")))
                }
                self._logger.info(f"Parsed vulneb ID: {vulneb_json[CveConstants.ID]} of package: {vulneb_json[CveConstants.PACKAGENAME]} and version: {vulneb_json[CveConstants.PACKAGEVERSION]}")
                if vulneb_json[CveConstants.ID]:
                    cve_manager.add_cve(json.dumps(vulneb_json))
                    package_manager.add_package(vulneb_json[CveConstants.PACKAGENAME], vulneb_json[CveConstants.PACKAGEVERSION], item.get("componentVersionOriginName"))
            except Exception as ex:
                self._logger.error(f"Exception ({ex}) occured while parsing item: {json.dumps(item, indent=4)}")
                self._logger.error(traceback.format_exc())
        self._processed_report = ProcessedReport(log_file_path=log_file_path,
                                                 id=version_id,
                                                 report_name=version_name,
                                                 cve_manager=cve_manager,
                                                 package_manager=package_manager)
    def get_vulnerability_report_json(self) -> Dict[str, Any]:
        return self._processed_report.toJson()
    
    def get_vulnerability_processed_report(self) -> ProcessedReport:
        return self._processed_report
