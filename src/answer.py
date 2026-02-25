import ollama
from services.chunking_embeding import retrieve_top_chunks_overall, context_converter
from services.pandas_queries import generate_pandas_with_dataset_selection
from services.models import LANGUAGE_MODEL
from services.prompts import get_answer_prompt, get_answer_chat, get_answer_prompt_top_5
from services.prompt_router import classifier_requete
from services.datasets_info import get_datasets_metadata



def explain_cross(
    question: str,
    results: dict,
    contexts: dict,
):
    prompt = get_answer_prompt(
        question,
        contexts,
        results
    )

    print(prompt)
    response = ollama.generate(model=LANGUAGE_MODEL, prompt=prompt)
    return response["response"]


def ask(question: str):

    classe = classifier_requete(question)

    if classe == "RAG" :
        contexts = retrieve_top_chunks_overall(question)
        contexts =context_converter(contexts)
        results = generate_pandas_with_dataset_selection(
            "analytic",
            contexts,
            question,
        )

        answer = explain_cross(
            question,
            results,
            contexts,
        )

    elif classe == "CHAT":
        prompt = get_answer_chat(question)
        response = ollama.generate(model=LANGUAGE_MODEL, prompt=prompt)
        answer = response["response"]

    else:
        answer = "Un problème est survenue"

    return answer

def get_top5():

    contexts = get_datasets_metadata()

    print(contexts)

    results = generate_pandas_with_dataset_selection(
        "synthesis",
        contexts,
    )


    prompt = get_answer_prompt_top_5(contexts, results)

    print (prompt)
    response = ollama.generate(model=LANGUAGE_MODEL, prompt=prompt)
    return response["response"]

if __name__ == "__main__":
    q1 = "Salut, comment ça fonctionne ?"
    print(get_top5())
