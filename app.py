import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configurazione pagina
st.set_page_config(page_title="Work Planner", layout="wide", page_icon="🚚")

# --- CONNESSIONE A GOOGLE SHEETS ---
# Incolla qui l'URL del tuo foglio Google
URL_FOGLIO = "1M48xFONAr45TXsWJ5QwmLOYhKPARcqg5hPWQejDOEV0/edit?usp=drivesdk"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Errore di connessione a Google Sheets. Verifica l'URL.")

# Funzione per leggere i dati aggiornati
def leggi_dati():
    return conn.read(spreadsheet=URL_FOGLIO, usecols=[0, 1]).dropna(how="all")

# Caricamento iniziale della rubrica
df_rubrica = leggi_dati()

# --- HEADER ---
st.title("📅 Organizzatore Itinerari di Lavoro")
st.markdown("Gestisci i tuoi clienti e crea percorsi ottimizzati su Google Maps.")

# --- TABS ---
tab1, tab2 = st.tabs(["📇 Rubrica Clienti", "📍 Pianifica Itinerario"])

# --- TAB 1: GESTIONE RUBRICA ---
with tab1:
    st.header("Gestione Anagrafica")
    
    with st.expander("➕ Aggiungi un nuovo cliente", expanded=False):
        with st.form("form_cliente"):
            nome = st.text_input("Nome Azienda / Cliente")
            indirizzo = st.text_input("Indirizzo Completo (Via, Civico, Città)")
            submit = st.form_submit_button("Salva in Rubrica")
            
            if submit:
                if nome and indirizzo:
                    # Crea il nuovo record
                    nuovo_dato = pd.DataFrame([{"Nome": nome, "Indirizzo": indirizzo}])
                    # Unisci al database esistente
                    updated_df = pd.concat([df_rubrica, nuovo_dato], ignore_index=True)
                    # Aggiorna Google Sheets
                    conn.update(spreadsheet=URL_FOGLIO, data=updated_df)
                    st.success(f"Cliente '{nome}' salvato correttamente!")
                    st.rerun()
                else:
                    st.warning("Per favore, compila entrambi i campi.")

    st.subheader("I tuoi contatti")
    st.dataframe(df_rubrica, use_container_width=True, hide_index=True)

# --- TAB 2: PIANIFICA ITINERARIO ---
with tab2:
    st.header("Costruisci il percorso di oggi")
    
    if not df_rubrica.empty:
        # Inizializziamo la lista tappe nella sessione
        if 'tappe_oggi' not in st.session_state:
            st.session_state.tappe_oggi = []

        col_a, col_b = st.columns([3, 1])
        
        with col_a:
            scelta_cliente = st.selectbox("Seleziona dalla rubrica", df_rubrica["Nome"])
            # Recupera l'indirizzo corrispondente
            indirizzo_sel = df_rubrica[df_rubrica["Nome"] == scelta_cliente]["Indirizzo"].values[0]
            st.info(f"📍 **Indirizzo:** {indirizzo_sel}")
            
        with col_b:
            st.write("##") # Spaziatore
            if st.button("➕ Aggiungi al Giro", use_container_width=True):
                if indirizzo_sel not in st.session_state.tappe_oggi:
                    st.session_state.tappe_oggi.append(indirizzo_sel)
                    st.rerun()
                else:
                    st.warning("Indirizzo già presente nell'itinerario.")

        st.divider()

        # Visualizzazione Itinerario creato
        if st.session_state.tappe_oggi:
            st.subheader("Tappe del giorno:")
            for i, t in enumerate(st.session_state.tappe_oggi):
                st.write(f"**{i+1}.** {t}")
            
            if st.button("🗑️ Svuota itinerario"):
                st.session_state.tappe_oggi = []
                st.rerun()

            # --- GENERAZIONE LINK GOOGLE MAPS ---
            st.subheader("Esecuzione")
            # Pulizia indirizzi per URL
            fermate_formattate = [t.replace(' ', '+') for t in st.session_state.tappe_oggi]
            percorso_stringa = "/".join(fermate_formattate)
            maps_url = f"https://www.google.com/maps/dir/{percorso_stringa}"
            
            st.link_button("🚀 APRI PERCORSO SU GOOGLE MAPS", maps_url, type="primary", use_container_width=True)
        else:
            st.write("L'itinerario è ancora vuoto. Aggiungi i clienti qui sopra.")
    else:
        st.warning("La rubrica è vuota. Inserisci dei clienti nel primo Tab.")
            
