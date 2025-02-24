#to start the Server with git Bash you have to type in: python -m streamlit run ui_main.py

import streamlit as st
from tinydb import TinyDB, Query
import matplotlib.pyplot as plt
from Gelenk import Gelenk
from Mechanismus import Mechanismus
from Glied import Glied


#Initialisierung der Datenbank
db = TinyDB('database.json')

# Konfigurieren der Streamlit-Seite
st.set_page_config(layout="wide")

# Unterteilung in zwei Spalten
eingabe, ausgabe = st.columns(2)




# Initialisieren der Buttons im Session State
if 'button_neues_gelenk' not in st.session_state:
    st.session_state.button_neues_gelenk = False
# Initialisieren der Buttons im Session State
if 'button_neuer_mechanismus' not in st.session_state:
    st.session_state.button_neuer_mechanismus = False





# Initialisieren der Variablen im Session State   
if 'x' not in st.session_state:
    st.session_state.x = ""
if 'y' not in st.session_state:
    st.session_state.y = ""
if 'statisch' not in st.session_state:
    st.session_state.statisch = False
if 'name_mechanismus' not in st.session_state:
    st.session_state.name_mechanismus = ""





with eingabe:
    st.header("Eingabe")

     # verwaltung der Buttons und auswahlmöglichkeiten
    if st.button("neuer Mechanismus"):
        st.session_state.button_neuer_mechanismus = True


    # Button: neuer Mechanismus
    if st.session_state.button_neuer_mechanismus:
        with st.form(key="key_mechanismus"):

            st.session_state.name_mechanismus = st.text_input("Name des Mechanismu", st.session_state.name_mechanismus)

            # Button zum Speichern des Gelenks
            mechanismus_anlegen = st.form_submit_button("Mechanismus anlegen")
            if mechanismus_anlegen:
                if st.session_state.name_mechanismus:
                    neuer_mechanismus = Mechanismus(st.session_state.name_mechanismus)
                    neuer_mechanismus.speichern(db)
                    st.write("Mechanismus angelegt")
                    st.session_state.button_neuer_mechanismus = False
                    st.rerun()
                else:
                    st.write("Bitte Namen eingeben")
      


    #auswahl_mechanismen = Mechanismus.laden_name(db)
    auswahl_mechanismen = [m["name"] for m in db.table("mechanismen").all()]
    aktiver_mechanismus = st.selectbox("Mechanismus auswählen", auswahl_mechanismen)
    


    # Button: neues Gelenk (schliesst wieder nach erneutem drücken)
    if st.button("neues Gelenk"):
        st.session_state.button_neues_gelenk = not st.session_state.button_neues_gelenk

   

    # Button: neues Gelenk
    if st.session_state.button_neues_gelenk:
        with st.form(key="key_gelenk"):
            start1, start2 = st.columns(2)



            with start1:
                st.session_state.x = st.text_input("x-Koordinate Start", st.session_state.x)
            with start2:
                st.session_state.y = st.text_input("y-Koordinate Start", st.session_state.y)
                st.session_state.statisch = st.checkbox("Statisch", st.session_state.statisch)

            # Button zum Speichern des Gelenks
            gelenk_gespeichert = st.form_submit_button("Gelenk speichern")
            if gelenk_gespeichert:
                if aktiver_mechanismus:

                    
                    neues_gelenk = Gelenk(float(st.session_state.x), float(st.session_state.y), st.session_state.statisch)
                    print(f"in neues gelenk ist folgendes gespeichert:{neues_gelenk}")
                    mechanismus = Mechanismus.laden(db, aktiver_mechanismus)
                    mechanismus.add_gelenk(neues_gelenk)
                    mechanismus.speichern(db)

                    st.write("Gelenk gespeichert")

                    st.session_state.x = ""
                    st.session_state.y = ""
                    st.session_state.statisch = False
                    st.rerun()




with ausgabe:
    st.header("Simulation")
    
    # Erstellen des Koordinatensystems
    fig, ax = plt.subplots()
    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")


    # Visualisieren der Gelenke und Glieder
    if st.session_state.x and st.session_state.y:
        ax.scatter(st.session_state.x, st.session_state.y, color="red")

    st.pyplot(fig)

st.write("Session State:")
st.session_state
