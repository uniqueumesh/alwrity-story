# Alwrity - AI Story Writer

An AI Story Writer that generates stories from your inputs. Choose a writer persona, describe setting and characters, and get a narrative in your chosen style and length. Supports **Gemini** and **Groq** backends (Groq has a higher free-tier limit).

**Try it free (no install):** [https://www.alwrity.com/ai-story-writer](https://www.alwrity.com/ai-story-writer) — test the tool in your browser without running anything locally.

## Features

- **Persona selection:** Pick a writer persona or genre (e.g. Science Fiction, Mystery, Romance).
- **Story inputs:** Setting, characters, plot elements, tone, style, POV, audience, and ending preference.
- **Story length:** 1–10 pages (about 300 words per page).
- **Dual backend:** Use **Gemini** or **Groq**; Groq free tier offers more requests per minute.
- **Streamlit UI:** Run locally or deploy on Streamlit Cloud.

## How to run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set an API key

You need at least one of:

- **Gemini:** Get a key from [Google AI Studio](https://aistudio.google.com/apikey). Set `GEMINI_API_KEY`.
- **Groq:** Get a key from [Groq Console](https://console.groq.com/keys). Set `GROQ_API_KEY`.

**Local (PowerShell):**

```powershell
$env:GEMINI_API_KEY = "your-gemini-key"
# or
$env:GROQ_API_KEY = "your-groq-key"
```

**Local (Linux/macOS):**

```bash
export GEMINI_API_KEY="your-gemini-key"
# or
export GROQ_API_KEY="your-groq-key"
```

### 3. Start the app

```bash
streamlit run story_writer.py
```

Open the URL shown in the terminal (e.g. http://localhost:8501). Choose **Gemini** or **Groq** in the app, fill the form, and click **AI, Write a Story..**.

## Streamlit Cloud

1. Push this repo to GitHub and connect it to [Streamlit Cloud](https://streamlit.io/cloud).
2. In the app **Settings → Secrets**, add:

   ```
   GEMINI_API_KEY = "your-gemini-key"
   GROQ_API_KEY = "your-groq-key"
   ```

   (You can set only one if you use just one backend.)
3. Deploy; the app will use the selected backend and the matching key.

## Project structure

| File / folder   | Purpose |
|-----------------|--------|
| `story_writer.py` | Entry point; runs the Streamlit app. |
| `forms.py`        | Story form UI (persona, setting, characters, backend selector, etc.). |
| `ai_story_writer.py` | Story generation flow: prompts → API calls → continuation loop → trim. |
| `api.py`         | API key handling and clients for Gemini and Groq; `generate_with_retry`. |
| `prompts.py`     | Prompt templates and builders (edit here to improve story quality). |
| `config.py`      | Constants, personas, dropdown options, model names. |
| `ui.py`          | Page config, CSS, hide Streamlit chrome. |
| `utils.py`       | Helpers (e.g. `word_count`). |
| `requirements.txt` | Dependencies: `streamlit`, `google-genai`, `groq`, `requests`. |

## Usage tips

1. **Backend:** Groq free tier typically allows more requests per minute than Gemini’s free tier; use Groq if you hit quota limits.
2. **Length:** Shorter stories (fewer pages) use fewer API calls and finish faster.
3. **Prompts:** To tune how stories are written, edit the templates in `prompts.py`.

## License

See repository license (if any). Original idea from [AJaySi/alwrity-story](https://github.com/AJaySi/alwrity-story); this fork includes modular refactor, Groq backend, and prompt/config separation.
