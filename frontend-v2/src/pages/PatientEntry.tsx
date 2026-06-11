import { useState } from 'react';
import axios from 'axios';
import { usePatientStore } from '@/store/usePatientStore';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useNavigate } from 'react-router-dom';
import { Activity } from 'lucide-react';

export default function PatientEntry() {
  const { patientData, setPatientData, setPredictionResult } = usePatientStore();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    const isNum = ['age', 'bmi', 'systolic_bp', 'fasting_glucose', 'cholesterol_total', 'ldl', 'hdl', 'hba1c', 'triglycerides', 'sleep_hours'].includes(name);
    setPatientData({ [name]: isNum ? Number(value) : value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/api/predict', patientData);
      setPredictionResult(res.data);
      navigate('/app');
    } catch (err) {
      console.error(err);
      alert('Error connecting to ML Engine. Is FastAPI running on port 8000?');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Patient Profile Setup</h1>
        <p className="text-muted-foreground">Enter clinical biomarkers to run the prediction engine.</p>
      </div>

      <Card className="glass-card border-none">
        <CardHeader>
          <CardTitle>Vitals & Labs</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2"><label className="text-sm">Age</label><Input type="number" name="age" value={patientData.age} onChange={handleChange} /></div>
              <div className="space-y-2"><label className="text-sm">BMI</label><Input type="number" step="0.1" name="bmi" value={patientData.bmi} onChange={handleChange} /></div>
              <div className="space-y-2"><label className="text-sm">Systolic BP</label><Input type="number" name="systolic_bp" value={patientData.systolic_bp} onChange={handleChange} /></div>
              <div className="space-y-2"><label className="text-sm">Fasting Glucose</label><Input type="number" name="fasting_glucose" value={patientData.fasting_glucose} onChange={handleChange} /></div>
              <div className="space-y-2"><label className="text-sm">Total Cholesterol</label><Input type="number" name="cholesterol_total" value={patientData.cholesterol_total} onChange={handleChange} /></div>
              <div className="space-y-2"><label className="text-sm">HbA1c</label><Input type="number" step="0.1" name="hba1c" value={patientData.hba1c} onChange={handleChange} /></div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-border/50">
              <div className="space-y-2">
                <label className="text-sm">Smoking Status</label>
                <select name="smoking_status" value={patientData.smoking_status} onChange={handleChange} className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors text-white outline-none">
                  <option value="Never">Never</option>
                  <option value="Former">Former</option>
                  <option value="Current">Current</option>
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-sm">Physical Activity</label>
                <select name="physical_activity_level" value={patientData.physical_activity_level} onChange={handleChange} className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors text-white outline-none">
                  <option value="Sedentary">Sedentary</option>
                  <option value="Light">Light</option>
                  <option value="Active">Active</option>
                </select>
              </div>
            </div>

            <Button type="submit" size="lg" className="w-full" disabled={loading}>
              {loading ? <span className="flex items-center gap-2"><Activity className="animate-spin"/> Analyzing...</span> : 'Generate Intelligence Report'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
