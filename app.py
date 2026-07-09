import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google import genai

# Configurazione della pagina
st.set_page_config(page_title="RistoData AI - Menu Engineering", page_icon="🍔")

st.title("🍔 RistoData AI - Dashboard Interna")
st.write("Area riservata per la generazione dei Report di Menu Engineering.")

file_caricato = st.file_uploader("Carica il file CSV del cliente", type=["csv"])

if file_caricato is not None:
    df = pd.read_csv(file_caricato)
    
    st.write("### 📊 Anteprima Dati:")
    st.dataframe(df.head())
    
    colonne = df.columns.tolist()
    
    indice_predefinito = 0
    for i, col in enumerate(colonne):
        if "prodotto" in col.lower() or "piatto" in col.lower() or "stato" in col.lower() or "reparto" in col.lower():
            indice_predefinito = i
            break
            
    colonna_selezionata = st.selectbox("Seleziona la colonna da analizzare:", colonne, index=indice_predefinito)
    
    if colonna_selezionata:
        conteggio_valori = df[colonna_selezionata].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        conteggio_valori.plot(kind='bar', ax=ax, color='#E63946')
        ax.set_ylabel("Quantità")
        ax.set_xlabel(colonna_selezionata)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        
        st.subheader("👨‍🍳 Testo generato dall'AI per il Report PDF")
        
        if "GEMINI_API_KEY" not in st.secrets:
            st.warning("Configura GEMINI_API_KEY nei Secrets di Streamlit.")
        else:
            with st.spinner("Generazione analisi in corso..."):
                try:
                    dati_riassunti = conteggio_valori.to_string()
                    chiave_segreta = st.secrets["GEMINI_API_KEY"]
                    
                    # Inizializzazione corretta della libreria google-genai
                    client = genai.Client(api_key=chiave_segreta)
                    
                    prompt_ristorazione = (
                        "Agisci come un Restaurant Manager esperto e un consulente finanziario specializzato nel settore Food & Beverage. "
                        f"Analizza i seguenti dati di vendita estratti dalla colonna '{colonna_selezionata}' del software di cassa del mio ristorante:\n"
                        f"{dati_riassunti}\n\n"
                        "Genera un report di ingegneria del menu (Menu Engineering) strutturato in lingua italiana. Segui rigorosamente questi punti:\n"
                        "1. **ANALISI DELLE PERFORMANCE**: Commenta l'andamento dei dati evidenziando cosa sta funzionando e cosa no.\n"
                        "2. **CLASSIFICAZIONE STRATEGICA**: Classifica le voci in base ai volumi descritti.\n"
                        "3. **3 CONSIGLI AZIENDALI PRATICI**: Fornisci tre azioni immediate e concrete che il proprietario può applicare per aumentare lo scontrino medio o tagliare i costi dei piatti meno redditizi.\n\n"
                        "Usa un tono autorevole, professionale, persuasivo ed estremamente orientato al profitto aziendale."
                    )
                    
                    # CHIAMATA CORRETTA: models.generate_content (plurale)
                    risposta = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_ristorazione,
                    )
                    
                    st.info(risposta.text)
                    
                except Exception as e:
                    st.error(f"Errore durante l'elaborazione dell'AI: {e}")
