from ..constants.blackduckreportparser import BlackduckReportParserConstants
from ..constants.gloobal import GlobalConstants
from ..constants.twistlockreportparser import TwistlockReportParserConstants
from datetime import datetime
from typing import Optional

def parse_common_date(date: str) -> Optional[datetime]:
    try:
        return datetime.strptime(date, GlobalConstants.DATE_FORMAT)
    except Exception as ex:
        return None

def parse_common_time(time: str) -> Optional[datetime]:
    try:
        return datetime.strptime(time, GlobalConstants.TIME_FORMAT)
    except Exception as ex:
        return None

def parse_common_date_time(date_time: str) -> Optional[datetime]:
    try:
        return datetime.strptime(date_time, GlobalConstants.DATE_TIME_FORMAT)
    except Exception as ex:
        return None

def format_common_date(date: datetime) -> str:
    try:
        return date.strftime(GlobalConstants.DATE_FORMAT)
    except Exception as ex:
        return ""

def format_common_time(time: datetime) -> str:
    try:
        return time.strftime(GlobalConstants.TIME_FORMAT)
    except Exception as ex:
        return ""

def format_common_date_time(date_time: datetime) -> str:
    try:
        return date_time.strftime(GlobalConstants.DATE_TIME_FORMAT)
    except Exception as ex:
        return ""

def parse_bduck_date_time(date_time: str) -> Optional[datetime]:
    try:
        return datetime.strptime(date_time, BlackduckReportParserConstants.DATE_TIME_FORMAT)
    except Exception as ex:
        return None

def format_bduck_date_time(date_time: datetime) -> str:
    try:
        return date_time.strftime(BlackduckReportParserConstants.DATE_TIME_FORMAT)
    except Exception as ex:
        return ""

def parse_twistlock_date_time(date_time: str) -> Optional[datetime]:
    try:
        return datetime.strptime(date_time, TwistlockReportParserConstants.DATE_TIME_FORMAT)
    except Exception as ex:
        return None

def format_twistlock_date_time(date_time: datetime) -> str:
    try:
        return date_time.strftime(TwistlockReportParserConstants.DATE_TIME_FORMAT)
    except Exception as ex:
        return ""