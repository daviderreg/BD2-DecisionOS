from pymongo import MongoClient
from config import settings

client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DB_NAME]
collection = db[settings.MONGODB_COLLECTION]

# Prendi un documento a campione
doc = collection.find_one()

if doc and 'embedding' in doc:
    dim = len(doc['embedding'])
    print(f"✅ Verifica completata!")
    print(f"La dimensione reale dei vettori nel database è: {dim}")
    
    if dim == 1536:
        print("👉 L'indice su Atlas DEVE essere impostato a 1536.")
    elif dim == 768:
        print("👉 L'indice su Atlas DEVE essere impostato a 768.")
else:
    print("❌ Nessun documento trovato o campo embedding mancante.")