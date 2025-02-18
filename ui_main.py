#to start the Server with git Bash you have to type in: python -m streamlit run ui_main.py

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
        button_neues_Gelenk = True

    # Eingabefelder anzeigen, wenn der Button gedrückt wurde
    if button_neues_Gelenk:
        start1, start2 = st.columns(2)

    #Startpunkte definieren
        with start1:
            x_start = st.text_input("x-Koordinate Start", "hier Wert eingeben")
        with start2:
            y_start = st.text_input("y-Koordinate Start", "hier Wert eingeben")
        statisch = st.checkbox("Statisch", False)

    # Button zum Speichern des Gelenks
        gelenk_gespeichert = st.form_submit_button("Gelenk speichern")
        if gelenk_gespeichert:
            neues_gelenk = Gelenk(x_start, y_start, x_end, y_end, statisch, statisch2)
            neues_gelenk.speichern()
            st.write("Gelenk gespeichert")


    #Endpunkte definieren
        end1, end2 = st.columns(2)
        with end1:
            x_end = st.text_input("x-Koordinate Ende", "hier Wert eingeben")
        with end2:
            y_end = st.text_input("y-Koordinate Ende", "hier Wert eingeben")
        statisch2 = st.checkbox("Statisch2", False)

        


with ausgabe:
    st.header("Simulation")
    
    # Erstellen des Koordinatensystems
    fig, ax = plt.subplots()
    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")


    # Visualisieren der Gelenke und Glieder
    if x_start and y_start:
        ax.scatter(x_start, y_start, color="red")

    if st.session_state.x_end and st.session_state.y_end:
        ax.scatter(x_end, y_end, color="blue")
    st.pyplot(fig)

st.write("Session State:")
st.session_state