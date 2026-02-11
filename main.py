# uvicorn main:app --reload --port 3000

import requests
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

class SearchEngine():
    def __init__(self):
        self.api = "https://fr.wikipedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "AppMoteurSearch (contact: lucasdealmeidameira@gmail.com) Python requests",
            "Accept": "application/json",
            "Connect": "keep-alive"
        })
        self.summarizer = TextRankSummarizer()

    def search_wikipedia(self, query, limit=10):

        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "format": "json"
        }

        r = self.session.get(self.api, params=params, timeout=30)
        r.raise_for_status()

        return r.json()["query"]["search"]
    
    def get_text(self, query):
        result = self.search_wikipedia(query)

        id = []
        title = []

        for r in result:
            id.append(r["pageid"])
            title.append(r["title"])

        data = {}

        pageids = [str(r["pageid"]) for r in result]

        params = {
            "action": "query",
            "prop": "extracts|info",
            "explaintext": 1,      # texte brut
            "exintro": 1,
            "redirects": 1,
            "inprop": "url",
            "pageids": "|".join(pageids),
            "format": "json",
        }

        r = self.session.get(self.api, params=params, timeout=30)
        r.raise_for_status()
        
        pages = r.json()["query"]["pages"]

        text_for_resume = ""

        for pageid, page in pages.items():
            title = page.get("title", "Unknown")
            text = page.get("extract", "")
            url = page.get("fullurl", "")

            text_for_resume += text

            data[title] = [url, text[150:]]

        parser = PlaintextParser.from_string(text_for_resume, Tokenizer("french"))
        summary = self.summarizer(parser.document, 3)

        resume = ""
        for sentence in summary:
            resume += str(sentence)

        return data, resume

app = FastAPI()

# CORS: autorise ton front Vite (sinon le navigateur bloque)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


engine_search = SearchEngine()

@app.get("/search")
def search(q: str = Query(..., min_length=1), limit: int = 10):
        dic_page, resume = engine_search.get_text(q)

        results = []
        for title, (url, snippet) in dic_page.items():
            results.append({
                "title": title,
                "url": url,
                "snippet": snippet,
            })

        return {
            "summary": resume,
            "results": results,
        }