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
- inserimento delle Decision Card
- verifica dell’indice vettoriale

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
