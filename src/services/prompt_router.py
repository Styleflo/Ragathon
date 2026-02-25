import ollama
from services.models import LANGUAGE_MODEL


def classifier_requete(user_query):
    prompt = f"""
    Système: Tu es un classifieur d'intention ultra-rapide.
    Règles: 
    - Réponds 'RAG' si la question demandé concerne:
        * les collisions routières et accidents à Montréal.
        * l'ensemble des spécifications techniques du flux GTFS de la Société de transport de Montréal (STM), détaillant les structures des tables (agences, arrêts, lignes, trajets et horaires) nécessaires à la modélisation complète du réseau de transport collectif.
        * les requêtes et plaintes de la route géré par le service 311 de Montréal, détaillant la nature des requêtes (information, commentaire, requête ou plainte), leur provenance multicanale, leur localisation géographique et leur état de traitement.
    - Réponds 'CHAT' si c'est une salutation, un remerciement ou du bavardage ou tout autre question.

    Requête: "{user_query}"
    Classification (un seul mot):"""

    try:
        response = ollama.generate(
            model=LANGUAGE_MODEL,
            prompt=prompt,
            options={
                "temperature": 0,
                "num_predict": 5,
                "stop": ["\n"]
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
        "combien y a t il eu de requetes 311 en 2025 liée aux motos ?",

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
