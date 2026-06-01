# BD2-DecisionOS

## Corporate Memory System

Sistema per la gestione e memorizzazione di decisioni aziendali con supporto a ricerca semantica (RAG) e MongoDB Atlas.

## Decision Card Schema

Il sistema utilizza il seguente modello dati:

- titolo
- decisione_finale
- motivazione
- alternative_scartate
- decisori
- timestamp
- tags
- parent_id (per branching decisionale)
- embedding (per ricerca semantica)

Lo schema è progettato per supportare:
- MongoDB document-based storage
- future integrazioni con vector search (RAG)

## Setup configurazione e MongoDB

### Prerequisiti
- Python 3.x
- MongoDB Atlas (cluster attivo)

### Configurazione ambiente

1. Creare un file `.env` nella root del progetto
2. Copiare il contenuto di `.env.example`
3. Inserire la propria stringa di connessione MongoDB

Esempio:

MONGODB_URI=your_mongodb_connection_string_here  
MONGODB_DB_NAME=DecisionOS  
MONGODB_COLLECTION=decisions 
API_KEY=your_api_key  
EMBEDDING_MODEL=gemini-embedding-001

## Database Service

Il sistema include un layer di accesso ai dati tramite la classe `DatabaseService`.

Questo componente è responsabile di:

- connessione a MongoDB Atlas
- creazione documenti
- recupero Decision Card singole
- recupero liste di Decision Card
- aggiornamento documenti
- eliminazione documenti
- gestione ObjectId MongoDB
- verifica dell’indice vettoriale
- gestione errori e logging

## Vector Service

Il sistema include un servizio per la generazione degli embedding tramite la classe `VectorService`.

Questo componente è responsabile di:
- generazione embedding a partire da testo (decisione + motivazione)
- utilizzo di un modello configurabile tramite variabili d’ambiente
- pulizia del testo prima della chiamata API
- gestione errori e logging

## Seeding Pipeline

Il sistema include una pipeline di inserimento dati tramite la classe `SeedingPipeline`.

Questo componente è responsabile di:
- processamento di un dataset (Gold Dataset)
- validazione dei dati tramite `DecisionCard`
- generazione embedding tramite `VectorService`
- inserimento nel database tramite `DatabaseService`
- gestione errori e logging durante il processo

La pipeline esegue il flusso:
validazione → embedding → inserimento
Lanciare la classe `verify_dimensions` per verificare la dimensione reale dei vettori nel database 

## Search Service

Il sistema include un servizio di ricerca semantica tramite la classe `SearchService`.
Questo componente è responsabile del recupero dei documenti più rilevanti dalla memoria aziendale attraverso similarità vettoriale.

Responsabilità principali:
- generazione embedding della query tramite `VectorService`
- esecuzione di query semantiche su MongoDB Atlas
- utilizzo dell’operatore `$vectorSearch`
- ricerca basata su cosine similarity
- recupero dei documenti più rilevanti (top-k)
- gestione errori e logging

Pipeline di ricerca:
Query testuale  
→ Embedding query  
→ Vector Search su MongoDB Atlas  
→ Ranking per similarità  
→ Output documenti rilevanti

Configurazione tecnica:
- indice vettoriale: `vector_index`
- campo embedding: `embedding`
- metrica: cosine similarity
- top_k configurabile (default: 3)

## API Data Models

Il sistema utilizza DTO (Data Transfer Objects) separati per supportare la validazione delle API FastAPI.

Sono presenti:
- `DecisionCardCreate`
- `DecisionCardUpdate`
- `DecisionCardResponse`

La serializzazione degli ObjectId MongoDB è gestita tramite `PyObjectId`.

Il layer di validazione utilizza Pydantic per garantire:
- validazione input/output
- compatibilità MongoDB
- separazione tra schema database e schema API

## FastAPI API

Il sistema espone una REST API tramite FastAPI per la gestione completa delle Decision Card.

Sono disponibili endpoint per:

creazione decisioni
recupero decisioni
aggiornamento decisioni
eliminazione decisioni

L’API integra:

DatabaseService
VectorService
DTO Pydantic

Gli embedding vengono generati automaticamente durante la creazione e aggiornati quando cambiano:

decisione_finale
motivazione

## Avvio server
python -m uvicorn main:app --reload

## Documentazione API

Una volta avviato il server:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

## Architettura del sistema

Il sistema è organizzato nei seguenti layer:

- API Layer (`main.py`)
- Validation Layer (`models.py`)
- Persistence Layer (`database_service.py`)
- Embedding Layer (`vector_service.py`)
- Data Ingestion Layer (`seeding_pipeline.py`)
- Retrieval Layer (`search_service.py`)

Flusso principale:

API Request → Validation → Embedding Generation → MongoDB Persistence

### Installazione dipendenze

```bash
pip install -r requirements.txt


## Stato del progetto

✔ Milestone 1 - Semantic Foundation (completata)
- Schema Decision Card definiton
- Setup configurazione progetto e connessione MongoDB
- DatabaseService per accesso ai dati
- VectorService per generazione embedding
- SeedingPipeline per inserimento dati

✔ Milestone 2 - The Memory Engine (completata)
- DTO API e validazione
- CRUD MongoDB
- REST API FastAPI
- Gestione automatica embedding
- Lifecycle completo Decision Card

🚧 Milestone 3 - RAG Pipeline (in corso)
- SearchService per ricerca semantica 


## Copyright

© 2026 **DecisionOS**. Tutti i diritti riservati.

Questo software e la relativa documentazione sono proprietà intellettuale di **DecisionOS**. 
È vietata la riproduzione, la copia o la distribuzione non autorizzata di qualsiasi parte del codice o del design.
