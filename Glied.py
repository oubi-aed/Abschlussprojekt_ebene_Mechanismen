from tinydb import TinyDB, Query

class Glied:
    id_counter = 1  # Automatische ID-Vergabe

    def __init__(self, start_id: int, ende_id: int, laenge: float, id: int = None):
        """Ein Glied verbindet zwei Gelenke über deren IDs."""
        if id is None:
            self.id = Glied.id_counter
            Glied.id_counter += 1
        else:
            self.id = id  # Falls aus TinyDB geladen wird, behalten wir die ID bei

        self.start_id = start_id
        self.ende_id = ende_id
        self.laenge = laenge

    def speichern(self, db: TinyDB):
        """Speichert das Glied in TinyDB."""
        table = db.table("glieder")
        table.upsert({"id": self.id, "start_id": self.start_id, "ende_id": self.ende_id, "laenge": self.laenge}, Query().id == self.id)

    @staticmethod
    def laden(db: TinyDB, id: int):
        """Lädt ein Glied aus TinyDB anhand seiner ID."""
        table = db.table("glieder")
        daten = table.get(Query().id == id)
        if daten:
            return Glied(daten["start_id"], daten["ende_id"], daten["laenge"], id=daten["id"])
        return None

    def __repr__(self):
        return f"Glied(ID={self.id}, Start={self.start_id}, Ende={self.ende_id}, Länge={self.laenge})"
