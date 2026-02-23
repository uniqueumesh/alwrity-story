#####################################################
#
# google-gemini-cookbook - Story_Writing_with_Prompt_Chaining
#
#####################################################

import os
from pathlib import Path
from google import genai
import streamlit as st

from config import DEFAULT_MODEL_NAME, FALLBACK_MODELS, WORDS_PER_PAGE
from prompts import (
    build_story_persona,
    get_premise_prompt,
    get_outline_prompt,
    get_starting_prompt,
    get_continuation_prompt,
)
from utils import word_count


def generate_with_retry(client, prompt, model_name):
    """
    Generates content from the model with retry handling for errors.

    Parameters:
        client (genai.Client): The Gemini client to use for content generation.
        prompt (str): The prompt to generate content from.
        model_name (str): The Gemini model name to use.

    Returns:
        str: The generated content.
    """
    models_to_try = [model_name] + [m for m in FALLBACK_MODELS if m != model_name]
    last_error = None

    for candidate_model in models_to_try:
        try:
            return client.models.generate_content(
                model=candidate_model,
                contents=prompt,
            )
        except Exception as e:
            last_error = e
            msg = str(e).upper()
            # Retry with fallback model only for quota/availability issues.
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


def ai_story_generator(persona, story_setting, character_input, 
                       plot_elements, writing_style, story_tone, narrative_pov,
                       audience_age_group, content_rating, ending_preference, page_length=3):
    """
    Write a story using prompt chaining and iterative generation.

    Parameters:
        persona (str): The persona statement for the author.
        story_genre (str): The genre of the story.
        characters (str): The characters in the story.
    """
    st.info(f"""
        You have chosen to create a story set in **{story_setting}**. 
        The main characters are: **{character_input}**.
        The plot will revolve around the theme of **{plot_elements}**.
        The story will be written in a **{writing_style}** style with a **{story_tone}** tone, from a **{narrative_pov}** perspective. 
        It is intended for a **{audience_age_group}** audience with a **{content_rating}** rating. 
        You prefer the story to have a **{ending_preference}** ending.
        Story length: **{page_length}** pages (about {page_length * WORDS_PER_PAGE} words).
        """)
    try:
        target_words = page_length * WORDS_PER_PAGE
        persona_full = build_story_persona(
            persona, story_setting, character_input, plot_elements,
            writing_style, story_tone, narrative_pov, audience_age_group,
            content_rating, ending_preference,
        )
        premise_prompt = get_premise_prompt(persona_full, story_setting, character_input)
        outline_prompt = get_outline_prompt(persona_full)
        initial_words = min(2000, target_words)
        starting_prompt = get_starting_prompt(persona_full, initial_words, target_words)
        continuation_prompt = get_continuation_prompt(persona_full, target_words)

        # Initialize Gemini client (st.secrets on Cloud, env var locally)
        api_key = None
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("API key not set. Add GEMINI_API_KEY in Streamlit Cloud Secrets or set the environment variable.")
            return
        client = genai.Client(api_key=api_key)
        model_name = DEFAULT_MODEL_NAME

        # Generate prompts
        try:
            premise = generate_with_retry(client, premise_prompt, model_name).text
            st.info(f"The premise of the story is: {premise}")
        except Exception as err:
            st.error(f"Premise Generation Error: {err}")
            return

        outline = generate_with_retry(client, outline_prompt.format(premise=premise), model_name).text
        with st.expander("🧙‍♂️ Click to Checkout the outline, writing still in progress..", expanded=True):
            st.markdown(f"The Outline of the story is: {outline}\n\n")
        
        if not outline:
            st.error("Failed to generate outline. Exiting...")
            return

        # Generate starting draft
        with st.status("🦸Story Writing in Progress..", expanded=True) as status:
            try:
                starting_draft = generate_with_retry(
                    client, starting_prompt.format(premise=premise, outline=outline), model_name
                ).text
                status.update(label=f"🪂 Current draft length: {len(starting_draft)} characters")
            except Exception as err:
                st.error(f"Failed to Generate Story draft: {err}")
                return False

            try:
                draft = starting_draft
                continuation = generate_with_retry(
                    client,
                    continuation_prompt.format(premise=premise, outline=outline, story_text=draft),
                    model_name,
                ).text
                status.update(label=f"🏄 Current draft length: {len(continuation)} characters")
            except Exception as err:
                st.error(f"Failed to write the initial draft: {err}")

            # Add the continuation to the initial draft, keep building the story until we see 'IAMDONE'
            try:
                draft += '\n\n' + continuation
                status.update(label=f"Current draft length: {len(draft)} characters")
            except Exception as err:
                st.error(f"Failed as: {err} and {continuation}")
        
            while 'IAMDONE' not in continuation and word_count(draft) < target_words:
                try:
                    status.update(label=f"⏳ Writing... {word_count(draft)} / {target_words} words")
                    continuation = generate_with_retry(
                        client,
                        continuation_prompt.format(premise=premise, outline=outline, story_text=draft),
                        model_name,
                    ).text
                    draft += '\n\n' + continuation
                except Exception as err:
                    st.error(f"Failed to continually write the story: {err}")
                    return
            status.update(label=f"✔️  Story Completed ✔️ ... Scroll Down for the story.")

        # Remove 'IAMDONE' and trim to target word count
        final = draft.replace('IAMDONE', '').strip()
        words = final.split()
        if len(words) > target_words:
            final = ' '.join(words[:target_words])
        return final

    except Exception as e:
        st.error(f"Main Story writing: An error occurred: {e}")
