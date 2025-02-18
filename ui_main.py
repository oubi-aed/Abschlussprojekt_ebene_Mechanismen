#to start the Server with git Bash you have to type in: python -m streamlit run ui_main.py

#to start the Server with git Bash you have to type in: python -m streamlit run ui_main.py

import streamlit as st
from tinydb import TinyDB, Query
import matplotlib.pyplot as plt


# Konfigurieren der Streamlit-Seite
st.set_page_config(layout="wide")

# Unterteilung in zwei Spalten
eingabe, ausgabe = st.columns(2)


# Initialisieren der Variablen im Session State
if 'show_joint_inputs' not in st.session_state:
    st.session_state.show_joint_inputs = False
if 'x_start' not in st.session_state:
    st.session_state.x_start = ""
if 'y_start' not in st.session_state:
    st.session_state.y_start = ""
if 'x_end' not in st.session_state:
    st.session_state.x_end = ""
if 'y_end' not in st.session_state:
    st.session_state.y_end = ""
if 'statisch' not in st.session_state:
    st.session_state.statisch = False
if 'statisch2' not in st.session_state:
    st.session_state.statisch = False


with eingabe:
    st.header("Eingabe")
    # Button zum Anzeigen der Eingabefelder für ein neues Gelenk
    if st.button("neues Gelenk"):
        st.session_state.show_joint_inputs = True

    # Eingabefelder anzeigen, wenn der Button gedrückt wurde
    if st.session_state.show_joint_inputs:
        start1, start2 = st.columns(2)

        with start1:
            st.session_state.x_start = st.text_input("x-Koordinate Start", st.session_state.x_start)
        with start2:
            st.session_state.y_start = st.text_input("y-Koordinate Start", st.session_state.y_start)
        statisch = st.checkbox("Statisch", st.session_state.statisch)


        end1, end2 = st.columns(2)
        with end1:
            st.session_state.x_end = st.text_input("x-Koordinate Ende", st.session_state.x_end)
        with end2:
            st.session_state.y_end = st.text_input("y-Koordinate Ende", st.session_state.y_end)
        statisch2 = st.checkbox("Statisch2", st.session_state.statisch)

with ausgabe:
    st.header("Simulation")
    
    # Erstellen des Koordinatensystems
    fig, ax = plt.subplots()
    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")


    # Visualisieren der Gelenke und Glieder
    if st.session_state.x_start and st.session_state.y_start:
        ax.scatter(st.session_state.x_start, st.session_state.y_start, color="red")

    if st.session_state.x_end and st.session_state.y_end:
        ax.scatter(st.session_state.x_end, st.session_state.y_end, color="blue")
    st.pyplot(fig)

st.write("Session State:")
st.session_state