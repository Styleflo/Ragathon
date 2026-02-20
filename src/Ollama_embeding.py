import chromadb
import ollama
import pandas as pd
import os
import re

# 1. Chargement des données CSV
df = pd.read_csv("data/requetes311.csv", low_memory=False)

# 2. Chargement des chunks Markdown (RAG)
# On récupère chaque fichier .md dans le dossier spécifique
chunks_dir = "data/311_chunks"
markdown_files = [f for f in os.listdir(chunks_dir) if f.endswith(".md")]

# Configuration Chroma
client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("events_rag")


def embed(text):
    response = ollama.embed(model="nomic-embed-text", input=text)
    return response["embeddings"][0]


# Indexation des fichiers Markdown
print(f"Indexation de {len(markdown_files)} fichiers de description...")
for filename in markdown_files:
    path = os.path.join(chunks_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    collection.add(
        ids=[filename],  # On utilise le nom du fichier comme ID
        documents=[content],
        embeddings=[embed(content)],
        metadatas=[{"dataset": "requetes311", "source": filename}]
    )


# 3. Fonctions de récupération et génération
def retrieve(query):
    query_emb = embed(query)
    results = collection.query(query_embeddings=[query_emb], n_results=3)

    retrieved_docs = []
    # results["documents"][0] contient les textes
    # results["metadatas"][0] contient les dict de métadonnées
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        retrieved_docs.append({
            "text": doc,
            "source": meta["source"]
        })
    return retrieved_docs


def generate_pandas(question):
    docs_with_meta = retrieve(question)

    # On construit un contexte structuré
    context_parts = []
    for d in docs_with_meta:
        part = f"--- SOURCE: {d['source']} ---\n{d['text']}"
        context_parts.append(part)

    context = "\n\n".join(context_parts)

    prompt = f"""
Tu es un expert en Pandas et science des données.
Utilise les extraits de documentation ci-dessous pour répondre à la question en générant du code Python.

DOCUMENTATION :
{context}

QUESTION :
{question}

RÈGLES DE GÉNÉRATION :
1. Fais attention à la SOURCE : si la source est '[nom].md', utilise la colonne 'NOM'.
2. Pour les dates ('DDS_DATE_CREATION'), utilise : pd.to_datetime(df['DDS_DATE_CREATION']).
3. Retourne UNIQUEMENT le code Python permettant de filtrer ou d'agréger le dataframe 'df'.
4. Ne mets pas de commentaires ou d'explications.
"""
    response = ollama.generate(model="gemma3:4b", prompt=prompt)
    return response["response"].strip().replace('`', '')


def execute_pandas(code):
    try:
        # Nettoyage des balises Markdown et du mot "python"
        code_match = re.search(r"```(?:python)?\s*(.*?)\s*```", code, re.DOTALL)
        code_clean = code_match.group(1).strip() if code_match else code.strip()
        code_clean = re.sub(r"^(python\n|df\s*=\s*)", "", code_clean).strip()

        print(f"Code à exécuter :\n{code_clean}")

        # Utilisation d'un dictionnaire local pour récupérer le résultat
        local_vars = {"df": df, "pd": pd, "result": None}

        # On force la dernière ligne à être assignée à 'result' si ce n'est pas fait
        if "result =" not in code_clean:
            lines = code_clean.split('\n')
            lines[-1] = f"result = {lines[-1]}"
            code_clean = '\n'.join(lines)

        exec(code_clean, {"pd": pd}, local_vars)
        return {"ok": True, "result": local_vars["result"], "code": code_clean}
    except Exception as e:
        return {"ok": False, "error": str(e), "code": code}


def explain_result(question, exec_result):
    if not exec_result["ok"]:
        return f"Désolé, j'ai rencontré une erreur technique : {exec_result['error']}"

    result = exec_result["result"]

    if isinstance(result, pd.DataFrame):
        if result.empty:
            return "Je n'ai trouvé aucun résultat correspondant à votre recherche dans la base de données."

        count = len(result)
        # Dynamique : On prend la première colonne disponible pour faire un top 5
        # ou on laisse le LLM voir un échantillon des données
        summary_data = result.head(5).to_string()
    else:
        # Si le résultat est une simple valeur (ex: un count ou une moyenne)
        count = 1
        summary_data = str(result)

    prompt = f"""
User Question: {question}
Number of results found: {count}
Summary of categories:
{summary_data}

Task: Summarize in 10 lines the findings clearly. 
- Mention the total number of requests.
- List the main types of activities found.
- Keep it concise and professional.
"""
    response = ollama.generate(model="gemma3:4b", prompt=prompt)
    return response["response"]


def ask(question):
    print(f"\n--- Question: {question} ---")
    pandas_code = generate_pandas(question)
    print(f"Code généré : {pandas_code}")

    exec_result = execute_pandas(pandas_code)
    return explain_result(question, exec_result)


# Test
print(ask("Donne moi la répartition des requetes en 2025 ?"))