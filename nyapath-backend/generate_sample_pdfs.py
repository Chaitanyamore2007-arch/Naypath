import os
from fpdf import FPDF

PDF_DIR = "./regulations"
os.makedirs(PDF_DIR, exist_ok=True)

docs = {
    "MPCB_Guidelines_2026.pdf": [
        "Maharashtra Pollution Control Board (MPCB) Guidelines for Industrial Setup 2026.",
        "Section 1: General Requirements",
        "All manufacturing units generating hazardous waste or wastewater must obtain Consent to Establish (CTE) before beginning construction.",
        "Section 4: Effluent Treatment Plan (ETP)",
        "Section 4b: Pharmaceutical and Chemical units (Red Category) must include explicit ETP capacity specifications in their factory layout. The design must incorporate Reverse Osmosis (RO) modules to ensure Zero Liquid Discharge (ZLD).",
        "Section 7: Fees",
        "Processing fee for Red Category industries with investment above 50 Crores is INR 180,000.",
        "Estimated processing time is 45 to 60 days."
    ],
    "Fire_Safety_Act_Maharashtra.pdf": [
        "Maharashtra Fire Prevention and Life Safety Measures Act",
        "Annexure A: Industrial and Hazardous Storage",
        "1. Any industrial facility storing raw materials or chemicals exceeding 500 sq meters is strictly required to install an Automatic Sprinkler System and foam-based fire extinguishers.",
        "2. Emergency Exits: Minimum width for fire exits in hazardous units must be at least 1.5 meters. Anything less (e.g., 1.2m) is considered non-compliant and will result in rejection of the Fire Safety NOC.",
        "3. Provisional NOC takes approximately 20 days. Final NOC is granted post-inspection."
    ],
    "MIDC_Allotment_Rules.pdf": [
        "Maharashtra Industrial Development Corporation (MIDC) Land Allotment Policy",
        "Chapter 3: Application Process",
        "For new units, a Detailed Project Report (DPR), Company PAN, and Board Resolution must be submitted.",
        "Common rejection reasons include insufficient justification for the requested land area.",
        "Chapter 8: Incentives",
        "Under the Package Scheme of Incentives (PSI) 2019, Pharmaceutical or IT units established in Zone D are eligible for 100% SGST refund for a period of 10 years, and a 100% waiver on stamp duty for lease agreements."
    ]
}

for filename, lines in docs.items():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in lines:
        # Multi_cell handles text wrapping
        pdf.multi_cell(0, 10, txt=line)
        pdf.ln(2)
    
    filepath = os.path.join(PDF_DIR, filename)
    pdf.output(filepath)
    print(f"Generated {filepath}")

print("All sample PDFs generated successfully.")
