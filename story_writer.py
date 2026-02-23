from forms import input_section
from ui import custom_css, hide_elements, set_page_config


def main():
    set_page_config()
    custom_css()
    hide_elements()
    input_section()


if __name__ == "__main__":
    main()
