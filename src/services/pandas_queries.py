import json
import pandas as pd
import ollama
from services.prompts import get_pandas_prompt, get_pandas_prompt_top_5
from services.models import LANGUAGE_MODEL
from services.datasets_info import requetes311, collisions_routieres, meteo_montreal, agency, calendar, calendar_dates, feed_info, routes, shapes, stop_times, stops, trips, translations
from config import DEBUG

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
    mode,
    contexts: dict,
    question: str = None,
    tries = 1
):
    
    prompt= None
    match mode:
        case "analytic":
            prompt = get_pandas_prompt(
                question,
                contexts,
            )
        case "synthesis":
            prompt = get_pandas_prompt_top_5(
                contexts,
            )

    if DEBUG : print(prompt)
    response = ollama.generate(model=LANGUAGE_MODEL, prompt=prompt)
    raw = response["response"].strip()
    if DEBUG: print(raw)

    json_pandas_output = safe_json_loads(raw)

    return recursive_validator(json_pandas_output,mode, contexts, question, tries)

def recursive_validator(json_pandas_output: dict, mode, context, question = None, tries = 1):
    results = {}

    env = {
        "requetes311": requetes311,
        "collisions_routieres": collisions_routieres,
        "meteo_montreal": meteo_montreal,
        "agency": agency,
        "calendar": calendar,
        "calendar_dates": calendar_dates,
        "feed_info": feed_info,
        "routes": routes,
        "shapes": shapes,
        "stop_times": stop_times,
        "stops": stops,
        "trips": trips,
        "translations": translations,
        "pd": pd,
    }

    for key, code in json_pandas_output.items():
        if DEBUG: print(key, code)
        try:
            res = eval(code, env)
            results[key] = {"ok": True, "result": res, "code": code}
        except Exception as e:
            tries = tries+1
            if tries > 3:
                results[key] = {"ok": False, "result": str(e), "code": code}
            else:
                print("request failed")
                return generate_pandas_with_dataset_selection(mode, context, question, tries)
    return results