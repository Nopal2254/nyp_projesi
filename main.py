from app.modules.module_1.implementations import (
    TrafficLight,
    SpeedCamera,
    IntersectionSensor,
    RoadConditionSensor,
    SimulationClock,
    IncidentManagerService,
    TrafficService,
)
from app.modules.module_1.repository import TrafficRepository

from app.modules.module_2.implementations import (
    Base2SubClass1, Base2SubClass2
)

from app.modules.module_3.implementations import (
    Base3SubClass1, Base3SubClass2
)

from app.modules.module_4.implementations import (
    Base4SubClass1, Base4SubClass2
)

def run_demo():
    print("=== AKILLI SEHIR MENU ===")
    print("\n--- Trafik Yonetim Sistemi Demo ---\n")

    # Ogrenci 1 (Modul 1) => Trafik Yonetim Sistemi
    traffic_repo = TrafficRepository.initialize_default()
    traffic_service = TrafficService.create_zone_service("Sehir-Merkezi")
    traffic_clock = SimulationClock(start_hour=17)
    traffic_incident_manager = IncidentManagerService(traffic_repo)

    traffic_elements = [
        TrafficLight("TL-100", "1st St & A Ave", "Active", "Kirmizi"),
        SpeedCamera("SC-100", "1st St", "Active", 120, speed_limit=60),
        RoadConditionSensor("RCS-100", "Highway 1", "Active", road_temperature=-5, moisture=45),
        IntersectionSensor("IS-100", "A Ave & B Ave", "Active", sensitivity=8),
    ]
    # Register elements
    for e in traffic_elements:
        traffic_repo.add(e)
        traffic_service.register_device(e)
    print("\n")
    
    # Simulate time changes and system evaluations
    traffic_service.syncing_with_clock(traffic_clock)
    traffic_service.evaluate_city_safety()  #Speed/Ice check

    # Ogrenci 2 (Modul 2)
    base_2 = [
        Base2SubClass1("parametre3"),
        Base2SubClass2("parametre4")
    ]
    for e in base_2:
        e.method2()

        
    # Ogrenci 3 (Modul 3)
    base_3 = [
        Base3SubClass1("parametre5"),
        Base3SubClass2("parametre6")
    ]
    for p in base_3:
        p.method3()

    # Ogrenci 4 (Modul 4)
    object1 = Base4SubClass1("parametre7")
    object2 = Base4SubClass2("parametre8")
    object1.method4()
    object2.method4()

if __name__ == "__main__":
    run_demo()