from compliance import Compliance, ComplianceManager
from constants import ProcessedReportConstants
from cve import Cve, CveManager
from logger import Logger
from package import Package, PackageManager
from typing import Any, Dict, List, Optional

import json
import traceback

class ProcessedReport:
    _cve_manager: CveManager
    _package_manager: PackageManager
    _compliance_manager: ComplianceManager
    _logger: Logger
    _id: str
    _name: str
    _distro: str
    _distro_version: str
    _digest: str
    _namespaces: str
    _secrets: str

    def __init__(self, log_file_path: str,
                 id: str = None,
                 report_name: str = None,
                 distro: str = None,
                 distro_release: str = None,
                 digest: str = None,
                 namespace: str = None,
                 secrets: str = None,
                 cve_manager: CveManager = None, 
                 package_manager: PackageManager = None,
                 compliance_manager: ComplianceManager = None) -> None:
        self._id = id
        self._name = report_name
        self._distro = distro
        self._distro_version = distro_release
        self._digest = digest
        self._namespaces = namespace
        self._secrets = secrets
        self._cve_manager = cve_manager if cve_manager else CveManager(log_file_path)
        self._package_manager = package_manager if package_manager else PackageManager()
        self._compliance_manager = compliance_manager if compliance_manager else ComplianceManager(log_file_path)
        self._logger = Logger(log_file_path)
    
    def toJson(self) -> Optional[Dict[str, Any]]:
        try:
            cve_results: Dict[str, Any] = {}
            compliance_result_list: List[Dict[str, str]] = []
            cve: Cve
            package: Package
            compliance: Compliance
            for cve in self._cve_manager.get_all_cves():
                pkg_name: str = cve.get_package_name()
                pkg_version: str = cve.get_package_version()
                if pkg_name not in cve_results:
                    cve_results[pkg_name] = {}
                if pkg_version not in cve_results[pkg_name]:
                    cve_results[pkg_name][pkg_version] = {}
                if ProcessedReportConstants.PATH not in cve_results[pkg_name][pkg_version]:
                    paths: List[str] = []
                    for package in self._package_manager.get_packages_by_name_and_version(pkg_name, pkg_version):
                        paths.append(package.get_path())
                    cve_results[pkg_name][pkg_version][ProcessedReportConstants.PATH] = list(set(paths))
                if ProcessedReportConstants.CVES not in cve_results[pkg_name][pkg_version]:
                    cve_results[pkg_name][pkg_version][ProcessedReportConstants.CVES] = {}
                cve_results[pkg_name][pkg_version][ProcessedReportConstants.CVES][cve.get_id()] = cve.toJson()
            for compliance in self._compliance_manager.get_all_compliances():
                compliance_result_list.append(compliance.toJson())
            return {
                ProcessedReportConstants.ID: self._id,
                ProcessedReportConstants.NAME: self._name,
                ProcessedReportConstants.DISTRO: self._distro,
                ProcessedReportConstants.DISTRORELEASE: self._distro_version,
                ProcessedReportConstants.DIGEST: self._digest,
                ProcessedReportConstants.NAMESPACES: self._namespaces,
                ProcessedReportConstants.SECRETS: self._secrets,
                ProcessedReportConstants.CVE_RESULTS: cve_results,
                ProcessedReportConstants.COMPLIANCE_RESULTS: compliance_result_list
            }
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured processing json report")
            self._logger.error(traceback.format_exc())
            return False
    
    def save_report(self, abs_report_path: str) -> bool:
        try:
            with open(abs_report_path, "w", encoding='utf8') as fl:
                json.dump(self.toJson(), fl, indent=4, sort_keys=True)
            self._logger.info(f"Successfully saved the processed results in `{abs_report_path}`")
            return True
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while saving json to file: {abs_report_path}")
            self._logger.error(traceback.format_exc())
            return False