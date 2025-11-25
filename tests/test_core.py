from warhead.core import greet

def test_greet():
    assert greet("David") == "Warhead ready, David"
