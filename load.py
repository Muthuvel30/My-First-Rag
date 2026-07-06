from pypdf import PdfReader
from io import BytesIO

def load_pdf(file_bytes):
    reader = PdfReader(BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
def chunk_text(text,chunk_size=500,overlap=50):
    chunks=[]
    start=0
    while start < len(text):
        end=start+chunk_size
        chunk=text[start:end]
        chunks.append(chunk)
        start=end-overlap
    return chunks
