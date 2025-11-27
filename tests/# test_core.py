# test_core.py
# Basic sanity test to verify environment, imports, and project structure.

def greeting():
    return "WARHEAD SYSTEM: CORE MODULE ONLINE"

def test_greeting():
    message = greeting()
    print(message)
    assert "ONLINE" in message
