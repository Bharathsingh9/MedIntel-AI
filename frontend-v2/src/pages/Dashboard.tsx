import { usePatientStore } from '@/store/usePatientStore';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Activity, Heart, ShieldAlert, Zap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import ChatWindow from '@/components/chat/ChatWindow';

export default function Dashboard() {
  const { predictionResult } = usePatientStore();
  const navigate = useNavigate();

  if (!predictionResult) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center">
        <Activity className="h-16 w-16 text-muted-foreground mb-4 opacity-50" />
        <h2 className="text-2xl font-bold mb-2">No Active Patient Data</h2>
        <p className="text-muted-foreground mb-6">Please input patient biomarkers to generate the dashboard.</p>
        <Button onClick={() => navigate('/app/patient')}>Setup Patient Profile</Button>
      </div>
    );
  }

  const res = predictionResult;
  const isCritical = res.overall_health_score <= 50;

  const riskData = [
    { name: 'Diabetes', value: res.diabetes_risk, color: '#3b82f6' },
    { name: 'Heart', value: res.heart_risk, color: '#ef4444' },
    { name: 'Stroke', value: res.stroke_risk, color: '#8b5cf6' },
    { name: 'Kidney', value: res.kidney_risk, color: '#10b981' },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Health Intelligence Dashboard</h1>
      
      {/* Top Level KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className={`glass-card ${isCritical ? 'border-destructive/50 shadow-[0_0_30px_rgba(239,68,68,0.2)]' : 'border-primary/30'}`}>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-muted-foreground flex items-center justify-between">Overall Health <Heart size={16}/></CardTitle></CardHeader>
          <CardContent>
            <div className={`text-4xl font-black ${isCritical ? 'text-destructive' : 'text-primary'}`}>{res.overall_health_score}/100</div>
            <p className="text-sm mt-1">{res.health_category}</p>
          </CardContent>
        </Card>
        
        <Card className="glass-card">
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-muted-foreground flex items-center justify-between">Bio Age <Activity size={16}/></CardTitle></CardHeader>
          <CardContent>
            <div className="text-4xl font-black">{res.biological_age}</div>
            <p className="text-sm mt-1 text-muted-foreground">Estimated Years</p>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-muted-foreground flex items-center justify-between">Cardio Score <Zap size={16}/></CardTitle></CardHeader>
          <CardContent>
            <div className="text-4xl font-black">{res.cardiovascular_score}</div>
            <p className="text-sm mt-1 text-muted-foreground">0-100 Scale</p>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-muted-foreground flex items-center justify-between">Metabolic Score <Activity size={16}/></CardTitle></CardHeader>
          <CardContent>
            <div className="text-4xl font-black">{res.metabolic_score}</div>
            <p className="text-sm mt-1 text-muted-foreground">0-100 Scale</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        {/* ML Risk Probabilities */}
        <Card className="glass-card lg:col-span-2">
          <CardHeader><CardTitle>Multi-Disease Risk Probabilities</CardTitle></CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={riskData} innerRadius={80} outerRadius={110} paddingAngle={5} dataKey="value" label={({name, value}) => `${name}: ${value}%`}>
                  {riskData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.color} />)}
                </Pie>
                <Tooltip contentStyle={{backgroundColor: '#0f172a', borderColor: '#334155'}} />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Alerts & Recs */}
        <div className="space-y-6">
          <Card className="glass-card border-destructive/30">
            <CardHeader><CardTitle className="flex items-center gap-2"><ShieldAlert className="text-destructive"/> Clinical Alerts</CardTitle></CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {res.alerts.map((a, i) => (
                  <li key={i} className="text-sm p-3 bg-destructive/10 text-destructive rounded-lg border border-destructive/20">{a}</li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader><CardTitle>AI Recommendations</CardTitle></CardHeader>
            <CardContent>
              <ul className="space-y-3 list-disc pl-4 text-sm text-muted-foreground">
                {res.recommendations.map((r, i) => <li key={i}>{r}</li>)}
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
      
      {/* Explainability Section */}
      <Card className="glass-card mt-6">
          <CardHeader><CardTitle>SHAP Explainability Insights</CardTitle></CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(res.shap_explanations).map(([disease, explanation]: any, i) => (
                <div key={i} className="p-4 bg-background/50 rounded-lg border border-border/50">
                   <h4 className="font-bold capitalize mb-2">{disease} Risk Drivers</h4>
                   <p className="text-sm text-muted-foreground mb-3">{explanation.insight}</p>
                   <div className="flex gap-2 flex-wrap">
                     {explanation.top_drivers?.map((d:string, j:number) => (
                       <span key={j} className="px-2 py-1 bg-primary/20 text-primary text-xs rounded-full">{d}</span>
                     ))}
                   </div>
                </div>
              ))}
            </div>
          </CardContent>
      </Card>

      {/* AI Assistant Chat Section */}
      <div className="mt-6 grid grid-cols-1">
        <ChatWindow />
      </div>
    </div>
  );
}
