from app.modules.emergency.base import EmergencyUnit, UnitStatus
from app.modules.emergency.repository import EmergencyRepository

class Incident:
    incident_id:str
    incident_type:str
    severity:int
    location:str
    description:str

class FireDepartment(EmergencyUnit):
    def __init__(self, unit_id, location, water_capacity: int, staff_count: int):
        super().__init__(unit_id, "Fire", location)
        self.water_capacity = water_capacity
        self.current_water = water_capacity
        self.staff_count = staff_count
        self.has_ladder = True

    @property
    def water_level_percentage(self) -> float:
        return (self.current_water / self.water_capacity) * 100

    @property
    def current_water(self):
        return self.current_water
    
    @current_water.setter
    def current_water(self,value):
        if value < 0:
            self.current_water = 0
            self.status = UnitStatus.MAINTENANCE
        else:
            self.current_water = value

    def respond_to_incident(self, incident_id:str, severity:int):
        if self.availability and self.current_water > 500:
            self.status = UnitStatus.ON_SCENE
            print(f"{self.unit_id} bu {incident_id}'i calisiyor")
            return True
        print(f"{self.unit_id} cannot respond (Low water or busy)")
        return False
    
    def calculate_estimated_arrival(self, destination):
        return 12.5  #Just random value
    
    def get_unit_capabilities(self):
        return ["Fire Supression","Search or Rescue","Hydrant Connection"]

class Ambulance(EmergencyUnit):
    def __init__(self, unit_id, location, medical_tier: str):
        super().__init__(unit_id, "Medical", location)
        self.medical_tier = medical_tier # Specific attribute [cite: 132]
        self.patient_on_board = False

    def respond_to_incident(self, incident_id:str, severity:int):
        if self.availability:
            self.status = UnitStatus.ON_SCENE
            print(f"Ambulance {self.unit_id} bu {incident_id} calisiyor")
            return True
        return False
    
    def calculate_estimated_arrival(self, destination):
        return 8
    
    def get_unit_capabilities(self):
        return ["Emergency Medical Care","Patient Transport"]
    
class PoliceUnit(EmergencyUnit):
    def __init__(self, unit_id, location, patrol_zone: str,officer_count:int):
        super().__init__(unit_id, "Security", location)
        self.patrol_zone = patrol_zone
        self.officer_count = officer_count
        self.is_armed = True

    @property
    def patrol_zone(self):
        return self.patrol_zone
    
    @patrol_zone.setter
    def patrol_zone(self,value):
        if not value:
            raise ValueError("Patrol zone cant be empty")
        self.patrol_zone = value
    
    @property
    def officer_count(self):
        return self.officer_count
    
    def respond_to_incident(self, incident_id,severity):
        if not self.availability:
            print(f"Unit {self.unit_id} is currently busy")
            return False
        if severity >= 4:
            print(f"High alert : {self.unit_id} moving to high-risk scene")
        else:
            print(f"Police unit {self.unit_id} respont to {incident_id}")
        
        self.status = UnitStatus.ON_SCENE
        return True

    def calculate_eta(self, destination):
        return 5

    def get_unit_capabilities(self):
        return ["Traffic Control","Public Safety","Investigation"]
        
class HazmatUnit(EmergencyUnit):
    def __init__(self, unit_id, unit_type, location,protection_level):
        super().__init__(unit_id, "Radiation", location)
        self.protection_level = protection_level
        self.gas_mask_count = 10

    def respond_to_incident(self, incident_id, severity):
        if severity > 3 and self.protection_level != "A":
            print(f"Hazmat {self.unit_id} protection too low for the {incident_id} incident")
            return False
        
        if self.availability:
            self.status = UnitStatus.ON_SCENE
            return True
        return False
    
    def calculate_eta(self, destination):
        return 15
    
    def get_unit_capabilities(self):
        return ["Chemical Detection","Decontamination","Radiation Monitoring"]
    
class EmergencyService:
    def __init__(self):
        self.activity_log = []
        self.active_incidents = {}
        self.repo = EmergencyRepository
    
    def create_incident_report(self,incident_id:str,type:str,severity:int,location:str) -> Incident:
        if not (1 <= severity <= 5):
            raise ValueError("Severity must between 1 to 5")

        new_incident = Incident(
            incident_id = incident_id,
            incident_type = type,
            severity = severity,
            location = location,
            description = f"Level {severity} {type} at {location}"
        )

        self.active_incidents[incident_id] = new_incident
        self.log_event(f"Incident {incident_id} registered")
        return new_incident
    
    def generate_intervention_plan(self,incident:Incident,unit:EmergencyUnit) -> str:
        plan_steps = [
            f"PLAN_ID :{incident.incident_id}-PLAN",
            f"Assigned Unit:{unit.unit_id} {unit.unit_type}",
            f"Target Location: {incident.location}",
            "---PROCEDURAL STEPS---"
        ]
        
        if unit.unit_type == "Fire":
            plan_steps.append("1. Connect to nearest hydrant.")
            plan_steps.append("2. Deploy ladder if structure is > 2 floors.")
            if incident.severity > 3:
                plan_steps.append("3. Call for backup water tankers.")
        
        elif unit.unit_type == "Security":
            plan_steps.append("1. Establish 50m safety perimeter.")
            plan_steps.append("2. Divert traffic from the main road.")
            plan_steps.append("3. Apprehend or secure the scene.")

        elif unit.unit_type == "Medical":
            plan_steps.append("1. Perform initial triage.")
            plan_steps.append("2. Stabilize patient for transport.")
            plan_steps.append("3. Alert nearest Hospital ER.")

        plan_steps.append("--- END OF PLAN ---")
        return "\n".join(plan_steps)
    
    def log_event(self,message:str):
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.activity_log.append(f"[{timestamp}] {message}")

    @property
    def total_active_cases(self):
        return len(self.active_incidents)
    
    #ASDASDASDASD
    def dispatch_nearest_unit(self,incident:Incident):
        available_unit = self.repo.get_all_unit()

        suitable_unit = [u for u in available_unit if u.unit_type in incident.incident_type]

        if not suitable_unit:
            return f"No available {incident.incident_type} unit for incident {incident.incident_id} !"

        unit = suitable_unit[0]
        success = unit.respond_to_incident(incident.incident_id,incident.severity)

        if success:
            return f"Dispatch Successfull : {unit.unit_id} moving into {incident.location}"
        return f"Dispatch failed {unit.unit_id} reject the call"
