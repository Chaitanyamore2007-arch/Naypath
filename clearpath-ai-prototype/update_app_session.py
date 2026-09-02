import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

app_repl = """function App() {
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
  };"""

content = re.sub(
    r"function App\(\) \{.*?(?=  return \()",
    app_repl + "\n\n",
    content,
    flags=re.DOTALL
)

content = content.replace("onRestart={() => setCurrentView('landing')}", "onRestart={handleRestart}")

with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
