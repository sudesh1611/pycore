from compliance import Compliance
from logger import Logger
from typing import Set

import traceback

class ComplianceManager:
    _logger: Logger
    def __init__(self, log_file_path: str) -> None:
        self._logger = Logger(log_file_path)
        self._compliances: Set[Compliance] = set()
    
    def add_compliance(self, compliance_json_string: str) -> None:
        try:
            new_compliance = Compliance(compliance_json_string, self._logger.log_file_path)
            self._compliances.add(new_compliance)
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while creating Compliance for json: {compliance_json_string}")
            self._logger.error(traceback.format_exc())
    
    def get_all_compliances(self) -> Set[Compliance]:
        return self._compliances