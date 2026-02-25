import ollama
from services.chunking_embeding import retrieve_top_chunks_overall, context_converter
from services.pandas_queries import generate_pandas_with_dataset_selection
from services.models import LANGUAGE_MODEL
from services.prompts import get_answer_prompt, get_answer_chat
from services.prompt_router import classifier_requete


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
            question,
            contexts,
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

if __name__ == "__main__":
    q1 = "Salut, comment ça fonctionne ?"
    print(ask(q1))
