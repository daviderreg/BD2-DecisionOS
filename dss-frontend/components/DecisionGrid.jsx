import React, { useState, useEffect } from 'react';
import { DecisionAPI } from '../services/api';
import { Plus, Search, Edit3, Loader2 } from 'lucide-react';

export default function DecisionGrid({ onSelectDecision, onCreateClick, onEditClick, onSemanticSearch, semanticResults, onClearSearch }) {
  const [decisions, setDecisions] = useState([]);
  const [filter, setFilter] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  const loadDecisions = async () => {
    try {
      const { data } = await DecisionAPI.getAll();
      console.log("DEBUG: Decisioni caricate dal server:", data);
      setDecisions(data);
    } catch (error) {
      console.error("Errore nel caricamento delle decisioni:", error);
    }
  };

  useEffect(() => { 
    loadDecisions(); 
  }, []);

  const handleKeyDown = async (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (filter.trim()) {
        setIsSearching(true);
        // Se l'app ha implementato onSemanticSearch, lo chiamiamo
        if (onSemanticSearch) {
          await onSemanticSearch(filter);
        }
        setIsSearching(false);
      }
    }
  };

  // Logica di visualizzazione: Priorità ai risultati semantici se presenti
  const filtered = React.useMemo(() => {
    console.log("DEBUG: Eseguo filtraggio. Filter text:", filter, "Semantic results:", semanticResults, "Total decisions in state:", decisions.length);
    
    if (semanticResults && semanticResults.length > 0) {
      const results = decisions.filter(d => semanticResults.includes(d._id));
      console.log("DEBUG: Risultati filtrati per ID semantici:", results);
      return results;
    }

    if (!filter) return decisions;

    const searchTerm = filter.toLowerCase();
    const results = decisions.filter(d => {
      const titleMatch = d.titolo?.toLowerCase().includes(searchTerm);
      const decisionMatch = d.decisione_finale?.toLowerCase().includes(searchTerm);
      const motivationMatch = d.motivazione?.toLowerCase().includes(searchTerm);
      const tagMatch = d.tags?.some(t => t?.toLowerCase().includes(searchTerm));
      return titleMatch || decisionMatch || motivationMatch || tagMatch;
    });
    console.log("DEBUG: Risultati filtrati per keyword:", results);
    return results;
  }, [decisions, filter, semanticResults]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div className="relative w-full max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <input 
            className="w-full pl-10 pr-4 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-white"
            placeholder="Cerca per titolo o tag... (Premi INVIO per AI Search)"
            value={filter}
            onChange={(e) => {
              setFilter(e.target.value);
              if (onClearSearch) onClearSearch();
            }}
            onKeyDown={handleKeyDown}
          />
          {isSearching && <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 animate-spin text-blue-500" size={18} />}
        </div>
        <button 
          onClick={onCreateClick}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 hover:bg-blue-700 transition-all shadow-sm active:scale-95"
        >
          <Plus size={18} /> Nuova Decisione
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.length > 0 ? (
          filtered.map(doc => (
            <div 
              key={doc._id} 
              onClick={() => onSelectDecision(doc._id)}
              className="p-4 bg-white border border-slate-200 rounded-xl hover:border-blue-400 cursor-pointer transition-all shadow-sm group"
            >
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-bold text-slate-800 group-hover:text-blue-600 transition-colors line-clamp-1">{doc.titolo}</h4>
                <button 
                  onClick={(e) => { e.stopPropagation(); onEditClick(doc); }}
                  className="p-1 hover:bg-slate-100 rounded text-slate-400 hover:text-blue-600 transition-colors"
                >
                  <Edit3 size={14} />
                </button>
              </div>
              <p className="text-xs text-slate-500 line-clamp-2 mb-3">{doc.motivazione}</p>
              <div className="flex flex-wrap gap-1">
                {doc.tags?.map(t => (
                  <span key={t} className="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">{t}</span>
                )) || <span className="text-[10px] text-slate-400">No tags</span>}
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full py-10 text-center text-slate-400 italic text-sm">
            Nessuna decisione trovata per "{filter}"
          </div>
        )}
      </div>
    </div>
  );
}