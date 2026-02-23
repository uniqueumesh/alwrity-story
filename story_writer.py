import streamlit as st

from ai_story_writer import ai_story_generator
from config import (
    PERSONAS,
    PERSONA_DESCRIPTIONS,
    SLIDER_DEFAULT,
    SLIDER_MAX,
    SLIDER_MIN,
    WORDS_PER_PAGE,
    WRITING_STYLES,
    STORY_TONES,
    NARRATIVE_POVS,
    AUDIENCE_AGE_GROUPS,
    CONTENT_RATINGS,
    ENDING_PREFERENCES,
)
from ui import custom_css, hide_elements, set_page_config


def main():
    set_page_config()
    custom_css()
    hide_elements()
    input_section()


def input_section():
    st.title("🧕 Alwrity - AI Story Writer")

    selected_persona_name = st.selectbox(
        "Select Your Story Writing Persona Or Book Genre",
        options=[persona[0] for persona in PERSONAS]
    )

    # Story Setting
    st.subheader("🌍 Story Setting")
    story_setting = st.text_area(
        label="**Story Setting** (e.g., medieval kingdom in the past, futuristic city in the future, haunted house in the present):",
        placeholder="""Enter settings for your story, like Location (e.g., medieval kingdom, futuristic city, haunted house),
        Time period in which your story is set (e.g: Past, Present, Future)
        Example: 'A bustling futuristic city with towering skyscrapers and flying cars, set in the year 2150. 
        The city is known for its technological advancements but has a dark underbelly of crime and corruption.'""",
        help="Describe the main location and time period where the story will unfold in a detailed manner."
    )
    
    # Main Characters
    st.subheader("👥 Main Characters")
    character_input = st.text_area(
        label="**Character Information** (Names, Descriptions, Roles)",
        placeholder="""Example:
        Character Names: John, Xishan, Amol
        Character Descriptions: John is a tall, muscular man with a kind heart. Xishan is a clever and resourceful woman. Amol is a mischievous and energetic young boy.
        Character Roles: John - Hero, Xishan - Sidekick, Amol - Supporting Character""",
        help="Enter character information as specified in the placeholder."
    )
    
    # Plot Elements
    st.subheader("🗺️ Plot Elements")
    plot_elements = st.text_area(
        "**Plot Elements** - (Theme, Key Events & Main Conflict)",
        placeholder="""Example:
        Story Theme: Love conquers all, The hero's journey, Good vs. evil.
        Key Events: The hero meets the villain, The hero faces a challenge, The hero overcomes the conflict.
        Main Conflict: The hero must save the world from a powerful enemy, The hero must overcome a personal obstacle to achieve their goal.""",
        help="Enter plot elements as specified in the placeholder."
    )
    
    # Tone and Style
    st.subheader("🎨 Tone and Style")
    col1, col2, col3 = st.columns(3)
    with col1:
        writing_style = st.selectbox(
            "**Writing Style:**",
            WRITING_STYLES,
            help="Choose the writing style that fits your story."
        )
    with col2:
        story_tone = st.selectbox(
            "**Story Tone:**",
            STORY_TONES,
            help="Select the overall tone or mood of the story."
        )
    with col3:
        narrative_pov = st.selectbox(
            "**Narrative Point of View:**",
            NARRATIVE_POVS,
            help="Choose the point of view from which the story is told."
        )
    
    # Target Audience
    st.subheader("👨‍👩‍👧‍👦 Target Audience")
    col1, col2, col3 = st.columns(3)
    with col1:
        audience_age_group = st.selectbox(
            "**Audience Age Group:**",
            AUDIENCE_AGE_GROUPS,
            help="Choose the intended audience age group."
        )
    with col2:
        content_rating = st.selectbox(
            "**Content Rating:**",
            CONTENT_RATINGS,
            help="Select a content rating for appropriateness."
        )
    with col3:
        ending_preference = st.selectbox(
            "Story Conclusion:",
            ENDING_PREFERENCES,
            help="Choose the type of ending you prefer for the story."
        )

    # Story length
    st.subheader("📄 Story Length")
    page_length = st.slider(
        "Number of pages",
        min_value=SLIDER_MIN,
        max_value=SLIDER_MAX,
        value=SLIDER_DEFAULT,
        help=f"1 page ≈ {WORDS_PER_PAGE} words. Shorter stories use fewer API calls."
    )

    if st.button('AI, Write a Story..'):
        if character_input.strip():
            with st.spinner("Generating Story...💥💥"):
                story_content = ai_story_generator(PERSONA_DESCRIPTIONS[selected_persona_name],
                        story_setting, character_input, plot_elements, writing_style,
                        story_tone, narrative_pov, audience_age_group, content_rating,
                        ending_preference, page_length)
                if story_content:
                    st.subheader('**🧕 Your Awesome Story:**')
                    st.markdown(story_content)
                else:
                    st.error("💥 **Failed to generate Story. Please try again!**")
        else:
            st.error("Describe the story you have in your mind.. !")


if __name__ == "__main__":
    main()
