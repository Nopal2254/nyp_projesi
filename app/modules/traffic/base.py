"""
TRAFİK YÖNETİM MODÜLÜ - TEMEL SOYUT SINIF TANIMLAMALARI
Bu modül, Akıllı Şehir Yönetim Sistemi'nin trafik bileşenleri için 
temel arayüzü ve ortak özellikleri tanımlar.
"""

from abc import ABC, abstractmethod # 
from datetime import datetime

class TrafficElement(ABC): # [cite: 73]
    """
    Trafik sistemindeki tüm fiziksel cihazlar (Işık, Kamera, Sensör) 
    için temel soyut sınıf.
    """

    def __init__(self, element_id: str, location: str, status: str = "Active"):
        """
        Başlangıç değerlerini atar. 
        :param element_id: Cihazın benzersiz kimliği
        :param location: Cihazın bulunduğu koordinat veya bölge
        :param status: Cihazın çalışma durumu (Active, Inactive, Maintenance)
        """
        self._element_id = element_id
        self._location = location
        self._status = status
        self._last_update = datetime.now()

    # --- GETTER / SETTER ---
    @property
    def element_id(self):
        return self._element_id

    @property
    def location(self):
        return self._location

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self._last_update = datetime.now()

    # --- SOYUT METOTLAR (Abstract Methods) ---
    # Bu metotlar tüm alt sınıflar tarafından override edilmek zorundadır. [cite: 28, 33]

    @abstractmethod
    def perform_action(self):
        """Cihazın ana işlevini yerine getirmesini sağlar (Işık yakma, hız ölçme vb.)."""
        pass

    @abstractmethod
    def get_status_report(self) -> dict:
        """Cihazın mevcut durumu hakkında detaylı bir rapor döndürür."""
        pass

    # --- SINIF METOTLARI (Class Methods) ---
    # PDF'de istenen 2 adet sınıf metodu gereksinimini karşılar. 

    @classmethod
    def create_maintenance_element(cls, element_id: str, location: str):
        """Bakım modunda yeni bir element oluşturur."""
        return cls(element_id, location, status="Maintenance")

    @classmethod
    def get_version(cls):
        """Sistemin versiyon bilgisini döner."""
        return "v1.0.2 - Traffic Management Core"

    # --- STATİK METOTLAR (Static Methods) ---
    # PDF'de istenen 2 adet statik metot gereksinimini karşılar. 

    @staticmethod
    def validate_id(element_id: str) -> bool:
        """ID formatının doğruluğunu kontrol eder (Örn: TRF-123)."""
        return element_id.startswith("TRF-") and len(element_id) > 4

    @staticmethod
    def calculate_uptime(install_date: datetime) -> int:
        """Kurulum tarihinden itibaren geçen gün sayısını hesaplar."""
        delta = datetime.now() - install_date
        return delta.days