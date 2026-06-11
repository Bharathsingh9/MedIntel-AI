import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [formData, setFormData] = useState({
    age: 55, gender: 'Male', bmi: 31.5, systolic_bp: 145, fasting_glucose: 130,
    cholesterol_total: 220, ldl: 150, hdl: 35, hba1c: 6.2, triglycerides: 180,
    smoking_status: 'Current', alcohol_consumption: 'Regular', physical_activity_level: 'Sedentary',
    sleep_hours: 5, stress_level: 'High'
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    // parse numbers where appropriate
    const isNum = ['age', 'bmi', 'systolic_bp', 'fasting_glucose', 'cholesterol_total', 'ldl', 'hdl', 'hba1c', 'triglycerides', 'sleep_hours'].includes(name);
    setFormData(prev => ({ ...prev, [name]: isNum ? Number(value) : value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Assuming FastAPI runs on 8000
      const res = await axios.post('http://localhost:8000/api/predict', formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert('Error fetching prediction. Is the FastAPI server running on port 8000?');
    }
    setLoading(false);
  };

  const getScoreClass = (score) => {
    if (score <= 50) return 'score-critical';
    if (score <= 80) return 'score-warning';
    return 'score-healthy';
  };

  return (
    <div className="app-container">
      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h1>MedIntel AI</h1>
        <p className="text-muted">Explainable Multi-Disease Prediction & Health Analytics Platform</p>
      </div>

      <div className={result ? 'grid-2' : ''}>
        {/* Input Form */}
        <div className="glass-card animate-in">
          <h2>Patient Profile</h2>
          <form onSubmit={handleSubmit}>
            <div className="grid-2">
              <div className="input-group"><label>Age</label><input type="number" name="age" value={formData.age} onChange={handleChange} /></div>
              <div className="input-group"><label>BMI</label><input type="number" step="0.1" name="bmi" value={formData.bmi} onChange={handleChange} /></div>
              <div className="input-group"><label>Fasting Glucose</label><input type="number" name="fasting_glucose" value={formData.fasting_glucose} onChange={handleChange} /></div>
              <div className="input-group"><label>Systolic BP</label><input type="number" name="systolic_bp" value={formData.systolic_bp} onChange={handleChange} /></div>
              
              <div className="input-group">
                <label>Smoking Status</label>
                <select name="smoking_status" value={formData.smoking_status} onChange={handleChange}>
                  <option value="Never">Never</option><option value="Former">Former</option><option value="Current">Current</option>
                </select>
              </div>
              <div className="input-group">
                <label>Physical Activity</label>
                <select name="physical_activity_level" value={formData.physical_activity_level} onChange={handleChange}>
                  <option value="Sedentary">Sedentary</option><option value="Light">Light</option><option value="Active">Active</option>
                </select>
              </div>
            </div>
            
            <div className="input-group" style={{marginTop: '16px'}}>
               <p className="text-muted" style={{fontSize: '0.85rem'}}>Advanced biomarkers (Lipids, HbA1c, etc.) are pre-filled in state for demonstration.</p>
            </div>

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Analyzing Neural Pathways...' : 'Generate Clinical Intelligence'}
            </button>
          </form>
        </div>

        {/* Results Dashboard */}
        {result && (
          <div className="glass-card animate-in" style={{ animationDelay: '0.2s' }}>
            <h2>Health Intelligence Report</h2>
            <div className={`score-circle ${getScoreClass(result.overall_health_score)}`}>
              {result.overall_health_score}
            </div>
            <h3 style={{ textAlign: 'center', margin: 0 }}>{result.health_category}</h3>
            
            <div className="grid-3" style={{ marginTop: '30px' }}>
              <div className="glass-card" style={{ padding: '16px', background: 'rgba(0,0,0,0.2)' }}>
                <p className="text-muted" style={{ margin: 0 }}>Cardio Score</p>
                <h2>{result.cardiovascular_score}/100</h2>
              </div>
              <div className="glass-card" style={{ padding: '16px', background: 'rgba(0,0,0,0.2)' }}>
                <p className="text-muted" style={{ margin: 0 }}>Metabolic Score</p>
                <h2>{result.metabolic_score}/100</h2>
              </div>
              <div className="glass-card" style={{ padding: '16px', background: 'rgba(0,0,0,0.2)' }}>
                <p className="text-muted" style={{ margin: 0 }}>Biological Age</p>
                <h2>{result.biological_age} yrs</h2>
              </div>
            </div>

            <h3 style={{ marginTop: '30px' }}>Clinical Recommendations</h3>
            <ul style={{ color: 'var(--text-muted)', lineHeight: '1.6' }}>
              {result.recommendations.map((rec, i) => <li key={i}>{rec}</li>)}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
