from .package import Package
from typing import Set

import json

class PackageManager():
    def __init__(self) -> None:
        self._packages: Set[Package] = set()
    
    def add_package(self, name: str, version: str, type: str = None, path: str = None) -> None:
        self._packages.add(Package(name, type, version, path))
    
    def get_all_packages(self) -> Set[Package]:
        return self._packages
    
    def get_packages_by_name(self, name: str) -> Set[Package]:
        return set([package for package in self._packages if package.get_name() == name])
    
    def get_packages_by_type(self, type: str) -> Set[Package]:
        return set([package for package in self._packages if package.get_type() == type])
    
    def get_packages_by_name_and_type(self, name: str, type: str) -> Set[Package]:
        return set([package for package in self._packages if package.get_name() == name and package.get_type() == type])
    
    def get_packages_by_name_and_version(self, name: str, version: str) -> Set[Package]:
        return set([package for package in self._packages if package.get_name() == name and package.get_version() == version])
    
    def __str__(self) -> str:
        return json.dumps(self.get_all_packages())

    def __repr__(self) -> str:
        return self.__str__()