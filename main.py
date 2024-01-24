from fastapi import FastAPI 
import uvicorn 
from src.logic import wiki as wikilogic 
from src.logic import search_wiki
from src.logic import phrase as wikiphrases
app = FastAPI()

@app.get("/")
async def root(): 
    return {"message": "Wikipedia API. Call /search or /wiki"}

@app.get("/search/{value}")
async def search(value: str)->dict: 
    """Page to search in wikipedia."""
    return {"results": search_wiki(value)}

@app.get("/wiki/{name}")
async def wiki(name: str)->dict: 
    """Retrieve wikipedia page."""
    return {"results": wikilogic(name)}

@app.get("/phrase/{name}")
async def phrase(name: str): 
    """Retrieve wikipedia page phrase"""
    return {"result": wikiphrases(name)}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
