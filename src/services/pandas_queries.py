import json
import pandas as pd
import ollama
from services.prompts import get_pandas_prompt
from services.models import LANGUAGE_MODEL
from services.datasets_info import requetes311, collisions_routieres, gtfs_stm, meteo_montreal

def safe_json_loads(raw: str):

    if not raw or not raw.strip():
        raise ValueError("LLM returned empty output instead of JSON.")

    cleaned = raw.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if "\n" in cleaned:
            cleaned = cleaned.split("\n", 1)[1]
    
    return json.loads(cleaned)


def generate_pandas_with_dataset_selection(
    question: str,
    contexts: dict,
    tries = 1
):

    prompt = get_pandas_prompt(
        question,
        contexts,
    )

    print(prompt)
    response = ollama.generate(model=LANGUAGE_MODEL, prompt=prompt)
    raw = response["response"].strip()
    print(raw)

    json_pandas_output = safe_json_loads(raw)

    return recursive_validator(json_pandas_output, question, contexts, tries)

def recursive_validator(json_pandas_output: dict, question, context, tries = 1):
    results = {}

    env = {
        "requetes311": requetes311,
        "collisions_routieres": collisions_routieres,
        "gtfs_stm": gtfs_stm,
        "meteo_montreal": meteo_montreal,
        "pd": pd,
    }

    for key, code in json_pandas_output.items():
        print(key, code)
        try:
            res = eval(code, env)
            results[key] = {"ok": True, "result": res, "code": code}
        except Exception as e:
            tries = tries+1
            if tries > 3:
                results[key] = {"ok": False, "result": str(e), "code": code}
            else:
                return generate_pandas_with_dataset_selection(question, context, tries)
    return results