import fitz

def create_bad_pdf():
    # Use PyMuPDF to create a simple PDF
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "DRAFT APPLICATION FOR MIDC LAND ALLOTMENT")
    page.insert_text((50, 70), "Applicant Name: Chaitanya")
    page.insert_text((50, 90), "Industry: Pharma")
    page.insert_text((50, 110), "Note: Missing environmental clearance annexure as requested.")
    doc.save("Draft_Factory_Application.pdf")

create_bad_pdf()
