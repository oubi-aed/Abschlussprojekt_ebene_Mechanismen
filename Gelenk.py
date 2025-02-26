from tinydb import TinyDB, Query

class Gelenk:
    id_counter = 1  # Automatische ID-Vergabe

    def __init__(self, x: float, y: float, ist_statisch: bool = False, ist_antrieb: bool = False, id: int = None):
        """Ein Gelenk mit Position, Statisch-Status und optionalem Antrieb."""
        if id is None:
            self.id = Gelenk.id_counter
            Gelenk.id_counter += 1
        else:
            self.id = id  # Falls aus DB geladen, ID beibehalten

        self.x = x
        self.y = y
        self.ist_statisch = ist_statisch
        self.ist_antrieb = ist_antrieb

    def speichern(self, db: TinyDB):
        """Speichert das Gelenk in die Datenbank."""
        table = db.table("Gelenke")
        table.upsert({
            "id": self.id, "x": self.x, "y": self.y,
            "ist_statisch": self.ist_statisch, "ist_antrieb": self.ist_antrieb
        }, Query().id == self.id)

    @staticmethod
    def laden(db: TinyDB, id: int):
        """Lädt ein Gelenk aus der Datenbank."""
        table = db.table("Gelenke")
        daten = table.get(Query().id == id)
        if daten:
            return Gelenk(daten["x"], daten["y"], daten["ist_statisch"], daten["ist_antrieb"], id=daten["id"])
        return None

    def __repr__(self):
        return f"Gelenk(ID={self.id}, x={self.x}, y={self.y}, Statisch={self.ist_statisch}, Antrieb={self.ist_antrieb})"
