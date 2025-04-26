import streamlit as st
from app.ui.optionbar import draw_optionbar
from app.ui.stats_cards import cards_show
from app.ui import render_pages as pages
from app.services.data_manager import get_data


st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main() -> None:
    st.title("💬 WhatsApp Chat Analyzer")
    col1, col2, col3 = st.columns([1, 2, 1])
    # ---------- File uploader ----------
    with col2:
        uploaded_file = st.file_uploader(
            "Upload your *WhatsApp* `.txt` log",
            type=["txt"],
            accept_multiple_files=False,
            label_visibility="collapsed"
        )

        if uploaded_file is None:
            st.info("Drop a WhatsApp chat export here to start the analysis.")
            st.stop()

    try:
        df, dframes, figs = get_data(uploaded_file)
    except st.runtime.scriptrunner.StopException:
        st.stop()


    cards_show(df)
    st.divider()

    menu_selection  = draw_optionbar()

    # Default section
    if menu_selection  is None:
        menu_selection = "Tables"


    if menu_selection == "Tables":
        pages.render_tables(dframes)
    elif menu_selection == "Visualization":
        pages.render_charts(figs)


if __name__ == "__main__":
    main()
