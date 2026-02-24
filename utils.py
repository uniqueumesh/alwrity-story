import re


def word_count(text):
    """Return number of words in text."""
    return len(re.findall(r'\w+', text))


def trim_to_complete_sentences(text, max_words):
    """Trim text to at most max_words, ending at the last complete sentence."""
    if not text or max_words <= 0:
        return text
    words = text.split()
    if len(words) <= max_words:
        return text
    truncated = ' '.join(words[:max_words])
    # Split on sentence boundaries (after . ! ?)
    parts = re.split(r'(?<=[.!?])\s+', truncated)
    complete = [p for p in parts if re.search(r'[.!?]["\']?$', p.strip())]
    if complete:
        return ' '.join(complete)
    return truncated


def format_story_paragraphs(text, sentences_per_paragraph=3):
    """Format story into short paragraphs of about N sentences each for readability."""
    if not text or not text.strip():
        return text
    text = text.strip()
    # Split into sentences (after . ! ?)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return text
    result = []
    for i in range(0, len(sentences), sentences_per_paragraph):
        chunk = sentences[i:i + sentences_per_paragraph]
        result.append(' '.join(chunk))
    return '\n\n'.join(result)
