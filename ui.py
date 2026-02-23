import streamlit as st

from config import LAYOUT, PAGE_TITLE


def set_page_config():
    st.set_page_config(
        page_title=PAGE_TITLE,
        layout=LAYOUT,
    )


def custom_css():
    st.markdown("""
    <style>
        ::-webkit-scrollbar-track {
        background: #e1ebf9;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }

        ::-webkit-scrollbar {
            width: 16px;
        }

        div.stButton > button:first-child {
	        background: #1565C0;
	        color: white;
	        border: none;
	        padding: 12px 24px;
	        border-radius: 8px;
	        text-align: center;
	        text-decoration: none;
	        display: inline-block;
	        font-size: 16px;
	        margin: 10px 2px;
	        cursor: pointer;
	        transition: background-color 0.3s ease;
	        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
	        font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)


def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)
