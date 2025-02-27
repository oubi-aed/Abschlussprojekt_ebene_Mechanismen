# Abschlussprojekt_ebene_Mechanismen
Eine streamlitanwendung mit welcher beliebige ebene Mechanismen ( mit gewissen Einschränkungen) definiert und deren Kinematik simuliert werden

## Projektbeschreibung
Dieses Projekt ist eine Simulation für ebene Mechanismen die aus Gelenken und Gliedern bestehen. Die Mechanismen können definiert, validiert und simuliert werden. Eine Web-UI (mit Streamlit) ermöglicht es, Mechanismen interaktiv zu erstellen und ihre Kinematik zu analysieren.

## Implementierte Funktionen

In diesem Projekt haben wir folgende Funktionen implementiert:

- **Erstellung und Speicherung von Mechanismen**: Gelenke und Glieder können über die UI definiert und in einer Datenbank gespeichert sowie auch geladen werden.
- **Validierung der Mechanismen**: Automatische Überprüfung, ob alle Gelenke verbunden sind und mindestens ein statisches Gelenk und ein Antriebsgelenk vorhanden ist.
- **Simulation der Mechanismen**: Berechnung der Bewegung mit numerischer Optimierung und Ausgabe von Bahnkurven.
- **Visualisierung**: Darstellung des Mechanismus als auch die Bahnkurven der dynamischen Gelenke als Animation und Export als GIF zur besseren Nachverfolgung der Bewegung.
- **Benutzerfreundliche Oberfläche**: Umsetzung mit Streamlit, um eine einfache Interaktion mit den Mechanismen zu ermöglichen.
- **Downloadbare csv-Datei der Bahnkurvendaten**
- **Plot der Längenfehler als Funktion des Winkels**
- **Interaktive Tabellen**: Gelenke und Glieder sind auch nach deren Speicherung in den Tabellen änderbar.

---

## Visualisierungen und UI

- Foto und Video der UI sowie auch der Visualisierung eines Mechanismus

![UI](https://github.com/oubi-aed/Abschlussprojekt_ebene_Mechanismen/blob/main/images/UI.png)

[Video ansehen](https://github.com/oubi-aed/Abschlussprojekt_ebene_Mechanismen/blob/main/images/Aufzeichnung_Strandbeest.mp4)

---

## Beweis am Strandbeest

Zur Validierung der Implementierung wurde das Prinzip des **Strandbeest-Mechanismus** getestet. Dabei wurde ein Mechanismus nach den Konstruktionsprinzipien von Theo Jansen nachgebildet. Durch die Simulation konnte nachgewiesen werden, dass sich der Mechanismus entsprechend der theoretischen Berechnungen bewegt.

![Animation](https://github.com/oubi-aed/Abschlussprojekt_ebene_Mechanismen/blob/main/images/Gif.gif)


Die Simulationsergebnisse zeigen, dass die Gelenke des Strandbeest-Mechanismus sich synchron bewegen und eine zyklische Laufbewegung ermöglichen. Dies bestätigt die korrekte Umsetzung der Mechanik in unserem Modell.

## Installation

### Voraussetzungen
- Python >= 3.8
- Pip installiert
- Virtuelle Umgebung

### Projekt klonen & Abhängigkeiten installieren
```bash
# Repository klonen
git clone https://github.com/oubi-aed/Abschlussprojekt_ebene_Mechanismen.git
cd Abschlussprojekt_ebene_Mechanismen

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

#Anwendung starten
 python -m streamlit run ui_main.py
```




