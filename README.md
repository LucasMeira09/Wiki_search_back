# Wiki Search API (FastAPI + Wikipedia)

## Description
Ce projet est une **API FastAPI** qui :
- recherche des articles sur **Wikipedia (FR)** via l’API officielle,
- récupère un extrait de texte + l’URL de chaque résultat,
- génère un **résumé automatique** (TextRank) à partir des introductions des pages trouvées.

## Stack
- Python
- FastAPI
- Uvicorn
- Requests
- Sumy (TextRank summarizer)
- CORS Middleware

## Fonctionnalités
-  Endpoint `/search` pour rechercher sur Wikipedia
-  Retourne une liste de résultats : `title`, `url`, `snippet`
-  Retourne aussi un résumé global : `summary`
-  CORS activé pour un front en local (Vite)

## Installation
### 1) Créer un environnement virtuel
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Mac/Linux
source .venv/bin/activate
```
### 2) Installer les dépendances
```
pip install fastapi uvicorn requests sumy
```

## Lancer le serveur
```
uvicorn main:app --reload --port 3000
```
