import re


def word_count(text):
    """Return number of words in text."""
    return len(re.findall(r'\w+', text))
