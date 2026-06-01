import google.generativeai as genai
from config import settings

# Configurazione
genai.configure(api_key=settings.GOOGLE_API_KEY)

print("--- Modelli disponibili per la tua API Key che supportano la generazione di contenuti ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Nome Modello: {m.name}")
except Exception as e:
    print(f"Errore durante il recupero dei modelli: {e}")