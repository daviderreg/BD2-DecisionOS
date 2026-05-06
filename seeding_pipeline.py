from models import DecisionCard
from vector_service import VectorService
from database_service import DatabaseService
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeedingPipeline:
    def __init__(self):
        self.vector_service = VectorService()
        self.db_service = DatabaseService()

    def process_gold_dataset(self, dataset: list):
        """
        Pipeline di seeding: 
        1. Validazione Schema -> 2. Generazione Embedding -> 3. Persistenza
        """
        success_count = 0
        for record in dataset:
            try:
                # 1. Validazione Input
                # Convertiamo timestamp string to datetime if necessary
                if isinstance(record.get('timestamp'), str):
                    record['timestamp'] = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
                
                decision = DecisionCard(**record)
                
                # 2. Creazione Testo per Embedding (Decisione + Motivazione)
                text_to_embed = f"{decision.decisione_finale} {decision.motivazione}"
                
                # 3. Generazione Vettori
                logger.info(f"Generazione embedding per: {decision.titolo}")
                embedding = self.vector_service.generate_embedding(text_to_embed)
                
                # 4. Aggiornamento modello e salvataggio
                decision.embedding = embedding
                self.db_service.insert_decision(decision.to_mongodb())
                
                success_count += 1
            except Exception as e:
                logger.error(f"Fallimento processamento record {record.get('titolo')}: {str(e)}")

        logger.info(f"Seeding completato. Record inseriti: {success_count}/{len(dataset)}")

# --- ESECUZIONE MAIN ---
if __name__ == "__main__":
    gold_dataset = [
        {
            "titolo": "Migrazione storage messaggi da Cassandra a ScyllaDB",
            "decisione_finale": "Sostituzione di Apache Cassandra con ScyllaDB",
            "motivazione": "Necessità di eliminare le pause del Garbage Collector (GC) di Java che causavano latenze imprevedibili e risolvere il problema delle 'Hot Partitions' in cluster con miliardi di messaggi.",
            "alternative_scartate": [
                {"opzione": "Rimanere su Apache Cassandra", "motivo_scarto": "Troppo overhead operativo per il tuning della JVM e instabilità delle latenze P99 sotto carico estremo."},
                {"opzione": "Ritorno a MongoDB", "motivo_scarto": "Incapacità di gestire il throughput di scrittura richiesto a quella scala."}
            ],
            "decisori": ["Infrastructure Team", "Backend Architects"],
            "timestamp": "2023-03-06T00:00:00Z",
            "parent_id": None,
            "tags": ["database", "scalability", "latency", "ScyllaDB"]
        },
        
  {
    "titolo": "Strategia di Pricing: Freemium vs Free Trial",
    "decisione_finale": "Adozione modello Freemium con limitazioni basate su volume di dati",
    "motivazione": "L'analisi di mercato indica che il nostro target (developer) preferisce testare il prodotto senza scadenza temporale, ma è disposto a pagare per scalare l'operatività.",
    "alternative_scartate": [
      { "opzione": "Free Trial di 14 giorni", "motivo_scarto": "Troppo attrito nell'onboarding; tasso di conversione stimato più basso per prodotti a bassa barriera d'ingresso." },
      { "opzione": "Pay-per-use puro", "motivo_scarto": "Rende imprevedibile il costo per l'utente finale, scoraggiando l'adozione iniziale." }
    ],
    "decisori": ["Chief Product Officer", "Head of Marketing"],
    "timestamp": "2025-11-10T10:00:00Z",
    "parent_id": None,
    "tags": ["pricing", "growth", "product-strategy"]
  },
  {
    "titolo": "Scelta Framework Frontend: React vs Vue",
    "decisione_finale": "Standardizzazione su React",
    "motivazione": "Ampiezza dell'ecosistema di librerie e facilità di reperimento di talenti sul mercato del lavoro, riducendo i tempi di recruiting.",
    "alternative_scartate": [
      { "opzione": "Vue.js", "motivo_scarto": "Sebbene più semplice da apprendere, l'ecosistema di componenti enterprise è meno maturo rispetto a React." },
      { "opzione": "Svelte", "motivo_scarto": "Troppo precoce per un progetto enterprise; mancanza di supporto a lungo termine garantito." }
    ],
    "decisori": ["Lead Frontend Dev", "CTO"],
    "timestamp": "2025-08-15T09:00:00Z",
    "parent_id": None,
    "tags": ["frontend", "tech-stack", "hiring"]
  },
  {
    "titolo": "Politica di Lavoro: Remote-First vs Hybrid",
    "decisione_finale": "Adozione modello Remote-First con hub fisico opzionale",
    "motivazione": "Permette di attrarre talenti globali senza limiti geografici, riducendo i costi fissi di gestione degli uffici del 40%.",
    "alternative_scartate": [
      { "opzione": "Hybrid (3 giorni in ufficio)", "motivo_scarto": "Crea disparità tra dipendenti locali e remoti, limitando la scalabilità del team." },
      { "opzione": "Full Office", "motivo_scarto": "Rischio elevato di turnover dei talenti senior che richiedono flessibilità." }
    ],
    "decisori": ["CEO", "HR Director"],
    "timestamp": "2026-01-20T14:00:00Z",
    "parent_id": None,
    "tags": ["HR", "culture", "operations"]
  },
  {
    "titolo": "Architettura API: REST vs GraphQL",
    "decisione_finale": "Implementazione di GraphQL per il Backend-for-Frontend (BFF)",
    "motivazione": "Riduzione del fenomeno 'over-fetching' e 'under-fetching' dei dati, migliorando drasticamente le performance sulle app mobile.",
    "alternative_scartate": [
      { "opzione": "REST API standard", "motivo_scarto": "Richiederebbe troppe chiamate API diverse per comporre una singola vista utente complessa." }
    ],
    "decisori": ["System Architect", "Mobile Lead"],
    "timestamp": "2025-09-12T11:00:00Z",
    "parent_id": None,
    "tags": ["API", "performance", "architecture"]
  },
  {
    "titolo": "Gestione Autenticazione: Auth0 vs Custom Solution",
    "decisione_finale": "Integrazione di Auth0",
    "motivazione": "Riduzione del time-to-market e delega della sicurezza (SOC2, GDPR) a un provider specializzato, evitando rischi legali e bug critici.",
    "alternative_scartate": [
      { "opzione": "Sviluppo custom di identity provider", "motivo_scarto": "Costo di manutenzione troppo elevato e rischio di vulnerabilità di sicurezza." }
    ],
    "decisori": ["CTO", "Security Officer"],
    "timestamp": "2025-07-01T16:00:00Z",
    "parent_id": None,
    "tags": ["security", "auth", "compliance"]
  },
  {
    "titolo": "Strategia Cloud: Multi-Cloud vs Single Vendor (AWS)",
    "decisione_finale": "Single Vendor (AWS) con strategia di astrazione via Terraform",
    "motivazione": "Semplificazione operativa e massima integrazione tra i servizi. L'astrazione via IaC permette una migrazione futura se necessario.",
    "alternative_scartate": [
      { "opzione": "Multi-Cloud (AWS + Azure)", "motivo_scarto": "Troppa complessità nella gestione delle reti e duplicazione dei costi di gestione." }
    ],
    "decisori": ["DevOps Lead", "CTO"],
    "timestamp": "2025-06-10T08:30:00Z",
    "parent_id": None,
    "tags": ["cloud", "infrastructure", "DevOps"]
  },
  {
    "titolo": "Metodologia di Sviluppo: Scrum vs Kanban",
    "decisione_finale": "Adozione di Scrumban (ibrido)",
    "motivazione": "Necessità di mantenere la pianificazione a sprint (Scrum) ma con la flessibilità di gestire bug urgenti in flusso continuo (Kanban).",
    "alternative_scartate": [
      { "opzione": "Pure Scrum", "motivo_scarto": "Troppo rigido per gestire le emergenze di produzione senza rompere lo sprint." },
      { "opzione": "Pure Kanban", "motivo_scarto": "Mancanza di scadenze chiare per le feature strategiche." }
    ],
    "decisori": ["Engineering Manager", "Product Owner"],
    "timestamp": "2025-05-20T10:00:00Z",
    "parent_id": None,
    "tags": ["process", "agile", "productivity"]
  },
  {
    "titolo": "Scelta Payment Gateway: Stripe vs Adyen",
    "decisione_finale": "Integrazione di Stripe",
    "motivazione": "Facilità di integrazione via API e gestione superiore dei pagamenti ricorrenti (subscriptions) per il mercato USA.",
    "alternative_scartate": [
      { "opzione": "Adyen", "motivo_scarto": "Più potente per volumi massivi globali, ma processo di onboarding troppo lento per l'attuale fase di crescita." }
    ],
    "decisori": ["CFO", "Lead Backend"],
    "timestamp": "2025-04-11T12:00:00Z",
    "parent_id": None,
    "tags": ["payments", "finance", "integrations"]
  },
  {
    "titolo": "Strategia di Log: ELK Stack vs Datadog",
    "decisione_finale": "Migrazione a Datadog",
    "motivazione": "Riduzione drastica dell'overhead di manutenzione dei cluster Elasticsearch e migliore visibilità end-to-end (APM + Logs).",
    "alternative_scartate": [
      { "opzione": "Auto-hosted ELK", "motivo_scarto": "Il team DevOps spendeva il 20% del tempo solo a mantenere l'infrastruttura di log." }
    ],
    "decisori": ["DevOps Lead", "SRE"],
    "timestamp": "2025-03-05T09:00:00Z",
    "parent_id": None,
    "tags": ["monitoring", "observability", "ops"]
  },
  {
    "titolo": "Gestione Repository: Monorepo vs Polyrepo",
    "decisione_finale": "Adozione di un Monorepo (via Nx)",
    "motivazione": "Semplificazione della condivisione di tipi TypeScript tra frontend e backend e atomicità dei commit che impattano più servizi.",
    "alternative_scartate": [
      { "opzione": "Polyrepo", "motivo_scarto": "Troppo overhead nella gestione delle versioni delle librerie condivise e dipendenze incrociate." }
    ],
    "decisori": ["Lead Architect", "Frontend Lead"],
    "timestamp": "2025-02-18T15:00:00Z",
    "parent_id": None,
    "tags": ["git", "architecture", "dx"]
  },
  {
    "titolo": "Certificazione di Sicurezza: SOC2 vs ISO 27001",
    "decisione_finale": "Priorità alla certificazione SOC2 Type II",
    "motivazione": "Requisito fondamentale per chiudere contratti con clienti Enterprise negli Stati Uniti.",
    "alternative_scartate": [
      { "opzione": "ISO 27001", "motivo_scarto": "Molto riconosciuta in EU, ma meno richiesta dai buyer tech americani in fase di MVP." }
    ],
    "decisori": ["CEO", "Compliance Officer"],
    "timestamp": "2025-01-10T11:00:00Z",
    "parent_id": None,
    "tags": ["compliance", "security", "sales"]
  },
  {
    "titolo": "Strategia Mobile: Native vs Cross-Platform",
    "decisione_finale": "Sviluppo in Flutter",
    "motivazione": "Possibilità di mantenere un unico codebase per iOS e Android con performance quasi native e tempi di rilascio dimezzati.",
    "alternative_scartate": [
      { "opzione": "Native (Swift/Kotlin)", "motivo_scarto": "Costi di sviluppo raddoppiati e difficoltà nel sincronizzare le feature tra le due piattaforme." },
      { "opzione": "React Native", "motivo_scarto": "Problemi di performance riscontrati nei prototipi per l'interfaccia grafica complessa richiesta." }
    ],
    "decisori": ["Mobile Lead", "CPO"],
    "timestamp": "2024-12-01T10:00:00Z",
    "parent_id": None,
    "tags": ["mobile", "flutter", "ux"]
  },
  {
    "titolo": "Sistema di Notifiche: Push vs Email vs SMS",
    "decisione_finale": "Implementazione di un sistema multi-canale orchestrato via Novu",
    "motivazione": "Permettere all'utente di scegliere il canale di ricezione, migliorando l'engagement senza saturare la inbox email.",
    "alternative_scartate": [
      { "opzione": "Solo Email", "motivo_scarto": "Tasso di apertura troppo basso per notifiche urgenti." }
    ],
    "decisori": ["Product Manager", "Backend Dev"],
    "timestamp": "2024-11-15T14:00:00Z",
    "parent_id": None,
    "tags": ["engagement", "notifications", "ux"]
  },
  {
    "titolo": "Gestione Task: Jira vs Linear",
    "decisione_finale": "Migrazione da Jira a Linear",
    "motivazione": "Linear è drasticamente più veloce e orientato alla velocità dei team di prodotto, riducendo il tempo speso in 'ticket management'.",
    "alternative_scartate": [
      { "opzione": "Rimanere su Jira", "motivo_scarto": "Troppa complessità e lentezza dell'interfaccia, percepita come ostacolo dalla produttività del team." }
    ],
    "decisori": ["Engineering Manager", "Team Leads"],
    "timestamp": "2024-10-05T09:00:00Z",
    "parent_id": None,
    "tags": ["tools", "productivity", "workflow"]
  },
  {
    "titolo": "Strategia Content: Blog Tecnico vs Social Media",
    "decisione_finale": "Investimento primario in Blog Tecnico di approfondimento",
    "motivazione": "Costruzione di autorità nel settore (Thought Leadership) che genera lead di qualità superiore nel lungo periodo (SEO).",
    "alternative_scartate": [
      { "opzione": "Campagne massive su TikTok/Instagram", "motivo_scarto": "Portata ampia ma lead di scarsa qualità per un prodotto B2B Enterprise." }
    ],
    "decisori": ["Head of Growth", "CEO"],
    "timestamp": "2024-09-20T11:00:00Z",
    "parent_id": None,
    "tags": ["marketing", "growth", "content"]
  },
  {
    "titolo": "Approccio Testing: Manuale vs Automatizzato",
    "decisione_finale": "Obbligo di test automatizzati (Integration + E2E) per ogni PR",
    "motivazione": "Riduzione dei regression bug in produzione che stavano rallentando il ciclo di rilascio.",
    "alternative_scartate": [
      { "opzione": "QA manuale dedicato", "motivo_scarto": "Collo di bottiglia insostenibile con l'aumento della frequenza dei deploy." }
    ],
    "decisori": ["QA Lead", "CTO"],
    "timestamp": "2024-08-12T15:00:00Z",
    "parent_id": None,
    "tags": ["quality", "testing", "ci-cd"]
  },
  {
    "titolo": "Gestione Debito Tecnico: Sprint dedicati vs 20% time",
    "decisione_finale": "Allocazione del 20% di ogni sprint al debito tecnico",
    "motivazione": "Evita l'accumulo massivo di debito che renderebbe necessario un 'freeze' totale del prodotto ogni 6 mesi.",
    "alternative_scartate": [
      { "opzione": "Uno sprint di cleanup ogni 2 mesi", "motivo_scarto": "Rallenta troppo l'erogazione di valore al cliente e crea frustrazione nel business." }
    ],
    "decisori": ["Engineering Manager", "CPO"],
    "timestamp": "2024-07-01T10:00:00Z",
    "parent_id": None,
    "tags": ["tech-debt", "management", "process"]
  },
  {
    "titolo": "Scelta Provider Email: SendGrid vs Postmark",
    "decisione_finale": "Passaggio a Postmark per le email transazionali",
    "motivazione": "Deliverability superiore e tempi di consegna più rapidi per email critiche (reset password, MFA).",
    "alternative_scartate": [
      { "opzione": "SendGrid", "motivo_scarto": "Troppi problemi di deliverability e supporto clienti inefficiente." }
    ],
    "decisori": ["Backend Lead", "Product Manager"],
    "timestamp": "2024-06-15T12:00:00Z",
    "parent_id": None,
    "tags": ["infrastructure", "email", "ux"]
  },
  {
    "titolo": "Strategia di Onboarding: Self-Serve vs Guided",
    "decisione_finale": "Implementazione di un flusso Self-Serve assistito da AI",
    "motivazione": "Scalabilità del processo di onboarding senza dover aumentare linearmente il numero di Customer Success Manager.",
    "alternative_scartate": [
      { "opzione": "Onboarding guidato via call", "motivo_scarto": "Impossibile da scalare per l'obiettivo di acquisire 1000+ clienti all'anno." }
    ],
    "decisori": ["Head of CS", "CPO"],
    "timestamp": "2024-05-10T14:00:00Z",
    "parent_id": None,
    "tags": ["onboarding", "growth", "customer-success"]
  },
  {
    "titolo": "Scelta Database Cache: Redis vs Memcached",
    "decisione_finale": "Adozione di Redis",
    "motivazione": "Necessità di strutture dati avanzate (Sorted Sets, Hashes) per implementare le classifiche in tempo reale e le sessioni utente.",
    "alternative_scartate": [
      { "opzione": "Memcached", "motivo_scarto": "Troppo limitato; supporta solo coppie chiave-valore semplici." }
    ],
    "decisori": ["Backend Architect", "CTO"],
    "timestamp": "2024-04-01T09:00:00Z",
    "parent_id": None,
    "tags": ["cache", "performance", "backend"]
  },
  
  {
    "titolo": "Scelta Provider Cloud - Vincolo Corporate",
    "decisione_finale": "Adozione di Azure",
    "motivazione": "Nonostante il team tecnico preferisse AWS per la maturità dei servizi serverless, l'ufficio acquisti ha imposto Azure per via di un accordo quadro globale con Microsoft che abbatte i costi del 30%.",
    "alternative_scartate": [
      { "opzione": "AWS", "motivo_scarto": "Costo superiore e mancanza di sconti corporate." }
    ],
    "decisori": ["CFO", "CTO (con riserva)"],
    "timestamp": "2026-01-10T09:00:00Z",
    "parent_id": None,
    "tags": ["budget", "corporate-policy", "cloud"]
  },
  {
    "titolo": "Revisione Database Reporting (Evoluzione)",
    "decisione_finale": "Implementazione di un mirror in PostgreSQL per i report",
    "motivazione": "La decisione originale di usare solo MongoDB (DEC-001) si è rivelata insufficiente per query analitiche complesse. Invece di migrare tutto, creiamo un flusso ETL verso Postgres.",
    "alternative_scartate": [
      { "opzione": "Migrazione totale a Postgres", "motivo_scarto": "Troppo costoso e rischioso per l'operatività corrente." }
    ],
    "decisori": ["Lead Architect", "Data Engineer"],
    "timestamp": "2026-03-15T11:00:00Z",
    "parent_id": "DEC-001", 
    "tags": ["performance", "data-architecture", "iteration"]
  },
  {
    "titolo": "Scelta UI Library - Decisione Vaga",
    "decisione_finale": "Utilizzo di Material UI",
    "motivazione": "È stata scelta perché è molto comune e piace al team.",
    "alternative_scartate": [],
    "decisori": ["Frontend Dev"],
    "timestamp": "2026-04-01T10:00:00Z",
    "parent_id": None,
    "tags": ["ui", "frontend"]
  },
  {
    "titolo": "Strategia di Sicurezza - Compromesso Rapido",
    "decisione_finale": "Rilascio in produzione senza audit di sicurezza completo",
    "motivazione": "Necessità di rispettare la scadenza del cliente X. Il rischio è accettato temporaneamente per evitare penali contrattuali, con l'impegno di fare il cleanup nel prossimo sprint.",
    "alternative_scartate": [
      { "opzione": "Rinvio del rilascio", "motivo_scarto": "Rischio legale e perdita di credibilità con il cliente chiave." }
    ],
    "decisori": ["CEO", "Product Manager"],
    "timestamp": "2026-04-12T17:00:00Z",
    "parent_id": None,
    "tags": ["risk", "deadline", "security"]
  },
  {
    "titolo": "Cambio Metodologia di Lavoro - Conflitto Interno",
    "decisione_finale": "Ritorno a Scrum puro",
    "motivazione": "Il tentativo di usare Kanban è fallito perché il team non aveva abbastanza disciplina nel gestire il flusso. Nonostante le lamentele dei senior sulla rigidità degli sprint, torniamo a Scrum per riprendere il controllo delle scadenze.",
    "alternative_scartate": [
      { "opzione": "Scrumban", "motivo_scarto": "Troppo ibrido, non ha risolto i problemi di pianificazione." }
    ],
    "decisori": ["Engineering Manager"],
    "timestamp": "2026-04-15T09:00:00Z",
    "parent_id": None,
    "tags": ["process", "management", "conflict"]
  }

]
    

    pipeline = SeedingPipeline()
    pipeline.process_gold_dataset(gold_dataset)
