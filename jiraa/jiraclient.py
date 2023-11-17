from ..configs import JiraClientConfig
from ..logger import Logger
from jira import JIRA, Issue
from time import sleep
from typing import List, Optional

import traceback

class JiraClient:
    _client: JIRA
    _logger: Logger

    def __init__(self, personal_access_token: str, log_file_path: str = None) -> None:
        options = {
            "verify": JiraClientConfig.VERIFY_JIRA_SERVER_CERTIFICATE
        }
        self._client = JIRA(JiraClientConfig.HOST, token_auth=personal_access_token, options=options)
        self._logger = Logger(log_file_path)
    
    def get_issue(self, issue: str) -> Optional[Issue]:
        retry_count = 0
        max_retry = 3
        while retry_count < max_retry:
            retry_count += 1
            try:
                issue = self._client.issue(issue)
                self._logger.info(f"Fetched {issue} details from Jira")
                return issue
            except Exception as ex:
                if "Issue Does Not Exist" in ex.text:
                    self._logger.error(f"Jira issue({issue}) does not exist")
                    return None
                else:
                    self._logger.error(f"Exception ({ex}) occured while getting issue details for {issue}")
                    self._logger.error(traceback.format_exc())
                    sleep(3)
        return None
    
    def execute_query(self, search_query:str, max_results: int) -> List[Issue]:
        to_return: List[Issue] = []
        try:
            starting_key = 0
            ending_key = max_results
            results_per_query = 40 if max_results > 40 else max_results
            while(starting_key < ending_key and starting_key < max_results):
                retry_count = 0
                max_retry = 3
                while retry_count < max_retry:
                    retry_count += 1
                    try:
                        self._logger.info(f"Jira fetching results of query ({search_query}) from {starting_key} to {starting_key + results_per_query}")
                        issues = self._client.search_issues(search_query, startAt=starting_key, maxResults=max_results)
                        self._logger.info(f"Jira fetched results of query ({search_query}) from {starting_key} to {starting_key + results_per_query}")
                        to_return += issues
                        starting_key = starting_key + results_per_query
                        ending_key = issues.total
                    except Exception as ex:
                        self._logger.error(f"Exception ({ex}) occured while fetching results")
                        self._logger.error(traceback.format_exc())
                        sleep(3)
            return to_return
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while getting issues for query {search_query}")
            self._logger.error(traceback.format_exc())
            return to_return