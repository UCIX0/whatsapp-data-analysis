import re
import pandas as pd


def extract_line(line: str) -> tuple:
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


def parse_datetime(date_str: str, time_str: str) -> pd.Timestamp:
    """
    Convierte cadenas de texto que representan una fecha y una hora en un objeto Timestamp de pandas.

    Parámetros:
    ----------
    date_str : str
        Fecha en formato 'dd/mm/yy' o 'dd/mm/yyyy'.
    time_str : str
        Hora en formato de 12 o 24 horas, con o sin segundos, y con posibles puntos o espacios extras
        (por ejemplo, '11:23 p. m.', '14:01:15').

    Retorna:
    -------
    pd.Timestamp
        Objeto de tipo Timestamp con la fecha y hora parseadas.

    Lanza:
    ------
    ValueError
        Si la cadena de fecha y hora no puede ser parseada con los formatos esperados.
    """
    clean_time = re.sub(r'\.', '', time_str)
    clean_time = " ".join(clean_time.split())
    clean_time = re.sub(r'(?i)\b([ap])\s+([m])\b', r'\1\2', clean_time)
    has_ampm = re.search(r'\b(?:am|pm)\b', clean_time, re.IGNORECASE)
    has_seconds = clean_time.count(':') == 2
    short_year = len(date_str.split('/')[-1]) == 2
    if has_ampm: # Para formato 12 horas
        date_format = "%d/%m/%y" if short_year else "%d/%m/%Y"
        time_format = " %I:%M:%S %p" if has_seconds else " %I:%M %p"
    else: # Para formato 24 horas
        date_format = "%d/%m/%y" if short_year else "%d/%m/%Y"
        time_format = " %H:%M:%S" if has_seconds else " %H:%M"

    dt_format = date_format + time_format
    date_time_str = f"{date_str} {clean_time}"
    try:
        dt = pd.to_datetime(date_time_str, format=dt_format)
    except Exception as e:
        raise ValueError(f"Error parseando datetime: {e}")
    return dt