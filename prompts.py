"""
Story-generation prompt templates and builders.
Edit prompts here to improve results without changing generation logic.
"""

WRITING_GUIDELINES = """\
Writing Guidelines:

Delve deeper. Lose yourself in the world you're building. Unleash vivid
descriptions to paint the scenes in your reader's mind.
Develop your characters — let their motivations, fears, and complexities unfold naturally.
Weave in the threads of your outline, but don't feel constrained by it.
Allow your story to surprise you as you write. Use rich imagery, sensory details, and
evocative language to bring the setting, characters, and events to life.
Introduce elements subtly that can blossom into complex subplots, relationships,
or worldbuilding details later in the story.
Keep things intriguing but not fully resolved.
Avoid boxing the story into a corner too early.
Plant the seeds of subplots or potential character arc shifts that can be expanded later.

Remember, your main goal is to write as much as you can. If you get through
the story too fast, that is bad. Expand, never summarize.
"""


def build_story_persona(persona, story_setting, character_input, plot_elements,
                        writing_style, story_tone, narrative_pov, audience_age_group,
                        content_rating, ending_preference):
    """Build the full persona string with story details (move only; wording unchanged)."""
    return f"""{persona}
            Write a story with the following details:

		**The stroy Setting is:**
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

        Write an outline for the plot of your story.
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

        Your task is to continue where you left off and write the next part of the story.
        You are not expected to finish the whole story now. Your writing should be
        detailed enough that you are only scratching the surface of the next part of
        your outline. Try to write AT MINIMUM 1000 WORDS. The complete story must be at
        most {target_words} words. When you are near that length, wrap up and write IAMDONE.
        However, only once the story is COMPLETELY finished, write IAMDONE. Remember, do NOT
        write a whole chapter right now.

        {WRITING_GUIDELINES}
        """
