import React, { useState } from 'react';
import axios from 'axios';
import LandingPage from './components/LandingPage';
import ProcessingPage from './components/ProcessingPage';
import Dashboard from './components/Dashboard';

function App() {
  const [currentView, setCurrentView] = useState(() => (localStorage.getItem('nyapath_roadmapData') ? 'dashboard' : 'landing'));
  const [projectData, setProjectData] = useState(() => JSON.parse(localStorage.getItem('nyapath_projectData')) || null);
  const [roadmapData, setRoadmapData] = useState(() => JSON.parse(localStorage.getItem('nyapath_roadmapData')) || null);
  const [apiError, setApiError] = useState(null);

  const handleRestart = () => {
    localStorage.removeItem('nyapath_projectData');
    localStorage.removeItem('nyapath_roadmapData');
    localStorage.removeItem('nyapath_inspections');
    setProjectData(null);
    setRoadmapData(null);
    setCurrentView('landing');
  };

  const handleGenerate = async (data) => {
    setProjectData(data);
    localStorage.setItem('nyapath_projectData', JSON.stringify(data));
    
    setRoadmapData(null);
    setApiError(null);
    setCurrentView('processing');

    const startTime = Date.now();

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/roadmap`,
        data,
        { timeout: 20000 }
      );
      setRoadmapData(response.data);
      localStorage.setItem('nyapath_roadmapData', JSON.stringify(response.data));
    } catch (error) {
      console.error('Failed to generate roadmap:', error);
      setApiError(error.message || 'Request failed');
    } finally {
      const elapsed = Date.now() - startTime;
      const minDisplayTime = 800;
      const remaining = Math.max(0, minDisplayTime - elapsed);
      setTimeout(() => setCurrentView('dashboard'), remaining);
    }
  };

  return (
    <div className="w-full h-screen bg-[#F7F4EC] overflow-hidden flex flex-col font-['Inter']">
      <main className="flex-1 relative overflow-hidden">
        {currentView === 'landing' && <LandingPage onGenerate={handleGenerate} />}
        {currentView === 'processing' && (
          <ProcessingPage projectData={projectData} />
        )}
        {currentView === 'dashboard' && (
          <Dashboard
            projectData={projectData}
            roadmapData={roadmapData}
            apiError={apiError}
            onRestart={handleRestart}
          />
        )}
      </main>
    </div>
  );
}

export default App;
