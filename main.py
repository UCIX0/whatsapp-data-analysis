import streamlit as st
from app.ui.optionbar import draw_optionbar
from app.ui.stats_cards import cards_show
from app.ui import render_pages as pages
from app.services.data_manager import get_data


st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="static/logo_icon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main() -> None:
    """
    Entrypoint de la aplicación **WhatsApp Chat Analyzer**.

    Esta función controla el flujo completo de la interfaz Streamlit:

    1. Configura la cabecera y el logo de la página.
    2. Presenta un *file-uploader* que acepta **un único** archivo `.txt`
        exportado desde WhatsApp.
    3. Envía el archivo a :pyfunc:`app.services.data_manager.get_data`, donde
        se realiza el ―costoso― preprocesamiento (parseo, limpieza, estadísticas
        y visualizaciones).
        Los resultados se almacenan en ``st.session_state`` para que persistan
       entre *reruns* y no se recalculen en cada interacción del usuario.
    4. Muestra tarjetas con KPIs de alto nivel mediante
        :pyfunc:`app.ui.stats_cards.cards_show`.
    5. Renderiza una barra de navegación (``Tables`` / ``Visualization``)
        y, según la opción elegida, delega la presentación detallada a:

        - :pyfunc:`app.ui.render_pages.render_tables`
        (tablas con los DataFrames precalculados).
        - :pyfunc:`app.ui.render_pages.render_charts`
        (gráficos de línea y *word-cloud*).

    Parámetros
    ----------
    Ninguno
    Todo el I/O se gestiona a través de componentes Streamlit.

    Retorna
    -------
    None
    La función imprime elementos en la interfaz y luego cede el control al
    motor de Streamlit.
    """
    # ---------- Columnas para alinear el logo ----------
    col1, col2 = st.columns([1, 15])
    with col1:
        st.image("static/logo.png", width=120)

    with col2:
        st.title("WhatsApp Chat Analyzer")
    col1, col2, col3 = st.columns([1, 2, 1])
    # ---------- Carga del archivo ----------
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
    # ---------- Preprocesamiento y caché ----------
    try:
        df, dframes, figs = get_data(uploaded_file)
    except st.runtime.scriptrunner.StopException:
        st.stop()

    # ---------- Tarjetas de métricas ----------
    cards_show(df)
    st.divider()
    # ---------- Menú de navegación ----------
    menu_selection  = draw_optionbar()
    # ---------- Renderizado según la selección ----------
    # Default section
    if menu_selection  is None:
        menu_selection = "Tables"


    if menu_selection == "Tables":
        pages.render_tables(dframes)
    elif menu_selection == "Visualization":
        pages.render_charts(figs)


if __name__ == "__main__":
    main()
