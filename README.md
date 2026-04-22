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

## Stato del progetto

✔ Milestone 1 - Semantic Foundation (in corso)
- Schema Decision Card definito