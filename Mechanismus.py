from tinydb import TinyDB, Query
from Gelenk import Gelenk
from Glied import Glied

class Mechanismus:
    id_counter = 1

    def __init__(self, name, glieder=None, gelenke=None):
        """Erstellt einen Mechanismus mit Gelenken und Gliedern."""
        self.id = Mechanismus.id_counter
        Mechanismus.id_counter += 1

        self.name = name
        self.glieder = glieder if glieder else []
        self.gelenke = gelenke if gelenke else []
        self.antrieb = None  # ID des angetriebenen Gelenks
        self.statik = []  # Liste von IDs der fixen Gelenke

    def add_gelenk(self, gelenk: Gelenk):
        """Fügt ein Gelenk hinzu."""
        self.gelenke.append(gelenk)

    def add_glied(self, glied: Glied):
        """Fügt ein Glied hinzu."""
        self.glieder.append(glied)

    def set_antrieb(self):
        """Sucht nach einem Gelenk mit ist_antrieb=True und setzt das zugehörige Glied als Kurbel."""
        antriebsgelenk = next((g for g in self.gelenke if g.ist_antrieb), None)

        if antriebsgelenk is None:
            print("Fehler: Kein Gelenk ist als Antrieb markiert!")
            return

        for glied in self.glieder:
            if glied.start_id == antriebsgelenk.id or glied.ende_id == antriebsgelenk.id:
                glied.ist_kurbel = True
                self.antrieb = antriebsgelenk.id
                print(f"Antrieb gesetzt: Gelenk {antriebsgelenk.id} treibt Glied {glied.id} an.")
                return

        print("Fehler: Kein passendes Glied für den Antrieb gefunden!")

    def set_statik(self, gelenk_id: int):
        """Markiert ein Gelenk als statisch (Fixpunkt)."""
        if any(g.id == gelenk_id for g in self.gelenke):
            if gelenk_id not in self.statik:
                self.statik.append(gelenk_id)
        else:
            print(f"Fehler: Gelenk {gelenk_id} existiert nicht!")

    def speichern(self):
        """Speichert den Mechanismus in TinyDB."""
        db = TinyDB("database.json")
        mechanismus_tabelle = db.table("mechanismen")

        daten = {
            "id": self.id,
            "name": self.name,
            "gelenke": [{"id": g.id, "x": g.x, "y": g.y, "ist_statisch": g.ist_statisch, "ist_antrieb": g.ist_antrieb} for g in self.gelenke],
            "glieder": [{"id": gl.id, "start_id": gl.start_id, "ende_id": gl.ende_id, "ist_kurbel": getattr(gl, 'ist_kurbel', False)} for gl in self.glieder],
            "antrieb": self.antrieb,
            "statik": self.statik,
        }

        mechanismus_tabelle.upsert(daten, Query().id == self.id)
        print(f"Mechanismus '{self.name}' gespeichert.")

    @staticmethod
    def laden(mechanismus_id: int):
        """Lädt einen Mechanismus aus TinyDB."""
        db = TinyDB("database.json")
        mechanismus_tabelle = db.table("mechanismen")

        daten = mechanismus_tabelle.get(Query().id == mechanismus_id)
        if not daten:
            print(f"Fehler: Kein Mechanismus mit ID {mechanismus_id} gefunden!")
            return None

        gelenke = [Gelenk(g["id"], g["x"], g["y"], g.get("ist_statisch", False), g.get("ist_antrieb", False)) for g in daten["gelenke"]]
        glieder = [Glied(gl["id"], gl["start_id"], gl["ende_id"], gl.get("ist_kurbel", False)) for gl in daten["glieder"]]

        mechanismus = Mechanismus(daten["name"], glieder, gelenke)
        mechanismus.antrieb = daten["antrieb"]
        mechanismus.statik = daten["statik"]

        print(f"Mechanismus '{mechanismus.name}' geladen.")
        return mechanismus

    def __repr__(self):
        return f"Mechanismus({self.name}, Gelenke={len(self.gelenke)}, Glieder={len(self.glieder)}, Antrieb={self.antrieb}, Fixpunkte={self.statik})"
