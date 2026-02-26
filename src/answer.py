import ollama
from services.chunking_embeding import retrieve_top_chunks_overall, context_converter
from services.pandas_queries import generate_pandas_with_dataset_selection
from services.models import LANGUAGE_MODEL
from services.prompts import get_answer_prompt, get_answer_chat, get_answer_prompt_top_5
from services.prompt_router import classifier_requete
from services.prompts import get_answer_prompt
from config import DEBUG
from services.datasets_info import get_datasets_metadata


def format_history(history: list[tuple[str, str]]) -> str:
    """Format conversation history for the prompt."""
    if not history:
        return ""
    
    formatted = []
    for role, content in history:
        prefix = "Utilisateur" if role == "user" else "Assistant"
        formatted.append(f"{prefix}: {content}")
    
    return "\n".join(formatted)

def explain_cross(
    question: str,
    results: dict,
    contexts: dict,
    history: list[tuple[str, str]] = None,
):
    prompt = get_answer_prompt(
        question,
        contexts,
        results
    )
    
    # Add conversation history if present
    if history:
        history_text = format_history(history)
        prompt = f"""Historique de la conversation:
{history_text}

{prompt}"""

    if DEBUG: print(prompt)
    response = ollama.generate(model=LANGUAGE_MODEL, prompt=prompt)
    return response["response"]


def ask(question: str, history: list[tuple[str, str]] = None):
    """Answer a question with optional conversation history.
    
    Args:
        question: The user's current question
        history: List of (role, content) tuples representing conversation history
    """
    if history is None:
        history = []

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
            history,
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
    print("Mobility Copilot - Mode interactif")
    print("Tapez 'quit' pour quitter\n")
    
    history = []
    while True:
        question = input("Vous: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue
        
        response = ask(question, history)
        print(f"\nAssistant: {response}\n")
        
        history.append(("user", question))
        history.append(("assistant", response))