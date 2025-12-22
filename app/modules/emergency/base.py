from abc import ABC, abstractmethod
from enum import Enum
from typing import List

class UnitStatus(Enum):
    IDLE = "Idle"
    ON_SCENE = "On Scene"
    MAINTENANCE = "Maintenance"

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

    @unit_id.setter
    def unit_id(self, value):
        self.__unit_id = value

    @property
    def unit_type(self):
        return self.__unit_type
    
    @unit_type.setter
    def unit_type(self, value):
        self.__unit_type = value

    @property
    def current_location(self):
        return self.__current_location
    
    @current_location.setter
    def current_location(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Location must be non-empty string")
        self.__current_location = value

    @property
    def availability(self):
        if self.__status == UnitStatus.IDLE:
            return True
        else:
            return False
    
    @property
    def status(self,new_status:UnitStatus):
        if not isinstance(new_status,UnitStatus):
            raise ValueError("Invalid status type provided")
        self.__status = new_status
        print(f"Unit {self.__unit_id} status updated to {new_status.value}")