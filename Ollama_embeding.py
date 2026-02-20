import chromadb
import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load your documentation
with open("corpus/description.txt", "r") as f:
    text = f.read()

# Chunk it
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)
chunks = splitter.split_text(text)

# Create Chroma client
client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("events_rag")

# Correct embed function
def embed(chunk):
    response = ollama.embed(
        model="nomic-embed-text",
        input=chunk
    )
    return response["embeddings"][0]

# Add chunks to Chroma
for i, chunk in enumerate(chunks):
    vec = embed(chunk)
    collection.add(
        ids=[f"chunk_{i}"],
        documents=[chunk],
        embeddings=[vec]
    )

def retrieve(query):
    query_emb = embed(query)

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=3
    )

    # Chroma returns [["chunk1"], ["chunk2"], ...]
    # We flatten it into ["chunk1", "chunk2", ...]
    flat_docs = [doc for sublist in results["documents"] for doc in sublist]
    return flat_docs



def answer_with_llama3(question):
    # Retrieve relevant chunks
    docs = retrieve(question)
    context = "\n\n".join(docs)

    prompt = f"""
You are a helpful data assistant. Use ONLY the context below to answer the question.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.generate(
        model="llama3",
        prompt=prompt
    )

    return response["response"]

print(answer_with_llama3("What does the severity ACTI_NOM mean"))
