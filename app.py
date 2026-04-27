import streamlit as st
import pandas as pd

# Funzione per generare il link multi-tappa di Google Maps
def genera_link_percorso(fermate):
    # Base URL per le direzioni di Google Maps
    base_url = "https://www.google.com/maps/dir/"
    # Formattiamo gli indirizzi per l'URL (sostituendo spazi con + e unendo con /)
    path = "/".join([addr.replace(' ', '+') for addr in fermate])
    return base_url + path

# --- TAB 2: PIANIFICA ITINERARIO ---
with tab2:
    st.header("📍 Pianifica il giro di oggi")
    
    if not df_rubrica.empty:
        # Inizializziamo una lista nello stato della sessione per le tappe di oggi
        if 'tappe_oggi' not in st.session_state:
            st.session_state.tappe_oggi = []

        col1, col2 = st.columns([2, 1])
        
        with col1:
            scelta = st.selectbox("Seleziona cliente dalla rubrica", df_rubrica["Nome"])
            indirizzo_sel = df_rubrica[df_rubrica["Nome"] == scelta]["Indirizzo"].values[0]
            st.write(f"Indirizzo selezionato: **{indirizzo_sel}**")
            
        with col2:
            st.write(" ") # Spazio estetico
            if st.button("➕ Aggiungi al giro"):
                if indirizzo_sel not in st.session_state.tappe_oggi:
                    st.session_state.tappe_oggi.append(indirizzo_sel)
                    st.success("Aggiunto!")
                else:
                    st.warning("Già presente!")

        # Visualizzazione delle tappe scelte
        if st.session_state.tappe_oggi:
            st.subheader("Il tuo itinerario attuale:")
            for i, tappa in enumerate(st.session_state.tappe_oggi):
                st.write(f"{i+1}. {tappa}")
            
            if st.button("🗑️ Svuota tutto"):
                st.session_state.tappe_oggi = []
                st.rerun()
            
            # --- TASTO MAGICO ---
            st.divider()
            link_finale = genera_link_percorso(st.session_state.tappe_oggi)
            
            st.link_button("🗺️ APRI PERCORSO SU GOOGLE MAPS", link_finale, type="primary", use_container_width=True)
            st.info("Nota: Google Maps supporta fino a 10 tappe per volta.")
    else:
        st.warning("La rubrica è vuota. Vai nel Tab 1 e aggiungi i tuoi clienti!")
    
