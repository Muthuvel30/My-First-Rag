from fastapi import FastAPI,UploadFile
from pydantic import BaseModel
import chromadb
from embed import get_embeed
from load import load_pdf,chunk_text
from llm import ask_llm
import uuid

app=FastAPI()
client=chromadb.PersistentClient(path="Chroma_db")
collection=client.get_or_create_collection("docs")

class Question(BaseModel):
    text:str

@app.post("/upload")
async def upload(file:UploadFile):
    file_byte=await file.read()
    content=load_pdf(file_byte)
    chunks=chunk_text(content)
    for i,chunk in enumerate(chunks):
        embedding=get_embeed(chunk)
        collection.add(
        ids=[str(uuid.uuid4())],
        embeddings=[embedding],
        documents=[chunk],
        metadatas=[{"source":file.filename,"chunk_index":i}]
    )
    return "File Uploaded Sucessfully"

@app.post("/ask")
def ask(question:Question):
    result=get_embeed(question.text)
    q_query=collection.query(query_embeddings=[result],n_results=2)
    content=q_query["documents"][0]
    context="\n".join(content)
    
    
    prompt = f"""Answer the question using ONLY the context below.
answer concisely in your own words-summarize and interpret
If you dont know , say you don't know.

Context: {context}

Question: {question.text}"""
    ans=ask_llm(prompt)
    return ans