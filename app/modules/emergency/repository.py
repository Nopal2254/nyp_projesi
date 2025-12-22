# repository.py
from app.modules.emergency.base import EmergencyUnit
from typing import List,Optional,Dict
from app.modules.emergency.implementations import (
    FireDepartment,
    Ambulance,
    PoliceUnit,
    HazmatUnit,
    Incident)

class EmergencyRepository:
    def __init__(self):
        self._units:Dict[str,EmergencyUnit] = {}
        self.incident_history:Dict[str,Incident] = {}
        self.dispacth_log:List[str] = []

    def add_unit(self, unit:EmergencyUnit):
        if unit.unit_id in self._units:
            raise ValueError(f"Unit {unit.unit_id} already exist")
        
        self._units[unit.unit_id] = unit
        self.log_system_event(f"System : New Unit {unit.unit_id} registered")
    
    def get_unit_by_id(self,unit_id:str):
        return self._units.get(unit_id)

    def get_all_unit(self):
        return list(self._units.values())
    
    def get_available_unit_by_type(self,unit_type:str) -> List[EmergencyUnit]:
        return [
            unit for unit in self._units.values()
            if unit.unit_type == unit_type and unit.availability
        ]
    
    def save_incident(self,incident:Incident):
        self.incident_history[incident.incident_id] = incident
        self.log_system_event(f"Log: Incident {incident.incident_id} archived")
    
    def get_incident_history(self):
        return list(self.incident_history.values())
    
    def log_system_event(self,message):
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dispacth_log.append(f"[{timestamp}] {message}")

    def get_system_log(self):
        return self.dispacth_log
    
    def operational_stats(self)-> dict:
        total = len(self._units)
        available = len([u for u in self._units.values() if u.availability])

        return{
            "total_units":total,
            "available_units":available,
            "readiness_sco  re":(available/total * 100) if total > 0 else 0,
            "active_incidents" : len(self.incident_history)
        }