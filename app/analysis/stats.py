import pandas as pd
import numpy as np
import re



# Expresión regular para detectar URLs en los mensajes
_URL_RE = re.compile(r"http[s]?://\S+")


def user_message_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cuenta cuántos mensajes envió cada usuario.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame que contiene las columnas 'user' y 'message'.

    Retorna:
    -------
    pd.DataFrame
        DataFrame con columnas:
        - 'Users': nombre del usuario.
        - 'Messages count': cantidad de mensajes enviados.
    """
    top_users = df.groupby("user")["message"].count().sort_values(ascending=False).reset_index()
    return top_users.rename(columns={"user": "Users", "message": "Messages count"})


def messages_per_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cuenta la cantidad de mensajes enviados por fecha (día calendario).

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame con una columna 'datetime' y 'message'.

    Retorna:
    -------
    pd.DataFrame
        DataFrame con columnas:
        - 'datetime': fecha.
        - 'Messages count': cantidad de mensajes por día.
    """
    df_messages_day = df.groupby(df['datetime'].dt.date)['message'].count().sort_values(ascending=False).reset_index()
    df_messages_day.columns = ["Dates", "Messages count"]
    return df_messages_day


def messages_per_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cuenta los mensajes enviados por cada hora del día (0–23).

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame que contiene la columna 'datetime'.

    Retorna:
    -------
    pd.DataFrame
        DataFrame con columnas:
        - 'Hour': hora del día en formato HH:00.
        - 'Messages count': cantidad de mensajes en esa hora.
    """
    df_messages_hour = df["datetime"].dt.hour.value_counts()
    hour_order = np.arange(24)
    df_messages_hour = df_messages_hour.reindex(hour_order, fill_value=0).reset_index()
    df_messages_hour.columns = ["Hour", "Messages count"]
    df_messages_hour["Hour"] = df_messages_hour["Hour"].apply(lambda h: f"{h:02d}:00")
    return df_messages_hour


def messages_per_weekday(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cuenta la cantidad de mensajes enviados por día de la semana en el DataFrame dado.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene al menos una columna 'datetime' de tipo datetime.

    Retorna:
    pd.DataFrame: DataFrame con dos columnas:
        - 'Days': nombre del día de la semana (de lunes a domingo).
        - 'Messages count': cantidad de mensajes enviados ese día.
    """
    df_messages_weekday = df["datetime"].dt.day_name().value_counts()
    weekdays_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df_messages_weekday = df_messages_weekday.reindex(weekdays_order, fill_value=0).reset_index()
    df_messages_weekday.columns = ["Days", "Messages count"]
    return df_messages_weekday


def link_sharing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae y cuenta los enlaces compartidos en los mensajes.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame con una columna 'message'.

    Retorna:
    -------
    pd.DataFrame
        DataFrame con columnas:
        - 'index': URL compartida.
        - 'message': cantidad de veces que fue compartida.
    """
    df_links = df["message"].str.findall(_URL_RE).explode().value_counts().reset_index()
    return df_links.rename(columns={"index": "Links", "message": "Count"})


def remove_links(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra y devuelve un nuevo DataFrame sin los mensajes que contienen enlaces.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame con una columna 'message'.

    Retorna:
    -------
    pd.DataFrame
        DataFrame con solo los mensajes que no contienen enlaces.
    """
    mask = ~df["message"].str.contains(_URL_RE, na=False)
    return df.loc[mask].copy()
