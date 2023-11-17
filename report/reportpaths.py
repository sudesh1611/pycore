from constants import ReportPathsConstants
from typing import Any, Dict

import json

class ReportPaths:
    def __init__(self, image_name: str = None, raw_report_path: str = None, processed_report_path: str = None, formatted_report_path: str = None) -> None:
        self.image_name = image_name
        self.raw_report_path = raw_report_path
        self.processed_report_path = processed_report_path
        self.formatted_report_path = formatted_report_path
    
    def toJson(self) -> Dict[str, str]:
        return {
            ReportPathsConstants.NAME: self.image_name,
            ReportPathsConstants.RAWREPORTPATH: self.raw_report_path,
            ReportPathsConstants.FORMATTEDREPORTPATH: self.formatted_report_path,
            ReportPathsConstants.PROCESSEDREPORTPATH: self.processed_report_path
        }
    
    def toJsonString(self) -> str:
        return json.dumps(self.toJson(), indent=4)
    
    def fromJsonString(self, jsonString: str) -> 'ReportPaths':
        loaded_json: Dict[str, str] = json.loads(jsonString)
        return self.fromJson(loaded_json)
    
    def fromJson(self, loaded_json: Dict[str, Any]) -> 'ReportPaths':
        self.image_name = loaded_json.get(ReportPathsConstants.NAME)
        self.raw_report_path = loaded_json.get(ReportPathsConstants.RAWREPORTPATH)
        self.processed_report_path = loaded_json.get(ReportPathsConstants.PROCESSEDREPORTPATH)
        self.formatted_report_path = loaded_json.get(ReportPathsConstants.FORMATTEDREPORTPATH)
        return self