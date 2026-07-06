import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google import genai

st.title("Analizzatore Aziendale con Intelligenza Artificiale")
st.write("Carica il tuo file CSV per ottenere grafici e un report scritto dall'AI.")

# 1. Configurazione dell'AI di Google
# Per questo test locale, inserisci la tua API Key gratuita tra le virgolette.
# Puoi ottenerne una gratis su: https://google.com
API_KEY = st.secrets["GEMINI_API_KEY"]

file_caricato = st.file_uploader("Scegli un file CSV", type=["csv"])

if file_caricato is not None:
    df = pd.read_csv(file_caricato)
    
    st.write("Anteprima dei dati:")
    st.dataframe(df.head())
    
    colonne = df.columns.tolist()
    colonna_selezionata = st.selectbox("Seleziona la colonna da inserire nel grafico:", colonne)
    
    if colonna_selezionata:
        # Conteggio dei dati per il grafico
        conteggio_valori = df[colonna_selezionata].value_counts()
        
        # Creazione del grafico con Matplotlib
        fig, ax = plt.subplots()
        conteggio_valori.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_ylabel("Quantità")
        ax.set_xlabel(colonna_selezionata)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        
        # --- NUOVA SEZIONE AI ---
        st.subheader("🤖 Report e Consigli dell'Intelligenza Artificiale")
        
        if API_KEY == "LA_TUA_GEMINI_API_KEY_QUI":
            st.warning("Per attivare i commenti dell'AI, inserisci una chiave API valida nel codice.")
        else:
            with st.spinner("L'AI sta analizzando i tuoi dati..."):
                try:
                    # Prepariamo i dati in formato testo da inviare all'AI
                    dati_riassunti = conteggio_valori.to_string()
                    
                    # Inizializziamo il client di Google GenAI
                    client = genai.Client(api_key=API_KEY)
                    
                    # Chiediamo all'AI di fare l'analisi
                    risposta = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"Agisci come un consulente aziendale esperto. Analizza questi dati estratti dalla colonna '{colonna_selezionata}' di un file aziendale:\n{dati_riassunti}\n\nFornisci un riassunto breve, evidenzia eventuali problemi e dai 2 consigli pratici in italiano.",
                    )
                    
                    # Mostriamo la risposta sul sito web
                    st.write(risposta.text)
                    
                except Exception as e:
                    st.error(f"Errore durante la generazione del report AI: {e}")
