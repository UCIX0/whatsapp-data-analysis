import pandas as pd
import re
import io
from app.pipeline.chat_parser import extract_line, parse_datetime

def chat_to_dataframe(file_obj) -> pd.DataFrame:
    # Si el archivo subido es binario, lo envolvemos como un flujo de bytes
    if isinstance(file_obj, bytes):
        file_obj = io.BytesIO(file_obj)
    # Si el archivo es un flujo binario, lo convertimos a texto usando codificación UTF-8
    if isinstance(file_obj , (io.BytesIO, io.BufferedReader)):
        file_obj  = io.TextIOWrapper(file_obj, encoding="utf-8", errors="strict")


    records = []
    # Patrones diferentes para Android y Apple según el formato del archivo de exportación
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
    #Lectura y procesamiento línea por línea del archivo
    try:
        for line in file_obj:
            # Eliminamos caracteres invisibles que pueden corromper el texto
            line = line.rstrip()
            line = re.sub(r'[\u200B-\u200F\u202A-\u202E\u2060-\u206F\uFEFF]', '', line)
            # Extraemos fecha, hora, usuario y mensaje de la línea usando nuestra función extract_line()
            date_str, time_str, user, message = extract_line(line)

            if date_str and time_str and user is not None:
                # Convertimos la fecha y hora a un objeto datetime unificado
                try:
                    dt = parse_datetime(date_str, time_str)
                except Exception as e:
                    print(f"Error al analizar la fecha y hora: {e}")
                    continue
                # Agregamos el mensaje parseado a la lista de registros
                records.append({"datetime": dt, "user": user, "message": message})
            # Si la línea no es una línea de inicio, es una continuación del mensaje anterior
            elif not (re.match(system_pattern_Android, line) or re.match(system_pattern_Apple, line)) and records:
                records[-1]["message"] += " " + line.strip()

    #Manejo de errores comunes
    except UnicodeDecodeError as e:
        raise ValueError(f"Error de codificación: {e}. Asegúrate de que el archivo esté en UTF-8.")
    except Exception as e:
        raise e

    #Construcción del DataFrame final y validación
    df = pd.DataFrame(records, columns=["datetime", "user", "message"])
    if df.empty:
        raise ValueError("El DataFrame resultante está vacío. Verifica el formato y contenido del archivo.")
    return df