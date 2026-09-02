import re

with open("src/components/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

target = """<header className="h-16 bg-transparent border-b border-[#1C2333] flex items-center justify-between px-6 z-10">
          <div className="flex items-center gap-4 relative">"""

replacement = """<header className="h-16 bg-transparent border-b border-[#1C2333] flex items-center justify-between px-6 z-10">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-[#1C2333] flex items-center justify-center text-[#F7F4EC] font-bold font-['Fraunces']">N</div>
            <span className="font-bold text-[#1C2333] font-['Fraunces']">{I18N[language].dashboard}</span>
          </div>
          <div className="flex items-center gap-4 relative">"""

# replace ignores whitespace if we don't match it exactly, so let's use regex
content = re.sub(
    r"<header className=\"h-16 bg-transparent border-b border-\[\#1C2333\] flex items-center justify-between px-6 z-10\">\s*<div className=\"flex items-center gap-4 relative\">",
    replacement,
    content,
    flags=re.DOTALL
)

with open("src/components/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
