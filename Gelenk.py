from tinydb import TinyDB, Query

import os
from serializer import serializer




class Gelenk:
    
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database_test2.json'), storage=serializer).table('devices')

    def __init__(self, x: float, y: float, ist_statisch: bool = False):
        """Ein Gelenk mit ID, Position und Status (statisch oder beweglich)."""
        Gelenk.id_counter = 1
        self.id_gelenk = Gelenk.id_counter
        Gelenk.id_counter += 1

        self.x = x
        self.y = y
        self.ist_statisch = ist_statisch

    def speichern(self):
        """Speichert das Gelenk in TinyDB."""
        print("Storing data...")
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")