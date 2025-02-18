from tinydb import TinyDB, Query



class Gelenk:
    Gelenk.id_counter += 1

    def __init__(self, x: float, y: float, ist_statisch: bool = False):
        """Ein Gelenk mit ID, Position und Status (statisch oder beweglich)."""
        self.id_gelenk = Gelenk.id_counter
        Gelenk.id_counter += 1

        self.x = x
        self.y = y
        self.ist_statisch = ist_statisch

    def speichern(self, db: TinyDB):
        """Speichert das Gelenk in TinyDB."""
        table = db.table("Gelenke")
        table.upsert({"id_Gelenk": self.id_gelenk, "x": self.x, "y": self.y, "ist_statisch": self.ist_statisch}, Query().id == self.id)

    @staticmethod
    def laden(db: TinyDB, id_gelenk: int):
        """Lädt ein Gelenk aus TinyDB anhand seiner ID."""
        table = db.table("Gelenke")
        daten = table.get(Query().id_gelenk == id_gelenk)
        if daten:
            return Gelenk(daten["id_Gelenk"], daten["x"], daten["y"], daten["ist_statisch"])
        return None

    def __repr__(self):
        return f"Gelenk(ID={self.id}, x={self.x}, y={self.y}, Statisch={self.ist_statisch})"
