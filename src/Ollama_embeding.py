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


conversation_state = {
    "last_question": None,
    "last_answer": None,
    "last_dataset_keys": None,
    "last_code_map": None,
    "last_results": None,
    "last_contexts": None
}


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


def is_follow_up(question: str) -> bool:
    prompt = f"""
        You are a classifier.

        User question:
        {question}

        Determine if this question is a FOLLOW-UP to a previous one.
        Return ONLY "yes" or "no".
        """
    response = ollama.generate(model="gemma3:4b", prompt=prompt)
    return response["response"].strip().lower() == "yes"


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
    previous_question: str | None = None,
    previous_answer: str | None = None
):

    if previous_question and previous_answer:
        followup_block = f"""
            This is a FOLLOW-UP question.

            Previous user question:
            {previous_question}

            Previous assistant answer:
            {previous_answer}
            """
    else:
        followup_block = "This is an INDEPENDENT question (not a follow-up)."
        

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
        You are a multi-dataset data assistant.

        {followup_block}

         Here are the available datasets, each with:
        - its dataset key
        - its dataframe name
        - its retrieved context (column descriptions, semantics)

        DATASETS (JSON):
        {json.dumps(datasets_block, indent=2, ensure_ascii=False)}

        Current user question:
        {question}

        Return ONLY a JSON object:
        - "datasets": list of dataset keys
        - "code": mapping dataset_key → pandas expression

        Your tasks:
        1. Decide which datasets are relevant to the question.
        2. For each relevant dataset, generate a pandas expression using the correct dataframe name.
        3. If this is a follow-up, REUSE the relevant filters from the previous answer when appropriate
        4. Only use columns that exist whithin the dataset column list.
        5. NEVER mix columns from different datasets.
        6. ALWAYS return full pandas expressions.

        Contrainte:
        The code MUST be valid Python using pandas. Absolutely NO R syntax, NO tidyverse
        ONLY return an output if the corresponding dataset is relevant.

         Example output:
        {{
        "datasets": ["requetes311"],
        "code": {{
            "requetes311": "df_requetes311[df_requetes311['ACTI_NOM'] == 'Organisme divers']"
        }}
        }}
        """

    response = ollama.generate(model="gemma3:4b", prompt=prompt)
    raw = response["response"].strip()
    print(raw)
    print(contexts)

    return safe_json_loads(raw)

def normalize_code_map(result):
    datasets_list = result.get("datasets", [])
    code_block = result.get("code")

    if isinstance(code_block, dict):
        return code_block

    if isinstance(code_block, str):
        if len(datasets_list) != 1:
            raise ValueError("LLM returned a single code string but multiple datasets were selected.")
        return {datasets_list[0]: code_block}

    raise ValueError(f"Invalid code format returned by LLM: {code_block}")



def execute_multi(code_map: dict):
    results = {}

    env = {
        "df_requetes311": df_requetes311,
        "df_collisions_routieres": df_collisions_routieres,
        "pd": pd,
    }

    for key, code in code_map.items():
        try:
            res = eval(code, env)
            results[key] = {"ok": True, "result": res, "code": code}
        except Exception as e:
            results[key] = {"ok": False, "error": str(e), "code": code}
            

    return results


def explain_cross(
    question: str,
    results: dict,
    dataset_keys,
    contexts: dict,
    previous_question: str | None = None,
    previous_answer: str | None = None
):

    previews = []
    for key in dataset_keys:
        info = results.get(key)
        if not info:
            continue

        if not info["ok"]:
            previews.append(f"Dataset {key} FAILED with error: {info['error']}")
        else:
            df_res = info["result"]
            if hasattr(df_res, "head"):
                preview = df_res.head(10).to_string()
            else:
                preview = str(df_res)

            previews.append(f"Dataset: {key}\nCode: {info['code']}\nPreview:\n{preview}")

    previews_text = "\n\n====\n\n".join(previews)

    if previous_question and previous_answer:
        followup_block = f"""
            Cette question est un SUIVI (follow-up).

            Question précédente :
            {previous_question}

            Réponse précédente :
            {previous_answer}

            Tu dois interpréter la nouvelle question à la lumière de cette interaction précédente,
            et préciser clairement comment les nouveaux résultats se comparent ou se rattachent aux précédents.
            """
    else:
        followup_block = "Cette question est indépendante."

    prompt = f"""
        Tu es un assistant analytique.

        {followup_block}

        Contexte des jeux de données :
        {json.dumps(contexts, indent=2, ensure_ascii=False)}

        Question actuelle :
        {question}

        Résultats :
        {previews_text}

        Tâche :
        1. Ne rejoute pas d'information, répond aussi précisément que possible et le plus bref possible.
        2. Si c'est un suivi, explique explicitement le lien avec la réponse précédente
        3. Ajoute ensuite une section intitulée : "Limites / risques d’interprétation "
        - Mentionne les hypothèses fragiles, les biais possibles, les limites des données.
        4. Ajoute enfin une section : "Ce que je vérifierais ensuite"
        - Propose des validations, tests, croisements de données ou analyses complémentaires.

        Contrainte:
        - Tu ne peux pas inventer de chiffres, tout doit provenir des données.
        - Ne réfère jamais au nom du dataset utilisé directement.
        - La réponse DOIT être cohérente avec la question.

        Respecte strictement ce format :

        ### Analyse
        (réponse analytique)

        ### Limites / risques d’interprétation
        (critique)

        ### Ce que je vérifierais ensuite
        (suite logique)
        """

    response = ollama.generate(model="gemma3:4b", prompt=prompt)
    return response["response"]


def handle_follow_up(question: str):
    global conversation_state

    previous_question = conversation_state["last_question"]
    previous_answer = conversation_state["last_answer"]

    contexts = retrieve_all_datasets(question)

    result = generate_pandas_with_dataset_selection(
        question,
        contexts,
        previous_question=previous_question,
        previous_answer=previous_answer
    )

    dataset_keys = result["datasets"]
    code_map = normalize_code_map(result)

    results = execute_multi(code_map)

    answer = explain_cross(
        question,
        results,
        dataset_keys,
        contexts,
        previous_question=previous_question,
        previous_answer=previous_answer
    )

    conversation_state.update({
        "last_question": question,
        "last_answer": answer,
        "last_dataset_keys": dataset_keys,
        "last_code_map": code_map,
        "last_results": results,
        "last_contexts": contexts
    })

    return answer


def ask(question: str):
    global conversation_state

    if is_follow_up(question) and conversation_state["last_question"] is not None:
        print("Detected follow-up question.")
        return handle_follow_up(question)

    contexts = retrieve_all_datasets(question)

    result = generate_pandas_with_dataset_selection(
        question,
        contexts,
        previous_question=None,
        previous_answer=None
    )

    dataset_keys = result["datasets"]
    code_map = normalize_code_map(result)

    results = execute_multi(code_map)
    for k, v in results.items():
        print(f"[{k}] ok={v['ok']}")

    answer = explain_cross(
        question,
        results,
        dataset_keys,
        contexts,
        previous_question=None,
        previous_answer=None
    )

    conversation_state.update({
        "last_question": question,
        "last_answer": answer,
        "last_dataset_keys": dataset_keys,
        "last_code_map": code_map,
        "last_results": results,
        "last_contexts": contexts
    })

    return answer

if __name__ == "__main__":
    q1 = "en quelle année y a t'il eu le plus de bicyclette dans des accidents?"
    print(ask(q1))

    q2 = "y a t'il eu une tendance à la hausse pour le nombre de bicyclette?"
    print(ask(q2))





