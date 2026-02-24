import chromadb
import ollama
from langchain_text_splitters import MarkdownHeaderTextSplitter
import pandas as pd
import json

EMBEDDING_MODEL = "bge-m3"
LANGUAGE_MODEL = "gemma3:4b"

datasets = {
    "requetes311": {
        "df": pd.read_csv("data/requetes311.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path="db_requetes311").get_or_create_collection("requetes311_rag"),
        "description_file": "desc/requetes311.md"
    },
    "collisions_routieres": {
        "df": pd.read_csv("data/collisions_routieres.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path="db_collisions_routieres").get_or_create_collection("collisions_routieres_rag"),
        "description_file": "desc/collisions_routieres.md"
    },
    "gtfs_stm": {
        "df": pd.read_csv("data/gtfs_stm.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path="db_gtfs_stm").get_or_create_collection("gtfs_stm_rag"),
        "description_file": "desc/gtfs_columns.md"
    },
    "meteo_montreal": {
        "df": pd.read_csv("data/meteo_montreal.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path="db_meteo_montreal").get_or_create_collection("meteo_montreal_rag"),
        "description_file": "desc/contexte_metier_meteo.md"
    }
}

requetes311 = datasets["requetes311"]["df"]
collisions_routieres = datasets["collisions_routieres"]["df"]
gtfs_stm = datasets["gtfs_stm"]["df"]
meteo_montreal = datasets["meteo_montreal"]["df"]


def embed(text: str):
    response = ollama.embed(model=EMBEDDING_MODEL, input=text)
    return response["embeddings"][0]

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


def safe_json_loads(raw: str):

    if not raw or not raw.strip():
        raise ValueError("LLM returned empty output instead of JSON.")

    cleaned = raw.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if "\n" in cleaned:
            cleaned = cleaned.split("\n", 1)[1]
    
    return json.loads(cleaned)

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





    

def generate_pandas_with_dataset_selection(
    question: str,
    contexts: dict,
):

    prompt = f"""
        You are a python/pandas query generator.

        Your job:
        Generate pandas expressions that help answer the user's question, using ONLY the datasets and columns in `contexts`.

        MODES:
        1. If the question clearly relates to specific columns, generate queries ONLY for those columns.
        2. If the question is vague, general, or does not match any column, switch to EXPLORATORY MODE:
        - Treat ALL datasets as relevant.
        - Select several meaningful columns from each dataset.
        - Generate exploratory queries for them.

        OUTPUT FORMAT (IMPORTANT):
        - Output MUST be a FLAT JSON object.
        - Each key MUST be a string.
        - Each value MUST be a SINGLE pandas expression.
        - Keys MUST follow this format: dataset_column_queryIndex
        Example: meteo_montreal_Temp_moy_1
        - Do NOT output nested JSON.
        - Do NOT output lists.
        - Do NOT output explanations or comments.

        RULES:
        - Use ONLY dataset and column names from `contexts`.
        - Pandas variable name = dataset name.
        - Use bracket notation only: dataset["column"].
        - Do NOT invent columns, datasets, or expressions.

        QUERY GENERATION:
        For each selected column, generate 1–3 useful analytical queries:
        - value_counts()
        - describe()
        - groupby() if meaningful
        - comparisons or trends if numeric/time columns exist

        CONTEXTS:
        {json.dumps(contexts, indent=2, ensure_ascii=False)}

        QUESTION:
        {question}

        Output MUST be a flat JSON object of the form, but there are no limit to the number of entries the more the better:
        {{
            "key1": "pandas_expression1"¨
            "key2": "pandas_expression2"
            "key3": "pandas_expression3"
            "key4": "pandas_expression4"
            "key5": "pandas_expression5"
        }}
    """




    print(prompt)
    response = ollama.generate(model=LANGUAGE_MODEL, prompt=prompt)
    raw = response["response"].strip()
    print(raw)

    return safe_json_loads(raw)



def execute_multi(code_map: dict):
    results = {}

    env = {
        "requetes311": requetes311,
        "collisions_routieres": collisions_routieres,
        "gtfs_stm ": gtfs_stm ,
        "meteo_montreal": meteo_montreal,
        "pd": pd,
    }

    for key, code in code_map.items():
        print(key, code)
        try:
            res = eval(code, env)
            results[key] = {"ok": True, "result": res, "code": code}
        except Exception as e:
            results[key] = {"ok": False, "error": str(e), "code": code}
            

    return results


def explain_cross(
    question: str,
    results: dict,
    contexts: dict,
):
    prompt = f"""
        You are a data analyst that use data to answer questions.

        You may use this context to help formulate your answer, but only only use data from the data.:
        {json.dumps(contexts, indent=2, ensure_ascii=False)}

        The data, this is you main source of informations:
        {results}

        This is the question you must answer has precisely has possible :
        {question}

        Constraint:
        1. You MUST NOT invent number in your answer, only use the ones present in the provided data.
        2. After the answer you must provide:
            ➢ Limite /risques d’interprétation ET/OU 
            ➢ Ce que je vérifierais ensuite.
        3. Answer in french
        4. If the data is irrelevant and you cant answer properly you must say so.
        5. Do not use the columns names and data names directly in the answer, use descriptions.
        
        Your task :

        ### Analyse

        Here are example of questions and the type of answer expected, chose the proper format accodingly

        a.Chat analytique “data-grounded” 
            • Exemples de questions : 
                o Quels secteurs ont une hausse de collisions en conditions de pluie/neige 
                ? 
                o Quels types de requêtes 311 augmentent quand la température passe sous 
                0°C ? 
                o Autour de quels axes STM (arrêts/lignes) observe-t-on le plus de 
                collisions graves ? 
            • Réponses avec preuves : citations de lignes/agrégats, filtres appliqués, période, et 
            limites. 
        b. Génération de synthèses utiles 
            • Briefing automatique hebdomadaire : 
                o top 5 hotspots, tendances, signaux faibles 
                o recommandations (p. ex. : ciblage de déneigement, signalisation, 
                inspection) 
            • Version grand public vs municipalité (2 tons, même fondement data). 
                Plus précisément, … 
                Top 5 hotspots 
                Les 5 endroits (ou zones) où le problème est le plus concentré, selon un critère 
                clair. 
            • Exemples de critères : 
                o Collisions : intersections / segments de rue avec le plus de collisions 
                (ou collisions graves) sur une période. 
                o 311 : secteurs avec le plus de requêtes « nids-de-poule », 
                « déneigement », « éclairage ». 
                o STM : arrêts/lignes avec le plus de perturbations (si dispo.). 
            • Format attendu : 
                o Hotspot #1 : Intersection A - 32 collisions (dont 6 graves), surtout 
                entre 16h–19h, pluie. 
                o Hotspot #2 : Zone B (rayon 300 m) - 120 requêtes 311 
                « déneigement » en 2 semaines. 
        c. Tendances 
            L’évolution dans le temps : ça augmente, ça baisse, ça change de nature. 
            • Exemples : 
                o Les collisions piétons augmentent de 18% sur les 3 derniers mois vs 
                la même période l’an passé. 
                o Les requêtes 311 « nids-de-poule » explosent 7 à 10 jours après les 
                cycles gel/dégel. 
                o Le pic horaire se déplace : avant entre 17h et 19h, maintenant entre 
                15h et 17h. 
                • Format attendu : 
                o Période, comparaison (p. ex., semaine vs semaine / mois vs mois), et 
                une phrase d’interprétation. 
        """

    print(prompt)
    response = ollama.generate(model=LANGUAGE_MODEL, prompt=prompt)
    return response["response"]


def ask(question: str):
    global conversation_state

    contexts = retrieve_top_chunks_overall(question)
    contexts =context_converter(contexts)
    results = generate_pandas_with_dataset_selection(
        question,
        contexts,
    )


    results = execute_multi(results)

    answer = explain_cross(
        question,
        results,
        contexts,
    )
    return answer

if __name__ == "__main__":
    q1 = "quelle est le type de collision la plus commune top 5"
    print(ask(q1))





