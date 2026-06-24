import React, { useState, useEffect } from 'react';
import { DecisionAPI } from '../services/api';
import { X, Clock, Users, Tag, AlertCircle, ArrowLeft, Trash2 } from 'lucide-react';

export default function DecisionDetail({ id, onClose, onDelete }) {
  const [decision, setDecision] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDetails = async () => {
      try {
        setIsLoading(true);
        const { data } = await DecisionAPI.getOne(id);
        setDecision(data);
      } catch (err) {
        setError("Impossibile caricare i dettagli della decisione.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    if (id) fetchDetails();
  }, [id]);

  if (isLoading) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 backdrop-blur-sm">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
        <div className="bg-white p-6 rounded-2xl max-w-md text-center">
          <AlertCircle className="mx-auto text-red-500 mb-4" size={48} />
          <p className="text-slate-800 font-medium mb-4">{error}</p>
          <button onClick={onClose} className="bg-slate-800 text-white px-4 py-2 rounded-lg">Chiudi</button>
        </div>
      </div>
    );
  }

  if (!decision) return null;

  const handleRemove = async () => {
    if (window.confirm("Sei sicuro di voler eliminare questa Decision Card? Questa azione è irreversibile.")) {
      try {
        await DecisionAPI.delete(id);
        onDelete(); 
      } catch (err) {
        alert("Errore nell'eliminazione del documento.");
        console.error(err);
      }
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/40 backdrop-blur-sm transition-all">
      {/* Overlay per chiudere al click fuori */}
      <div className="absolute inset-0" onClick={onClose}></div>

      {/* Pannello Dettagli (Slide-over) */}
      <div className="relative w-full max-w-2xl bg-white h-full shadow-2xl overflow-y-auto animate-in slide-in-from-right duration-300">
        
        {/* Header */}
        <div className="sticky top-0 bg-white/80 backdrop-blur-md border-b p-6 flex justify-between items-center z-10">
          <button onClick={onClose} className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-500">
            <ArrowLeft size={20} />
          </button>
          
          <div className="flex items-center gap-2">
            <button 
              onClick={handleRemove}
              className="p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
              title="Elimina Decisione"
            >
              <Trash2 size={20} />
            </button>
            <button onClick={onClose} className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-500">
              <X size={20} />
            </button>
          </div>
        </div>

        <div className="p-8 space-y-8">
          {/* Sezione Titolo e Meta */}
          <section>
            <h2 className="text-3xl font-extrabold text-slate-900 mb-4 leading-tight">
              {decision.titolo}
            </h2>
            <div className="flex flex-wrap gap-4 text-xs text-slate-500 font-medium">
              <div className="flex items-center gap-1.5 bg-slate-100 px-3 py-1 rounded-full">
                <Clock size={14} />
                {new Date(decision.timestamp).toLocaleDateString('it-IT', { 
                  day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' 
                })}
              </div>
              <div className="flex items-center gap-1.5 bg-slate-100 px-3 py-1 rounded-full">
                <Users size={14} />
                {decision.decisori?.join(', ') || 'Non specificati'}
              </div>
            </div>
          </section>

          {/* Decisione Finale - Highlighted */}
          <section className="bg-blue-50 border-l-4 border-blue-600 p-6 rounded-r-xl">
            <h3 className="text-xs font-bold text-blue-700 uppercase tracking-wider mb-2">Decisione Finale</h3>
            <p className="text-lg text-slate-800 font-medium leading-relaxed">
              {decision.decisione_finale}
            </p>
          </section>

          {/* Motivazione */}
          <section className="space-y-3">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Motivazione Tecnica</h3>
            <p className="text-slate-700 leading-relaxed text-base">
              {decision.motivazione}
            </p>
          </section>

          {/* Alternative Scartate */}
          <section className="space-y-4">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Alternative Analizzate e Scartate</h3>
            <div className="grid gap-4">
              {decision.alternative_scartate && decision.alternative_scartate.length > 0 ? (
                decision.alternative_scartate.map((alt, i) => (
                  <div key={i} className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
                    <div className="flex items-center gap-2 text-sm font-bold text-slate-800">
                      <div className="w-2 h-2 bg-red-400 rounded-full"></div>
                      {alt.opzione}
                    </div>
                    <p className="text-sm text-slate-600 pl-4 italic border-l-2 border-slate-200">
                      {alt.motivo_scarto}
                    </p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-400 italic">Nessuna alternativa registrata per questa decisione.</p>
              )}
            </div>
          </section>

          {/* Tags */}
          <section className="pt-6 border-t">
            <div className="flex flex-wrap gap-2">
              {decision.tags?.map(tag => (
                <span key={tag} className="flex items-center gap-1 text-[10px] bg-slate-100 text-slate-600 px-2 py-1 rounded-md font-medium">
                    <Tag size={10} /> {tag}
                </span>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}