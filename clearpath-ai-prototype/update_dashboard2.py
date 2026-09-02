import re

with open("src/components/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add i18n
i18n = """
const I18N = {
  EN: {
    dashboard: "Regulatory Intelligence Dashboard",
    overview: "Roadmap",
    audit: "Document Audit",
    schemes: "Incentive Schemes",
    alerts: "Intelligence Alerts",
    generate: "Generate Intelligence Report",
    chatPlaceholder: "ASK ABOUT COMPLIANCE...",
    runAudit: "Run Document Audit",
    uploadPrompt: "Drag & drop your project documents here",
    uploadSub: "Supports PDF (Max 10MB per file)"
  },
  MR: {
    dashboard: "नियामक बुद्धिमत्ता डॅशबोर्ड",
    overview: "रोडमॅप",
    audit: "कागदपत्र ऑडिट",
    schemes: "प्रोत्साहन योजना",
    alerts: "बुद्धिमत्ता सूचना",
    generate: "बुद्धिमत्ता अहवाल तयार करा",
    chatPlaceholder: "अनुपालनाबद्दल विचारा...",
    runAudit: "कागदपत्र ऑडिट चालवा",
    uploadPrompt: "तुमची प्रकल्प कागदपत्रे येथे ड्रॅग आणि ड्रॉप करा",
    uploadSub: "PDF समर्थित (प्रति फाईल कमाल 10MB)"
  }
};
"""

content = re.sub(
    r"const FALLBACK_ROADMAP =",
    i18n + "\nconst FALLBACK_ROADMAP =",
    content
)

content = content.replace(
  ">Regulatory Intelligence Dashboard<",
  ">{I18N[language].dashboard}<"
).replace(
  ">Overview<",
  ">{I18N[language].overview}<"
).replace(
  ">Document Audit<",
  ">{I18N[language].audit}<"
).replace(
  ">Schemes & Subsidies<",
  ">{I18N[language].schemes}<"
).replace(
  'placeholder="ASK ABOUT COMPLIANCE..."',
  'placeholder={I18N[language].chatPlaceholder}'
)

with open("src/components/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
