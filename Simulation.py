import numpy as np
from scipy.optimize import minimize
from Mechanismus import Mechanismus
from Gelenk import Gelenk
from Glied import Glied

class Simulation:
    def __init__(self, mechanismus: Mechanismus, schritte=100):
        """Initialisiert die Simulation mit einem Mechanismus und Anzahl der Berechnungsschritte."""
        self.mechanismus = mechanismus
        self.schritte = schritte
        self.winkel_schritte = np.linspace(0, 2*np.pi, schritte)  # 0° bis 360° in Schritten

    def fehlerfunktion(self, positionen):
        """Berechnet den Gesamtfehler der Gliederlängen."""
        fehler = 0
        bewegliche_gelenke = [g for g in self.mechanismus.gelenke if g.id not in self.mechanismus.statik]

        for i, gelenk in enumerate(bewegliche_gelenke):
            gelenk.x = positionen[2*i]
            gelenk.y = positionen[2*i + 1]

        for glied in self.mechanismus.glieder:
            start = next(g for g in self.mechanismus.gelenke if g.id == glied.start_id)
            ende = next(g for g in self.mechanismus.gelenke if g.id == glied.ende_id)
            ist_laenge = np.linalg.norm([start.x - ende.x, start.y - ende.y])
            fehler += (ist_laenge - glied.laenge) ** 2  # Fehlerquadrate aufsummieren

        return fehler

    def optimierung(self):
        """Optimiert die Gelenkpositionen, um den Fehler zu minimieren."""
        initiale_positionen = []
        bewegliche_gelenke = [g for g in self.mechanismus.gelenke if g.id not in self.mechanismus.statik]

        for gelenk in bewegliche_gelenke:
            initiale_positionen.extend([gelenk.x, gelenk.y])

        result = minimize(self.fehlerfunktion, initiale_positionen)

        for i, gelenk in enumerate(bewegliche_gelenke):
            gelenk.x = result.x[2*i]
            gelenk.y = result.x[2*i + 1]

        print(f"Optimierung abgeschlossen, Fehler: {result.fun}")

    def kinematik(self):
        """Simuliert die Bewegung des Mechanismus durch Variieren des Antriebswinkels."""
        ergebnisse = []

        if self.mechanismus.antrieb is None:
            print("Kein Antrieb definiert!")
            return []

        antrieb_gelenk = next(g for g in self.mechanismus.gelenke if g.id == self.mechanismus.antrieb)

        for theta in self.winkel_schritte:
            # Berechnung der neuen Position des Antriebsgelenks
            antrieb_gelenk.x = antrieb_gelenk.radius * np.cos(theta)
            antrieb_gelenk.y = antrieb_gelenk.radius * np.sin(theta)

            # Optimierung der Gelenkpositionen für den neuen Antriebswinkel
            self.optimierung()
            ergebnisse.append([(g.x, g.y) for g in self.mechanismus.gelenke])

        return ergebnisse
