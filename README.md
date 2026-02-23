# Mobility Copilot - RAG
### Assistant GenAI pour la mobilité urbaine et la sécurité routière à Montréal


## Présentation du Projet
**Mobility Copilot** est un assistant intelligent conçu pour aider la ville de Montréal et ses citoyens à mieux comprendre les enjeux de mobilité et de sécurité.
En s'appuyant sur l'intelligence artificielle générative (GenAI), l'application RAG analyse des données multi-sources pour transformer des chiffres complexes en **insights actionnables** (décisions, priorités, interventions).

Ce projet s'inscrit dans le cadre d'une sélection pour le Hackathon GenAI à Paris. Le sujet s'inspire d'un projet d'Orange proposé l'an dernier sur les rapports d'incidences.


## Qu'est-ce que le RAG ?
Dans le cadre de ce projet, nous utilisons l'architecture **RAG (Retrieval-Augmented Generation)**. 

Le RAG est une technique qui permet à l'intelligence artificielle de "consulter" une base de connaissances spécifique avant de répondre. Au lieu de se fier uniquement à sa mémoire interne (ce qui peut mener à des inventions ou "hallucinations"), l'IA va :
1. **Chercher** l'information pertinente dans un corpus de documents indexés.
2. **Intégrer** ces données réelles (définitions, glossaires, métadonnées) dans sa réflexion.
3. **Générer** une réponse fiable, sourcée et ancrée dans la réalité des données de la Ville de Montréal.

Notre RAG fonctionne comme suit :
- Il identifie les données pertinentes pour répondre à la question posée.
- Le LMM crée une requête Pandas pour collecter ces données pertinentes.
- Il utilise ces données pour répondre à la question posée.


## Fonctionnalités
L'application repose sur trois piliers majeurs :

- **Chat Analytique "Data-Grounded" :** Répond en langage naturel à des questions complexes, comme l'impact de la météo sur les collisions ou l'augmentation des requêtes 311 sous $0^{\circ}$C.
- **Génération de Synthèses Utiles :** 
  - **Briefing hebdomadaire :** Production automatique de rapports.
  - **Top 5 Hotspots :** Identification des 5 zones où les problèmes (collisions, nids-de-poule, déneigement) sont les plus concentrés.
- **Tableau de Bord :** Interface visuelle incluant une heatmap des collisions et un nuage des motifs 311.


## Sources de Données
Le copilote utilise exclusivement des données ouvertes :
* **Requêtes 311 :** Types de demandes, dates et secteurs.
* **Collisions routières :** Localisation, gravité et contexte.
* **Transport collectif (STM) :** Arrêts, lignes et structure du réseau (GTFS).
* **Météo Canada :** Observations historiques (température, précipitations).


## installation et Utilisation

### Étape 1 : cloner le repertoire
```bash
   git clone https://github.com/Styleflo/Ragathon.git
   cd Ragathon
```

### Étape 2 : Créer un environnement python
```bash
  python -m venv venv
  source venv/bin/activate
```

### Étape 3 : Installer les dépendances
```bash
  pip install -r requirements.txt
```

### Étape 4 : Installer Ollama

#### Mac / Linux :
```bash
  curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows : 
```bash
  irm https://ollama.com/install.ps1 | iex
```

### Étape 5 : Installer les modèles d'embedding et de génération
```bash
  ollama pull qwen2.5-coder
  ollama pull bge-m3
```

### Étape 6 : Télécharger les données
```bash
  cd ./src/helper
  python csv_reloader.py
```
Cela crée un dossier data dans le dossier src et ajoute les datasets nécessaires.
Les derniers datasets sont à télécharger [ici](https://drive.google.com/drive/folders/1oFofq2gwn5JJhCBvQEOQleBHtVOwhDt9?usp=sharing).

### Étape 7 : Lancer le projet
```bash
  cd ./src/frontend
  streamlit run ui.py
```
