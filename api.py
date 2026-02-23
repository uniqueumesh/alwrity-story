import os
import time
import streamlit as st
from google import genai
from groq import Groq

from config import FALLBACK_MODELS, GROQ_MODEL_NAME


class _TextResponse:
    """Wrapper so callers can use .text for both Gemini and Groq."""

    def __init__(self, text):
        self.text = text or ""


def get_gemini_api_key():
    """Return GEMINI_API_KEY from st.secrets or os.getenv, or None."""
    try:
        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY")


def get_groq_api_key():
    """Return GROQ_API_KEY from st.secrets or os.getenv, or None."""
    try:
        key = st.secrets.get("GROQ_API_KEY")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY")


def get_client(backend="gemini"):
    """
    Return client for the given backend, or None if API key not set.
    backend: "gemini" | "groq"
    """
    if backend == "groq":
        api_key = get_groq_api_key()
        if not api_key:
            return None
        return Groq(api_key=api_key)
    # gemini
    api_key = get_gemini_api_key()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def generate_with_retry(client, prompt, model_name, backend="gemini"):
    """
    Generate text from the model. Returns an object with .text (same for Gemini and Groq).
    backend: "gemini" | "groq"
    """
    if backend == "groq":
        last_error = None
        for attempt in range(2):
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=model_name,
                )
                content = response.choices[0].message.content
                return _TextResponse(content)
            except Exception as e:
                last_error = e
                msg = str(e).upper()
                if ("429" in msg or "503" in msg or "UNAVAILABLE" in msg) and attempt == 0:
                    time.sleep(15)
                    continue
                raise
        raise RuntimeError(f"Groq request failed. Last error: {last_error}")

    # Gemini: try primary then fallback models
    models_to_try = [model_name] + [m for m in FALLBACK_MODELS if m != model_name]
    last_error = None
    for candidate_model in models_to_try:
        try:
            response = client.models.generate_content(
                model=candidate_model,
                contents=prompt,
            )
            return response
        except Exception as e:
            last_error = e
            msg = str(e).upper()
            retryable = (
                "429" in msg
                or "RESOURCE_EXHAUSTED" in msg
                or "503" in msg
                or "UNAVAILABLE" in msg
            )
            if retryable:
                print(f"Model {candidate_model} failed, trying fallback: {e}")
                continue
            raise
    raise RuntimeError(f"All fallback models failed. Last error: {last_error}")
