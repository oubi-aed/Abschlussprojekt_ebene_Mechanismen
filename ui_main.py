#to start the Server with git Bash you have to type in: python -m streamlit run ui_main.py

import streamlit as st
from tinydb import TinyDB, Query
import matplotlib.pyplot as plt
from Gelenk import Gelenk

#Initialisierung der Datenbank
db = TinyDB('database.json')

# Konfigurieren der Streamlit-Seite
st.set_page_config(layout="wide")

# Unterteilung in zwei Spalten
eingabe, ausgabe = st.columns(2)


# Initialisieren der Variablen im Session State
if 'button_neues_gelenk' not in st.session_state:
    st.session_state.button_neues_gelenk = False
if 'x' not in st.session_state:
    st.session_state.x = ""
if 'y' not in st.session_state:
    st.session_state.y = ""
if 'statisch' not in st.session_state:
    st.session_state.statisch = False



with eingabe:
    st.header("Eingabe")
    # Button zum Anzeigen der Eingabefelder für ein neues Gelenk
    if st.button("neues Gelenk"):
        st.session_state.button_neues_gelenk = True

    # Eingabefelder anzeigen, wenn der Button gedrückt wurde
    if st.session_state.button_neues_gelenk:
        with st.form(key="key_gelenk"):
            start1, start2 = st.columns(2)

            with start1:
                st.session_state.x = st.text_input("x-Koordinate Start", st.session_state.x)
            with start2:
                st.session_state.y = st.text_input("y-Koordinate Start", st.session_state.y)
                st.session_state.statisch = st.checkbox("Statisch", st.session_state.statisch)

            print("hallo das schaffst du auch noch")
            print(f"x: {st.session_state.x}")

            # Button zum Speichern des Gelenks
            gelenk_gespeichert = st.form_submit_button("Gelenk speichern")
            if gelenk_gespeichert:
                neues_gelenk = Gelenk(st.session_state.x, st.session_state.y, st.session_state.statisch)
                neues_gelenk.speichern(db)
                st.write("Gelenk gespeichert")
                st.session_state.x = ""
                st.session_state.y = ""
                st.session_state.statisch = False



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

"""
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

db = TinyDB('database_test2.json')

with eingabe:
    st.header("Eingabe")
    if 'button_neues_gelenk' not in st.session_state:
        st.session_state.button_neues_gelenk = False

    # Button zum Anzeigen der Eingabefelder für ein neues Gelenk
    if st.button("neues Gelenk"):
        st.session_state.button_neues_gelenk = True

    if st.session_state.button_neues_gelenk:
        with st.form(key="Gelenk_key"):
            x = st.text_input("x-Koordinate")
            print("hier ist der x wert")
            y = st.text_input("y-Koordinate")
            statisch = st.checkbox("Statisch", False)


            print("hallo das schaffst du auch noch")
            print(f"x: {x}, y: {y}, statisch: {statisch}")

            st.write("hallo das schaffst du auch noch")
            st.write(f"x: {x}, y: {y}, statisch: {statisch}")"""

"""            # Button zum Speichern des Gelenks
            gelenk_gespeichert = st.form_submit_button("Gelenk speichern")
            if gelenk_gespeichert:
                neues_gelenk = Gelenk(x, y, statisch)
                db.insert(neues_gelenk.__dict__)
                st.write("Gelenk gespeichert")
                st.rerun()"""


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
"""
