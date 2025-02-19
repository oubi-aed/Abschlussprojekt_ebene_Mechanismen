from tinydb import TinyDB, Query



class Gelenk:
    id_counter = 1  # Automatische ID-Vergabe

    def __init__(self, x: float, y: float, ist_statisch: bool = False, id: int = None):
        """Ein Gelenk mit Position und Status (statisch oder beweglich)."""
        if id is None:
            self.id = Gelenk.id_counter
            Gelenk.id_counter += 1
        else:
            self.id = id  # Falls aus TinyDB geladen wird, behalten wir die ID bei

        self.x = x
        self.y = y
        self.ist_statisch = ist_statisch

    def speichern(self, db: TinyDB):
        """Speichert das Gelenk in TinyDB."""
        table = db.table("Gelenke")
        table.upsert({"id": self.id, "x": self.x, "y": self.y, "ist_statisch": self.ist_statisch}, Query().id == self.id)

    @staticmethod
    def laden(db: TinyDB, id: int):
        """Lädt ein Gelenk aus TinyDB anhand seiner ID."""
        table = db.table("Gelenke")
        daten = table.get(Query().id == id)
        if daten:
            return Gelenk(daten["x"], daten["y"], daten["ist_statisch"], id=daten["id"])
        return None

    def __repr__(self):
        return f"Gelenk(ID={self.id}, x={self.x}, y={self.y}, Statisch={self.ist_statisch})"