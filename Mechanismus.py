from tinydb import TinyDB, Query
from Gelenk import Gelenk
from Glied import Glied
import networkx as nx


class Mechanismus:
    id_counter = 1

    def __init__(self, name, db: TinyDB, glieder=None, gelenke=None):
        """Erstellt einen Mechanismus mit Gelenken und Gliedern."""
        self.id = Mechanismus.id_counter
        Mechanismus.id_counter += 1

        self.name = name
        self.db = db  # Speichert TinyDB
        self.glieder = glieder if glieder else []
        self.gelenke = gelenke if gelenke else []
        self.antrieb = None  # ID des angetriebenen Gelenks
        self.statik = []  # Liste von IDs der fixen Gelenke

        # Automatische Erkennung von Antrieb und statischen Gelenken
        self.set_antrieb()
        self.set_statische_gelenke()
        

    def ist_valide(self):
        """Einfache Validierung des Mechanismus."""

        statische_gelenke = [g for g in self.gelenke if g.ist_statisch]
        if len(statische_gelenke) == 0:
            print("Fehler: Es gibt kein statisches Gelenk. Mindestens eines muss fixiert sein.")
            return False

        antriebsgelenke = [g for g in self.gelenke if g.ist_antrieb]
        if len(antriebsgelenke) != 1:
            print(f"Fehler: Es gibt {len(antriebsgelenke)} Antriebsgelenke. Es sollte genau eines sein.")
            return False

        verbundene_gelenke = set()
        for glied in self.glieder:
            verbundene_gelenke.add(glied.start_id)
            verbundene_gelenke.add(glied.ende_id)

        alle_gelenke = {g.id for g in self.gelenke}
        if not alle_gelenke.issubset(verbundene_gelenke):
            print("Fehler: Es gibt isolierte Gelenke, die mit keinem Glied verbunden sind.")
            return False

        print("Der Mechanismus ist gültig!")
        return True
    
    def add_gelenk(self, gelenk: Gelenk):
        """Fügt ein Gelenk hinzu."""
        self.gelenke.append(gelenk)
        gelenk.speichern(self.db)  # Gelenk in DB speichern
        self.speichern()  # Mechanismus aktualisieren

    def add_glied(self, glied: Glied):
        """Fügt ein Glied hinzu."""
        self.glieder.append(glied)
        glied.speichern(self.db)  # Glied in DB speichern
        self.speichern()  # Mechanismus aktualisieren

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

    def set_statische_gelenke(self):
        """Markiert ein Gelenke als statisch."""
        self.statik = [g.id for g in self.gelenke if g.ist_statisch]

    def speichern(self):
        """Speichert oder aktualisiert den Mechanismus in TinyDB."""
        mechanismus_tabelle = self.db.table("mechanismen")
        
        # Prüfe, ob Mechanismus mit demselben Namen existiert
        if mechanismus_tabelle.contains(Query().name == self.name):
            # Falls vorhanden, aktualisiere Eintrag
            mechanismus_tabelle.update({
                "gelenke": [{"id": g.id, "x": g.x, "y": g.y, "ist_statisch": g.ist_statisch, "ist_antrieb": g.ist_antrieb} for g in self.gelenke],
                "glieder": [{"id": gl.id, "start_id": gl.start_id, "ende_id": gl.ende_id, "ist_kurbel": gl.ist_kurbel} for gl in self.glieder],
                "antrieb": self.antrieb,
                "statik": self.statik,
            }, Query().name == self.name)
        else:
            # Falls nicht vorhanden, neuen Mechanismus anlegen
            mechanismus_tabelle.insert({
                "id": self.id,
                "name": self.name,
                "gelenke": [{"id": g.id, "x": g.x, "y": g.y, "ist_statisch": g.ist_statisch, "ist_antrieb": g.ist_antrieb} for g in self.gelenke],
                "glieder": [{"id": gl.id, "start_id": gl.start_id, "ende_id": gl.ende_id, "ist_kurbel": gl.ist_kurbel} for gl in self.glieder],
                "antrieb": self.antrieb,
                "statik": self.statik,
            })

    @staticmethod
    def laden(name: str, db: TinyDB):
        """Lädt einen Mechanismus aus TinyDB."""
        mechanismus_tabelle = db.table("mechanismen")
        daten = mechanismus_tabelle.get(Query().name == name)
        if not daten:
            return None

        gelenke = [Gelenk(g["x"], g["y"], g["ist_statisch"], g["ist_antrieb"], id=g["id"]) for g in daten["gelenke"]]
        glieder = [Glied(gl["start_id"], gl["ende_id"], gl["ist_kurbel"], id=gl["id"]) for gl in daten["glieder"]]

        return Mechanismus(daten["name"], db, glieder, gelenke)


    def __repr__(self):
        return f"Mechanismus({self.name}, Gelenke={len(self.gelenke)}, Glieder={len(self.glieder)}, Antrieb={self.antrieb}, Fixpunkte={self.statik})"
