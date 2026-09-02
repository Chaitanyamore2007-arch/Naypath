import re

with open("src/components/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

state_add = """
  // --- Inspections ---
  const [inspections, setInspections] = useState(() => JSON.parse(localStorage.getItem('nyapath_inspections')) || {});
  const [inspectionDate, setInspectionDate] = useState('');

  const bookInspection = () => {
    if (!inspectionDate) return;
    const next = { ...inspections, [activeId]: inspectionDate };
    setInspections(next);
    localStorage.setItem('nyapath_inspections', JSON.stringify(next));
    setInspectionDate('');
  };
"""

content = re.sub(
    r"(const \[language, setLanguage\] = useState\('EN'\);)",
    r"\1\n" + state_add,
    content
)

ui_add = """
                    <div className="mt-6">
                      <h3 className="text-sm font-bold text-[#1C2333] font-['Fraunces'] mb-3 flex items-center gap-2 border-b border-[#1C2333] pb-2">
                        <Clock className="w-4 h-4" /> Schedule Inspection
                      </h3>
                      {inspections[activeId] ? (
                        <div className="bg-transparent p-3 border border-[#5C7A5E] flex items-center gap-2">
                          <CheckCircle2 className="w-5 h-5 text-[#5C7A5E]" />
                          <div>
                            <div className="text-xs font-bold text-[#5C7A5E] uppercase tracking-widest font-['IBM_Plex_Mono']">Slot Booked</div>
                            <div className="text-sm text-[#1C2333] font-medium">{new Date(inspections[activeId]).toLocaleDateString('en-GB')} at 10:00 AM</div>
                          </div>
                        </div>
                      ) : (
                        <div className="bg-transparent p-4 border border-[#1C2333]">
                          <p className="text-xs text-[#3A5A78] mb-3">Pre-book an on-site physical inspection slot with the {details.department} department once your documents are cleared.</p>
                          <div className="flex gap-2">
                            <input 
                              type="date" 
                              className="flex-1 bg-transparent border border-[#1C2333] px-2 py-1.5 text-sm outline-none focus:ring-1 focus:ring-[#1C2333]"
                              value={inspectionDate}
                              onChange={(e) => setInspectionDate(e.target.value)}
                            />
                            <button 
                              onClick={bookInspection}
                              className="bg-[#1C2333] text-[#F7F4EC] px-3 py-1.5 text-xs font-bold uppercase tracking-widest font-['IBM_Plex_Mono'] hover:bg-[#3A5A78]"
                            >
                              Book
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
"""

content = re.sub(
    r"(<ul className=\"space-y-2\">.*?</ul>\s*</div>)",
    r"\1" + ui_add,
    content,
    flags=re.DOTALL
)

with open("src/components/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
