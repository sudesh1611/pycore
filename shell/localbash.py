from .bash import Bash
from subprocess import Popen, PIPE

import traceback
class LocalBash(Bash):
    def __init__(self, log_file_path: str) -> None:
        super().__init__(log_file_path)

    def execute_command(self, command: str, write_output_to_screen: bool = True) -> None:
        self._initialize_values(command)
        try:
            self._logger.info(f"Executing `{command}` on local host")
            cmd_process = ""
            with Popen(command, stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True, shell=True) as cmd_process:
                for line in cmd_process.stdout:
                    if write_output_to_screen:
                        self._logger.info(f"## {line.strip()}")
                    self._stdout.append(line.strip())
                self._stderr.extend(cmd_process.stderr.readlines())
                if write_output_to_screen:
                    [self._logger.error(f"~~ {line}") for line in self._stderr]
            self._return_code = cmd_process.returncode
            self._result = True
        except Exception as ex:
            self._logger.error(f"Exception ({ex}) occured while executing command: `{command}`")
            self._logger.error(traceback.format_exc())