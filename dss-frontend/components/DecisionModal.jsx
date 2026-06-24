import React, { useState } from 'react';
import { DecisionAPI } from '../services/api';
import { X, Plus, Trash2 } from 'lucide-react';

export default function DecisionModal({ onClose, onRefresh }) {
  const [form, setForm] = useState({
    titolo: '', 
    decisione_finale: '', 
    motivazione: '', 
    tags: '', 
    decisori: '',
    alternatives: []
  });

  const addAlternative = () => {
    setForm({ ...form, alternatives: [...form.alternatives, { opzione: '', motivo_scarto: '' }] });
  };

  const updateAlternative = (index, field, value) => {
    const newAlts = [...form.alternatives];
    newAlts[index][field] = value;
    setForm({ ...form, alternatives: newAlts });
  };

  const removeAlternative = (index) => {
    setForm({ ...form, alternatives: form.alternatives.filter((_, i) => i !== index) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = {
      titolo: form.titolo,
      decisione_finale: form.decisione_finale,
      motivazione: form.motivazione,
      tags: form.tags.split(',').map(t => t.trim()).filter(t => t !== ""),
      decisori: form.decisori.split(',').map(d => d.trim()).filter(d => d !== ""),
      alternative_scartate: form.alternatives
    };
    
    try {
      await DecisionAPI.create(data);
      onRefresh();
      onClose();
    } catch (error) {
      const errorMessage = error.response?.data?.detail 
        ? typeof error.response.data.detail === 'string' 
          ? error.response.data.detail 
          : JSON.stringify(error.response.data.detail)
        : error.message || "Errore durante l'inserimento della Decision Card.";
      alert(`Errore: ${errorMessage}`);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex justify-center items-center z-[60] p-4">
      <div className="bg-white rounded-2xl p-6 w-full max-w-2xl shadow-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-slate-800">Nuova Decision Card</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 transition-colors">
            <X size={20} />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase">Titolo</label>
              <input className="w-full p-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500" 
                placeholder="E.g. Scelta Framework Frontend" 
                onChange={e => setForm({...form, titolo: e.target.value})} required />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase">Decisori</label>
              <input className="w-full p-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500" 
                placeholder="Nome1, Nome2..." 
                onChange={e => setForm({...form, decisori: e.target.value})} />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase">Motivazione / Problema</label>
            <textarea className="w-full p-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500 h-24" 
              placeholder="Descrivi il problema e il contesto..." 
              onChange={e => setForm({...form, motivazione: e.target.value})} required />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase">Decisione Finale</label>
            <textarea className="w-full p-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500 h-24" 
              placeholder="Qual è la soluzione adottata?" 
              onChange={e => setForm({...form, decisione_finale: e.target.value})} required />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase">Tags</label>
            <input className="w-full p-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500" 
              placeholder="architettura, frontend, performance..." 
              onChange={e => setForm({...form, tags: e.target.value})} />
          </div>

          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <label className="text-xs font-bold text-slate-500 uppercase">Alternative Scartate</label>
              <button type="button" onClick={addAlternative} className="text-blue-600 text-xs flex items-center gap-1 hover:underline">
                <Plus size={12} /> Aggiungi Opzione
              </button>
            </div>
            
            <div className="space-y-3">
              {form.alternatives.map((alt, i) => (
                <div key={i} className="flex gap-2 p-3 bg-slate-50 rounded-lg border border-slate-200 relative group">
                  <input 
                    className="flex-1 p-2 text-xs border rounded bg-white outline-none focus:ring-1 focus:ring-blue-400" 
                    placeholder="Opzione scartata" 
                    value={alt.opzione}
                    onChange={e => updateAlternative(i, 'opzione', e.target.value)}
                  />
                  <input 
                    className="flex-1 p-2 text-xs border rounded bg-white outline-none focus:ring-1 focus:ring-blue-400" 
                    placeholder="Motivo scarto" 
                    value={alt.motivo_scarto}
                    onChange={e => updateAlternative(i, 'motivo_scarto', e.target.value)}
                  />
                  <button type="button" onClick={() => removeAlternative(i)} className="text-slate-300 hover:text-red-500 transition-colors">
                    <Trash2 size={16} />
                  </button>
                </div>
              ))}
              {form.alternatives.length === 0 && <p className="text-xs text-slate-400 italic text-center py-2">Nessuna alternativa aggiunta.</p>}
            </div>
          </div>

          <button type="submit" className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition-all shadow-lg">
            Salva Decision Card
          </button>
        </form>
      </div>
    </div>
  );
}