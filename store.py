import chromadb
from embed import get_embeed
from load import load_pdf,chunk_text
from llm import ask_llm

content=load_pdf("Muthuvel Resume.pdf")
chunks=chunk_text(content)
client=chromadb.PersistentClient(path="Chroma_db")
collection=client.get_or_create_collection("docs")
if collection.count()==0:
    for i,chunk in enumerate(chunks):
        embedding=get_embeed(chunk)
        collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[chunk]
    )
question = "what is my education  level"
q_embedding = get_embeed(question)

results = collection.query(query_embeddings=[q_embedding], n_results=2)
retrieved = results["documents"][0]
context = "\n".join(retrieved)


prompt = f"""Answer the question using ONLY the context below.
answer concisely in your own words-summarize and interpret
If the answer isn't in the context, say you don't know.

Context: {context}

Question: {question}"""

answer = ask_llm(prompt)
print("Answer:", answer)