from typing import List
from .blackduckproject import BlackduckProjectConfig
from .twistlockproject import TwistlockProjectConfig

class WebAppConfig:
    LOG_FILE_PATH = "/absolute/path/to/file/to/store/application/logs"

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-5(-((41zl6*%$eowajji96ez#!)^&@hrstlu5h)8n6-d55e9lm'

    # Postgresql
    POSTGRESQL_DOMAIN_IP = "10.45.20.247" # Postgresql domain or IP
    POSTGRESQL_PORT = "5432"
    POSTGRESQL_DB_NAME = "dashboard"
    POSTGRESQL_USERNAME_KEY = "PSQL_USERNAME" # Environment variable holding username to access postgresql
    POSTGRESQL_PASSWORD_KEY = "PSQL_PASSWORD" # Environment variable holding password of username to access postgresql
    
    # Web Application
    HOSTNAME = f"http://10.45.7.45:80" # sdl dashboard web app domain along with port
    USERNAME_KEY = "UI_USERNAME" # Environment variable holding username to access sdl dashboard web app
    PASSWORD_KEY = "UI_PASSWORD" # Environment variable holding password of username to access sdl dashboard web app

    # REST APIs
    VERIFY_WEBAPP_SERVER_CERTIFICATE = False
    SCAN_REPORT_REST_API = f"{HOSTNAME}/api/scan-report/"
    REPORT_DETAILS_PREFIX_URL = f"{HOSTNAME}/report-details/?"
    CVE_JIRA_API = f"{HOSTNAME}/api/cve/"

    # Possible Scan Types supported
    POSSIBLE_SCAN_TYPES: List[str] = list(set(TwistlockProjectConfig.PROJECT_TYPES + list(BlackduckProjectConfig.PROJECT_NAME_ID_MAPPING.values())))