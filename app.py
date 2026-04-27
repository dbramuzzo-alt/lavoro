import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Il Mio Itinerario di Lavoro", layout="centered")

st.title("📅 Organizzatore Itinerari Giornalieri")

# Inizializzazione dello stato della sessione per salvare i dati temporaneamente
if 'itinerario' not in st.session_state:
    st.session_state.itinerario = []

# --- Sidebar per l'inserimento dati ---
st.sidebar.header("Aggiungi Fermata")
cliente = st.sidebar.text_input("Nome Cliente/Sito")
indirizzo = st.sidebar.text_input("Indirizzo")
orario = st.sidebar.time_input("Orario previsto", datetime.now().time())
note = st.sidebar.text_area("Note/Attività")

if st.sidebar.button("Aggiungi all'itinerario"):
    nuova_tappa = {
        "Orario": orario.strftime("%H:%M"),
        "Cliente": cliente,
        "Indirizzo": indirizzo,
        "Note": note
    }
    st.session_state.itinerario.append(nuova_tappa)
    st.sidebar.success("Aggiunto!")

# --- Visualizzazione Itinerario ---
if st.session_state.itinerario:
    df = pd.DataFrame(st.session_state.itinerario)
    df = df.sort_values(by="Orario") # Ordina per orario

    st.subheader("I tuoi impegni di oggi")
    st.table(df)

    if st.button("Svuota Itinerario"):
        st.session_state.itinerario = []
        st.rerun()
else:
    st.info("L'itinerario è vuoto. Usa la barra laterale per aggiungere appuntamenti.")
  
