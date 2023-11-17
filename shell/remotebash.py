from shell import Bash

import paramiko
import traceback

class RemoteBash(Bash):
    _host_port: int
    _host_ip: str
    _username: str
    _password: str
    

    def __init__(self, log_file_path: str, username: str, password: str, host_ip: str, host_port: int = 22) -> None:
        super().__init__(log_file_path)
        self._host_port = host_port
        self._username = username
        self._password = password
        self._host_ip = host_ip
    
    def execute_command(self, command: str, write_output_to_screen: bool = True) -> None:
        try:
            self._initialize_values(command)
            self._logger.info(f"Executing `{command}` on {self._host_ip}")
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=self._host_ip, username=self._username, password=self._password, port=self._host_port)
            _, stdout, stderr = ssh_client.exec_command(command)
            self._return_code = stdout.channel.recv_exit_status()
            self._stdout = stdout.readlines()
            self._stderr = stderr.readlines()
            if write_output_to_screen:
                [self._logger.info(f"## {line.strip()}") for line in self._stdout]
                [self._logger.error(f"~~ {line.strip()}") for line in self._stderr]
            ssh_client.close()
            self._result = True
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while executing `{command}`")
            self._logger.error(traceback.format_exc())