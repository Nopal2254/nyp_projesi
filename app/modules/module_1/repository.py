from app.modules.module_1.base import TrafficElement
from datetime import datetime

class TrafficRepository:
    @classmethod
    def initialize_default(cls):
        repo = cls()
        return repo
    
    def __init__(self):
        #imma using dictionary
        self.__storage = {}

    #generate log entry
    @staticmethod
    def format_log(action,id):
        return f"[{datetime.now()}] {action.upper()} - Cihaz ID : {id}"
    
    #add new element
    def add(self,element:TrafficElement):
        if element.id in self.__storage:
            print(f"Warning: Cihaz {element.id} zaten mevcut!")
            return False
        self.__storage[element.id] = element
        print(self.format_log("ekleme",element.id))
        return True
    
    #find element by id
    def get_by_id(self,id):
        return self.__storage.get(id,None)
    
    #find elements by location
    def find_by_location(self,location):
        results = []
        for element in self.__storage.values():
            if element.location == location:
                results.append(element)
        return results
    
    #find elements by type
    def find_by_type(self,type):
        return [element for element in self.__storage.values() if isinstance(element,type)]

    def remove(self,id):
        if id in self.__storage:
            del self.__storage[id]
            print(self.format_log("silme",id))
            return True
        else:
            print(f"Warning: Cihaz {id} bulunamadi!")
            return False
    
    @property
    def count(self):
        return len(self.__storage)
    