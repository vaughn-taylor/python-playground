from hello import greet

def test_greet_alice():
    assert greet("Alice") == "Hello, Alice! Welcome to your Python project."

def test_greet_bob():
    assert greet("Bob") == "Hello, Bob! Welcome to your Python project."

def test_greet_empty_string():
    assert greet("") == "Hello, ! Welcome to your Python project."

def test_greet_special_characters():
    assert greet("🌟Zelda🌟") == "Hello, 🌟Zelda🌟! Welcome to your Python project."

def test_greet_case_sensitive():
    assert greet("ALICE") == "Hello, ALICE! Welcome to your Python project."
