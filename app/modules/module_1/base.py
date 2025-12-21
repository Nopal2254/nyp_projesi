from abc import ABC, abstractmethod

class TrafficElement(ABC):
    def __init__(self,id, location,status):
        self.__id = id
        self.__location = location
        self.__status = status  

    #update status of the element
    @abstractmethod
    def update_status(self):
        pass
    
    #get service report of the element
    @abstractmethod
    def get_service_report(self):
        pass
    
    #restart the system
    def system_restart(self):
        self.__status = "Rebooting"
        print(f"Sistem {self.__id} yeniden baslatiliyor...")

    @property
    def id(self):
        return self.__id
    
    @property
    def location(self):
        return self.__location

    @property
    def status(self):
        return self.__status

    @id.setter
    def id(self, value):
        if value:
            self.__id = value    
    
    @location.setter
    def location(self, value):
        if value:
            self.__location = value
    
    @status.setter
    def status(self, value):
        statuses = ["Active","Inactive","Rebooting","Maintenance"]

        if value in statuses:
            self.__status = value
            print(f"{self.__id} durumu {value} olarak degistirildi.")
        else:
            self.__status = "Unknown"
            print(f"Warning: Gecersiz durum! {self.__id} durumu Unknown olarak ayarlandi.")