import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import PatientEntry from './pages/PatientEntry';
import Simulator from './pages/Simulator';
import Report from './pages/Report';
import { Activity, LayoutDashboard, UserSquare2, FileText, BarChart3 } from 'lucide-react';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/app/*" element={
          <div className="flex h-screen overflow-hidden">
            <nav className="w-64 border-r border-border/50 bg-card/30 backdrop-blur-xl p-4 flex flex-col gap-4">
              <div className="flex items-center gap-2 mb-8 px-2">
                <Activity className="text-primary" />
                <span className="font-bold text-xl tracking-tight text-white">MedIntel AI</span>
              </div>
              <Link to="/app" title="Dashboard" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors">
                <LayoutDashboard size={18} /> Dashboard
              </Link>
              <Link to="/app/patient" title="Patient Profile" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors">
                <UserSquare2 size={18} /> Patient Profile
              </Link>
              <Link to="/app/simulator" title="Trend Simulator" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors">
                <BarChart3 size={18} /> Trend Simulator
              </Link>
              <Link to="/app/report" title="Reports" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors">
                <FileText size={18} /> Reports
              </Link>
            </nav>
            <main className="flex-1 overflow-y-auto p-8 relative">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/patient" element={<PatientEntry />} />
                <Route path="/simulator" element={<Simulator />} />
                <Route path="/report" element={<Report />} />
              </Routes>
            </main>
          </div>
        } />
      </Routes>
    </Router>
  );
}

export default App;
