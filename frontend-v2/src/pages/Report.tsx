import { usePatientStore } from '@/store/usePatientStore';
import { Button } from '@/components/ui/button';
import { FileText, Download, Activity } from 'lucide-react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export default function Report() {
  const { predictionResult, patientData } = usePatientStore();

  if (!predictionResult) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center">
        <Activity className="h-16 w-16 text-muted-foreground mb-4 opacity-50" />
        <h2 className="text-2xl font-bold mb-2">No Report Available</h2>
      </div>
    );
  }

  const handleDownload = async () => {
    const input = document.getElementById('pdf-report-content');
    if (!input) return;
    
    const canvas = await html2canvas(input, { scale: 2 });
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
    
    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
    pdf.save('MedIntel_Clinical_Report.pdf');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold flex items-center gap-2"><FileText className="text-primary"/> Report Generation</h1>
        <Button onClick={handleDownload} className="gap-2"><Download size={18}/> Export PDF</Button>
      </div>

      <div id="pdf-report-content" className="bg-white text-black p-8 rounded-xl shadow-2xl">
        <div className="border-b-2 border-black pb-4 mb-6">
          <h1 className="text-4xl font-black mb-2 text-blue-600">MedIntel AI</h1>
          <p className="text-xl font-bold text-gray-700">Clinical Health Intelligence Report</p>
        </div>

        <div className="grid grid-cols-2 gap-8 mb-8">
          <div>
            <h3 className="font-bold text-lg mb-3 border-b pb-1">Patient Demographics</h3>
            <p><strong>Age:</strong> {patientData.age}</p>
            <p><strong>Gender:</strong> {patientData.gender}</p>
            <p><strong>BMI:</strong> {patientData.bmi}</p>
          </div>
          <div>
            <h3 className="font-bold text-lg mb-3 border-b pb-1">Top Line Intelligence</h3>
            <p><strong>Overall Health Score:</strong> <span className={predictionResult.overall_health_score <= 50 ? 'text-red-600 font-bold' : 'text-green-600 font-bold'}>{predictionResult.overall_health_score}/100</span></p>
            <p><strong>Risk Category:</strong> {predictionResult.health_category}</p>
            <p><strong>Biological Age:</strong> {predictionResult.biological_age}</p>
          </div>
        </div>

        <div className="mb-8">
           <h3 className="font-bold text-lg mb-3 border-b pb-1">Disease Probabilities</h3>
           <div className="grid grid-cols-4 gap-4 text-center">
             <div className="bg-gray-100 p-4 rounded-lg">
               <p className="text-sm font-bold">Diabetes</p>
               <p className="text-2xl text-blue-600">{predictionResult.diabetes_risk}%</p>
             </div>
             <div className="bg-gray-100 p-4 rounded-lg">
               <p className="text-sm font-bold">Heart</p>
               <p className="text-2xl text-red-600">{predictionResult.heart_risk}%</p>
             </div>
             <div className="bg-gray-100 p-4 rounded-lg">
               <p className="text-sm font-bold">Stroke</p>
               <p className="text-2xl text-purple-600">{predictionResult.stroke_risk}%</p>
             </div>
             <div className="bg-gray-100 p-4 rounded-lg">
               <p className="text-sm font-bold">Kidney</p>
               <p className="text-2xl text-green-600">{predictionResult.kidney_risk}%</p>
             </div>
           </div>
        </div>

        <div className="mb-8">
          <h3 className="font-bold text-lg mb-3 border-b pb-1 text-red-600">Clinical Alerts</h3>
          <ul className="list-disc pl-5 space-y-1">
            {predictionResult.alerts.map((a, i) => <li key={i}>{a}</li>)}
          </ul>
        </div>

        <div>
          <h3 className="font-bold text-lg mb-3 border-b pb-1 text-green-600">Actionable Recommendations</h3>
          <ul className="list-disc pl-5 space-y-1 text-sm">
            {predictionResult.recommendations.map((r, i) => <li key={i}>{r}</li>)}
          </ul>
        </div>
        
        <div className="mt-12 text-center text-gray-500 text-xs border-t pt-4">
          Generated automatically by MedIntel AI Explainable Neural Networks. Not a substitute for professional medical advice.
        </div>
      </div>
    </div>
  );
}
