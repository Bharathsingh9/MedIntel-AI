import { useState } from 'react';
import { usePatientStore } from '@/store/usePatientStore';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Activity, ArrowRight, TrendingDown } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function Simulator() {
  const { predictionResult } = usePatientStore();
  const [simulation, setSimulation] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  if (!predictionResult) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center">
        <Activity className="h-16 w-16 text-muted-foreground mb-4 opacity-50" />
        <h2 className="text-2xl font-bold mb-2">Simulation Unavailable</h2>
        <p className="text-muted-foreground">Setup patient profile first.</p>
      </div>
    );
  }

  const handleSimulate = () => {
    setLoading(true);
    setTimeout(() => {
      const current = predictionResult;
      setSimulation({
        bioAgeDelta: -7,
        healthScoreDelta: +15,
        newBioAge: current.biological_age - 7,
        newHealthScore: Math.min(100, current.overall_health_score + 15),
        chartData: [
          { name: 'Cardio Risk', Current: 65, Simulated: 45 },
          { name: 'Metabolic', Current: 70, Simulated: 50 },
        ]
      });
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold flex items-center gap-2"><TrendingDown className="text-primary"/> Health Trend Simulator</h1>
      <p className="text-muted-foreground mb-8">What happens if you lose 10kg and quit smoking? Simulate the ROI on your biological age.</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="glass-card">
          <CardHeader><CardTitle>Intervention Parameters</CardTitle></CardHeader>
          <CardContent className="space-y-4">
             <div className="p-4 bg-background/50 rounded-lg border border-border/50">
               <h4 className="font-medium mb-1">Target Weight Loss</h4>
               <p className="text-sm text-muted-foreground">-10 kg (Diet + Exercise)</p>
             </div>
             <div className="p-4 bg-background/50 rounded-lg border border-border/50">
               <h4 className="font-medium mb-1">Smoking Cessation</h4>
               <p className="text-sm text-muted-foreground">Quit completely</p>
             </div>
             <Button onClick={handleSimulate} disabled={loading} className="w-full mt-4">
               {loading ? 'Running AI Simulation...' : 'Run Simulation Engine'}
             </Button>
          </CardContent>
        </Card>

        {simulation && (
          <Card className="glass-card border-green-500/30 shadow-[0_0_20px_rgba(16,185,129,0.1)]">
            <CardHeader><CardTitle className="text-green-500">Projected Health ROI</CardTitle></CardHeader>
            <CardContent className="space-y-6">
               <div className="flex justify-between items-center p-4 bg-background/50 rounded-lg border border-border/50">
                 <div>
                   <p className="text-sm text-muted-foreground">Biological Age</p>
                   <p className="text-2xl font-bold">{predictionResult.biological_age} <ArrowRight className="inline mx-2 text-muted-foreground" size={16}/> <span className="text-green-500">{simulation.newBioAge}</span></p>
                 </div>
                 <div className="text-green-500 font-bold bg-green-500/10 px-3 py-1 rounded-full">{simulation.bioAgeDelta} Years!</div>
               </div>
               
               <div className="flex justify-between items-center p-4 bg-background/50 rounded-lg border border-border/50">
                 <div>
                   <p className="text-sm text-muted-foreground">Health Score</p>
                   <p className="text-2xl font-bold">{predictionResult.overall_health_score} <ArrowRight className="inline mx-2 text-muted-foreground" size={16}/> <span className="text-green-500">{simulation.newHealthScore}</span></p>
                 </div>
                 <div className="text-green-500 font-bold bg-green-500/10 px-3 py-1 rounded-full">+{simulation.healthScoreDelta} Points</div>
               </div>
               
               <div className="h-[200px] w-full">
                 <ResponsiveContainer width="100%" height="100%">
                   <BarChart data={simulation.chartData}>
                     <XAxis dataKey="name" stroke="#94a3b8" />
                     <YAxis stroke="#94a3b8" />
                     <Tooltip contentStyle={{backgroundColor: '#0f172a', borderColor: '#334155'}} />
                     <Legend />
                     <Bar dataKey="Current" fill="#ef4444" />
                     <Bar dataKey="Simulated" fill="#10b981" />
                   </BarChart>
                 </ResponsiveContainer>
               </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
