class TwistlockClientConfig:
    BASE_API = "https://containersecurity.somedomain.com/api/v1" # Twistlock portal/server API base url
    PROJECT_VALUE = "PKS" # Name of the twistlock project on portal/server
    AUTHENTICATE_API = BASE_API + "/authenticate"
    HOST_REPORT_API = BASE_API + "/hosts"
    HOST_INFO_API = BASE_API + "/hosts/info"
    IMAGE_NAMES_API = BASE_API + "/images/names"
    IMAGE_REPORT_API = BASE_API + "/images"
    TOKEN_EXPIRY_SPAN = 30 # Twistlock token expiry time in minutes
    VERIFY_TWISTLOCK_SERVER_CERTIFICATE = False