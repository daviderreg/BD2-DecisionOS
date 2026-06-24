"use client";
import React, { useState, useCallback } from 'react';
import ChatInterface from '../components/ChatInterface';
import DecisionGrid from '../components/DecisionGrid';
import DecisionDetail from '../components/DecisionDetail';
import DecisionModal from '../components/DecisionModal';
import { DecisionAPI } from '../services/api';

export default function DSSDashboard() {
  const [selectedDecisionId, setSelectedDecisionId] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [decisionToEdit, setDecisionToEdit] = useState(null);
  const [refreshCount, setRefreshCount] = useState(0);
  const [semanticResults, setSemanticResults] = useState(null);

  // Funzione per ricaricare i dati (passata alla Grid e al Modal)
  const refreshData = useCallback(() => {
    setRefreshCount(prev => prev + 1);
    setSemanticResults(null);
  }, []);

  const handleOpenCreate = () => {
    setDecisionToEdit(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (decision) => {
    setDecisionToEdit(decision);
    setIsModalOpen(true);
  };

  return (
    <main className="min-h-screen bg-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8 flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-extrabold text-slate-900">DecisionOS</h1>
            <p className="text-slate-500">Corporate Memory & RAG Intelligence</p>
          </div>
          <div className="text-right text-xs text-slate-400 font-mono">v3.0.0 - Production Ready</div>
        </header>

        <div className="grid grid-cols-12 gap-6">
          {/* Colonna Sinistra: Gestione Decisioni */}
          <div className="col-span-12 lg:col-span-7 space-y-6">
             <DecisionGrid 
               key={refreshCount}
               onSelectDecision={(id) => setSelectedDecisionId(id)} 
               onCreateClick={handleOpenCreate}
               onEditClick={handleOpenEdit}
               onSemanticSearch={async (query) => {
                try {
                  const { data } = await DecisionAPI.ask(query);
                  // Data contiene { answer: "...", sources: ["id1", "id2"] }
                  setSemanticResults(data.sources);
                } catch (e) {
                  console.error("Errore ricerca semantica:", e);
                }
              }}
              semanticResults={semanticResults}
              onClearSearch={() => setSemanticResults(null)}
            />
            
             {selectedDecisionId && (
               <DecisionDetail 
                 id={selectedDecisionId} 
                 onClose={() => setSelectedDecisionId(null)} 
                 onDelete={() => {
                   setSelectedDecisionId(null);
                   refreshData();
                 }} 
               />
             )}
          </div>

          {/* Colonna Destra: AI Interface */}
          <div className="col-span-12 lg:col-span-5">
            <ChatInterface onSourceClick={(id) => setSelectedDecisionId(id)} />
          </div>
        </div>
      </div>

       <DecisionModal 
         isOpen={isModalOpen}
         decisionToEdit={decisionToEdit}
         onClose={() => setIsModalOpen(false)} 
         onRefresh={refreshData} 
       />
    </main>
  );
}