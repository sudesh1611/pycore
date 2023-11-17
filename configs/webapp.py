class WebAppConfig:
    HOSTNAME = "http://10.123.1.248" # sdl dashboard web app domain
    USERNAME_KEY = "UI_USERNAME" # Environment variable holding username to access sdl dashboard web app
    PASSWORD_KEY = "UI_PASSWORD" # Environment variable holding password of username to access sdl dashboard web app
    SCAN_REPORT_REST_API = f"{HOSTNAME}/api/twistlock-scan-report/"
    REPORT_DETAILS_PREFIX_URL = f"{HOSTNAME}/report-details/?"
    CVE_JIRA_API = f"{HOSTNAME}/api/cve/"
    VERIFY_WEBAPP_SERVER_CERTIFICATE = False