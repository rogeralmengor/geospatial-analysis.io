import wikipedia # type: ignore


def wiki(name="War Goddess", length=1)->str:
    """This is a wikipedia fetcher."""

    return wikipedia.summary(name, length)
