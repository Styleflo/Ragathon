from langchain_text_splitters import MarkdownHeaderTextSplitter
import ollama
from services.models import EMBEDDING_MODEL
from services.datasets_info import datasets

def embed(text: str):
    response = ollama.embed(model=EMBEDDING_MODEL, input=text)
    return response["embeddings"][0]


def build_context_dict(top_k_chunks):
    context = {}

    if top_k_chunks:
            for chunk in top_k_chunks:
                meta = chunk["metadata"]
                col = meta.get("Column Name", "Inconnue")
                dtype = meta.get("Data Type", "N/A")
                examples = meta.get("Value Examples", "N/A")
                key = chunk["dataset"]

                if key not in context:
                    context[key] = ""
                context[key] += f"DATASET: {key}\n"
                context[key] += f"- COLUMN: {col} | TYPE: {dtype}\n"
                context[key] += f"- DESCRIPTION: {chunk['content']}\n"
                context[key] += f"- EXAMPLES: {examples}\n"
            context[key] += "\n"
    return context


def context_converter(contexts):
    clean = {}

    for dataset_name, messy_text in contexts.items():
        clean[dataset_name] = {"columns": {}}
        current_column = None

        for line in messy_text.splitlines():
            line = line.strip()

            if line.startswith("- COLUMN:"):
                if "Nom de la colonne" in line:
                    col = line.split("Nom de la colonne")[-1].split("|")[0].replace(":", "").strip()
                else:
                    col = line.split("- COLUMN:")[1].split("|")[0].strip()

                current_column = col
                clean[dataset_name]["columns"][current_column] = {
                    "description": "",
                    "type": ""
                }

                if "| TYPE:" in line:
                    clean[dataset_name]["columns"][current_column]["type"] = line.split("TYPE:")[1].strip()

            elif line.startswith("- DESCRIPTION:") and current_column:
                clean[dataset_name]["columns"][current_column]["description"] = line.split("- DESCRIPTION:")[1].strip()

    return clean


def retrieve_top_chunks_overall(question: str, top_k=10):
    all_candidates = []
    for key in datasets.keys():
        collection = datasets[key]["collection"]
        query_emb = embed(question)

        results = collection.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )

        for i in range(len(results["documents"][0])):
            all_candidates.append({
                "dataset": key,
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

    all_candidates.sort(key=lambda x: x["distance"])
    top_k_chunks = all_candidates[:top_k]

    context = build_context_dict(top_k_chunks)
    return context

headers_to_split_on=[ 
    ("##", "Column Name"),
    ("###", "Data Type"), 
    ("####", "Value Examples"), 
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on, 
    strip_headers=True 
)

for key, info in datasets.items():
    collection = info["collection"]
    if collection.count() > 0:
        continue

    with open(info["description_file"], "r", encoding="utf-8") as f:
        text = f.read()

    chunks = markdown_splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        text_content = chunk.page_content
        metadata = chunk.metadata
        metadata["Dataset"] = key
        collection.add(
            ids=[f"{key}_chunk_{i}"],
            documents=[text_content],
            embeddings=[embed(text_content)],
            metadatas=[metadata]
        )