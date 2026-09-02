import re

with open("src/components/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add states
state_addition = """
  // --- Chat ---
  const [chatHistory, setChatHistory] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);

  // --- Schemes ---
  const [schemes, setSchemes] = useState([]);
  const [schemesLoading, setSchemesLoading] = useState(false);
  const [schemesLoaded, setSchemesLoaded] = useState(false);

  const handleChat = async () => {
    if (!chatInput.trim()) return;
    const newHistory = [...chatHistory, { role: 'user', content: chatInput }];
    setChatHistory(newHistory);
    setChatInput('');
    setChatLoading(true);
    try {
      const { data } = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/chat`, {
        question: chatInput,
        profile: projectData,
        history: chatHistory
      });
      setChatHistory([...newHistory, { role: 'assistant', content: data.answer }]);
    } catch (e) {
      setChatHistory([...newHistory, { role: 'assistant', content: 'Connection failed.' }]);
    }
    setChatLoading(false);
  };

  const loadSchemes = async () => {
    if (schemesLoaded || !projectData) return;
    setSchemesLoading(true);
    try {
      const { data } = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/schemes`, projectData);
      setSchemes(data.schemes || []);
      setSchemesLoaded(true);
    } catch (e) {
      console.error(e);
    }
    setSchemesLoading(false);
  };

  // Load schemes when tab is opened
  React.useEffect(() => {
    if (activeTab === 'schemes') loadSchemes();
  }, [activeTab]);
"""
content = re.sub(
    r"(const \[language, setLanguage\] = useState\('EN'\);)",
    r"\1\n" + state_addition,
    content
)

# 2. Update Details Panel Enrichment
details_replacement = """
  const details = {
    title: selected.name,
    department: selected.department,
    description: selected.description || `Mandatory clearance issued by ${selected.department}.`,
    timeline: `${selected.estimated_days} Days`,
    fees: formatINR(selected.estimated_fee_inr),
    documents: (selected.required_documents?.length > 0) ? selected.required_documents : enrichment.documents,
    commonRejections: (selected.common_rejection_reasons?.length > 0) ? selected.common_rejection_reasons : enrichment.commonRejections,
  };
"""
content = re.sub(
    r"const details = \{[\s\S]*?commonRejections: enrichment\.commonRejections,\n  \};",
    details_replacement.strip(),
    content
)

# 3. Update Schemes Tab UI
schemes_ui_replacement = """
          {/* SCHEMES TAB */}
          {activeTab === 'schemes' && (
            <div className="p-8 max-w-5xl mx-auto">
              <div className="bg-[#1C2333] border border-[#1C2333] p-8 text-[#F7F4EC] mb-8 flex items-center justify-between">
                <div>
                  <h2 className="text-3xl font-bold mb-2 font-['Fraunces']">AI Scheme Matcher</h2>
                  <p className="text-[#F7F4EC] max-w-xl">Based on your {projectData?.investment_scale_crores} Cr {projectData?.industry_type} investment in {projectData?.district}, our intelligence engine found matching state subsidies.</p>
                </div>
                <div className="hidden md:flex w-24 h-24 border border-[#F7F4EC] items-center justify-center">
                  <Gift className="w-12 h-12 text-[#F7F4EC]" />
                </div>
              </div>

              {schemesLoading ? (
                <div className="p-8 text-center text-[#1C2333] font-['IBM_Plex_Mono']">Analyzing state policies...</div>
              ) : schemes.length === 0 ? (
                <div className="p-8 text-center text-[#1C2333] font-['IBM_Plex_Mono']">No specific schemes found for this profile.</div>
              ) : (
                <div className="grid grid-cols-1 gap-6">
                  {schemes.map((scheme, i) => (
                    <div key={i} className="bg-transparent p-6 border border-[#5C7A5E] relative overflow-hidden">
                      <div className="absolute top-0 right-0 bg-[#5C7A5E] text-[#F7F4EC] text-xs font-bold px-4 py-1 font-['IBM_Plex_Mono'] uppercase tracking-widest">{scheme.match_level} MATCH</div>
                      <h3 className="text-xl font-bold text-[#1C2333] font-['Fraunces'] mb-2">{scheme.name}</h3>
                      <p className="text-[#1C2333] mb-4 max-w-3xl">{scheme.benefit}</p>
                      <p className="text-[#3A5A78] text-sm mb-4 max-w-3xl italic">{scheme.eligibility_note}</p>
                      <div className="flex gap-4">
                        {scheme.tags.map(tag => (
                           <span key={tag} className="bg-transparent text-[#5C7A5E] px-3 py-1 font-['IBM_Plex_Mono'] uppercase tracking-widest text-xs font-bold border border-[#5C7A5E]">{tag}</span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
"""
content = re.sub(
    r"\{\/\* SCHEMES TAB \*\/\}.*?\{\/\* Floating AI Chatbot \*\/\}",
    schemes_ui_replacement.strip() + "\n\n        {/* Floating AI Chatbot */}",
    content,
    flags=re.DOTALL
)

# 4. Update Chatbot UI
chatbot_replacement = """
                <div className="flex-1 p-4 overflow-y-auto bg-transparent flex flex-col gap-3">
                  <div className="bg-transparent border border-[#1C2333] p-3 text-sm text-[#1C2333] max-w-[85%]">
                    Hi! I'm trained on Maharashtra's entire regulatory graph. Do you have any questions about setting up a {projectData?.industry_type} unit in {projectData?.district}?
                  </div>
                  {chatHistory.map((msg, i) => (
                    <div key={i} className={`p-3 text-sm max-w-[85%] border ${msg.role === 'user' ? 'bg-[#1C2333] text-[#F7F4EC] self-end border-[#1C2333]' : 'bg-transparent text-[#1C2333] self-start border-[#1C2333]'}`}>
                      {msg.content}
                    </div>
                  ))}
                  {chatLoading && (
                     <div className="bg-transparent border border-[#1C2333] p-3 text-sm text-[#3A5A78] max-w-[85%] self-start italic">
                       Thinking...
                     </div>
                  )}
                </div>
                <div className="p-3 bg-transparent border-t border-[#1C2333] flex gap-2">
                  <input 
                    type="text" 
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleChat()}
                    placeholder="ASK ABOUT COMPLIANCE..." 
                    className="flex-1 bg-transparent border border-[#1C2333] px-3 py-2 text-xs font-['IBM_Plex_Mono'] outline-none focus:ring-1 focus:ring-[#1C2333]" 
                  />
                  <button onClick={handleChat} disabled={chatLoading} className="bg-[#1C2333] text-[#F7F4EC] p-2 hover:bg-[#3A5A78]">
                    <Send className="w-4 h-4" />
                  </button>
                </div>
"""
content = re.sub(
    r"<div className=\"flex-1 p-4 overflow-y-auto bg-transparent flex flex-col gap-3\">.*?<\/div>\s*<\/motion\.div>",
    chatbot_replacement.strip() + "\n              </motion.div>",
    content,
    flags=re.DOTALL
)

with open("src/components/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
