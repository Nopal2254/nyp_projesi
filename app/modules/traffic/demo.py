"""
TRAFİK MODÜLÜ DEMO SENARYOSU
Bu dosya, modülün tek başına nasıl çalıştığını simüle eder ve 
polimorfizm (çok biçimlilik) prensibini gösterir. [cite: 53, 54]
"""

from app.modules.traffic.implementations import TrafficLight, SpeedCamera, IntersectionSensor, TrafficService
from app.modules.traffic.repository import TransportRepository
import time

def run_traffic_demo():
    """Modülün ana çalışma senaryosu."""
    
    # 1. Repository ve Servis Hazırlığı [cite: 45, 48]
    repo = TransportRepository()
    service = TrafficService(repo)

    # 2. Farklı alt sınıf örneklerinin oluşturulması [cite: 31, 55]
    tl = TrafficLight("TRF-101", "Atatürk Bulvarı", "Red")
    sc = SpeedCamera("TRF-502", "Sahil Yolu", 70.0)
    is_sensor = IntersectionSensor("TRF-903", "Merkez Kavşak")

    # Nesneleri repository'ye kaydetme [cite: 88]
    repo.save(tl)
    repo.save(sc)
    repo.save(is_sensor)

    # 3. POLİMORFİZM GÖSTERİMİ [cite: 12, 56, 58]
    # Farklı tipteki nesneler aynı listede tutulur ve ortak metotları çağrılır.
    traffic_elements = [tl, sc, is_sensor]
    
    print("\n--- POLİMORFİZM ÇIKTISI ---")
    for element in traffic_elements:
        # Her nesne kendi 'perform_action' metodunu farklı şekilde icra eder 
        result = element.perform_action()
        print(f"Cihaz İşlemi: {result}")
        
        # Her nesne kendi 'get_status_report' raporunu sunar [cite: 28]
        report = element.get_status_report()
        print(f"Durum Raporu: {report}")
        print("-" * 20)

    # 4. SERVİS SENARYOSU [cite: 82, 96]
    print("\n--- TRAFİK SERVİS SENARYOSU ---")
    # Sensör veri okuması yapar
    is_sensor.vehicle_count = 85  # Yoğunluk simülasyonu
    density = service.calculate_intersection_density("TRF-903")
    print(f"Kavşak Durumu: {density}")

    # Yoğunluğa göre ışık süresi optimize edilir [cite: 84]
    optimization_result = service.optimize_light_timing("TRF-101", density)
    print(optimization_result)

if __name__ == "__main__":
    run_traffic_demo()