from tinydb import TinyDB, Query

class Gelenk:
    def __init__(self, id: int, x: float, y: float, ist_statisch: bool = False):
        """Ein Gelenk mit ID, Position und Status (statisch oder beweglich)."""
        self.id = id
        self.x = x
        self.y = y
        self.ist_statisch = ist_statisch

    def speichern(self, db: TinyDB):
        """Speichert das Gelenk in TinyDB."""
        table = db.table("gelenke")
        table.upsert({"id": self.id, "x": self.x, "y": self.y, "ist_statisch": self.ist_statisch}, Query().id == self.id)

    @staticmethod
    def laden(db: TinyDB, id: int):
        """Lädt ein Gelenk aus TinyDB anhand seiner ID."""
        table = db.table("gelenke")
        daten = table.get(Query().id == id)
        if daten:
            return Gelenk(daten["id"], daten["x"], daten["y"], daten["ist_statisch"])
        return None

    def __repr__(self):
        return f"Gelenk(ID={self.id}, x={self.x}, y={self.y}, Statisch={self.ist_statisch})"
