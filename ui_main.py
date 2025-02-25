#to start the Server with git Bash you have to type in: python -m streamlit run ui_main.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from tinydb import TinyDB, where
from Gelenk import Gelenk
from Glied import Glied
from Mechanismus import Mechanismus
from Simulation import Simulation

# Initialisierung der Datenbank
db = TinyDB('database.json')

# Konfigurieren der Streamlit-Seite
st.set_page_config(layout="wide")

# Unterteilung in zwei Spalten
eingabe, ausgabe = st.columns(2)

# Initialisieren der Variablen im Session State
if 'button_neues_gelenk' not in st.session_state:
    st.session_state.button_neues_gelenk = False
if 'button_neues_glied' not in st.session_state:
    st.session_state.button_neues_glied = False
if 'gelenke' not in st.session_state:
    st.session_state.gelenke = []
if 'glieder' not in st.session_state:
    st.session_state.glieder = []
if 'mechanismus' not in st.session_state:
    st.session_state.mechanismus = None
if 'simulationsergebnisse' not in st.session_state:
    st.session_state.simulationsergebnisse = []
if 'graph_limits' not in st.session_state:
    st.session_state.graph_limits = None  # Speichert die Skalierung
if 'button_neuer_mechanismus' not in st.session_state:
    st.session_state.button_neuer_mechanismus = False
if "letzter_mechanismus" not in st.session_state:
    st.session_state.letzter_mechanismus = None
if "aktiver_mechanismus" not in st.session_state:
    st.session_state.aktiver_mechanismus = None


if 'x' not in st.session_state:
    st.session_state.x = ""
if 'y' not in st.session_state:
    st.session_state.y = ""
if 'statisch' not in st.session_state:
    st.session_state.statisch = False
if 'ist_antrieb' not in st.session_state:
    st.session_state.ist_antrieb = False
if 'name_mechanismus' not in st.session_state:
    st.session_state.name_mechanismus = ""




with eingabe:
    st.header("Eingabe")


    # verwaltung der Buttons und auswahlmöglichkeiten
    
    # Button: neuer Mechanismus
    if st.button("neuer Mechanismus"):
        st.session_state.button_neuer_mechanismus = True
        st.session_state.gelenke = []
        st.session_state.glieder = []

    #abfrage der existierenden Mechanismen
    auswahl_mechanismen = [m["name"] for m in db.table("mechanismen").all()]

    if st.session_state.button_neuer_mechanismus:
        with st.form(key="key_mechanismus"):
            st.session_state.name_mechanismus = st.text_input("Name des Mechanismus", st.session_state.name_mechanismus)

            # Button zum Speichern des Mechanismus
            mechanismus_anlegen = st.form_submit_button("Mechanismus anlegen")
            if mechanismus_anlegen:
                if st.session_state.name_mechanismus:
                    if st.session_state.name_mechanismus not in auswahl_mechanismen:
                        neuer_mechanismus = Mechanismus(st.session_state.name_mechanismus, st.session_state.glieder, st.session_state.gelenke)
                        neuer_mechanismus.speichern(db)
                        st.write(f"Mechanismus: {st.session_state.name_mechanismus} angelegt")
                        st.session_state.button_neuer_mechanismus = False
                        st.rerun()
                    else:
                        st.write("ein Mechanismus mit diesem Namen existiert bereits")
                else:
                    st.write("Bitte Namen eingeben")

    #letzter Mechanismus immer vorausgewählt
    if len(auswahl_mechanismen) > 0:
        index_letzter_mechanismus = len(auswahl_mechanismen) -1
    else: 
        index_letzter_mechanismus = 0
    st.session_state.aktiver_mechanismus = st.selectbox("Mechanismus auswählen", auswahl_mechanismen, index_letzter_mechanismus)

# Auswahl der Mechanismen
    if st.session_state.aktiver_mechanismus != st.session_state.letzter_mechanismus:
        
        st.session_state.gelenke = []
        st.session_state.glieder = []
        mechanismus_daten = db.table("mechanismen").get(where('name') == st.session_state.aktiver_mechanismus)
        if mechanismus_daten:
            st.session_state.gelenke = mechanismus_daten["gelenke"]
            st.session_state.glieder = mechanismus_daten["glieder"]
        st.session_state.letzter_mechanismus = st.session_state.aktiver_mechanismus







    button1, button2 = st.columns(2)

    with button1:
        #Button: neues Gelenk (schliesst wieder nach erneutem drücken)
        if st.button("neues Gelenk"):
            st.session_state.button_neues_gelenk = not st.session_state.button_neues_gelenk
        # Button: neues Glied (schliesst wieder nach erneutem drücken)
    with button2:
        if st.button("neues Glied"):
            st.session_state.button_neues_glied = not st.session_state.button_neues_glied


    

    


   # Gelenk-Eingabe
    if st.session_state.button_neues_gelenk:
        with st.form(key="key_gelenk"):
            start1, start2 = st.columns(2)

            with start1:
                st.session_state.x = st.text_input("x-Koordinate Start", st.session_state.x)
                st.session_state.ist_antrieb = st.checkbox("Antrieb", st.session_state.ist_antrieb)
            with start2:
                st.session_state.y = st.text_input("y-Koordinate Start", st.session_state.y)
                st.session_state.statisch = st.checkbox("Statisch", st.session_state.statisch)

            # Button zum Speichern des Gelenks
            gelenk_gespeichert = st.form_submit_button("Gelenk speichern")
            if gelenk_gespeichert:
                if st.session_state.aktiver_mechanismus:
                    if st.session_state.x and st.session_state.y:
                        try:
                            neues_gelenk = Gelenk(float(st.session_state.x), float(st.session_state.y), st.session_state.statisch, st.session_state.ist_antrieb)
                            neues_gelenk.speichern(db, st.session_state.aktiver_mechanismus)
                            st.session_state.gelenke.append(neues_gelenk)
                            st.success("Gelenk gespeichert")
                            st.rerun()
                        except ValueError:
                            st.error("Bitte gültige Koordinaten eingeben")



    # Glieder-Eingabe
    if st.session_state.button_neues_glied:
        with st.form(key="key_glied"):
            st.session_state.gelenke = []
            st.session_state.glieder = []
            mechanismus_daten = db.table("mechanismen").get(where('name') == st.session_state.aktiver_mechanismus)
            if mechanismus_daten:
                st.session_state.gelenke = mechanismus_daten["gelenke"]
                st.session_state.glieder = mechanismus_daten["glieder"]
            
            start, end = st.columns(2)
            with start:
                start_id = st.selectbox("Startgelenk", [g["id"] for g in st.session_state.gelenke])
            with end:
                ende_id = st.selectbox("Endgelenk", [g["id"] for g in st.session_state.gelenke])
                
            #Button zum Speichern des Glieds
            glied_gespeichert = st.form_submit_button("Glied speichern")    
            if glied_gespeichert:
                if st.session_state.aktiver_mechanismus:
                    if start_id and ende_id:
                        if start_id != ende_id:
                            neues_glied = Glied(start_id, ende_id)
                            neues_glied.speichern(db, st.session_state.aktiver_mechanismus)
                            st.session_state.glieder.append(neues_glied)
                            st.success("Glied gespeichert")
                            st.rerun()


            


    # Simulation starten
    st.subheader("Simulation starten")
    if st.button("Mechanismus simulieren"):

        mechanismus_daten = db.table("mechanismen").get(where('name') == st.session_state.aktiver_mechanismus)
        if mechanismus_daten:
            st.session_state.gelenke = [Gelenk(**g) for g in mechanismus_daten["gelenke"]]
            st.session_state.glieder = [Glied(**g) for g in mechanismus_daten["glieder"]]


        
        st.session_state.mechanismus = Mechanismus(st.session_state.aktiver_mechanismus, st.session_state.glieder, st.session_state.gelenke)
        if st.session_state.mechanismus:
            sim = Simulation(st.session_state.mechanismus)
            sim.simuliere_mechanismus()
            st.session_state.simulationsergebnisse = sim.simulationsergebnisse
            st.success("Simulation abgeschlossen!")

            #Skalierung berechnen & fixieren
            all_x = [g.x for g in st.session_state.mechanismus.gelenke]
            all_y = [g.y for g in st.session_state.mechanismus.gelenke]

            if all_x and all_y:
                x_min, x_max = min(all_x) - 1, max(all_x) + 1
                y_min, y_max = min(all_y) - 1, max(all_y) + 1
                st.session_state.graph_limits = (x_min, x_max, y_min, y_max)










with ausgabe:
    st.header("Animation der Simulation")

    #Falls eine Simulation existiert, starte die Animation
    if st.session_state.simulationsergebnisse:
        plot_container = st.empty()  #Platzhalter für die Animation
        
        x_min, x_max, y_min, y_max = st.session_state.graph_limits or (-10, 10, -10, 10)

        for frame in range(len(st.session_state.simulationsergebnisse)):
            fig, ax = plt.subplots()
            ax.set_xlabel("X-Achse")
            ax.set_ylabel("Y-Achse")

            #Fixierte Achsen-Skalierung
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)

            positionen = st.session_state.simulationsergebnisse[frame]

            #Gelenke zeichnen
            for gelenk_id, pos in positionen.items():
                ax.scatter(pos[0], pos[1], color="red" if gelenk_id in st.session_state.mechanismus.statik else "blue")
                ax.text(pos[0], pos[1], f"{gelenk_id}", fontsize=12, ha='right')

            #Glieder zeichnen
            for glied in st.session_state.mechanismus.glieder:
                p1 = positionen[glied.start_id]
                p2 = positionen[glied.ende_id]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="black")

            plot_container.pyplot(fig)  #Animation aktualisieren
            time.sleep(0.01)  #Kleine Pause für Animationseffekt
        
    else:
        st.write("Starte eine Simulation, um die Animation zu sehen.")


st.write("Session State:")
st.session_state
