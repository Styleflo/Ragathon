import pandas as pd
import faiss
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
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
        content = f"Colonne: {col}. Valeurs types: {samples}. Nombre de valeurs uniques: {df[col].nunique()}"
        docs.append(Document(page_content=content, metadata={"col_name": col}))
    return docs


metadata_docs = create_column_metadata(df)

# 3. FAISS : Embedding et Similarité
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = FAISS(
    embedding_function=embeddings,
    index=faiss.IndexFlatL2(768),
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)
vector_store.add_documents(metadata_docs)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})  # On récupère les 5 colonnes les plus proches

# 4. Initialisation du LLM
llm = ChatOllama(model="gemma3:4b", temperature=0)

# 5. Prompt pour générer la requête Pandas
# On demande au LLM de ne renvoyer QUE le code Python
query_prompt = ChatPromptTemplate.from_template("""
Basé sur les descriptions de colonnes suivantes :
{context}

Question de l'utilisateur : {question}

Écris uniquement la ligne de code Python (Pandas) pour répondre. 
Le dataframe s'appelle 'df'. Ne mets pas de texte avant ou après le code.
La colonne des dates est une string
Exemple: df['status'].value_counts()
""")


# 6. Fonction pour exécuter le code et formater la réponse
def execute_pandas_and_answer(question):
    # Étape A: Trouver les colonnes pertinentes via FAISS
    relevant_cols = retriever.invoke(question)
    context = "\n".join([d.page_content for d in relevant_cols])

    # Étape B: Générer le code Python
    chain = query_prompt | llm | StrOutputParser()
    pandas_code = chain.invoke({"context": context, "question": question}).strip()

    # Nettoyage du code (enlever les balises markdown si présentes)
    pandas_code = pandas_code.replace("```python", "").replace("```", "").strip()

    print(f"--- Code généré : {pandas_code} ---")

    try:
        # Étape C: Exécuter le code sur le vrai DF
        resultat = eval(pandas_code)

        # Étape D: Synthèse finale
        final_prompt = f"L'utilisateur a demandé : {question}. Le calcul a donné : {resultat}. Réponds de manière concise."
        return llm.invoke(final_prompt).content
    except Exception as e:
        return f"Erreur lors de l'exécution du calcul : {e}. Code tenté : {pandas_code}"


# --- TEST ---
question_test = "Quelle est la répartition des requêtes en 2024 ?"
reponse = execute_pandas_and_answer(question_test)
print("\n--- RÉPONSE FINALE ---")
print(reponse)