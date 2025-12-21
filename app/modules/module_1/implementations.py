from app.modules.module_1.base import TrafficElement
from app.modules.module_1.repository import TrafficRepository
from datetime import datetime

#traffic light implemetation
class TrafficLight(TrafficElement):
    def __init__(self,id,location,status,current_state = "Kirmizi"):
        super().__init__(id,location,status)
        self.__current_state = current_state

    def update_status(self,new_status):
        self.status = new_status
        print(f"{self.id} trafik isigi durumu {self.status} olarak guncellendi.")

    def get_service_report(self):
        report_text = f"{self.id} trafik isigi {self.location} konumunda {self.__current_state} durumundadir"
        print(report_text)
        return report_text

    def system_restart(self):
        print(f"Trafik isigi {self.id} yeniden baslatiliyor...")
        self.__current_state = "Sari"
    
    def apply_mode_logic(self,mode):
        if mode == "NIGHT_MODU":
            self.status = "Maintenance"
            self.__current_state = "Sari Flasor"
            print(f"{self.id} Gece modu: Tassaruf ve dikkat modu aktif")

        elif mode == "RUSH_HOUR":
            self.status = "Active"
            print(f"{self.id} Yogun saat modu: Isik sureleri dinamik olarak optimize ediliyor")
        else:
            self.status = "Active"
            print(f"{self.id} Normal mod aktif")

    #control the traffic light change timing based on the vehicle volume (like how many vehicle are waiting etc)
    @staticmethod
    def light_change_timing(vehicle_volume):
        if vehicle_volume < 50:
            return 30  # secs
        else:
            return 60  # secs

#speed camera implemetation
class SpeedCamera(TrafficElement):
    def __init__(self,id,location,status,current_speed,speed_limit = 75):
        super().__init__(id,location,status)
        self.__current_speed = current_speed
        self.__speed_limit = speed_limit

    def update_status(self,new_status):
        self.status = new_status
        print(f"{self.id} hiz kamerası durumu {self.status} olarak guncellendi.")

    def get_service_report(self):
        report_text = f"{self.id} hiz kamerası {self.location} konumunda {self.__speed_limit} km/s hiz sinirindadir"
        print(report_text)
        return report_text

    def system_restart(self):
        print(f"Hiz kamerası {self.id} yeniden baslatiliyor...")

    @property
    def is_dangerous(self):
        reckless_threshold = self.__speed_limit + 30

        if self.__current_speed >= reckless_threshold:
            return True,"RECKLESS DRIVING HAZARD"
        return False,"Normal Driving"
    
    @staticmethod
    def fine_calculation(speed,limit):
        excess = speed - limit
        if excess > 0:
            return 500 * (excess * 25)
        else:
            return 0

#intersection sensor implemetation            
class IntersectionSensor(TrafficElement):
    def __init__(self,id,location,status,sensitivity = 10):
        super().__init__(id,location,status)
        self.__current_vehicle_count = 0
        self.__sensitivity = sensitivity

    def update_status(self,new_status):
        self.status = new_status
        print(f"{self.id} kavsak sensoru durumu {self.status} olarak guncellendi.")

    def get_service_report(self):
        report_text = f"{self.id} kavsak sensoru {self.location} konumunda {self.__current_vehicle_count} arac sayisina sahiptir"
        print(report_text)
        return report_text

    @staticmethod
    def traffic_density(count):
        if count > 100 :
            return "High"
        elif count > 50:
            return "Medium"
        else:
            return "Low"

#road condition sensor implemetation
class RoadConditionSensor(TrafficElement):
    def __init__(self,id,location,status,road_temperature,moisture):
        super().__init__(id,location,status)
        #road temperature
        self.__temperature = road_temperature
        #road moisture
        self.__moisture = moisture
        self.__isIcy = self.isItIcy(road_temperature,moisture)

    @property
    def road_temperature(self):
        return self.__temperature
    
    @road_temperature.setter
    def road_temperature(self, temp):
        if -50 < temp <50:
            self.__temperature = temp
            self.__isIcy = self.isItIcy(self.__temperature,self.__moisture)
        else:
            print("Warning: Gecersiz sicaklik degeri!")
    
    @property
    def moisture(self):
        return self.__moisture
    
    @moisture.setter
    def moisture(self, moist):
        if 0 <= moist <=100:
            self.__moisture = moist
            self.__isIcy = self.isItIcy(self.__temperature,self.__moisture)
        else:
            print("Warning: Gecersiz nem degeri!")

    @property
    def is_dangerous(self):
        temp = self.__temperature
        moisture = self.__moisture

        if temp <= 0 and moisture > 20:
            return True, "ICY_ROAD"
        elif moisture > 80:
            return True, "FLOOD_RISK"
        else:
            return False, "NORMAL_CONDITION"

    def update_status(self,new_status):
        self.status = new_status
        print(f"{self.id} yol durumu sensörü durumu {self.status} olarak guncellendi.")

    def get_service_report(self):
        if self.__isIcy:
            icy_status = "Buzlu"
        else:
            icy_status = "Normal"
        report_text = f"{self.id} yol durumu sensörü {self.location} konumunda sicaklik: {self.__temperature}°C, nem: {self.__moisture}%, durum: {icy_status}"
        print(report_text)
        return report_text

    @staticmethod
    def isItIcy(temp,moisture):
        if temp <= 0 and moisture > 20:
            return True
        else:
            return False

class DigitalSignage(TrafficElement):
    def __init__(self,id,location,status):
        super().__init__(id,location,status)
        self.__current_message = "Welcome to Smart City !"

    def update_status(self,new_status):
        self.status = new_status
        print(f"{self.id} dijital tabela durumu {self.status} olarak guncellendi.")

    def set_message(self,message):
        self.__current_message = message
        print(f"{self.id} dijital tabela mesajı guncellendi: {message}")
    
    def get_service_report(self):
        report_text = f"{self.id} dijital tabela {self.location} konumunda mesaj: {self.__current_message}"
        print(report_text)
        return report_text
    
    @property
    def current_message(self):
        return self.__current_message
    
class SimulationClock:
    def __init__(self,start_hour=8):
        self.__current_hour = start_hour

    def advance_time(self,hours):
        self.__current_hour = (self.__current_hour + hours) % 24
        print(f"Simulasyon Saati Guncellendi: {self.__current_hour}:00")

    @property
    def current_hour(self):
        return self.__current_hour
        
    @property
    def time_mode(self):
        if 7 <= self.__current_hour < 9 or 16 <= self.__current_hour < 19:
            return "RUSH_HOUR"
        elif 22 <= self.__current_hour or self.__current_hour < 5:
            return "NIGHT_MODE"
        else:
            return "NORMAL"
        
class IncidentManagerService:
    def __init__(self,repository):
        self.__repo = repository
        self.__active_incidents = []

    def log_incident(self,location,description,severity):
        incident = {
            "time":datetime.now().strftime("%H:%M"),
            "location":location,
            "description":description,
            "severity":severity
        }

        self.__active_incidents.append(incident)
        print(f"[OLAY KAYDI] {location} konmunda yeni olay:{description} {severity}")

        self.__notify_signage(location,f"UYARI:{description}")        

    def __notify_signage(self,location,message):
        signs = self.__repo.find_by_type(DigitalSignage)
        for sign in signs:
            if sign.location == location:
                sign.set_message(message)
    
class TrafficService:
    @classmethod
    def create_zone_service(cls,zone_id):
        return cls(f"{zone_id}-service")
    
    def __init__(self,service_name):
        self.__service_name = service_name
        self.__managed_elements = []
    
    #get service name
    @property
    def service_name(self):
        return self.__service_name

    #calculate average vehicle
    @staticmethod    
    def average_vehicle_flow(vehicle_counts):
        if vehicle_counts:
            return sum(vehicle_counts) / len(vehicle_counts)
        else:
            return 0

    def register_device(self,element:TrafficElement):
        self.__managed_elements.append(element)
        print(f"{element.id} cihazi {self.__service_name}'ye kaydedildi.")
    
    def run_system_health_check(self):
        print(f"{self.__service_name} sistem saglik kontrolu baslatiliyor...")
        print("\n")
        
        for e in self.__managed_elements:
            e.get_service_report()

    def timing_adjuster(self,location,new_duration):
        for e in self.__managed_elements:
            if e.location == location and "TrafficLight" in str(type(e)):
                e.update_status(new_duration)

    def monitor_road_safety(self):
        for e in self.__managed_elements:
            report = e.get_service_report()
            if "Danger" in report:  # need to define what a "danger" report is
                print(f"Uyari: {e.id} cihazindan tehlike sinyali alindi!")

    def evaluate_city_safety(self):
        for e in self.__managed_elements:
            if hasattr(e,'is_dangerous'):
                is_hazard, reason = e.is_dangerous
                if is_hazard:
                    print(f"Uyari: {e.id} {e.location} cihazindan tehlike sinyali alindi! Nedeni: {reason}")
                    self.emergency_protocol(e.location,reason)
    
    def emergency_protocol(self,location,reason):
        if reason == "ICY_ROAD":
            print(f"Acil Durum Protokolu: {location} konumunda buzlu yol tespit edildi. Trafik isigi sureleri uzatiliyor ve hiz sinirlari dusuruluyor.")

    def syncing_with_clock(self,clock):
        current_mode = clock.time_mode
        print(f"{self.__service_name}: Tum cihazlar {current_mode} moduna senkronize ediliyor.")

        for e in self.__managed_elements:
            if hasattr(e,'apply_mode_logic'):
                e.apply_mode_logic(current_mode)

class TrafficAnalyticService:
    def __init__(self,repo:TrafficRepository):
        self.__repo = repo
    
    def calculate_road_violation_revenue(self):
        total_revenue = 0
        camera = self.__repo.find_by_type(SpeedCamera)
        for cam in camera:
            total_revenue += cam.fine_calculation()
        return total_revenue
    
    def get_environmental_impact(self):
        sensors = self.__repo.find_by_type(IntersectionSensor)
        emission = 0
        for s in sensors:
            emission += s.current_vehicle_count
        return emission * 0.12 # average CO2 emission per vehicle in grams/km (its around 100 - 180 btw) source: trust me
    