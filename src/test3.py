import pandas as pd
import faiss
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Chargement du CSV
file_path = "data/requetes311.csv"
df = pd.read_csv(file_path)

# 2. Création des chunks par colonnes (Metadata Chunks)
def create_column_metadata(df):
    docs = []
    for col in df.columns:
        # On prend un petit échantillon de valeurs uniques pour l'aider
        samples = df[col].dropna().unique()[:10].tolist()
        samples2 = df[col].dropna().unique()
        random_samples = pd.Series(samples2).sample(n=min(100, len(samples2))).tolist()
        content = f"Colonne: {col}. Valeurs types: {samples}. Nombre de valeurs uniques: {df[col].nunique()}. Exemples: {random_samples}"
        docs.append(Document(page_content=content, metadata={"col_name": col}))
    return docs

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = FAISS(embedding_function=embeddings, index=faiss.IndexFlatL2(768),
                     docstore=InMemoryDocstore(), index_to_docstore_id={})
vector_store.add_documents(create_column_metadata(df))
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

llm = ChatOllama(model="gemma3:4b", temperature=0)

# 3. PROMPT pour générer le FILTRE PANDAS (Extraction de données)
# On demande ici au LLM de générer un code qui retourne un DataFrame filtré (.head(20))
query_prompt = ChatPromptTemplate.from_template("""
Basé sur les colonnes suivantes : {context}
Question : {question}

Écris UNIQUEMENT le code Pandas pour filtrer le dataframe 'df' et retourner les 100 premières lignes pertinentes.
Exemple pour 2024 : df[df['DDS_DATE_CREATION'].str.contains('2024', case=False, na=False)].head(100)
Attention la colonne des dates est en string
Code :""")


def execute_extraction_and_answer(question):
    # A. Trouver les colonnes via FAISS
    relevant_cols = retriever.invoke(question)
    context = "\n".join([d.page_content for d in relevant_cols])

    # B. Générer le code de filtrage
    chain = query_prompt | llm | StrOutputParser()
    pandas_code = chain.invoke({"context": context, "question": question}).strip()
    pandas_code = pandas_code.replace("```python", "").replace("```", "").strip()

    print(f"--- Extraction via : {pandas_code} ---")

    try:
        # C. EXTRACTION des données réelles
        # On utilise eval() pour récupérer un sous-ensemble du CSV (un DataFrame)
        data_extracted = eval(pandas_code)

        # D. SYNTHÈSE : On donne les données réelles au LLM
        final_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "Tu es un analyste. Voici un extrait de données réelles provenant du fichier CSV pour répondre à la question. Je veux une petite analyse en 5 phrases maximum"),
            ("human", "Données extraites :\n{data}\n\nQuestion : {question}")
        ])

        # On convertit l'extrait en texte (Markdown est bien lu par les LLM)
        final_chain = final_prompt | llm | StrOutputParser()
        return final_chain.invoke({"data": data_extracted.to_markdown(), "question": question})

    except Exception as e:
        return f"Erreur : {e}. Code tenté : {pandas_code}"


# --- TEST ---
question_test = "Quels secteurs ont une hausse de collisions entre 2024 et 2025 ?"
reponse = execute_extraction_and_answer(question_test)
print("\n--- RÉPONSE FINALE BASÉE SUR DONNÉES RÉELLES ---")
print(reponse)