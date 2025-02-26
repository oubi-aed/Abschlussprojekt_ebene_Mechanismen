import csv
import numpy as np
import scipy.optimize as opt
from Mechanismus import Mechanismus
from Gelenk import Gelenk
import matplotlib.pyplot as plt
import imageio

class Simulation:
    def __init__(self, mechanismus: Mechanismus, schritte=100):
        """Initialisiert die Simulation."""
        self.mechanismus = mechanismus
        self.schritte = schritte
        self.winkel_schritte = np.linspace(0, 2 * np.pi, schritte)
        self.gelenk_positionen = {g.id: np.array([g.x, g.y]) for g in mechanismus.gelenke}
        self.glied_laengen = self.berechne_gliederlaengen()
        self.simulationsergebnisse = []

        #Gelenkpositionen für die Bahnkurven
        self.bahnkurve = {g.id: [] for g in self.mechanismus.gelenke if g.id not in self.mechanismus.statik}

        # Identifiziere die Kurbel
        self.kurbel = next((gl for gl in self.mechanismus.glieder if gl.ist_kurbel), None)

        if not self.kurbel:
            print("Fehler: Keine Kurbel gefunden. Die Simulation kann nicht laufen.")
            self.valid = False
        else:
            self.valid = True


    def berechne_gliederlaengen(self):
        """Speichert die ursprünglichen Gliederlängen für die Optimierung."""
                    
        glied_laengen = {}
        for glied in self.mechanismus.glieder:
            p1 = self.gelenk_positionen[glied.start_id]
            p2 = self.gelenk_positionen[glied.ende_id]
            glied_laengen[glied.id] = np.linalg.norm(p2 - p1)
        return glied_laengen

    def bewege_kurbel(self, winkel):
        """Bewegt das Endgelenk der Kurbel entlang einer Kreisbahn."""
        if not self.kurbel:
            return

        antriebsgelenk = next((g for g in self.mechanismus.gelenke if g.id == self.mechanismus.antrieb), None)
        if not antriebsgelenk:
            print(f"Fehler: Antriebsgelenk {self.mechanismus.antrieb} nicht gefunden")
            return

        p_statisch = np.array([antriebsgelenk.x, antriebsgelenk.y])
        r = self.glied_laengen[self.kurbel.id]
        neue_position = p_statisch + r * np.array([np.cos(winkel), np.sin(winkel)])

        self.gelenk_positionen[self.kurbel.ende_id] = neue_position

    def fehlerfunktion(self, variablen):
        """Berechnet den Gesamtfehler der Gliederlängen."""
        fehler = 0
        idx = 0
        bewegliche_gelenke = [g for g in self.mechanismus.gelenke if g.id not in self.mechanismus.statik]

        # Aktualisiere Gelenkpositionen
        for gelenk in bewegliche_gelenke:
            gelenk.x = variablen[2 * idx]
            gelenk.y = variablen[2 * idx + 1]
            self.gelenk_positionen[gelenk.id] = np.array([gelenk.x, gelenk.y])
            idx += 1

        # Berechne Fehler basierend auf den Längen der Glieder
        for glied in self.mechanismus.glieder:
            start = self.gelenk_positionen[glied.start_id]
            ende = self.gelenk_positionen[glied.ende_id]
            ist_laenge = np.linalg.norm(start - ende)
            fehler += (ist_laenge - self.glied_laengen[glied.id]) ** 2

        return fehler

    def optimierung(self):
        """Optimiert die Gelenkpositionen, um den Fehler zu minimieren."""
        initiale_positionen = []
        bewegliche_gelenke = [g for g in self.mechanismus.gelenke if g.id not in self.mechanismus.statik]

        for gelenk in bewegliche_gelenke:
            initiale_positionen.extend(self.gelenk_positionen[gelenk.id])

        ergebnis = opt.minimize(self.fehlerfunktion, initiale_positionen, method='BFGS')

        if ergebnis.success:
            idx = 0
            for gelenk in bewegliche_gelenke:
                self.gelenk_positionen[gelenk.id] = np.array([ergebnis.x[2 * idx], ergebnis.x[2 * idx + 1]])
                idx += 1
        else:
            print("Warnung: Optimierung nicht erfolgreich")

    def berechne_kinematik(self, winkel):
        """Berechnet die Positionen aller Gelenke für einen gegebenen Kurbelwinkel."""
        if not self.valid:
            print("Simulation abgebrochen: Keine gültige Kurbel")
            return {}

        self.bewege_kurbel(winkel)
        self.optimierung()

        return self.gelenk_positionen

    def simuliere_mechanismus(self):
        """Simuliert eine komplette Umdrehung der Kurbel."""
        if not self.valid:
            print("Keine gültige Kurbel – Simulation kann nicht gestartet werden")
            return

        self.simulationsergebnisse = []
        for winkel in self.winkel_schritte:
            positionen = self.berechne_kinematik(winkel)
            self.simulationsergebnisse.append({k: v.copy() for k, v in positionen.items()})
            for gelenk_id, pos in positionen.items():
                if gelenk_id in self.bahnkurve:
                    self.bahnkurve[gelenk_id].append(pos)
            
        print("Simulation abgeschlossen")

    def export_bahnkurve(self, dateinahme="bahnkurve.csv"):
        """Exportiert die Bahnkurven als csv-Datei."""
        with open(dateinahme, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Gelenk", "X", "Y"])
            
            for gelenk_id, punkte in self.bahnkurve.items():
                for punkt in punkte:
                    writer.writerow([gelenk_id, punkt[0], punkt[1]])
        print(f"Bahnkurven exportiert nach {dateinahme}")

    def export_gif(self, limits, dateiname="Gif.gif"):
        """Exportiert den gesamten Mechanismus als GIF."""
        bilder = []

        # Durchlaufe alle Simulationsschritte
        for schritt in range(len(self.simulationsergebnisse)):
            fig, ax = plt.subplots()
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_title("Mechanismus-Simulation")

            positionen = self.simulationsergebnisse[schritt]

            #setzen der axenlimits
            if limits:
                x_min, x_max, y_min, y_max = limits
                ax.set_xlim(x_min, x_max)
                ax.set_ylim(y_min, y_max)
            else:
                ax.set_xlim(-10, 10) 
                ax.set_ylim(-10, 10)


            for glied in self.mechanismus.glieder:
                start = positionen[glied.start_id]
                ende = positionen[glied.ende_id]
                ax.plot([start[0], ende[0]], [start[1], ende[1]], "ro-", markersize=5, linewidth=2)

            fig.canvas.draw()
            bild = np.array(fig.canvas.renderer.buffer_rgba())
            bilder.append(bild)

            plt.close(fig)

        if bilder:
            imageio.mimsave(dateiname, bilder, duration=0.1)
            print(f"Mechanismus-GIF exportiert nach {dateiname}")