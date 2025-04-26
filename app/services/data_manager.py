import streamlit as st
import hashlib, io
import hydralit_components as hc

from app.pipeline.chat_to_df   import chat_to_dataframe
from app.pipeline.clean_dataframe import clean_dataframe
from app.services.compute_data   import compute_dataframes, compute_figures


def get_data(uploaded_file):
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
