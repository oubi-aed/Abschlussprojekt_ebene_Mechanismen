from tinydb import TinyDB, Query

class Glied:
    id_counter = 1  # Automatische ID-Vergabe

    def __init__(self, start_id: int, ende_id: int, ist_kurbel: bool = False, id: int = None):
        """Ein Glied verbindet zwei Gelenke. Falls es eine Kurbel ist, verbindet es ein statisches und ein dynamisches Gelenk."""
        if id is None:
            self.id = Glied.id_counter
            Glied.id_counter += 1
        else:
            self.id = id  # Falls aus TinyDB geladen wird, behalten wir die ID bei

        self.start_id = start_id
        self.ende_id = ende_id
        self.ist_kurbel = ist_kurbel  # Falls das Glied eine Kurbel ist (statisch <-> dynamisch)

    def speichern(self, db: TinyDB, mechanismus_name: str):
        """Speichert das Glied in TinyDB."""
        table = db.table("glieder")
        table_mechanismen = db.table("mechanismen")
        table.upsert({
            "id": self.id, "start_id": self.start_id, "ende_id": self.ende_id, "ist_kurbel": self.ist_kurbel
        }, Query().id == self.id)

        mechanismus = table_mechanismen.get(Query().name == mechanismus_name) 
        if mechanismus:
            mechanismus["glieder"].append ({
                "id": self.id, "start_id": self.start_id, "ende_id": self.ende_id, "ist_kurbel": self.ist_kurbel
            })
            table_mechanismen.update(mechanismus, Query().name == mechanismus_name)



    @staticmethod
    def laden(db: TinyDB, id: int):
        """Lädt ein Glied aus TinyDB anhand seiner ID."""
        table = db.table("glieder")
        daten = table.get(Query().id == id)
        if daten:
            return Glied(daten["start_id"], daten["ende_id"], daten["ist_kurbel"], id=daten["id"])
        return None

    def __repr__(self):
        return f"Glied(ID={self.id}, Start={self.start_id}, Ende={self.ende_id}, Kurbel={self.ist_kurbel})"
