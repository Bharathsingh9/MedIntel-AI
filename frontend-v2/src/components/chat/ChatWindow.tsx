import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { usePatientStore } from '@/store/usePatientStore';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Bot, User, Activity } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatWindow() {
  const { patientData, predictionResult } = usePatientStore();
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am your MedIntel AI clinical consultant. I have analyzed your biomarkers. What questions do you have regarding your health score or disease risks?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      const payload = {
        message: userMsg,
        patient_state: {
          patientData,
          predictionResult
        }
      };
      
      const res = await axios.post('http://localhost:8000/api/chat', payload);
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.answer }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'assistant', content: 'System Error: Unable to reach AI Engine. Ensure your API Key is set in the backend.' }]);
    }
    setLoading(false);
  };

  const handleSuggested = (q: string) => {
    setInput(q);
  };

  return (
    <Card className="glass-card flex flex-col h-[500px]">
      <CardHeader className="border-b border-border/50 pb-3">
        <CardTitle className="flex items-center gap-2 text-primary">
          <Bot size={20} /> AI Health Consultant
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col p-4 overflow-hidden gap-4">
        <div className="flex-1 overflow-y-auto space-y-4 pr-2 pb-4">
          {messages.map((m, i) => (
            <div key={i} className={`flex gap-3 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {m.role === 'assistant' && <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary shrink-0"><Bot size={16}/></div>}
              <div className={`px-4 py-3 rounded-2xl max-w-[80%] text-sm leading-relaxed ${m.role === 'user' ? 'bg-primary text-primary-foreground rounded-tr-none' : 'bg-background/80 border border-border/50 rounded-tl-none'}`}>
                {m.content}
              </div>
              {m.role === 'user' && <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white shrink-0"><User size={16}/></div>}
            </div>
          ))}
          {loading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary shrink-0"><Bot size={16}/></div>
              <div className="px-4 py-3 rounded-2xl bg-background/80 border border-border/50 rounded-tl-none flex items-center gap-2 text-sm text-muted-foreground">
                <Activity size={16} className="animate-spin text-primary" /> Analyzing clinical context...
              </div>
            </div>
          )}
          <div ref={endOfMessagesRef} />
        </div>
        
        <div>
          <div className="flex gap-2 mb-3 overflow-x-auto pb-1 scrollbar-hide">
             <Button variant="outline" size="sm" onClick={() => handleSuggested('Why is my diabetes risk high?')} disabled={loading} className="whitespace-nowrap text-xs bg-background/50">Why is my diabetes risk high?</Button>
             <Button variant="outline" size="sm" onClick={() => handleSuggested('How can I lower my biological age?')} disabled={loading} className="whitespace-nowrap text-xs bg-background/50">How to lower biological age?</Button>
          </div>

          <form onSubmit={handleSend} className="flex gap-2">
            <Input 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              placeholder="Ask your AI consultant..." 
              className="flex-1 bg-background"
              disabled={loading}
            />
            <Button type="submit" disabled={loading || !input.trim()}><Send size={18} /></Button>
          </form>
        </div>
      </CardContent>
    </Card>
  );
}
