from constants import PackageConstants

import json

class Package:
    def __init__(self, name: str, type: str, version: str, path: str) -> None:
        self._name: str = name
        self._type: str = type
        self._version: str = version
        self._path: str = path
    
    def get_version(self) -> str:
        return self._version
    
    def get_name(self) -> str:
        return self._name
    
    def get_type(self) -> str:
        return self._type
    
    def get_path(self) -> str:
        return self._path
    
    def __str__(self) -> str:
        return json.dumps({
            PackageConstants.NAME: self.get_name(),
            PackageConstants.TYPE: self.get_type(),
            PackageConstants.VERSION: self.get_version(),
            PackageConstants.PATH: self.get_path() 
        }, indent=4)

    def __repr__(self) -> str:
        return self.__str__()