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

# Acil Durum modulu
from app.modules.emergency.implementations import (
    FireDepartment,
    Ambulance,
    PoliceUnit,
    HazmatUnit,
    EmergencyService    
    )
from app.modules.emergency.repository import EmergencyRepository

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

def display_menu():
    print("\n---Ana Menu ---")
    print("1. Trafik Modulu")
    print("2. Acil Cikis Modulu")
    print("3. Cikis")
    return input("Seciminizi yapin: ")

def traffic_module_menu(traffic_manager,main_sensor,pedestrian_light):
    # Simülasyon için araç sayısını doğrudan yüksek bir değere ayarlıyoruz
    main_sensor.vehicle_count = 92 
    
    print("\n" + "-"*15 + " Şehir Trafik Akışı İzleniyor " + "-"*15)
    print(f"[{main_sensor.location}] Anlık Araç Sayısı: {main_sensor.vehicle_count}")
    
    # Yoğunluk hesaplama
    current_density = traffic_manager.calculate_intersection_density(main_sensor.element_id)
    
    # Eğer yoğunluk "Kritik" ise (92 araç ile öyle olmalı), tüm süreci yazdır
    if current_density == "Kritik":
        simulate_emergency_interaction(main_sensor.location, current_density)
        
        # Trafik ışığı optimizasyonu
        opt_msg = traffic_manager.optimize_light_timing(pedestrian_light.element_id, current_density)
        print(f"[TRAFİK KONTROL] {opt_msg}")
    else:
        print(f"[BİLGİ] Trafik akışı normal seyrediyor. (Yoğunluk: {current_density})")
    
    print("-" * 60)


def emergency_module_menu(emergency_service):
    print("\n--- Acil Durum Modülü ---")
    print("1. Olay Raporu Oluştur")
    print("2. Yeni Acil Durum Birimi Kaydet")
    print("3. Geri Dön")
    choice = input("Seçiminizi yapın: ")

    if choice == "1":
        incident_id = input("Olay ID: ")
        incident_type = input("Olay Türü (Fire/Medical/Security): ")
        severity = int(input("Şiddet (1-5): "))
        location = input("Konum: ")

        incident = emergency_service.create_incident_report(incident_id, incident_type, severity, location)
        print(f"\n[SISTEM] Olay Raporu Olusturuldu: {incident.description}")

        available_units = emergency_service.repo.get_all_unit()
        suitable_units = [u for u in available_units if u.unit_type == incident.incident_type and u.availability]
        
        if not suitable_units:
            print(f"[HATA] Uygun {incident_type} birimi bulunamadi")
        else:
            selected_unit = suitable_units[0]
            
            print("\n" + "="*20 + " MÜDAHALE PLANI " + "="*20)
            plan = emergency_service.generate_intervention_plan(incident, selected_unit)
            print(plan)
            print("="*56)

            print(f"\n[SİSTEM] Birim yönlendiriliyor...")
            result = emergency_service.dispatch_nearest_unit(incident)
            print(f"[SONUÇ] {result}")

    elif choice == "2":
        print("\n--Yeni  Birim Kaydi--")
        u_type = input("Birim Turu (1.Itfaiye, 2.Ambulance, 3.Polis, 4.Hazmat): ")
        u_id = input("Birim ID: ")
        u_loc = input("Gorev Bolgesi: ")

        if u_type == "1":
            water = int(input("Su kapasitesi (L): "))
            new_unit = FireDepartment(u_id,u_loc,water)
        elif u_type == "2":
            tier = input("Tıbbi Seviye (Basic/Advanced): ")
            new_unit = Ambulance(u_id, u_loc, tier)
        elif u_type == "3":
            zone = input("Devriye Bölgesi: ")
            new_unit = PoliceUnit(u_id, u_loc, zone)
        elif u_type == "4":
            level = input("Koruma Seviyesi (A/B/C): ")
            new_unit = HazmatUnit(u_id, u_loc, level)
        else:
            print("Geçersiz tür seçildi!")
            return
        emergency_service.repo.add_unit(new_unit)
        print(f"[SISTEM] {u_id} basariyla sisteme kaydildi")

    elif choice == "3":
        return   


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

    #Acil durum modulu
    emergency_db = EmergencyRepository()
    emergency_service = EmergencyService(emergency_db)

    while True:
        choice = display_menu()

        if choice == "1":
            traffic_module_menu(traffic_manager,main_sensor,pedestrian_light)
        elif choice == "2":
            emergency_module_menu(emergency_service)
        elif choice == "3":
            print("Cikis yapiliyor...")
            break
        else:
            print("Gecersiz secim,tekrar deneyin")
    # 3. SENARYO: YOĞUNLUK BAZLI YÖNETİM
    # ---------------------------------------------------------
    print("\n" + "="*60)
    print(f"{'SİSTEM BEKLEME MODUNDA':^60}")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Sistem Hatası: {e}")