"""
TRAFİK REPOSİTORY KATMANI (TRANSPORT REPOSITORY)

Bu dosya, trafik modülündeki tüm nesnelerin (ışıklar, kameralar, sensörler) 
bellek üzerinde (in-memory) yönetildiği, sorgulandığı ve depolandığı katmandır.
"""

from typing import List, Optional, Dict
from .base import TrafficElement
import datetime

class TransportRepository:
    """
    Trafik bileşenleri için bellek içi veri yönetim sınıfı. [cite: 48, 51]
    Bu sınıf, bir veritabanı gibi davranarak verilerin eklenmesi, silinmesi 
    ve filtrelenmesi işlemlerini yürütür.
    """

    def __init__(self):
        """
        Depo yapısını başlatır. Veriler hızlı erişim için sözlük (dict) 
        yapısında tutulur. [cite: 51]
        """
        # Key: element_id, Value: TrafficElement nesnesi
        self._elements: Dict[str, TrafficElement] = {}
        # İşlem günlüklerini tutmak için basit bir liste
        self._logs: List[str] = []

    # --- TEMEL VERİ İŞLEMLERİ (CRUD) ---

    def save(self, element: TrafficElement) -> bool:
        """
        Yeni bir trafik elemanını sisteme kaydeder veya günceller. [cite: 88]
        
        Args:
            element (TrafficElement): Kaydedilecek nesne.
        Returns:
            bool: İşlem başarısı.
        """
        if not element:
            return False
            
        self._elements[element.element_id] = element
        log_entry = f"[{datetime.datetime.now()}] KAYIT: {element.element_id} sisteme eklendi."
        self._logs.append(log_entry)
        return True

    def get_by_id(self, element_id: str) -> Optional[TrafficElement]:
        """
        ID bazlı arama yapar. 
        """
        return self._elements.get(element_id)

    def delete(self, element_id: str) -> bool:
        """Sistemden bir cihaz kaydını siler."""
        if element_id in self._elements:
            del self._elements[element_id]
            return True
        return False

    # --- SORGULAMA VE FİLTRELEME METOTLARI ---

    def find_all_by_location(self, location: str) -> List[TrafficElement]:
        """
        Belirli bir lokasyondaki tüm cihazları listeler. [cite: 89, 116]
        """
        results = [
            el for el in self._elements.values() 
            if el.location.lower() == location.lower()
        ]
        return results

    def filter_by_status(self, status: str) -> List[TrafficElement]:
        """
        Cihazları aktiflik durumuna göre filtreler. 
        """
        return [
            el for el in self._elements.values() 
            if el.status.lower() == status.lower()
        ]

    # --- SINIF VE STATİK METOTLAR (PDF ŞARTLARI) ---

    @classmethod
    def create_with_initial_data(cls, initial_elements: List[TrafficElement]):
        """
         Başlangıç verileriyle bir depo örneği oluşturur (Sınıf Metodu 1).
        """
        repo = cls()
        for el in initial_elements:
            repo.save(el)
        return repo

    @classmethod
    def get_storage_type(cls):
        """
        Kullanılan depolama tipini döndürür (Sınıf Metodu 2). [cite: 50]
        """
        return "InMemory / Dictionary Based Storage"

    @staticmethod
    def validate_element_data(data: dict) -> bool:
        """
        Gelen verinin kayıt için uygunluğunu kontrol eder (Statik Metot 1). 
        """
        required_fields = ["location", "type"]
        return all(field in data for field in required_fields)

    @staticmethod
    def get_help_guide() -> str:
        """
        Repository kullanımı için rehber metni döner (Statik Metot 2). 
        """
        return "Save, Get, Filter ve Delete metotlarını kullanın."