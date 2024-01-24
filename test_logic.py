from src.logic import wiki


def test_wiki() -> None:
    assert "god" in wiki()
