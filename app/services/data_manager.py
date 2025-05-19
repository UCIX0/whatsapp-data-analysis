import streamlit as st
import hashlib, io
import hydralit_components as hc

from app.pipeline.chat_to_df   import chat_to_dataframe
from app.pipeline.clean_dataframe import clean_dataframe
from app.services.compute_data   import compute_dataframes, compute_figures
"""
Es necesario debido al funcionamiento interno de Streamlit que al cambiar de pestaña o interactuar
con los widgets, el estado de la aplicación se reinicia y se pierden los datos en memoria.
"""

def get_data(uploaded_file) -> tuple:
    """
    Procesa el archivo de chat subido, limpia los datos y precalcula todos los
    análisis y visualizaciones. Si el archivo ya fue cargado previamente (según su hash),
    se recuperan los resultados desde la caché mantenida en `st.session_state`.

    Esto evita que los análisis se recalculen innecesariamente cada vez que Streamlit
    recarga la interfaz, mejorando significativamente el rendimiento y la experiencia de usuario.

    Parámetros:
    ----------
    uploaded_file : UploadedFile
        Archivo `.txt` cargado mediante `st.file_uploader` de Streamlit.

    Retorna:
    -------
    tuple
        Tupla con los siguientes objetos almacenados en `st.session_state`:
        - `df` (`pd.DataFrame`): DataFrame limpio con columnas 'datetime', 'user' y 'message'.
        - `dict_dframes` (`dict[str, pd.DataFrame]`): Diccionario de DataFrames con estadísticas preprocesadas.
        - `dict_figs` (`dict[str, matplotlib.figure.Figure]`): Diccionario con visualizaciones ya generadas.

        Todos estos objetos están almacenados en el estado de sesión de Streamlit bajo las claves:
        'df', 'dict_dframes', 'dict_figs'.

    Lanza:
    ------
    st.stop()
        En caso de error durante la lectura, limpieza o análisis del archivo.
    """
    file_bytes   = uploaded_file.getvalue()
    file_hash  = hashlib.md5(file_bytes).hexdigest()


    if st.session_state.get("file_hash") != file_hash:
        # Nuevo archivo procesar
        with hc.HyLoader("Processing chat…", hc.Loaders.pulse_bars):
            try:
                df = clean_dataframe(chat_to_dataframe(io.BytesIO(file_bytes)))
            except ValueError as ve:
                st.error(f"⚠️ {ve}")
                raise st.stop()
            except Exception as e:
                st.error(f"❌ Error inesperado al procesar el archivo: {e}")
                raise st.stop()

        dict_dataframes = compute_dataframes(df)
        dict_figs   = compute_figures(df)

        #Guardar en cache
        st.session_state.update(
            file_hash=file_hash,
            df=df,
            dict_dframes=dict_dataframes,
            dict_figs=dict_figs,
        )

    #Cargar desde cache
    return (
        st.session_state.df,
        st.session_state.dict_dframes,
        st.session_state.dict_figs,
    )
