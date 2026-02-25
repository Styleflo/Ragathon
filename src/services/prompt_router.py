import ollama
from services.models import LANGUAGE_MODEL


def classifier_requete(user_query):
    # Prompt optimisé pour Gemma 3 (très direct)
    prompt = f"""
    Système: Tu es un classifieur d'intention ultra-rapide.
    Règles: 
    - Réponds 'RAG' si la question demandé concerne la mobilité urbaine et la sécurité routière à Montréal.
    - Réponds 'CHAT' si c'est une salutation, un remerciement ou du bavardage ou tout autre question.

    Requête: "{user_query}"
    Classification (un seul mot):"""

    try:
        response = ollama.generate(
            model=LANGUAGE_MODEL,
            prompt=prompt,
            options={
                "temperature": 0,  # Pour la stabilité
                "num_predict": 5,  # Pour la vitesse (limite la réponse à 5 tokens)
                "stop": ["\n"]  # S'arrête dès qu'il passe à la ligne
            }
        )

        # Nettoyage de la réponse
        resultat = response['response'].strip().upper()

        if "RAG" in resultat:
            return "RAG"
        else:
            return "CHAT"


    except Exception as e:
        print(f"Erreur : {e}")
        return "ERREUR"


if __name__ == "__main__":
    questions = test_batch = [
        # --- CATÉGORIE RAG (Mobilité & Sécurité Montréal) ---
        "Quelles sont les intersections les plus dangereuses sur le Plateau ?",
        "Donne-moi les stats de collisions entre vélos et autos en 2023.",
        "Quelle est la limite de vitesse autorisée sur la rue Sainte-Catherine ?",
        "Peux-tu m'expliquer le plan Vision Zéro de la ville de Montréal ?",
        "Y a-t-il eu une augmentation des pistes cyclables à Rosemont ?",
        "Quel est l'impact des saillies de trottoir sur la sécurité des piétons ?",
        "Combien de décès routiers ont été recensés l'an dernier à Montréal ?",
        "Liste les projets de rues partagées prévus pour cet été.",
        "Est-ce que le radar photo sur Notre-Dame est efficace ?",
        "Comment la ville sécurise-t-elle les zones scolaires ?",

        # --- CATÉGORIE CHAT (Hors sujet ou bavardage) ---
        "Salut, tu peux m'aider ?",
        "Quel temps fait-il au centre-ville de Montréal ?",
        "Comment est le trafic sur le pont de Québec ?",
        "Merci pour tes réponses précédentes !",
        "Qui est l'actuelle mairesse de Montréal ?",
        "Je cherche une bonne poutine près du métro Berri-UQAM.",
        "Comment on répare un pneu de vélo crevé ?",
        "Raconte-moi une blague sur les cônes oranges.",
        "Quelles sont les règles de sécurité routière à Toronto ?",
        "C'est quoi la définition d'un algorithme RAG ?",
        "combien y a t il eu d'accidents de camions à Montréal ?"
    ]
    for q in questions:
        action = classifier_requete(q)
        print(f"[{q}] -> Action : {action}")
