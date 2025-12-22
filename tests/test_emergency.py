import unittest
from app.modules.emergency.base import UnitStatus
from app.modules.emergency.implementations import(
    FireDepartment,
    Ambulance,
    PoliceUnit,
    HazmatUnit,
    Incident,
    EmergencyService
)
from app.modules.emergency.repository import (
    EmergencyRepository,
    EmergencyUnit
    )
class TestEmergencyModule(unittest.TestCase):
    def setUp(self):
        self.repo = EmergencyRepository()
        self.service = EmergencyService()

        self.fire_unit = FireDepartment("F-TEST","North",water_capacity=10000)
        self.police_unit = PoliceUnit("P-TEST","South","Zone A",officer_count=50)

        self.repo.add_unit(self.fire_unit)
        self.repo.add_unit(self.police_unit)


    def test_unit_initialization(self):
        self.assertEqual(self.fire_unit.unit_id,"F-TEST")
        self.assertEqual(self.fire_unit.unit_type,"Fire")
        self.assertTrue(self.fire_unit.availability)
        self.assertEqual(self.fire_unit.status,UnitStatus.IDLE)

    def test_status_availability(self):
        self.fire_unit.status = UnitStatus.ON_SCENE
        self.assertFalse(self.fire_unit.availability)

        self.fire_unit.status = UnitStatus.IDLE
        self.assertTrue(self.fire_unit.availability)

    def test_repo_filtering(self):
        fire_unit = self.repo.get_available_unit_by_type("Fire")
        self.assertEqual(len(fire_unit),1)
        self.assertEqual(fire_unit[0].unit_id,"F-TEST")

    def test_repo_stats(self):
        stats = self.repo.operational_stats()
        self.assertEqual(stats["calculated_readiness_percentage"],100.0)

        self.police_unit.status = UnitStatus.ON_SCENE
        new_stats = self.repo.operational_stats()
        self.assertEqual(new_stats["calculated_readiness_percentage"],50.0)

    def test_dispatch_success(self):
        vaka = Incident("V-01","Fire",3,"Mall","Small Fire")
        result = self.service.dispatch_nearest_unit(vaka)

        self.assertIn("Dispatch Successful",result)
        self.assertEqual(self.fire_unit.status,UnitStatus.ON_SCENE)

    def test_dispatch_no_available_units(self):
        self.fire_unit.status = UnitStatus.MAINTENANCE

        vaka = Incident("V-02","Fire",2,"Home","Smoke Reported")
        plan = self.service.generate_intervention_plan(vaka,self.police_unit)

        self.assertIn("PLAN ID",plan)
        self.assertIn("Secure Perimeter",plan)

if __name__ == "__main__":
    unittest.main()