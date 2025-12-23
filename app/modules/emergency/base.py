from abc import ABC, abstractmethod
from enum import Enum
from typing import List

class UnitStatus(Enum):
    IDLE = "Idle"
    ON_SCENE = "On Scene"
    MAINTENANCE = "Maintenance"

class Incident:
    def __init__(self,incident_id:str,incident_type:str,severity:int,location:str,description:str):
        self.incident_id = incident_id
        self.incident_type = incident_type
        self.severity = severity
        self.location = location
        self.description = description

class EmergencyUnit(ABC):
    def __init__(self, unit_id:str, unit_type:str, location:str):
        self.__unit_id = unit_id
        self.__unit_type = unit_type
        self.__current_location = location
        self.__status = UnitStatus.IDLE

    @abstractmethod
    def respond_to_incident(self, incident_id: str, severity:int):
        pass

    @abstractmethod
    def calculate_eta(self, destination: str):
        pass
    
    def update_status(self, status: bool):
        self.availability = status

    @abstractmethod
    def get_unit_capabilities(self) -> List[str]:
        pass

    @property
    def unit_id(self):
        return self.__unit_id

    @property
    def unit_type(self):
        return self.__unit_type

    @property
    def current_location(self):
        return self.__current_location

    @property
    def availability(self):
        if self.__status == UnitStatus.IDLE:
            return True
        else:
            return False
    
    @property
    def status(self)->UnitStatus:
        return self.__status

    @unit_id.setter
    def unit_id(self, value):
        self.__unit_id = value
    
    @unit_type.setter
    def unit_type(self, value):
        self.__unit_type = value

    
    @current_location.setter
    def current_location(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Location must be non-empty string")
        self.__current_location = value
    
    @status.setter
    def status(self,value:UnitStatus):
        if not isinstance(value,UnitStatus):
            raise ValueError("Invalid status type")
        self.__status = value

