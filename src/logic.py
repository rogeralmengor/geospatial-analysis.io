import wikipedia  # type: ignore


def wiki(name:str="War Goddess", length:int=1) -> str:
    """This is a wikipedia fetcher."""

    return wikipedia.summary(name, length)


def search_wiki(name:str)->str:
    """Search Wikipedia by Names."""
    return wikipedia.search(name)