import pandas as pd
import re
import io
from app.pipeline.chat_parser import extract_line, parse_datetime

def chat_to_dataframe(file_obj) -> pd.DataFrame:
    """
    Procesa un archivo de chat en formato texto y retorna su contenido en un DataFrame de pandas.
    Soporta concatenación de líneas para mensajes que abarquen varias líneas.

    Parameters:
        file_path (str): Ruta al archivo de chat.

    Returns:
        DataFrame: DataFrame con columnas ['datetime', 'user', 'message'].

    Raises:
        UnicodeDecodeError: Si el archivo no está en formato UTF-8.
        FileNotFoundError: Si el archivo no existe.
        Exception: Para cualquier otro error durante el proceso.
    """


    #Normalizar a “objeto texto”
    if isinstance(file_obj, bytes):
        file_obj = io.BytesIO(file_obj)

    if isinstance(file_obj , (io.BytesIO, io.BufferedReader)):
        file_obj  = io.TextIOWrapper(file_obj, encoding="utf-8", errors="strict")


    records = []
    system_pattern_Android = (
        r'^(?P<date>\d{1,2}/\d{1,2}/\d{4}),\s+' # Fecha en formato dd/mm/yyyy
        r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[apAP]\.?[\s]*[mM]\.?)?)' # Tiempo (hh:mm, opcional :ss y opcional AM/PM)
        r'\s*-\s*' # Separador " - " con espacios opcionales
    )
    system_pattern_Apple = (
        r'^\[' # Comienza con un corchete abierto
        r'(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s*' # Fecha (dd/mm/yy o dd/mm/yyyy)
        r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[apAP]\.?[\s]*[mM]\.?)?)'  # Tiempo (hh:mm, opcional :ss y opcional AM/PM)
        r'\]\s+' # Cierra el corchete y sigue con espacios
        )
    try:
        for line in file_obj:
            line = line.rstrip()
            line = re.sub(r'[\u200B-\u200F\u202A-\u202E\u2060-\u206F\uFEFF]', '', line)
            date_str, time_str, user, message = extract_line(line)

            if date_str and time_str and user is not None:
                try:
                    dt = parse_datetime(date_str, time_str)
                except Exception as e:
                    print(f"Error al analizar la fecha y hora: {e}")
                    continue
                records.append({"datetime": dt, "user": user, "message": message})
            elif not (re.match(system_pattern_Android, line) or re.match(system_pattern_Apple, line)) and records:
                records[-1]["message"] += " " + line.strip()
    except UnicodeDecodeError as e:
        raise ValueError(f"Error de codificación: {e}. Asegúrate de que el archivo esté en UTF-8.")
    except Exception as e:
        raise e

    df = pd.DataFrame(records, columns=["datetime", "user", "message"])
    if df.empty:
        raise ValueError("El DataFrame resultante está vacío. Verifica el formato y contenido del archivo.")
    return df