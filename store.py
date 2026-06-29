import chromadb
from embed import get_embeed
from llm import ask_llm

client=chromadb.Client()
collection=client.create_collection("docs")

chunks=[
        "Muthuvel was born on March 5th, 2002.",
    "The capital of France is Paris.",
    "Python is a popular programming language."
]

for i,chunk in enumerate(chunks):
    embedding=get_embeed(chunk)
    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[chunk]
    )
print("Stored",collection.count(),"Chunks")
question="When was Muthuvel born?"
q_embedding=get_embeed(question)
# print(q_embedding)

results=collection.query(
    query_embeddings=[q_embedding],
    n_results=1
)
# print(type(results))
print("best Match:",results["documents"])
retrieved_chunk = results["documents"][0][0]

# build a prompt: give the LLM the context + the question
prompt = f"""Answer the question using the context below.
If the answer isn't in the context, say you don't know.

Context: {retrieved_chunk}

Question: {question}"""

answer = ask_llm(prompt)
print("Answer:", answer)
