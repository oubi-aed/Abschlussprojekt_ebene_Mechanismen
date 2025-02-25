from tinydb import TinyDB, Query

class Gelenk:
    id_counter = 1  # Automatische ID-Vergabe

    def __init__(self, x: float, y: float, ist_statisch: bool = False, ist_antrieb: bool = False, id: int = None):
        """Ein Gelenk mit Position, Statisch-Status und optionalem Antrieb mit Mittelpunkt."""
        if id is None:
            self.id = Gelenk.id_counter
            Gelenk.id_counter += 1
        else:
            self.id = id  # Falls aus TinyDB geladen wird, behalten wir die ID bei

        self.x = x
        self.y = y
        self.ist_statisch = ist_statisch
        self.ist_antrieb = ist_antrieb

    def speichern(self, db: TinyDB, mechanismus_name: str):
        """Speichert das Gelenk in TinyDB."""
        table_gelenke = db.table("Gelenke")
        table_mechanismen = db.table("mechanismen")

        table_gelenke.upsert({
            "id": self.id, "x": self.x, "y": self.y, "ist_statisch": self.ist_statisch,
            "ist_antrieb": self.ist_antrieb
        }, Query().id == self.id)

        mechanismus = table_mechanismen.get(Query().name == mechanismus_name) 
        if mechanismus:
            mechanismus["gelenke"].append ({
                "id": self.id, "x": self.x, "y": self.y,
                "ist_statisch": self.ist_statisch, "ist_antrieb": self.ist_antrieb
            })
            table_mechanismen.update(mechanismus, Query().name == mechanismus_name)


    @staticmethod
    def laden(db: TinyDB, id: int):
        """Lädt ein Gelenk aus TinyDB anhand seiner ID."""
        table = db.table("Gelenke")
        daten = table.get(Query().id == id)
        if daten:
            return Gelenk(daten["x"], daten["y"], daten["ist_statisch"], daten["ist_antrieb"], id=daten["id"])
        return None

    def __repr__(self):
        return f"Gelenk(ID={self.id}, x={self.x}, y={self.y}, Statisch={self.ist_statisch}, Antrieb={self.ist_antrieb})"
