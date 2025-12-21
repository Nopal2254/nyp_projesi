"""
TRAFİK MODÜLÜ IMPLEMENTASYONLARI
Bu dosya, somut trafik bileşenlerini ve trafik yönetimi için gerekli servisleri içerir.
Tüm sınıflar 'TrafficElement' base class'ından türetilmiştir. [cite: 31, 32]
"""

from .base import TrafficElement
from dataclasses import dataclass
from datetime import datetime
import random

# --- 1. ENTITIES / MODELS --- [cite: 37]
@dataclass
class TrafficViolation:
    """
    Trafik ihlallerini temsil eden veri sınıfı. [cite: 38]
    Hız kameraları tarafından tespit edilen verileri standartlaştırır.
    """
    violation_id: str
    vehicle_plate: str
    detected_speed: float
    limit: float
    timestamp: datetime

# --- 2. SUBCLASSES (Inheritance & Polymorphism) --- [cite: 30]

class TrafficLight(TrafficElement):
    """
    Trafik Işığı bileşeni. [cite: 78]
    Işık renk değişimi ve zamanlayıcı yönetimini sağlar.
    """
    def __init__(self, element_id: str, location: str, current_color: str = "Red"):
        # Base class constructor'ını çağırıyoruz [cite: 13, 75]
        super().__init__(element_id, location)
        self.current_color = current_color
        self.timer = 30  # Saniye cinsinden varsayılan süre

    def perform_action(self):
        """
        Işık rengini döngüsel olarak değiştirir. [cite: 33, 76]
        Red -> Yellow -> Green -> Red akışını simüle eder.
        """
        colors = ["Red", "Yellow", "Green"]
        try:
            current_idx = colors.index(self.current_color)
            next_index = (current_idx + 1) % len(colors)
            self.current_color = colors[next_index]
            return f"CIHAZ {self.element_id}: Işık rengi {self.current_color} olarak değişti."
        except ValueError:
            self.current_color = "Red"
            return "Hata: Geçersiz renk durumu sıfırlandı."

    def get_status_report(self) -> dict:
        """Işığın mevcut durum raporunu oluşturur. [cite: 33]"""
        return {
            "type": "TrafficLight",
            "id": self.element_id,
            "current_color": self.current_color,
            "timer_setting": self.timer,
            "last_update": datetime.now().strftime("%H:%M:%S")
        }

class SpeedCamera(TrafficElement):
    """
    Hız Kamerası bileşeni. [cite: 79]
    Araç hızlarını takip eder ve limit aşımında ihlal kaydı oluşturur.
    """
    def __init__(self, element_id: str, location: str, speed_limit: float = 70.0):
        super().__init__(element_id, location)
        self.speed_limit = speed_limit
        self.violation_count = 0

    def perform_action(self):
        """Hız ölçümü yapar ve ihlal varsa tespit eder. [cite: 85]"""
        simulated_speed = random.uniform(40.0, 110.0)
        if simulated_speed > self.speed_limit:
            self.violation_count += 1
            return f"ALARM: {self.location} konumunda {simulated_speed:.2f} km/s hız tespiti!"
        return f"Normal Akış: {simulated_speed:.2f} km/s."

    def get_status_report(self) -> dict:
        return {
            "type": "SpeedCamera",
            "id": self.element_id,
            "limit": self.speed_limit,
            "total_violations": self.violation_count
        }

class IntersectionSensor(TrafficElement):
    """
    Kavşak Yoğunluk Sensörü. [cite: 80]
    Anlık araç sayısını ölçerek trafik yoğunluğunu belirler.
    """
    def __init__(self, element_id: str, location: str):
        super().__init__(element_id, location)
        self.vehicle_count = 0

    def perform_action(self):
        """Araç sayısını günceller. [cite: 94]"""
        self.vehicle_count = random.randint(0, 100)
        return f"{self.location} sensörü {self.vehicle_count} araç algıladı."

    def get_status_report(self) -> dict:
        return {
            "type": "Sensor",
            "id": self.element_id,
            "vehicle_count": self.vehicle_count
        }

# --- 3. SERVICE LAYER --- [cite: 40]

class TrafficService:
    """
    Trafik modülünün iş kurallarını yöneten ana servis. [cite: 41, 82]
    """
    def __init__(self, repository):
        self.repository = repository

    def calculate_intersection_density(self, sensor_id: str):
        """Kavşaktaki araç sayısına göre yoğunluk durumu belirler. [cite: 83]"""
        sensor = self.repository.get_by_id(sensor_id)
        if sensor and isinstance(sensor, IntersectionSensor):
            if sensor.vehicle_count > 80:
                return "Kritik"
            elif sensor.vehicle_count > 40:
                return "Normal"
            else:
                return "Düşük"
        return "Bilinmiyor"

    def optimize_light_timing(self, light_id: str, density: str):
        """Yoğunluk durumuna göre ışık sürelerini ayarlar. [cite: 84]"""
        light = self.repository.get_by_id(light_id)
        if light and isinstance(light, TrafficLight):
            if density == "Kritik":
                light.timer = 60
            else:
                light.timer = 30
            return f"{light_id} için yeşil süre {light.timer} sn olarak güncellendi."
        return "Işık bulunamadı."