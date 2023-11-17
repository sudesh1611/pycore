from datetime import datetime
from helpers.datetimeconverter import parse_common_date_time, format_common_date_time, parse_bduck_date_time

class BlackDuckVersion:
    id: str = None
    name: str = None
    branch: str = None
    created: datetime = None
    updated: datetime = None
    def __init__(self, id: str, name: str, branch: str, created: str, updated: str) -> None:
        self.id = id
        self.name = name
        self.branch = branch
        self.created = parse_common_date_time(format_common_date_time(parse_bduck_date_time(created)))
        self.updated = parse_common_date_time(format_common_date_time(parse_bduck_date_time(updated)))