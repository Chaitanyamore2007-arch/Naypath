import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import email
from glob import glob
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

PDF_DIR = "./regulations"
CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")

def parse_mhtml(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        msg = email.message_from_file(f)
    
    html_content = ""
    for part in msg.walk():
        content_type = part.get_content_type()
        if content_type == "text/html":
            payload = part.get_payload(decode=True)
            if payload:
                html_content += payload.decode("utf-8", errors="ignore")
    
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    return [Document(page_content=text, metadata={"source": file_path})]

def ingest_documents():
    print("Looking for PDFs and MHTMLs...")
    pdf_files = glob(os.path.join(PDF_DIR, "*.pdf"))
    mhtml_files = glob(os.path.join(PDF_DIR, "*.mhtml"))
    
    documents = []
    
    for pdf_path in pdf_files:
        try:
            loader = PyMuPDFLoader(pdf_path)
            documents.extend(loader.load())
        except Exception:
            pass

    for mhtml_path in mhtml_files:
        try:
            documents.extend(parse_mhtml(mhtml_path))
        except Exception:
            pass

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    
    print(f"Created {len(chunks)} chunks. Generating embeddings...")
    
    embeddings = FastEmbedEmbeddings()
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    
    # Add in batches of 100 to avoid hanging
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        print(f"Adding batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}...")
        vectorstore.add_documents(batch)
    
    print(f"Success! Embedded and saved to {CHROMA_DIR}.")

if __name__ == "__main__":
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)
    ingest_documents()
