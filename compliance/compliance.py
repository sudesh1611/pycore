from ..constants import ComplianceConstants
from ..logger import Logger
from typing import Any, Dict, Optional

import json
import traceback

class Compliance:
    _logger: Logger
    def __init__(self, compliance_json_string: str, log_file_path: str) -> None:
        try:
            self._logger = Logger(log_file_path)
            self._compliance_json: Dict[str, Any] = json.loads(compliance_json_string)
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while parsing json: {compliance_json_string}")
            self._logger.error(traceback.format_exc())
    
    def get_title(self) -> Optional[str]:
        return self._compliance_json.get(ComplianceConstants.TITLE)
    
    def get_description(self) -> Optional[str]:
        return self._compliance_json.get(ComplianceConstants.DESCRIPTION)
    
    def get_severity(self) -> Optional[str]:
        return self._compliance_json.get(ComplianceConstants.SEVERITY)
    
    def get_cause(self) -> Optional[str]:
        return self._compliance_json.get(ComplianceConstants.CAUSE)

    def toJson(self) -> Dict[str, Any]:
        return {
            ComplianceConstants.TITLE: self.get_title(),
            ComplianceConstants.DESCRIPTION: self.get_description(),
            ComplianceConstants.CAUSE: self.get_cause(),
            ComplianceConstants.SEVERITY: self.get_severity()
        }
