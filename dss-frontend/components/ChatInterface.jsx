import React, { useState, useRef, useEffect } from 'react';
import { DecisionAPI } from '../services/api';
import { Send, Bot, User, BookOpen } from 'lucide-react';

export default function ChatInterface({ onSourceClick }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const { data } = await DecisionAPI.ask(input);
      setMessages(prev => [...prev, { 
        role: 'bot', 
        text: data.answer, 
        sources: data.sources 
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', text: "Errore di connessione al cervello AI.", isError: true }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-slate-50 rounded-xl border border-slate-200 shadow-sm">
      <div className="p-4 border-b bg-white rounded-t-xl flex items-center gap-2">
        <Bot className="text-blue-600" size={20} />
        <h3 className="font-semibold text-slate-800">AI Memory Assistant</h3>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-2xl ${
              msg.role === 'user' 
              ? 'bg-blue-600 text-white rounded-tr-none' 
              : 'bg-white text-slate-800 border border-slate-200 rounded-tl-none shadow-sm'
            }`}>
              <div className="flex items-center gap-2 mb-1 opacity-70 text-xs font-bold uppercase">
                {msg.role === 'user' ? <User size={12}/> : <Bot size={12}/>}
                {msg.role === 'user' ? 'You' : 'DecisionOS AI'}
              </div>
              <p className="text-sm leading-relaxed">{msg.text}</p>
              
              {msg.sources && (
                <div className="mt-3 pt-2 border-t border-slate-100 flex flex-wrap gap-2">
                  {msg.sources.map(id => (
                    <button 
                      key={id} 
                      onClick={() => onSourceClick(id)}
                      className="text-[10px] bg-blue-50 text-blue-600 px-2 py-1 rounded border border-blue-100 hover:bg-blue-100 transition-colors flex items-center gap-1"
                    >
                      <BookOpen size={10} /> Source {id.slice(-4)}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={scrollRef} />
      </div>

      <div className="p-4 bg-white border-t rounded-b-xl flex gap-2">
        <input 
          className="flex-1 p-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Chiedi alla memoria aziendale..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button 
          onClick={handleSend}
          disabled={isLoading}
          className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 disabled:bg-slate-300 transition-colors"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}