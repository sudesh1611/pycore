class BlackDuckClientConfig:
    BDUCK_API_TOKEN_KEY = "BLACKDUCK_API_KEY" #Environment variable holding Blackduck API token
    BDUCK_BASE_URL = "https://blackduck.somedomain.com" #Base url of blackduck portal/server
    BDUCK_AUTHENTICATE_API = f"{BDUCK_BASE_URL}/api/tokens/authenticate"
    BDUCK_PROJECTS_API = f"{BDUCK_BASE_URL}/api/projects"
    VERIFY_BDUCK_SERVER_CERTIFICATE = False