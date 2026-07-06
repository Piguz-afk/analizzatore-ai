import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google import genai

# Configurazione del titolo della pagina e dell'interfaccia focalizzata sui ristoranti
st.set_page_config(page_title="RistoData AI - Menu Engineering", page_icon="🍔")

st.title("🍔 RistoData AI - Ottimizzazione Menu")
st.write("Carica il file Excel/CSV delle vendite mensili per analizzare i margini del tuo ristorante.")

file_caricato = st.file_uploader("Trascina qui il file delle vendite della cassa (Formato CSV)", type=["csv"])

if file_caricato is not None:
    df = pd.read_csv(file_caricato)
    
    st.write("### 📊 Anteprima Registro Vendite Cassa:")
    st.dataframe(df.head())
    
    colonne = df.columns.tolist()
    
    # Tentiamo di preselezionare colonne comuni se esistono nel file
    indice_predefinito = 0
    for i, col in enumerate(colonne):
        if "prodotto" in col.lower() or "piatto" in col.lower() or "stato" in col.lower():
            indice_predefinito = i
            break
            
    colonna_selezionata = st.selectbox("Seleziona la colonna da analizzare nel grafico:", colonne, index=indice_predefinito)
    
    if colonna_selezionata:
        # Conteggio dei dati per il grafico delle performance del menu
        conteggio_valori = df[colonna_selezionata].value_counts()
        
        # Creazione del grafico con Matplotlib (stile professionale)
        fig, ax = plt.subplots(figsize=(10, 5))
        conteggio_valori.plot(kind='bar', ax=ax, color='#E63946')  # Rosso elegante per il settore food
        ax.set_ylabel("Quantità Ordini / Record")
        ax.set_xlabel(colonna_selezionata)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        
        # --- SEZIONE AI SPECIALIZZATA IN RESTAURANT MANAGEMENT ---
        st.subheader("👨‍🍳 Report Strategico del Restaurant Consultant AI")
        
        if "GEMINI_API_KEY" not in st.secrets:
            st.warning("Chiave di sblocco AI non configurata nei Secrets di Streamlit.")
        else:
            with st.spinner("L'intelligenza artificiale sta analizzando il tuo menu..."):
                try:
                    dati_riassunti = conteggio_valori.to_string()
                    chiave_segreta = st.secrets["GEMINI_API_KEY"]
                    client = genai.Client(api_key=chiave_segreta)
                    
                    # Istruzioni ad alto valore per l'analisi finanziaria del menu (Menu Engineering)
                    prompt_ristorazione = (
                        "Agisci come un Restaurant Manager esperto e un consulente finanziario specializzato nel settore del Food & Beverage. "
                        f"Analizza i seguenti dati di vendita estratti dalla colonna '{colonna_selezionata}' del software di cassa del mio ristorante:\n"
                        f"{dati_riassunti}\n\n"
                        "Genera un report di ingegneria del menu (Menu Engineering) strutturato in lingua italiana. Segui rigorosamente questi punti:\n"
                        "1. **ANALISI DELLE PERFORMANCE**: Commenta l'andamento dei dati evidenziando cosa sta funzionando e cosa no.\n"
                        "2. **CLASSIFICAZIONE STRATEGICA**: Se i dati lo consentono (es. se vedi riferimenti a margini o volumi), classifica i piatti in: "
                        "'Piatti Stella' (alta vendita, alto margine), 'Cavalli di Battaglia' (alta vendita, basso margine), 'Puzzle' (bassa vendita, alto margine) o 'Dog' (bassa vendita, basso margine).\n"
                        "3. **3 CONSIGLI AZIENDALI PRATICI**: Fornisci tre azioni immediate e concrete che lo chef o il proprietario possono applicare al menu questa settimana per aumentare lo scontrino medio o tagliare i costi dei piatti meno redditizi.\n\n"
                        "Usa un tono autorevole, professionale, persuasivo ed estremamente orientato al profitto aziendale."
                    )
                    
                    risposta = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_ristorazione,
                    )
                    
                    # Mostriamo la consulenza di alto valore sulla pagina web
                    st.info(risposta.text)
                    
                except Exception as e:
                    st.error(f"Errore durante l'elaborazione dei dati della ristorazione: {e}")
