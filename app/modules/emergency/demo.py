from app.modules.emergency.base import (
    EmergencyUnit,
    UnitStatus
    )
from app.modules.emergency.implementations import (
    FireDepartment,
    Ambulance,
    PoliceUnit,
    HazmatUnit,
    Incident,
    EmergencyService
    )
from app.modules.emergency.repository import EmergencyRepository

def run_emergency_demo():
    print("="*10)
    print("Initializing Emergency Service System")
    print("="*10)

    #Initialize
    repo = EmergencyRepository()
    service = EmergencyService(repo)

    #Populate with emergency units
    print("\n[1] Registering Emergency Unit...")
    unit_to_register = [
        FireDepartment("F-01","Sehir Merkezi",water_capacity=5000),
        FireDepartment("F-02","Sehir Merkezi",water_capacity=2500),
        Ambulance("A-01","City Hospital",medical_tier="A"),
        PoliceUnit("P-01","Downtown",patrol_zone="Zone-1",officer_count=25),
        HazmatUnit("H-01","Industrial Park",protection_level="A")
    ]

    for unit in unit_to_register:
        repo.add_unit(unit)
        print(f"Registered {unit.unit_type} Unit:{unit.unit_id}")
    
    #System readiness audit 
    print("\n[2] Performing Initial System Audit...")
    stats = repo.operational_stats()
    print(f"System readiness: {stats['calculated_readniness_percentage']}%")
    print(f"Status : {stats['system_status_indicator']}")

    #1. Scenario : Fire Incident
    print("\n[3] Scenario: High Rise Fire reported !")
    fire_vaka = service.create_incident_report(
        incident_id="FIRE-2025-001",
        type="Fire",
        severity=4,
        location="Grand Plaza Hotel"
    )
    #Dispatch method havent available rn

    unit_f01 = repo.get_unit_by_id("F-01")
    if unit_f01:
        print("\nGenerating mission plan:")
        print(service.generate_intervention_plan(fire_vaka,unit_f01))

    #2. Scenario : Traffic Accident with Injuries
    print("\n[4]Scenario: Traffic Accident reported !") 
    medical_vaka = service.create_incident_report(
        incident_id="MED-2025-001",
        type="Medical",
        severity=3,
        location="Intersection 5th & Main"
    )
    #Dispatch method havent available rn

    #3.Scenario : Security Breach
    print(f"\n[5]Scenario: Suspicious activity in Zone 1")
    secuirty_vaka = service.create_incident_report(
        incident_id="SEC-2025-01",
        type="Security",
        severity=2,
        location="City Bank"
    )
    #Dispatch method havent available rn

    #Final System Review
    print("\n" + "="*10)
    print("FINAL SYSTEM LOG SUMMARY")
    print("="*10)

    logs = repo.get_system_log()
    print("Showing last 5 events")
    for e in logs[-5]:
        print(e)

    final_stats = repo.operational_stats()
    print(f"Simulation End. Final Readiness: {final_stats['calculcate_readiness_percentage']}%")


if __name__ == "__main__":
    run_emergency_demo()