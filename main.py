# Este es solo un ejemplo rapido xd
import streamlit as st
import os
import tempfile

from app.analysis.analizar_inicios import analizar_inicios
#from app.analysis.estadiscs import pass
from app.pipeline.chat_to_df import chat_to_dataframe
from app.pipeline.clean_dataframe import clean_dataframe


def main():
    st.title("DEMO titulo chingo aqui")

    uploaded_file = st.file_uploader("Carga tu archivo weeee", type=["txt"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        try:
            # Procesar el archivo y mostrar el DataFrame
            df = chat_to_dataframe(temp_file_path)
            df_cleaned = clean_dataframe(df)
            with st.expander("Raw DataFrame"):
                st.dataframe(df_cleaned)
            st.subheader("¿Quién inicia más conversaciones?")
            countprop, inicios = analizar_inicios(df)
            st.dataframe(countprop)
            st.success("Pos funcionó :v")

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
            print(f"Error: {e}")

        # Después de terminar el procesamiento, se elimina el archivo temporal.
        try:
            os.remove(temp_file_path)
        except Exception as e:
            st.warning(f"Error al eliminar el archivo temporal: {e}")

if __name__ == "__main__":
    main()
