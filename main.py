"""
PROJE İSMİ: AKILLI ŞEHİR YÖNETİM SİSTEMİ (SMART CITY MANAGEMENT SYSTEM)
DOSYA: main.py - ANA SENARYO VE MODÜLLER ARASI ETKİLEŞİM YÖNETİMİ

Bu dosya, projenin giriş noktasıdır (entry point). Farklı öğrenciler tarafından 
geliştirilen modülleri bir araya getirerek şehir yönetim senaryolarını simüle eder.
"""

import time
from datetime import datetime

# Trafik Modülü Importları
from app.modules.traffic.implementations import TrafficLight, IntersectionSensor, TrafficService
from app.modules.traffic.repository import TransportRepository

# NOT: Diğer modüller (Enerji, Acil Durum, Sosyal Hizmetler) henüz tam yazılmadığı 
# için bu aşamada 'Mock' (geçici/taslak) yapılar veya temel sınıflar kullanılabilir.

def display_welcome_message():
    """Sistem açılış ekranı için bilgilendirme mesajı."""
    print("="*60)
    print(f"{'AKILLI ŞEHİR YÖNETİM SİSTEMİ BAŞLATILIYOR':^60}")
    print(f"{'Sistem Saati: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^60}")
    print("="*60)

def simulate_emergency_interaction(location, density_level):
    """
    MODÜLLER ARASI ETKİLEŞİM SENARYOSU
    Trafik yoğunluğu arttığında acil durum birimlerine haber verilmesini simüle eder.
    """
    print(f"\n[SİSTEM MESAJI] Etkileşim Tetiklendi: Trafik Modülü -> Acil Durum Modülü")
    print(f"[BİLGİ] {location} bölgesinde yoğunluk {density_level} seviyesine ulaştı.")
    print(f"[AKSİYON] Acil Durum birimleri (Ambulans/İtfaiye) alternatif rotalara yönlendiriliyor.")

def main():
    """Ana uygulama döngüsü ve senaryo yönetimi."""
    
    display_welcome_message()

    # 1. ALTYAPI KURULUMU (TRAFİK MODÜLÜ ÖRNEĞİ)
    # ---------------------------------------------------------
    # Repository ve Servis başlatma
    traffic_db = TransportRepository()
    traffic_manager = TrafficService(traffic_db)

    # 2. CİHAZ KAYITLARI (MODÜL ÖĞELERİNİN OLUŞTURULMASI)
    # ---------------------------------------------------------
    # Trafik Işığı ve Sensör örnekleri
    main_sensor = IntersectionSensor("TRF-99", "Merkez Meydan Kavşağı")
    pedestrian_light = TrafficLight("TL-404", "Atatürk Bulvarı", "Red")
    
    traffic_db.save(main_sensor)
    traffic_db.save(pedestrian_light)

    # 3. SENARYO: YOĞUNLUK BAZLI YÖNETİM
    # ---------------------------------------------------------
    print("\n--- Şehir Trafik Akışı İzleniyor ---")
    
    # Sensörden gelen veriyi simüle edelim (PDF: Yoğunluk hesaplama)
    main_sensor.vehicle_count = 92 # Kritik sınır
    print(f"[{main_sensor.location}] Anlık Araç Sayısı: {main_sensor.vehicle_count}")

    # Yoğunluk Analizi [cite: 83]
    current_density = traffic_manager.calculate_intersection_density(main_sensor.element_id)
    
    # MODÜLLER ARASI ETKİLEŞİM 
    if current_density == "Kritik":
        simulate_emergency_interaction(main_sensor.location, current_density)
        
        # Trafik Işığı Optimizasyonu [cite: 84]
        opt_msg = traffic_manager.optimize_light_timing(pedestrian_light.element_id, current_density)
        print(f"[TRAFİK KONTROL] {opt_msg}")

    print("\n" + "="*60)
    print(f"{'SİSTEM BEKLEME MODUNDA':^60}")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Sistem Hatası: {e}")