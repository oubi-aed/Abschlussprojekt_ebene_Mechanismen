#to start the Server with git Bash you have to type in: python -m streamlit run ui_main.py

import streamlit as st
from tinydb import TinyDB, Query
import matplotlib.pyplot as plt
from Gelenk import Gelenk

# Initialisierung der Datenbank
db = TinyDB('database.json')

# Konfigurieren der Streamlit-Seite
st.set_page_config(layout="wide")

# Unterteilung in zwei Spalten
eingabe, ausgabe = st.columns(2)

# Initialisieren der Variablen im Session State
if 'button_neues_gelenk' not in st.session_state:
    st.session_state.button_neues_gelenk = False
if 'gelenke' not in st.session_state:
    st.session_state.gelenke = []

with eingabe:
    st.header("Eingabe")
    
    # Button zum Anzeigen der Eingabefelder für ein neues Gelenk
    if st.button("Neues Gelenk"):
        st.session_state.button_neues_gelenk = True

    # Eingabefelder anzeigen, wenn der Button gedrückt wurde
    if st.session_state.button_neues_gelenk:
        with st.form(key="key_gelenk"):
            x = st.number_input("x-Koordinate", value=0.0, step=0.1)
            y = st.number_input("y-Koordinate", value=0.0, step=0.1)
            statisch = st.checkbox("Statisch")
            ist_antrieb = st.checkbox("Antrieb")

            # Button zum Speichern des Gelenks
            gelenk_gespeichert = st.form_submit_button("Gelenk speichern")
            if gelenk_gespeichert:
                neues_gelenk = Gelenk(x, y, statisch, ist_antrieb)
                neues_gelenk.speichern(db)
                st.session_state.gelenke.append(neues_gelenk)
                st.success("Gelenk gespeichert")
                st.session_state.button_neues_gelenk = False

with ausgabe:
    st.header("Visualisierung")
    
    # Erstellen des Koordinatensystems
    fig, ax = plt.subplots()
    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")
    
    # Laden der gespeicherten Gelenke aus der Datenbank
    gespeicherte_gelenke = db.table("Gelenke").all()
    for gelenk in gespeicherte_gelenke:
        ax.scatter(gelenk["x"], gelenk["y"], color="red" if gelenk["ist_statisch"] else "blue")
        ax.text(gelenk["x"], gelenk["y"], f"{gelenk['id']}", fontsize=12, ha='right')
    
    st.pyplot(fig)

st.write("Session State:", st.session_state)
