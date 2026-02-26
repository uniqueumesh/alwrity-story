"""
Story-generation prompt templates and builders.
Edit prompts here to improve results without changing generation logic.
"""

WRITING_GUIDELINES = """\
Writing Guidelines:

Engagement: Open with a hook—a striking image, a line of dialogue, or a moment of
action or tension. Avoid slow, generic openings like "Once upon a time" or long
setting dumps before something happens. Keep the reader curious: every scene should
have a want, a question, or a stake. Move the story forward; avoid long stretches
where nothing changes. Include conflict or tension early and carry it through; even
quiet stories need a central question or obstacle.

Craft: Show, don't just tell—use concrete actions, sensory details, and dialogue
instead of stating feelings or traits (e.g. prefer "She slammed the door" over "She
was angry"). Vary sentence length: mix short punchy lines with longer ones,
especially in moments of action or emotion. Be specific: use concrete images and
details rather than vague words like "beautiful," "interesting," or "very." Avoid
repeating the same idea in different words; each paragraph should add new
information or deepen the scene.

Character and plot: Develop characters through their actions and choices. Weave in
the outline but allow surprises. Use rich imagery and sensory detail. Plant
subplots subtly; avoid boxing the story in too early.

Completeness and pacing: The story must be complete within the given word limit—a
clear beginning, middle, and end. If the limit is short (e.g. one page), write one
tight, complete arc in that space. If the limit is longer, pace the plot so the
climax and resolution happen before the limit. Never deliver a cut-off or "to be
continued" story unless the user chose a cliffhanger ending. A 1-page story is one
full mini-story; a 3-page story has room for setup, conflict, and resolution—all
within those pages. Your goal is a complete story within the word limit: every part
of the story, including the ending the user asked for, must fit within that limit.

Use short paragraphs of about three lines each for readability.
"""


def build_story_persona(persona, story_setting, character_input, plot_elements,
                        writing_style, story_tone, narrative_pov, audience_age_group,
                        content_rating, ending_preference):
    """Build the full persona string with story details (move only; wording unchanged)."""
    return f"""{persona}
            Write a story with the following details:

		**The story Setting is:**
		{story_setting}
		
		**The Characters of the story are:**
		{character_input}
		
		**Plot Elements of the story:**
		{plot_elements}
		
		**Story Writing Style:**
		{writing_style}
		
		**The story Tone is:**
		{story_tone}
		
		**Write story from the Point of View of:**
		{narrative_pov}
		
		**Target Audience of the story:**
		{audience_age_group}, **Content Rating:** {content_rating}
		
		**Story Ending:**
		{ending_preference}
		
		Make sure the story is engaging and tailored to the specified audience and content rating.
        Ensure the ending aligns with the preference indicated.
        Write so the reader is pulled in from the first line and stays curious; favor concrete detail and tension over vague or generic description.

        """


def get_premise_prompt(persona_full, story_setting, character_input):
    """Return the premise prompt (no placeholders)."""
    return f"""\
        {persona_full}

        Write a single sentence premise for a {story_setting} story featuring {character_input}.
        """


def get_outline_prompt(persona_full):
    """Return the outline prompt with {{premise}} placeholder."""
    return f"""\
        {persona_full}

        You have a gripping premise in mind:

        {{premise}}

        Write an outline for the plot of your story. Include a clear conflict or central question and a turning point toward the ending.
        """


def get_starting_prompt(persona_full, initial_words, target_words):
    """Return the starting prompt with {{premise}} and {{outline}} placeholders."""
    return f"""\
        {persona_full}

        You have a gripping premise in mind:

        {{premise}}

        Your imagination has crafted a rich narrative outline:

        {{outline}}

        First, silently review the outline and the premise. Consider how to start the
        story.

        Open with a hook—a specific image, line of dialogue, or moment of action or tension—so the reader is drawn in immediately.

        Start to write the very beginning of the story. You are not expected to finish
        the whole story now. Your writing should be detailed enough that you are only
        scratching the surface of the first bullet of your outline. Try to write AT
        MINIMUM {initial_words} WORDS. The entire story must not exceed {target_words} words.

        {WRITING_GUIDELINES}
        """


def get_continuation_prompt(persona_full, target_words):
    """Return the continuation prompt with {{premise}}, {{outline}}, {{story_text}} placeholders."""
    return f"""\
        {persona_full}

        You have a gripping premise in mind:

        {{premise}}

        Your imagination has crafted a rich narrative outline:

        {{outline}}

        You've begun to immerse yourself in this world, and the words are flowing.
        Here's what you've written so far:

        {{story_text}}

        =====

        First, silently review the outline and story so far. Identify what the single
        next part of your outline you should write.

        Keep the reader curious: this section should raise a question, deepen conflict, or deliver a small surprise; avoid filler or repetition.

        Your task is to continue where you left off and write the next part of the story.
        You are not expected to finish the whole story now. Your writing should be
        detailed enough that you are only scratching the surface of the next part of
        your outline. Try to write AT MINIMUM 1000 WORDS. The complete story must be at
        most {target_words} words. When you are near that length, wrap up and write IAMDONE.
        However, only once the story is COMPLETELY finished, write IAMDONE. Remember, do NOT
        write a whole chapter right now.

        {WRITING_GUIDELINES}
        """
