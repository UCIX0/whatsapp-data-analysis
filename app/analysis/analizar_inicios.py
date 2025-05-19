import pandas as pd
from datetime import timedelta

def analizar_inicios(df: pd.DataFrame, umbral_minutos: int = 60) -> pd.DataFrame:
    """
    Analiza un DataFrame de mensajes de chat y determina qué usuario inicia más conversaciones.

    Una conversación se considera iniciada si hay una pausa entre mensajes superior al umbral de minutos especificado.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame que contiene al menos dos columnas: 'datetime' (de tipo datetime64) y 'user' (nombre del usuario).
    umbral_minutos : int, opcional
        Número de minutos mínimo entre mensajes para considerar el inicio de una nueva conversación.
        Por defecto es 60 minutos.

    Retorna:
    -------
    pd.DataFrame
        Un DataFrame con tres columnas:
        - 'User': nombre del usuario que inició conversaciones.
        - 'Conversations Initiated': cantidad de conversaciones iniciadas por cada usuario.
        - 'Start %': porcentaje de conversaciones iniciadas por cada usuario respecto al total.
    """

    df = df.sort_values(by='datetime').reset_index(drop=True)
    df['time_diff'] = df['datetime'].diff().fillna(pd.Timedelta(seconds=0))

    # Nueva columna que indica si ese mensaje es un nuevo inicio de conversación
    df['new_convo'] = df['time_diff'] > timedelta(minutes=umbral_minutos)

    # Filtramos solo los mensajes que inician conversación
    inicios = df[df['new_convo']]

    # Contamos quién inicia más
    conteo = inicios['user'].value_counts()
    total = conteo.sum()
    proporciones = conteo / total * 100
    countprop = pd.DataFrame({
        'User': conteo.index,
        'Conversations Initiated': conteo.values,
        'Start %': proporciones.values
    })
    return countprop.reset_index(drop=True)