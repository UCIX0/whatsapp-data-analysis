import re
import os
import pandas as pd
import logging
import logging_config

logger = logging.getLogger(__name__)

class ChatProcessingError(Exception):
    """Excepción para errores en el procesamiento del chat."""
    pass

def extract_line(line):
    """
    Extrae la fecha, hora, usuario y mensaje de una línea del chat.

    Parameters:
        line (str): Línea del archivo de chat.

    Returns:
        tuple: (date_str, time_str, user, message) si la extracción es exitosa;
        de lo contrario, (None, None, None, None).
    """
    if line.startswith('['):
        pattern = ( #Apple
            r'^\[' # Comienza con un corchete abierto
            r'(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s*' # Fecha (dd/mm/yy o dd/mm/yyyy)
            r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[apAP]\.?[\s]*[mM]\.?)?)'  # Tiempo (hh:mm, opcional :ss y opcional AM/PM)
            r'\]\s+' # Cierra el corchete y sigue con espacios
            r'(?P<user>.+?):\s' # Usuario seguido de dos puntos y espacio
            r'(?P<message>.*)' # Mensaje (todo el texto restante)
        )
    else:
        pattern = ( #Android
            r'^(?P<date>\d{1,2}/\d{1,2}/\d{4}),\s+' # Fecha en formato dd/mm/yyyy
            r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[apAP]\.?[\s]*[mM]\.?)?)' # Tiempo (hh:mm, opcional :ss y opcional AM/PM)
            r'\s*-\s*' # Separador " - " con espacios opcionales
            r'(?P<user>.+?):\s' # Usuario seguido de dos puntos y espacio
            r'(?P<message>.*)'  # Mensaje (todo el texto restante)
        )
    match = re.search(pattern, line)
    if match:
        return (
            match.group("date"),
            match.group("time"),
            match.group("user"),
            match.group("message")
        )
    return None, None, None, None

def parse_datetime(date_str, time_str):
    """
    Convierte cadenas de fecha y hora en un objeto datetime de pandas.

    Parameters:
        date_str (str): Fecha en formato dd/mm/yy o dd/mm/yyyy.
        time_str (str): Hora que puede incluir segundos y/o indicadores AM/PM.

    Returns:
        datetime: Objeto datetime parseado.

    Raises:
        ValueError: Si no se puede parsear la fecha y hora.
    """
    clean_time = re.sub(r'\.', '', time_str)
    clean_time = " ".join(clean_time.split())
    # Busca y reemplaza separadamente patrones de "a m" por "am"  insensible a mayúsculas/minúsculas
    clean_time = re.sub(r'(?i)\b([ap])\s+([m])\b', r'\1\2', clean_time)
    # Determina si la cadena de tiempo contiene el indicador AM/PM.
    has_ampm = re.search(r'\b(?:am|pm)\b', clean_time, re.IGNORECASE)
    has_seconds = clean_time.count(':') == 2 # Determina si se han incluido segundos contando ":"
    short_year = len(date_str.split('/')[-1]) == 2 # Verifica si el año se expresa en dos dígitos.

    if has_ampm: # Para formato 12 horas
        date_format = "%d/%m/%y" if short_year else "%d/%m/%Y"
        time_format = " %I:%M:%S %p" if has_seconds else " %I:%M %p"
    else: # Para formato 24 horas
        date_format = "%d/%m/%y" if short_year else "%d/%m/%Y"
        time_format = " %H:%M:%S" if has_seconds else " %H:%M"

    # Se compone el formato completo
    dt_format = date_format + time_format
    date_time_str = f"{date_str} {clean_time}"

    #intenta convertir a datime
    try:
        dt = pd.to_datetime(date_time_str, format=dt_format)
    except Exception as e:
        logger.error(
            "Error parseando datetime para '%s' usando el formato '%s': %s",
            date_time_str, dt_format, e
        )
        raise ValueError(f"Error parseando datetime: {e}")
    return dt

def chat_to_dataframe(file_path):
    """
    Procesa un archivo de chat en formato texto y retorna su contenido en un DataFrame de pandas.

    El DataFrame tendrá las columnas:
        - datetime: Fecha y hora combinadas parseadas a datetime.
        - user: Nombre del usuario.
        - message: Mensaje del usuario.

    Soporta concatenación de líneas para mensajes que abarquen varias líneas.

    Parameters:
        file_path (str): Ruta al archivo de chat.

    Returns:
        DataFrame: DataFrame con columnas ['datetime', 'user', 'message'].

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ChatProcessingError: Para otros errores relacionados con el procesamiento.
    """

    # Verifica si el archivo existe
    if not os.path.exists(file_path):
        error_msg = f"El archivo '{file_path}' no existe."
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

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
        with open(file_path, 'r', encoding='utf-8') as file:
            for num_line, line in enumerate(file, 1):
                # Eliminamos espacios laterales y caracteres invisibles problemáticos
                line = line.rstrip()
                line = re.sub(r'^[\u200e\u202f]+', '', line)

                # Extrae los componentes
                date_str, time_str, user, message = extract_line(line)

                # Intenta parsear
                if date_str and time_str and user is not None:
                    try:
                        dt = parse_datetime(date_str, time_str)
                    except Exception as e:
                        logger.warning(
                            "Registro %d: error en parseo de datetime; línea omitida. Error: %s",
                            num_line, e
                        )
                        continue
                    record = {"datetime": dt, "user": user, "message": message}
                    records.append(record)
                else:
                    if not (re.match(system_pattern_Android, line) or re.match(system_pattern_Apple, line)) and records:
                        records[-1]["message"] += " " + line.strip()
                    else:
                        logger.debug("Línea %d no coincide con ningún patrón: %s", num_line, line)

    #Error archivo codificado mal o corrupto
    except UnicodeDecodeError as e:
        error_msg = f"Error de decodificación al leer el archivo '{file_path}': {e}"
        logger.error(error_msg)
        raise ChatProcessingError(error_msg) from e
    #Error error del codigo al parsear
    except Exception as e:
        error_msg = f"Se produjo un error durante el procesamiento del archivo: {e}"
        logger.error(error_msg)
        raise ChatProcessingError(error_msg) from e

    df = pd.DataFrame(records, columns=["datetime", "user", "message"])
    #Error Dataframe vacio
    if df.empty:
        error_msg = "El DataFrame resultante está vacío. Verifica el formato y contenido del archivo."
        logger.warning(error_msg)
        raise ChatProcessingError(error_msg)

    return df

# Bloque de prueba (solo se ejecuta cuando se ejecuta el módulo directamente)
if __name__ == "__main__":
    try:
        df = chat_to_dataframe("chat2.txt")
        logger.info("Archivo procesado exitosamente. Mostrando las primeras líneas:")
        print(df)
    except Exception as e:
        logger.critical("Error crítico al procesar el archivo: %s", e)
