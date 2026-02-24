#####################################################
#
# google-gemini-cookbook - Story_Writing_with_Prompt_Chaining
#
#####################################################

import streamlit as st

from api import get_client, generate_with_retry
from config import DEFAULT_MODEL_NAME, GROQ_MODEL_NAME, WORDS_PER_PAGE
from prompts import (
    build_story_persona,
    get_premise_prompt,
    get_outline_prompt,
    get_starting_prompt,
    get_continuation_prompt,
)
from utils import word_count, trim_to_complete_sentences, format_story_paragraphs


def ai_story_generator(persona, story_setting, character_input,
                       plot_elements, writing_style, story_tone, narrative_pov,
                       audience_age_group, content_rating, ending_preference, page_length=3,
                       backend="gemini"):
    """
    Write a story using prompt chaining and iterative generation.

    Parameters:
        persona: Persona statement for the author.
        story_setting: Setting, location, and time period.
        character_input: Character names, descriptions, roles.
        plot_elements: Theme, key events, main conflict.
        writing_style: e.g. Formal, Casual, Poetic, Humorous.
        story_tone: e.g. Dark, Uplifting, Suspenseful, Whimsical.
        narrative_pov: First/Third person perspective.
        audience_age_group: e.g. Children, Young Adults, Adults.
        content_rating: e.g. G, PG, PG-13, R.
        ending_preference: e.g. Happy, Tragic, Cliffhanger, Twist.
        page_length: Number of pages (default 3).
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

        client = get_client(backend)
        if client is None:
            key_name = "GROQ_API_KEY" if backend == "groq" else "GEMINI_API_KEY"
            st.error(f"API key not set. Add {key_name} in Streamlit Cloud Secrets or set the environment variable.")
            return
        model_name = GROQ_MODEL_NAME if backend == "groq" else DEFAULT_MODEL_NAME

        # Generate prompts
        try:
            premise = generate_with_retry(client, premise_prompt, model_name, backend).text
            st.info(f"The premise of the story is: {premise}")
        except Exception as err:
            st.error(f"Premise Generation Error: {err}")
            return

        outline = generate_with_retry(client, outline_prompt.format(premise=premise), model_name, backend).text
        with st.expander("🧙‍♂️ Click to Checkout the outline, writing still in progress..", expanded=True):
            st.markdown(f"The Outline of the story is: {outline}\n\n")
        
        if not outline:
            st.error("Failed to generate outline. Exiting...")
            return

        # Generate starting draft
        with st.status("🦸Story Writing in Progress..", expanded=True) as status:
            try:
                starting_draft = generate_with_retry(
                    client, starting_prompt.format(premise=premise, outline=outline), model_name, backend
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
                    backend,
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
                        backend,
                    ).text
                    draft += '\n\n' + continuation
                except Exception as err:
                    st.error(f"Failed to continually write the story: {err}")
                    return
            status.update(label=f"✔️  Story Completed ✔️ ... Scroll Down for the story.")

        # Remove 'IAMDONE' and trim to target word count at a sentence boundary
        final = draft.replace('IAMDONE', '').strip()
        words = final.split()
        if len(words) > target_words:
            final = trim_to_complete_sentences(final, target_words)
        final = format_story_paragraphs(final)
        return final

    except Exception as e:
        st.error(f"Main Story writing: An error occurred: {e}")
