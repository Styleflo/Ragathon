import chromadb
import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd 

# Load CSV
df = pd.read_csv("data/requetes311.csv")

# Load description
with open("corpus/description.txt", "r") as f:
    text = f.read()

# Chunk description
splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
chunks = splitter.split_text(text)

# Chroma
client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("events_rag")

# Embeddings
def embed(chunk):
    response = ollama.embed(model="nomic-embed-text", input=chunk)
    return response["embeddings"][0]

# Store chunks
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[f"chunk_{i}"],
        documents=[chunk],
        embeddings=[embed(chunk)]
    )

# Retrieval
def retrieve(query):
    query_emb = embed(query)
    results = collection.query(query_embeddings=[query_emb], n_results=3)
    return [doc for sublist in results["documents"] for doc in sublist]

# Generate pandas code
def generate_pandas(question):
    docs = retrieve(question)
    context = "\n\n".join(docs)

    prompt = f"""
You are a data assistant. Use ONLY the dataset context below.

Context:
{context}

User question:
{question}

Task:
Generate a valid pandas expression using the dataframe 'df'.

Rules:
- ALWAYS return a full filtering expression like: df[df["COLUMN"] == "value"]
- NEVER return only a boolean condition.
- NEVER invent columns.
- Return ONLY the pandas code, nothing else.
"""


    response = ollama.generate(model="gemma3:4b", prompt=prompt)
    return response["response"].strip()

# Execute pandas
def execute_pandas(code):
    try:
        result = eval(code, {"df": df})
        return {"ok": True, "result": result}
    except Exception as e:
        return {"ok": False, "error": str(e), "code": code}


def explain_result(question, exec_result):
    # If execution failed, trigger correction loop
    if not exec_result["ok"]:
        prompt = f"""
The pandas code failed to execute.

User question:
{question}

The code was:
{exec_result["code"]}

The error was:
{exec_result["error"]}

Fix the pandas code. Return ONLY the corrected code.
"""
        response = ollama.generate(model="gemma3:4b", prompt=prompt)
        fixed_code = response["response"].strip()
        print("Fixed code:", fixed_code)

        return explain_result(question, execute_pandas(fixed_code))

    # Success path
    result = exec_result["result"]
    preview = result.head(10).to_string()

    # Retrieve context again for richer explanations
    docs = retrieve(question)
    context = "\n\n".join(docs)

    prompt = f"""
You are a helpful data assistant.

Dataset context:
{context}

User question:
{question}

Here is the result of the pandas query:
{preview}

Explain this result in simple, accurate terms.
Use the dataset context to clarify column meanings when helpful.
Keep it short and close to the question, do not add information that was not asked.
"""

    response = ollama.generate(model="gemma3:4b", prompt=prompt)
    return response["response"]



# Full assistant
def ask(question):
    pandas_code = generate_pandas(question)
    print("Generated code:", pandas_code)

    exec_result = execute_pandas(pandas_code)
    return explain_result(question, exec_result)


print(ask("Show me all rows where ACTI_NOM is 'Organisme divers'"))
