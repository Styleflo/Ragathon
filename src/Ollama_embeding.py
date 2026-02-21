import chromadb
import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd
import json

datasets = {
    "requetes311": {
        "df": pd.read_csv("data/requetes311.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path="db_requetes311").get_or_create_collection("requetes311_rag"),
        "description_file": "corpus/requetes311.txt"
    },
    "collisions_routieres": {
        "df": pd.read_csv("data/collisions_routieres.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path="db_collisions_routieres").get_or_create_collection("collisions_routieres_rag"),
        "description_file": "corpus/collisions_routieres.txt"
    }
}

df_requetes311 = datasets["requetes311"]["df"]
df_collisions_routieres = datasets["collisions_routieres"]["df"]


def embed(text: str):
    response = ollama.embed(model="nomic-embed-text", input=text)
    return response["embeddings"][0]


splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

for key, info in datasets.items():
    collection = info["collection"]
    if collection.count() > 0:
        continue

    with open(info["description_file"], "r", encoding="utf-8") as f:
        text = f.read()

    chunks = splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"{key}_chunk_{i}"],
            documents=[chunk],
            embeddings=[embed(chunk)]
        )


def retrieve(question: str, dataset_key: str):
    collection = datasets[dataset_key]["collection"]
    query_emb = embed(question)

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=3
    )

    return [doc for sublist in results["documents"] for doc in sublist]


def retrieve_all_datasets(question: str):
    contexts = {}
    for key in datasets.keys():
        docs = retrieve(question, key)
        contexts[key] = "\n\n".join(docs)
    return contexts


def safe_json_loads(raw: str):

    if not raw or not raw.strip():
        raise ValueError("LLM returned empty output instead of JSON.")

    cleaned = raw.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if "\n" in cleaned:
            cleaned = cleaned.split("\n", 1)[1]

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    try:
        start = cleaned.index("{")
        end = cleaned.rindex("}") + 1
        return json.loads(cleaned[start:end])
    except Exception:
        print(raw)
        raise ValueError("LLM returned invalid JSON and could not be recovered.")
    

def generate_pandas_with_dataset_selection(
    question: str,
    contexts: dict,
):

    datasets_block = {
        "requetes311": {
            "dataframe": "df_requetes311",
            "columns": list(df_requetes311.columns),
            "context": contexts.get("requetes311", "")
        },
        "collisions_routieres": {
            "dataframe": "df_collisions_routieres",
            "columns": list(df_collisions_routieres.columns),
            "context": contexts.get("collisions_routieres", "")
        }
    }

    prompt = f"""
        You are a python/pandas query generator.

        Your goal:
        Generate ALL pandas queries needed to fully answer the user’s question.

        COLUMN FAMILY RULE:
            If the question refers to a category (e.g., “types of vehicles”, “types of transport”, “types of locations”, etc.), 
            you MUST identify ALL columns in the dataset that belong to that category.

            A column belongs to a category if:
            - its name contains a shared prefix (e.g., nb_*)
            - its description indicates it is part of the same conceptual group
            - it measures a subtype of the same concept

            For each column in the category, you MUST generate at least one query.
            You MUST NOT invent aggregate columns (e.g., NB_VEH_IMPLIQUES_ACCDN).
            You MUST enumerate each real column individually.

        STRICT RULES:
            1. You may ONLY use the datasets and columns explicitly provided.
            2. You MUST NOT invent or guess column names.
            3. You MUST NOT use a dataset if none of its columns relate to the question.
            4. You MUST output ONLY a flat JSON dictionary:
            {{
                "dataset_query_1": "pandas_expression",
                "dataset_query_2": "pandas_expression"
            }}
            5. Each value MUST be a single pandas expression.
            6. You MUST NOT output lists, nested structures, explanations, or comments.

        How to determine relevance:
            1. A dataset is relevant if ANY of its columns semantically match a concept in the question.
            2. A column is relevant if its meaning overlaps with a concept in the question.
            3. If multiple columns match, you MUST generate one query PER COLUMN.
            4. You MUST NOT stop after the first relevant column.

        How to generate enough queries:
        For EACH core component of the question:
            1. Identify ALL relevant datasets.
            2. Identify ALL relevant columns in those datasets.
            3. For EACH relevant column, generate MULTIPLE analytical queries:
            - distribution (value counts, top/bottom)
            - grouping (e.g., by year, by arrondissement, by type)
            - trends over time (if a time column exists)
            - correlations (if multiple relevant numeric columns exist)
            - comparisons (if multiple categories exist)
            4. You MUST generate as many queries as needed to fully cover the question.
            5. You MUST be exhaustive and thorough.
            6. Do NOT stop at the simplest query.

        Guide to operate:
            1. Break the question into core components.
            2. For each component, explore ALL relevant datasets.
            3. For each dataset, explore ALL relevant columns.
            4. For each column, generate multiple queries covering different analytical angles.

        You can use this context to guide your decisions:
        {datasets_block}

        Current user question:
        {question}

        Your output MUST follow this exact schema:
        {{
            "dataset_key_1_query_1": "pandas_expression",
            "dataset_key_1_query_2": "pandas_expression",
            "dataset_key_2_query_1": "pandas_expression"
        }}
        """

    print(prompt)
    response = ollama.generate(model="gemma3:4b", prompt=prompt)
    raw = response["response"].strip()
    print(raw)

    return safe_json_loads(raw)



def execute_multi(code_map: dict):
    results = {}

    env = {
        "df_requetes311": df_requetes311,
        "df_collisions_routieres": df_collisions_routieres,
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
    response = ollama.generate(model="gemma3:4b", prompt=prompt)
    return response["response"]


def ask(question: str):
    global conversation_state

    contexts = retrieve_all_datasets(question)

    results = generate_pandas_with_dataset_selection(
        question,
        contexts,
    )


    results = execute_multi(results)
    for k, v in results.items():
        print(f"[{k}] ok={v['ok']}")

    answer = explain_cross(
        question,
        results,
        contexts,
    )
    return answer

if __name__ == "__main__":
    q1 = "quelle est le top 5 des locations des accidents de voiture et quelle est le top 5 des types de moyen de transport impliquer dans des accidents"
    print(ask(q1))





