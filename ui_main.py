#to start the Server with git Bash you have to type in: python -m streamlit run ui_main.py

import streamlit as st
from tinydb import TinyDB, Query
import matplotlib.pyplot as plt
from Gelenk import Gelenk



# Konfigurieren der Streamlit-Seite
st.set_page_config(layout="wide")

button_neues_Gelenk = False

# Unterteilung in zwei Spalten
eingabe, ausgabe = st.columns(2)


with eingabe:
    st.header("Eingabe")
    # Button zum Anzeigen der Eingabefelder für ein neues Gelenk
    if st.button("neues Gelenk"):
       with st.form(key="Gelenk"):
            start1, start2 = st.columns(2)
            with start1:
                x_start = st.text_input("x-Koordinate Start")
            with start2:
                y_start = st.text_input("y-Koordinate Start")
            statisch = st.checkbox("Statisch", False)

            # Button zum Speichern des Gelenks
            gelenk_gespeichert = st.form_submit_button("Gelenk speichern")
            if gelenk_gespeichert:
                neues_gelenk = Gelenk(float(x_start), float(y_start), statisch)
                neues_gelenk.speichern()
                st.write("Gelenk gespeichert")


"""    #Endpunkte definieren
        end1, end2 = st.columns(2)
        with end1:
            x_end = st.text_input("x-Koordinate Ende", "hier Wert eingeben")
        with end2:
            y_end = st.text_input("y-Koordinate Ende", "hier Wert eingeben")
        statisch2 = st.checkbox("Statisch2", False)"""

        


"""with ausgabe:
    st.header("Simulation")
    

    
    # Erstellen des Koordinatensystems
    fig, ax = plt.subplots()
    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")


    # Visualisieren der Gelenke und Glieder
    gelenke = db.table("Gelenke").all()
    for gelenk in gelenke:
        ax.scatter(gelenk['x'], gelenk['y'], color="red" if gelenk['ist_statisch'] else "blue")
    
    st.pyplot(fig)

    # Anzeigen der gespeicherten Werte in der Datenbank
    st.write("Gespeicherte Gelenke in der Datenbank:")
    st.write(gelenke)

st.write("Session State:")
st.session_state"""