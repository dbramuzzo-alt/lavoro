import streamlit as st
import pandas as pd

st.title("💼 Gestione Lavoro: Rubrica & Itinerari")

# Usiamo i tab per separare Rubrica e Itinerario
tab1, tab2 = st.tabs(["📇 Rubrica Clienti", "📅 Itinerario del Giorno"])

# --- TAB 1: RUBRICA CLIENTI ---
with tab1:
    st.header("Aggiungi un nuovo cliente")
    if 'rubrica' not in st.session_state:
        st.session_state.rubrica = pd.DataFrame(columns=["Nome", "Indirizzo"])

    with st.form("nuovo_cliente"):
        nome_c = st.text_input("Nome Azienda / Cliente")
        indirizzo_c = st.text_input("Indirizzo Completo")
        submit_c = st.form_submit_button("Salva in Rubrica")
        
        if submit_c and nome_c:
            nuovo_dato = pd.DataFrame([{"Nome": nome_c, "Indirizzo": indirizzo_c}])
            st.session_state.rubrica = pd.concat([st.session_state.rubrica, nuovo_dato], ignore_index=True)
            st.success(f"{nome_c} aggiunto correttamente!")

    st.subheader("I tuoi contatti")
    st.dataframe(st.session_state.rubrica, use_container_width=True)

# --- TAB 2: ITINERARIO (Migliorato) ---
with tab2:
    st.header("Costruisci il tuo giro")
    if not st.session_state.rubrica.empty:
        # Qui il vantaggio: selezioni il cliente dalla rubrica!
        cliente_scelto = st.selectbox("Seleziona Cliente dalla Rubrica", st.session_state.rubrica["Nome"])
        
        # Recupera l'indirizzo in automatico
        info_cliente = st.session_state.rubrica[st.session_state.rubrica["Nome"] == cliente_scelto]
        indirizzo_automatico = info_cliente["Indirizzo"].values[0]
        
        st.write(f"📍 **Indirizzo:** {indirizzo_automatico}")
        # ... qui prosegue la logica per aggiungere l'orario e salvare l'itinerario ...
    else:
        st.warning("Aggiungi prima dei clienti nella Rubrica per pianificare l'itinerario.")
        
