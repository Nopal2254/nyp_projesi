from app.modules.module_1.implementations import (
    TrafficLight,
    SpeedCamera,
    IntersectionSensor,
    RoadConditionSensor,
    SimulationClock,
    IncidentManagerService,
    TrafficService
)

from app.modules.module_1.repository import TrafficRepository

def run_demo():
    print("#Trafik Yonetim Sistemi Demo Basladi...\n")
    #Initialization
    repo = TrafficRepository.initialize_default()
    traffics_manager = TrafficService.create_zone_service("Sehir-Merkezi-01")
    
    #Normal mode sim
    clock = SimulationClock(12)
    traffics_manager.syncing_with_clock(clock)
    print("\n")
    
    #Rush hour sim
    clock.advance_time(9)
    traffics_manager.syncing_with_clock(clock)
    print("\n")
    
    #Night mode sim
    clock.advance_time(18)
    traffics_manager.syncing_with_clock(clock)
    print("\n")

    #Creating elements
    light_01 = TrafficLight("TL-001","5th Avenue & Main St","Active","Yesil")
    camera_01 = SpeedCamera("SC-001","5th Avenue","Active",50,speed_limit=60)
    sensor_01 = IntersectionSensor("IS-001","Main St & 6th Avenue","Active",sensitivity = 10)
    road_env_01 = RoadConditionSensor("RCS-001","Highway 101","Active",road_temperature=15,moisture=30)

    elements = [light_01, camera_01, sensor_01, road_env_01]

    for el in elements:
        repo.add(el)
        traffics_manager.register_device(el)
    
    print("\n-- Sistem Saglik Kontrolu --")
    traffics_manager.run_system_health_check()

    incident_service = IncidentManagerService(repo)
    is_hazard,reason = road_env_01.is_dangerous

    if is_hazard:
        incident_service.report_incident(road_env_01.location,reason,"High")

    #Speed violation simulation
    current_speed = 170
    fine = SpeedCamera.fine_calculation(current_speed,120)
    if fine > 0:
        print(f"Hiz ihlali {camera_01.location}'da tespit edildi! Hiciz: {current_speed} km/s. Ceza: {fine} TL")
    else:
        print("Hiz sinirinda seyahat ediliyor.")
    print("\n")

    #Winter hazard simulation
    road_env_01.road_temperature = -10
    road_env_01.moisture = 85

    traffics_manager.monitor_road_safety()

    #Finding devices by location
    print("\n-- Cihazlari Konuma Gore Bulma --")
    bridge_devices = repo.find_by_location("Highway 101")
    for d in bridge_devices:
        print(f"Found device at {d.location}: ID = {d.id}")
    
    print(f"\nToplam cihaz sayisi: {repo.count}")

    print("\nTrafik Yonetim Sistemi Demo Tamamlandi.")

if __name__ == "__main__":
    run_demo()

#if u wanna run the project through this file run with that below
# py -m base.modules.modules_1.demo