"""
TRAFİK MODÜLÜ BİRİM TESTLERİ (UNIT TESTS)

Bu dosya, Trafik Yönetim Modülü'nün tüm bileşenlerinin 
doğru çalışıp çalışmadığını test eder.
"""

import unittest
from datetime import datetime
from app.modules.traffic.base import TrafficElement
from app.modules.traffic.implementations import TrafficLight, SpeedCamera, IntersectionSensor, TrafficService
from app.modules.traffic.repository import TransportRepository

class TestTrafficModule(unittest.TestCase):
    """Trafik modülü için test senaryoları sınıfı."""

    def setUp(self):
        """Her testten önce çalışan hazırlık metodu."""
        self.repo = TransportRepository()
        self.service = TrafficService(self.repo)
        
        # Test verilerini oluşturma
        self.light = TrafficLight("TL-TEST", "Test Kavşağı", "Red")
        self.sensor = IntersectionSensor("SN-TEST", "Test Kavşağı")
        self.camera = SpeedCamera("CM-TEST", "Test Yolu", 70.0)
        
        self.repo.save(self.light)
        self.repo.save(self.sensor)
        self.repo.save(self.camera)

    # 1. REPOSİTORY TESTLERİ [cite: 95]
    def test_repository_save_and_get(self):
        """Repository kayıt ve getirme işlemini test eder."""
        found = self.repo.get_by_id("TL-TEST")
        self.assertIsNotNone(found)
        self.assertEqual(found.location, "Test Kavşağı")

    def test_repository_filter_location(self):
        """Lokasyona göre filtreleme test edilir. [cite: 89]"""
        results = self.repo.find_by_location("Test Kavşağı")
        self.assertEqual(len(results), 2) # Işık ve Sensör

    # 2. SİMÜLASYON TESTLERİ [cite: 92, 94]
    def test_traffic_light_action(self):
        """Trafik ışığı renk değişim döngüsü test edilir."""
        initial_color = self.light.current_color
        self.light.perform_action() # Red -> Yellow
        self.assertNotEqual(initial_color, self.light.current_color)

    def test_sensor_data_update(self):
        """Sensör veri üretimi test edilir. [cite: 94]"""
        self.sensor.perform_action()
        self.assertGreaterEqual(self.sensor.vehicle_count, 0)
        self.assertLessEqual(self.sensor.vehicle_count, 100)

    # 3. SERVİS VE YOĞUNLUK TESTLERİ [cite: 93, 96]
    def test_density_calculation_critical(self):
        """Kritik yoğunluk hesaplama senaryosu. [cite: 83]"""
        self.sensor.vehicle_count = 95
        density = self.service.calculate_intersection_density("SN-TEST")
        self.assertEqual(density, "Kritik")

    def test_light_optimization(self):
        """Yoğunluğa göre süre optimizasyonu test edilir. [cite: 84]"""
        # Kritik durumda süre 60 sn olmalı
        msg = self.service.optimize_light_timing("TL-TEST", "Kritik")
        self.assertEqual(self.light.timer, 60)
        self.assertIn("60 sn", msg)

    # 4. STATİK VE SINIF METOTLARI TESTLERİ [cite: 57]
    def test_static_methods(self):
        """Base class içindeki statik metotlar test edilir."""
        # Not: base.py'da yazdığımız metotlara göre düzenlenmeli
        is_valid = TrafficElement.is_valid_status("Active")
        self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()