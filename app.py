import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Gestione Itinerari", layout="wide")

# --- CONNESSIONE A GOOGLE SHEETS ---
# Sostituisci questo URL con quello del tuo foglio (assicurati che sia 'Editor')
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1M48xFONAr45TXsWJ5QwmLOYhKPARcqg5hPWQejDOEV0/edit?usp=drivesdk"

conn = st.connection("gsheets", type=GSheetsConnection)

# Funzione per leggere i dati
def leggi_rubrica():
    return conn.read(spreadsheet=URL_FOGLIO, usecols=[0, 1])

# Caricamento dati iniziale
df_rubrica = leggi_rubrica()

st.title("🚚 Organizzatore Lavoro con Google Sheets")

tab1, tab2 = st.tabs(["📇 Rubrica Clienti", "📅 Pianifica Itinerario"])

with tab1:
    st.header("Gestione Anagrafica")
    
    # Form per aggiungere nuovi clienti
    with st.form("nuovo_cliente"):
        nome = st.text_input("Nome Cliente/Azienda")
        indirizzo = st.text_input("Indirizzo Completo")
        submit = st.form_submit_button("Salva nel Cloud")
        
        if submit and nome:
            # Crea un nuovo record
            nuovo_dato = pd.DataFrame([{"Nome": nome, "Indirizzo": indirizzo}])
            # Unisci al vecchio database
            updated_df = pd.concat([df_rubrica, nuovo_dato], ignore_index=True)
            # Scrivi su Google Sheets
            conn.update(spreadsheet=URL_FOGLIO, data=updated_df)
            st.success(f"Cliente {nome} salvato su Google Sheets!")
            st.rerun()

    st.subheader("I tuoi contatti salvati")
    st.dataframe(df_rubrica, use_container_width=True)

with tab2:
    st.header("Crea l'itinerario di oggi")
    if not df_rubrica.empty:
        scelta = st.selectbox("Seleziona cliente dalla rubrica", df_rubrica["Nome"])
        indirizzo_sel = df_rubrica[df_rubrica["Nome"] == scelta]["Indirizzo"].values[0]
        
        st.info(f"📍 Destinazione: {indirizzo_sel}")
        # Qui potresti aggiungere i tasti per "Aggiungi al giro del giorno"
    else:
        st.warning("La rubrica è vuota. Vai nel Tab 1!")
    
