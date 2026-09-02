import re

with open("src/components/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add state for profile and notifications dropdown
state_add = """
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
"""
content = re.sub(
    r"(const \[isChatOpen, setIsChatOpen\] = useState\(false\);)",
    r"\1\n" + state_add,
    content
)

# 2. Fix translation (replace hardcoded strings with I18N[language].key)
# Avoid replacing inside standard keys
content = re.sub(r">Regulatory Intelligence Dashboard<", r">{I18N[language].dashboard}<", content)
content = re.sub(r">Overview<", r">{I18N[language].overview}<", content)
content = re.sub(r">Document Audit<", r">{I18N[language].audit}<", content)
content = re.sub(r">Schemes & Subsidies<", r">{I18N[language].schemes}<", content)
content = re.sub(r">AI Scheme Matcher<", r">{I18N[language].schemes}<", content)

# 3. Add dropdown UI for Notifications and Profile
nav_replace = """
          <div className="flex items-center gap-4 relative">
            <button 
              onClick={() => setLanguage(language === 'EN' ? 'MR' : 'EN')}
              className="border border-[#1C2333] px-3 py-1 font-['IBM_Plex_Mono'] font-bold text-xs"
            >
              {language}
            </button>
            <div className="relative">
              <button onClick={() => {setShowNotifications(!showNotifications); setShowProfile(false);}} className="relative p-2 text-[#3A5A78] hover:text-[#1C2333] transition-colors">
                <Bell className="w-5 h-5" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-[#C6742B] rounded-none border border-[#1C2333]"></span>
              </button>
              {showNotifications && (
                <div className="absolute right-0 mt-2 w-72 bg-[#F7F4EC] border border-[#1C2333] shadow-lg z-50">
                  <div className="p-3 border-b border-[#1C2333] font-bold text-sm">Notifications</div>
                  <div className="p-4 text-sm text-[#3A5A78]">
                    <div className="mb-2"><span className="text-[#C6742B] font-bold">Alert:</span> MPCB Rule Update (Aug 2026)</div>
                    <div>Your roadmap dependencies have been updated.</div>
                  </div>
                </div>
              )}
            </div>
            <div className="relative">
              <button onClick={() => {setShowProfile(!showProfile); setShowNotifications(false);}} className="w-8 h-8 border border-[#1C2333] flex items-center justify-center text-[#1C2333] font-bold text-sm font-['Fraunces'] hover:bg-[#1C2333] hover:text-[#F7F4EC] transition-colors">
                RK
              </button>
              {showProfile && (
                <div className="absolute right-0 mt-2 w-48 bg-[#F7F4EC] border border-[#1C2333] shadow-lg z-50">
                  <div className="p-3 border-b border-[#1C2333] font-bold text-sm">Ravi Kumar</div>
                  <div className="p-3 text-sm text-[#3A5A78] hover:bg-[#1C2333]/5 cursor-pointer">Project Settings</div>
                  <div className="p-3 text-sm text-[#3A5A78] hover:bg-[#1C2333]/5 cursor-pointer">Logout</div>
                </div>
              )}
            </div>
          </div>
"""
content = re.sub(
    r"<div className=\"flex items-center gap-4\">.*?RK\s*</div>\s*</div>",
    nav_replace.strip(),
    content,
    flags=re.DOTALL
)

with open("src/components/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
