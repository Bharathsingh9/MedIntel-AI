import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Activity, ShieldCheck, Zap } from 'lucide-react';

export default function Landing() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="p-6 border-b border-border/50 bg-background/80 backdrop-blur-md flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Activity className="text-primary" />
          <span className="font-bold text-xl">MedIntel AI</span>
        </div>
        <Link to="/app"><Button variant="outline">Launch Platform</Button></Link>
      </header>
      
      <main className="flex-1 flex flex-col items-center justify-center p-8 text-center">
        <h1 className="text-6xl md:text-8xl font-black mb-6 tracking-tight bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 text-transparent bg-clip-text">
          Predict. Explain. Prevent.
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mb-10">
          The next-generation healthcare analytics platform. Powered by explainable AI to detect multi-disease risks before they become critical.
        </p>
        <Link to="/app">
          <Button size="lg" className="text-lg px-8 py-6 rounded-full shadow-[0_0_40px_rgba(59,130,246,0.5)]">
            Start Clinical Assessment
          </Button>
        </Link>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24 max-w-5xl">
          <div className="glass-card p-6 flex flex-col items-center">
            <Activity className="h-12 w-12 text-blue-500 mb-4" />
            <h3 className="text-xl font-bold mb-2">Multi-Disease Models</h3>
            <p className="text-muted-foreground">Simultaneously predict Diabetes, Heart Disease, Stroke, and Kidney risks.</p>
          </div>
          <div className="glass-card p-6 flex flex-col items-center">
            <Zap className="h-12 w-12 text-purple-500 mb-4" />
            <h3 className="text-xl font-bold mb-2">SHAP Explainability</h3>
            <p className="text-muted-foreground">Understand the "Why" behind every ML prediction with local feature importance.</p>
          </div>
          <div className="glass-card p-6 flex flex-col items-center">
            <ShieldCheck className="h-12 w-12 text-green-500 mb-4" />
            <h3 className="text-xl font-bold mb-2">Trend Simulation</h3>
            <p className="text-muted-foreground">Simulate lifestyle interventions and instantly visualize the ROI on biological age.</p>
          </div>
        </div>
      </main>
    </div>
  );
}
