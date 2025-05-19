import pandas as pd
import matplotlib.pyplot as plt
from app.analysis import stats, visualization
from app.analysis.analizar_inicios import analizar_inicios

def compute_dataframes(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Genera un conjunto de DataFrames derivados del DataFrame original con distintos análisis.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame base que contiene los mensajes de un chat de WhatsApp con las columnas
        'datetime', 'user' y 'message'.

    Retorna:
    -------
    dict[str, pd.DataFrame]
        Diccionario con los siguientes DataFrames:
        - 'user_counts': cantidad de mensajes por usuario.
        - 'per_day': mensajes por día.
        - 'per_hour': mensajes por hora del día.
        - 'per_weekday': mensajes por día de la semana.
        - 'start_conversations': usuarios que más inician conversaciones.
        - 'links': enlaces compartidos y su frecuencia.
    """
    return {
        "user_counts":  stats.user_message_counts(df),
        "per_day":      stats.messages_per_dates(df),
        "per_hour":     stats.messages_per_hour(df),
        "per_weekday":  stats.messages_per_weekday(df),
        "start_conversations": analizar_inicios(df),
        "links":        stats.link_sharing(df),
    }

def compute_figures(df: pd.DataFrame) -> dict[str, plt.Figure]:
    """
    Genera visualizaciones a partir del DataFrame base.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame base con las columnas necesarias para generar las visualizaciones.

    Retorna:
    -------
    dict[str, plt.Figure]
        Diccionario con los siguientes gráficos:
        - 'messages_over_time': gráfico de línea con mensajes por día.
        - 'wordcloud': nube de palabras a partir de los mensajes.
    """
    return {
        "messages_over_time": visualization.messages_over_time_fig(df),
        "wordcloud":          visualization.build_wordcloud_fig(df),
    }
