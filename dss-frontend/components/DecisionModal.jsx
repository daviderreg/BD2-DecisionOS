import React, { useState, useEffect } from 'react';
import { DecisionAPI } from '../services/api';
import { X, Plus, Trash2, Loader2 } from 'lucide-react';

export default function DecisionModal({ isOpen, onClose, onRefresh, decisionToEdit = null }) {
  const [formData, setFormData] = useState({
    titolo: '', 
    decisione_finale: '', 
    motivazione: '', 
    tags: '', 
    decisori: '',
    alternative_scartate: []
  });
  const [isLoading, setIsLoading] = useState(false);

  // Sincronizzazione quando si apre in modalità Edit
  useEffect(() => {
    if (isOpen) {
      if (decisionToEdit) {
        setFormData({
          titolo: decisionToEdit.titolo,
          decisione_finale: decisionToEdit.decisione_finale,
          motivazione: decisionToEdit.motivazione,
          tags: decisionToEdit.tags?.join(', ') || '',
          decisori: decisionToEdit.decisori?.join(', ') || '',
          alternative_scartate: decisionToEdit.alternative_scartate || []
        });
      } else {
        // Reset per nuova creazione
        setFormData({
          titolo: '', decisione_finale: '', motivazione: '', 
          tags: '', decisori: '', alternative_scartate: [{ opzione: '', motivo_scarto: '' }]
        });
      }
    }
  }, [decisionToEdit, isOpen]);

  if (!isOpen) return null;

  const handleAddAlternative = () => {
    setFormData({ ...formData, alternative_scartate: [...formData.alternative_scartate, { opzione: '', motivo_scarto: '' }] });
  };

  const updateAlternative = (index, field, value) => {
    const newAlts = [...formData.alternative_scartate];
    newAlts[index][field] = value;
    setFormData({ ...formData, alternative_scartate: newAlts });
  };

  const removeAlternative = (index) => {
    setFormData({ ...formData, alternative_scartate: formData.alternative_scartate.filter((_, i) => i !== index) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validazione Client-Side rigorosa
    if (formData.titolo.length < 3 || formData.decisione_finale.length < 3 || formData.motivazione.length < 3) {
      alert("Errore: Titolo, Decisione e Motivazione sono campi obbligatori (min 3 caratteri).");
      return;
    }

    setIsLoading(true);
    try {
      const finalData = {
        ...formData,
        tags: formData.tags.split(',').map(t => t.trim()).filter(t => t !== ""),
        decisori: formData.decisori.split(',').map(d => d.trim()).filter(d => d !== ""),
      };

      if (decisionToEdit) {
        // Update Flow: PUT /decisions/{id}
        await DecisionAPI.update(decisionToEdit._id, finalData);
      } else {
        // Create Flow: POST /decisions
        await DecisionAPI.create(finalData);
      }

      await onRefresh(); // Sincronizzazione Grid
      onClose();
    } catch (error) {
      const msg = error.response?.data?.detail || "Errore durante il salvataggio della Decision Card.";
      alert(`Errore: ${msg}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div className="bg-white w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
        <div className="p-6 border-b flex justify-between items-center bg-slate-50">
          <h3 className="text-xl font-bold text-slate-800">
            {decisionToEdit ? 'Aggiorna Decisione' : 'Nuova Decision Card'}
          </h3>
          <button onClick={onClose} className="p-2 hover:bg-slate-200 rounded-full transition-colors">
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4 max-h-[80vh] overflow-y-auto">
          <div className="grid grid-cols-1 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Titolo *</label>
              <input required className="w-full p-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500" 
                value={formData.titolo} onChange={e => setFormData({...formData, titolo: e.target.value})} />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Decisione Finale *</label>
              <textarea required className="w-full p-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500" rows="3"
                value={formData.decisione_finale} onChange={e => setFormData({...formData, decisione_finale: e.target.value})} />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Motivazione *</label>
              <textarea required className="w-full p-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500" rows="3"
                value={formData.motivazione} onChange={e => setFormData({...formData, motivazione: e.target.value})} />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Decisori (csv)</label>
                <input className="w-full p-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500" 
                  value={formData.decisori} onChange={e => setFormData({...formData, decisori: e.target.value})} />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Tags (csv)</label>
                <input className="w-full p-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500" 
                  value={formData.tags} onChange={e => setFormData({...formData, tags: e.target.value})} />
              </div>
            </div>
            <div className="pt-4">
              <div className="flex justify-between items-center mb-2">
                <label className="block text-xs font-bold text-slate-500 uppercase">Alternative Scartate</label>
                <button type="button" onClick={handleAddAlternative} className="text-blue-600 hover:text-blue-800 flex items-center gap-1 text-xs font-bold">
                  <Plus size={14} /> Aggiungi
                </button>
              </div>
              {formData.alternative_scartate.map((alt, i) => (
                <div key={i} className="flex gap-2 mb-2">
                  <input placeholder="Opzione" className="flex-1 p-2 border rounded-lg text-sm" 
                    value={alt.opzione} onChange={e => updateAlternative(i, 'opzione', e.target.value)} />
                  <input placeholder="Motivo scarto" className="flex-1 p-2 border rounded-lg text-sm" 
                    value={alt.motivo_scarto} onChange={e => updateAlternative(i, 'motivo_scarto', e.target.value)} />
                  <button type="button" onClick={() => removeAlternative(i)} className="p-2 text-red-500 hover:bg-red-50 rounded-lg">
                    <Trash2 size={16} />
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-6 flex justify-end gap-3">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded-lg transition-colors">Annulla</button>
            <button type="submit" disabled={isLoading} className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-slate-300 flex items-center gap-2 transition-colors">
              {isLoading && <Loader2 className="animate-spin" size={16} />}
              {decisionToEdit ? 'Aggiorna' : 'Salva Decisione'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
