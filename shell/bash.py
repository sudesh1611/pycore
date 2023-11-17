from abc import ABC, abstractmethod
from logger import Logger
from typing import List, Optional

class Bash(ABC):
    _logger: Logger = None
    _result: bool = False
    _stdout:  List[str]= []
    _stderr: List[str] = []
    _return_code: int = -255
    _cmd: str = None

    def __init__(self, log_file_path: str) -> None:
        self._logger = Logger(log_file_path)
    
    def _initialize_values(self, cmd: str) -> None:
        self._result = False
        self._stdout = []
        self._stderr = []
        self._return_code = -255
        self._cmd = cmd
    
    def get_result(self) -> bool:
        return self._result
    
    def get_stdout(self) -> List[str]:
        return self._stdout
    
    def get_stderr(self) -> List[str]:
        return self._stderr
    
    def get_return_code(self) -> List[str]:
        return self._return_code
    
    def get_cmd(self) -> Optional[str]:
        return self._cmd
    
    @abstractmethod
    def execute_command(self, command: str, write_output_to_screen: bool = True) -> None:
        pass