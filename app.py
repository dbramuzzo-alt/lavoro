import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Work Planner Pro", layout="wide", page_icon="🚚")

# --- CONNESSIONE GOOGLE SHEETS ---
def init_connection():
    # Definiamo i permessi necessari
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Recuperiamo le credenziali dai Secrets di Streamlit
    try:
        creds_dict = st.secrets["gspread_creds"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        # ⚠️ SOSTITUISCI CON L'URL DEL TUO FOGLIO GOOGLE ⚠️
        url_foglio = "https://docs.google.com/spreadsheets/d/1M48xFONAr45TXsWJ5QwmLOYhKPARcqg5hPWQejDOEV0/edit?usp=drivesdk"
        
        return client.open_by_url(url_foglio).sheet1
    except Exception as e:
        st.error(f"Errore di connessione: {e}")
        return None

sheet = init_connection()

# Funzione per leggere i dati dal foglio
def leggi_rubrica():
    if sheet:
        # Recupera tutti i dati e trasforma in DataFrame
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    return pd.DataFrame(columns=["Nome", "Indirizzo"])

# Caricamento dati
df_rubrica = leggi_rubrica()

# --- INTERFACCIA UTENTE ---
st.title("📅 Organizzatore Itinerari Giornalieri")
st.markdown("Gestione clienti centralizzata su Google Sheets e navigazione Maps.")

tab1, tab2 = st.tabs(["📇 Rubrica Clienti", "📍 Pianifica Itinerario"])

# --- TAB 1: GESTIONE RUBRICA ---
with tab1:
    st.header("Anagrafica Clienti")
    
    with st.expander("➕ Aggiungi Nuovo Cliente", expanded=False):
        with st.form("form_inserimento"):
            nome_c = st.text_input("Nome Cliente / Azienda")
            indirizzo_c = st.text_input("Indirizzo Completo (Via, Civico, Città)")
            btn_salva = st.form_submit_button("Salva nel Cloud")
            
            if btn_salva:
                if nome_c and indirizzo_c:
                    # Aggiunge una riga in fondo al foglio Google
                    sheet.append_row([nome_c, indirizzo_c])
                    st.success(f"Cliente '{nome_c}' aggiunto con successo!")
                    st.rerun()
                else:
                    st.warning("Compila tutti i campi prima di salvare.")

    st.subheader("I tuoi contatti salvati")
    if not df_rubrica.empty:
        st.dataframe(df_rubrica, use_container_width=True, hide_index=True)
    else:
        st.info("La rubrica è vuota. Aggiungi il tuo primo cliente qui sopra.")

# --- TAB 2: PIANIFICAZIONE PERCORSO ---
with tab2:
    st.header("Crea il giro di oggi")
    
    if not df_rubrica.empty:
        # Inizializziamo la lista delle tappe nella sessione del browser
        if 'tappe_oggi' not in st.session_state:
            st.session_state.tappe_oggi = []

        col1, col2 = st.columns([3, 1])
        
        with col1:
            selezione = st.selectbox("Seleziona cliente dalla rubrica", df_rubrica["Nome"])
            # Trova l'indirizzo corrispondente al nome selezionato
            indirizzo_selezionato = df_rubrica[df_rubrica["Nome"] == selezione]["Indirizzo"].values[0]
            st.info(f"📍 **Indirizzo:** {indirizzo_selezionato}")
            
        with col2:
            st.write("##") # Spaziatore verticale
            if st.button("➕ Aggiungi al Giro", use_container_width=True):
                if indirizzo_selezionato not in st.session_state.tappe_oggi:
                    st.session_state.tappe_oggi.append(indirizzo_selezionato)
                    st.rerun()
                else:
                    st.warning("Destinazione già inserita.")

        st.divider()

        # Visualizzazione elenco tappe
        if st.session_state.tappe_oggi:
            st.subheader("Il tuo itinerario:")
            for i, tappa in enumerate(st.session_state.tappe_oggi):
                st.write(f"**{i+1}.** {tappa}")
            
            if st.button("🗑️ Svuota Itinerario"):
                st.session_state.tappe_oggi = []
                st.rerun()

            # --- GENERAZIONE LINK GOOGLE MAPS MULTI-TAPPA ---
            # Pulizia degli indirizzi per l'URL
            indirizzi_puliti = [t.replace(' ', '+') for t in st.session_state.tappe_oggi]
            percorso_stringa = "/".join(indirizzi_puliti)
            
            # Link per navigazione multi-tappa
            maps_url = f"https://www.google.com/maps/dir/{percorso_stringa}"
            
            st.link_button("🚀 APRI PERCORSO SU GOOGLE MAPS", maps_url, type="primary", use_container_width=True)
            st.caption("Il link aprirà l'app di Google Maps con tutte le tappe nell'ordine indicato.")
        else:
            st.write("Non hai ancora aggiunto tappe per oggi.")
    else:
        st.warning("Vai nel Tab 'Rubrica Clienti' per inserire i tuoi primi contatti.")
    
