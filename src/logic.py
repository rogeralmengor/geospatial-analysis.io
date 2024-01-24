import wikipedia  # type: ignore
from textblob import TextBlob # type: ignore

def wiki(name:str="War Goddess", length:int=1) -> str:
    """This is a wikipedia fetcher."""

    return wikipedia.summary(name, length)

def phrase(name:str): 
    """Returns phrases from wikipedia."""
    return TextBlob(wiki(name)).noun_phrases


def search_wiki(name:str)->str:
    """Search Wikipedia by Names."""
    return wikipedia.search(name)