import ollama
from services.chunking_embeding import retrieve_top_chunks_overall, context_converter
from services.pandas_queries import generate_pandas_with_dataset_selection
from services.models import LANGUAGE_MODEL
from services.prompts import get_answer_prompt


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
    return answer

if __name__ == "__main__":
    q1 = "quelle est le type de collision la plus commune top 5"
    print(ask(q1))





