# PyCore

PyCore is a base project encapsulating a variety of scripts enabling automation of scanning and reporting of vulnerabilities in container images in local system, remote systems and Kubernetes using Twistlock and Blackduck. Following are the projects that make use of this project:

- [SwayamVaha](https://github.com/sudesh1611/SwayamVaha) - A dashboard to manage reported vulnerablities by Twistlock and Blackduck, false positives as well as comparisions between different versions.

- [TwistlockAuto](https://github.com/sudesh1611/TwistlockAuto) - Vulnerability scanner and detector for container images in local system, remote systems and Kubernetes using Twistlock.

- [BlackDuckAuto](https://github.com/sudesh1611/BlackDuckAuto) - Fetch and parse Blackduck project reports for the vulnerabilities.

- [JiraAuto](https://github.com/sudesh1611/JiraAuto) - Scan Jira server for specified projects periodically and fetch bugs reported for vulnerabilities for different type of scans.

## Requirements

PyCore requires Python 3.6 or greater. Additional dependencies can be resolved by executing following:

`pip3 install -r requirements.txt`
