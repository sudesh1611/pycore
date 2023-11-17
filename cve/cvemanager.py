from cve import Cve
from logger import Logger
from typing import Set

import traceback

class CveManager:
    _logger: Logger
    def __init__(self, log_file_path: str) -> None:
        self._logger = Logger(log_file_path)
        self._cves: Set[Cve] = set()
    
    def add_cve(self, cve_json_string: str) -> None:
        try:
            new_cve = Cve(cve_json_string, self._logger.log_file_path)
            self._cves.add(new_cve)
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while creating CVE for json: {cve_json_string}")
            self._logger.error(traceback.format_exc())
    
    def get_all_cves(self) -> Set[Cve]:
        return self._cves
    
    def get_cves_by_id(self, id: str) -> Set[Cve]:
        return set([cve for cve in self._cves if cve.get_id() == id])
    
    def get_cves_by_severity(self, severity: str) -> Set[Cve]:
        return set([cve for cve in self._cves if cve.get_severity() == severity])
    
    def get_cves_by_package_name(self, pkg_name: str) -> Set[Cve]:
        return set([cve for cve in self._cves if cve.get_package_name() == pkg_name])
    
    def get_cves_by_package_name_and_version(self, pkg_name: str, pkg_version: str) -> Set[Cve]:
        return set([cve for cve in self._cves if cve.get_package_name() == pkg_name and cve.get_package_version() == pkg_version])