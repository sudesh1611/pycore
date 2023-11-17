from .reportpaths import ReportPaths
from ..constants import ScanReportConstants
from ..helpers.datetimeconverter import format_common_date, format_common_time, parse_common_date, parse_common_time
from datetime import datetime
from typing import Any, Dict, List

import json

class ScanReport:
    id: str = ""
    def __init__(self, type: str = None, version: str = None, user: str = None, date: str = None, time: str = None, root_dir: str = None, scan_software: str = None) -> 'ScanReport':
        self.type = type
        self.version = version
        self.user = user
        self.date: datetime = parse_common_date(date) if date else None
        self.time: datetime = parse_common_time(time) if time else None
        self.root_dir = root_dir
        self.ip_address_list = "[]"
        self.report_paths_list = "[]"
        self.scan_software = scan_software if scan_software else ScanReportConstants.TWISTLOCK

    def get_ip_address_list(self) -> List[str]:
        return json.loads(self.ip_address_list)
    
    def add_ip_address(self, ip_address: str) -> 'ScanReport':
        temp_ip_address_list = self.get_ip_address_list()
        temp_ip_address_list.append(ip_address)
        self.ip_address_list = json.dumps(list(set(temp_ip_address_list)))
        return self
    
    def get_report_paths_list(self) -> List[ReportPaths]:
        image_results_json: List[Dict[str, str]] = json.loads(self.report_paths_list)
        to_return: List[ReportPaths] = []
        for item in image_results_json:
            to_return.append(ReportPaths().fromJson(item))
        return to_return
    
    def add_image_result(self, image_result: ReportPaths) -> 'ScanReport':
        temp_image_result_list = self.get_report_paths_list()
        if image_result.image_name not in [image_result_item.image_name for image_result_item in temp_image_result_list]:
            temp_image_result_list.append(image_result)
        self.report_paths_list = json.dumps([image_result_item.toJson() for image_result_item in temp_image_result_list])
        return self
    
    def toJson(self) -> Dict[str, Any]:
        to_return = {
            ScanReportConstants.ID: self.id,
            ScanReportConstants.TYPE: self.type,
            ScanReportConstants.VERSION: self.version,
            ScanReportConstants.USER: self.user,
            ScanReportConstants.ROOT_DIR: self.root_dir,
            ScanReportConstants.IP_ADDRESS_LIST: self.get_ip_address_list(),
            ScanReportConstants.REPORT_PATHS_LIST: [image_result.toJson() for image_result in self.get_report_paths_list()],
            ScanReportConstants.SCAN_SOFTWARE: self.scan_software
        }
        if type(self.date) is str:
            to_return[ScanReportConstants.DATE] = self.date
        else:
            to_return[ScanReportConstants.DATE] = format_common_date(self.date)
        if type(self.time) is str:
            to_return[ScanReportConstants.TIME] = self.time
        else:
            to_return[ScanReportConstants.TIME] = format_common_time(self.time)
        return to_return
    
    def fromJsonString(self, json_repr: Dict[str, str]) -> 'ScanReport':
        self.id = json_repr.get(ScanReportConstants.ID)
        self.type = json_repr.get(ScanReportConstants.TYPE)
        self.version = json_repr.get(ScanReportConstants.VERSION)
        self.user = json_repr.get(ScanReportConstants.USER)
        self.date: datetime = parse_common_date(json_repr.get(ScanReportConstants.DATE))
        self.time: datetime = parse_common_time(json_repr.get(ScanReportConstants.TIME))
        self.root_dir = json_repr.get(ScanReportConstants.ROOT_DIR)
        self.ip_address_list = json_repr.get(ScanReportConstants.IP_ADDRESS_LIST)
        self.report_paths_list = json_repr.get(ScanReportConstants.REPORT_PATHS_LIST)
        self.scan_software = json_repr.get(ScanReportConstants.SCAN_SOFTWARE) if json_repr.get(ScanReportConstants.SCAN_SOFTWARE) else ScanReportConstants.TWISTLOCK
        return self