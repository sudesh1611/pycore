from constants import CveConstants
from helpers.datetimeconverter import format_common_date_time, parse_common_date_time
from logger import Logger
from typing import Any, Dict, Optional

import datetime
import json
import traceback

class Cve:
    _logger: Logger
    def __init__(self, cve_json_string: str, log_file_path: str) -> None:
        try:
            self._logger = Logger(log_file_path)
            self._cve_json: Dict[str, Any] = json.loads(cve_json_string)
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while parsing json: {cve_json_string}")
            self._logger.error(traceback.format_exc())
    
    def get_id(self) -> Optional[str]:
        cve_id = self._cve_json.get(CveConstants.ID)
        if type(cve_id) is int:
            cve_id = self._cve_json.get(CveConstants.CVE)
        return cve_id
    
    def get_description(self) -> Optional[str]:
        return self._cve_json.get(CveConstants.DESCRIPTION)
    
    def get_cvss_score(self) -> Optional[float]:
        return self._cve_json.get(CveConstants.CVSS)
    
    def get_status(self) -> Optional[str]:
        return self._cve_json.get(CveConstants.STATUS)
    
    def get_vector(self) -> Optional[str]:
        vector: str = self._cve_json.get(CveConstants.VECTOR)
        if vector is None:
            vector = self._cve_json.get(CveConstants.VECTOR_KUBERNETES)
        return vector
    
    def get_severity(self) -> Optional[str]:
        return self._cve_json.get(CveConstants.SEVERITY)
    
    def get_package_name(self) -> Optional[str]:
        return self._cve_json.get(CveConstants.PACKAGENAME)
    
    def get_package_version(self) -> Optional[str]:
        return self._cve_json.get(CveConstants.PACKAGEVERSION)
    
    def get_link_1(self) -> Optional[str]:
        return self._cve_json.get(CveConstants.VENDOR_LINK_KEY)
    
    def get_link_2(self) -> Optional[str]:
        if self.get_id():
            return f"{CveConstants.NVD_LINK_PREFIX}{self.get_id()}"
    
    def get_published_date(self) -> Optional[datetime.datetime]:
        p_date = self._cve_json.get(CveConstants.PUBLISHEDDATE)
        return parse_common_date_time(p_date)
    
    def get_discovered_date(self) -> Optional[datetime.datetime]:
        p_date = self._cve_json.get(CveConstants.DISCOVEREDDATE)
        return parse_common_date_time(p_date)
    
    def get_fixed_date(self) -> Optional[str]:
        p_date = self._cve_json.get(CveConstants.FIXEDDATE)
        return parse_common_date_time(p_date)

    def toJson(self) -> Dict[str, Any]:
        return {
            CveConstants.ID: self.get_id(),
            CveConstants.CVE: self.get_id(),
            CveConstants.PACKAGENAME: self.get_package_name(),
            CveConstants.PACKAGEVERSION: self.get_package_version(),
            CveConstants.CVSS: self.get_cvss_score(),
            CveConstants.STATUS: self.get_status(),
            CveConstants.SEVERITY: self.get_severity(),
            CveConstants.VENDOR_LINK_KEY: self.get_link_1(),
            CveConstants.NVD_LINK_KEY: self.get_link_2(),
            CveConstants.PUBLISHEDDATE: format_common_date_time(self.get_published_date()),
            CveConstants.DISCOVEREDDATE: format_common_date_time(self.get_discovered_date()),
            CveConstants.FIXEDDATE: format_common_date_time(self.get_fixed_date())
        }