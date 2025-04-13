# Este es solo un ejemplo rapido xd
import streamlit as st
import os
import tempfile
from app.chat_to_df import chat_to_dataframe

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
            st.success("Pos funcionó 🤩")
            st.dataframe(df)
        except Exception as e:
            st.error(e)

        # Después de terminar el procesamiento, se elimina el archivo temporal.
        try:
            os.remove(temp_file_path)
            print("Archivo temporal eliminado exitosamente.")

        except Exception as e:
            print(f"Error al eliminar el archivo temporal: {e}")

if __name__ == "__main__":
    main()
