from langchain_core.documents import Document
import pandas as pd
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
import faiss
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

file_path = "data/requetes311.csv"
data = pd.read_csv(file_path)

def create_metadata_chunks(df):
    metadata_docs = []
    
    for col in df.columns:
        # On récupère les valeurs uniques (limitées pour ne pas exploser le prompt)
        unique_values = df[col].unique()[:50].tolist() 
        count_unique = df[col].nunique()
        
        content = (
            f"Colonne: {col}\n"
            f"Nombre de valeurs uniques: {count_unique}\n"
            f"Exemples de valeurs: {', '.join(map(str, unique_values))}"
        )
        
        metadata_docs.append(Document(
            page_content=content, 
            metadata={"type": "schema", "column": col}
        ))
    return metadata_docs

docs = create_metadata_chunks(data)


embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2. Déterminer la dimension de l'index automatiquement

sample_embedding = embeddings.embed_query("test")
dimension = len(sample_embedding)

# 3. Créer l'index FAISS
index = faiss.IndexFlatL2(dimension)

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

vector_store.add_documents(documents=docs)

# 1. Initialiser le modèle LLM local via Ollama
# Vous pouvez changer "llama3" par "mistral" ou tout autre modèle téléchargé
llm = ChatOllama(model="gemma3:4b")

# 2. Configurer le retriever à partir de votre vector_store FAISS précédent
retriever = vector_store.as_retriever()

# 3. Définir le prompt système
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 4. Créer la chaîne de documents (RAG)
# On passe ici le LLM Ollama défini plus haut
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


answer= rag_chain.invoke({"input": "Quels sont les appels les plus courants ?"})
print(answer['answer'])