import pandas as pd
import numpy as np
import re


def user_message_counts(df: pd.DataFrame) -> pd.Series:
    """Series: mensajes por usuario (desc)."""
    return df.groupby("user")["message"].count().sort_values(ascending=False)

def messages_per_day(df: pd.DataFrame) -> pd.Series:
    """Series: nº de mensajes por fecha."""
    return df.groupby(df['datetime'].dt.date)['message'].count()

def messages_per_hour(df: pd.DataFrame) -> pd.Series:
    """Series: nº de mensajes por hora del día."""
    return df.groupby(df['datetime'].dt.hour)['message'].count()

def messages_per_weekday(df: pd.DataFrame) -> pd.Series:
    """Series: distribución por día de la semana."""
    return df["datetime"].dt.day_name().value_counts()

_URL_RE = re.compile(r"http[s]?://\S+")

def link_sharing(df: pd.DataFrame) -> pd.Series:
    """Series: enlaces por mensaje."""
    return df["message"].str.findall(_URL_RE).explode().value_counts()

def remove_links(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una copia sin mensajes que contengan URLs."""
    mask = ~df["message"].str.contains(_URL_RE, na=False)
    return df.loc[mask].copy()

