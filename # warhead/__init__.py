# warhead/__init__.py
@'
"""Warhead core package - minimal stub for development."""
__version__ = "0.0.1"
'@ | Out-File -FilePath .\warhead\__init__.py -Encoding utf8

# warhead/core.py (simple logic to test)
@'
def greet(name: str) -> str:
    """Small function to test."""
    return f"Warhead ready, {name}"
'@ | Out-File -FilePath .\warhead\core.py -Encoding utf8

# tests/test_core.py (pytest test)
@'
from warhead.core import greet

def test_greet():
    assert greet("David") == "Warhead ready, David"
'@ | Out-File -FilePath .\tests\test_core.py -Encoding utf8
