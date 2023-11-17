class JiraClientConfig:
    HOST = "https://jira.somedomain.com" #Jira base domain
    PAT_ENVIRONMENT_VAR_KEY = "JIRA_PAT_VALUE" #Environment variable holding Jira Personal Access Token
    VERIFY_JIRA_SERVER_CERTIFICATE = False