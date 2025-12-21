import unittest
from app.modules.module_1.implementations import TrafficLight,RoadConditionSensor
from app.modules.module_1.repository import TrafficRepository

class TestTrafficModule(unittest.TestCase):
    ##TrafficLight durum guncelleme testi
    def test_traffic_light_status(self):
        light = TrafficLight("TL-1","Location-A","Active","Kirmizi")

        light.update_status("Maintenance")
        self.assertEqual(light.status,"Maintenance")

        light.update_status("InvalidStatus")
        self.assertEqual(light.status,"Unknown")

    ##Dangerous durum testi
    def test_road_sensor_danger_threshold(self):
        sensor = RoadConditionSensor("ENV-01","Location-B","Active",20.0)
        sensor.moisture = 10

        self.assertFalse(sensor.is_dangerous())

        sensor.road_temperature = -5
        sensor.moisture = 50

        self.assertTrue(sensor.is_dangerous())

    ##Repository ekleme ve sayma testi
    def test_repo_storage(self):
        repo = TrafficRepository()
        light = TrafficLight("TL-2","Location-C","Active","Yesil")

        repo.add(light)
        self.assertEqual(repo.count,1)

        retrievd = repo.get_by_id("TL-2")
        self.assertEqual(retrievd.location,"Location-C")

if __name__ == "__main__":
    unittest.main()