import pandas as pd
import numpy as np
import re


def user_message_counts(df: pd.DataFrame) -> pd.Series:
    top_users = df.groupby("user")["message"].count().sort_values(ascending=False).reset_index()
    return top_users.rename(columns={"user": "Users", "message": "Messages count"})


def messages_per_dates(df: pd.DataFrame) -> pd.Series:
    df_messages_day = df.groupby(df['datetime'].dt.date)['message'].count().sort_values(ascending=False).reset_index()
    return df_messages_day.rename(columns={"datetime": "Dates", "message": "Messages count"})

def messages_per_hour(df: pd.DataFrame) -> pd.Series:
    df_messages_hour = df["datetime"].dt.hour.value_counts()
    hour_order = np.arange(24)
    df_messages_hour = df_messages_hour.reindex(hour_order, fill_value=0).reset_index()
    df_messages_hour.columns = ["Hour", "Messages count"]
    df_messages_hour["Hour"] = df_messages_hour["Hour"].apply(lambda h: f"{h:02d}:00")
    return df_messages_hour

def messages_per_weekday(df: pd.DataFrame) -> pd.Series:
    df_messages_weekday = df["datetime"].dt.day_name().value_counts()
    weekdats_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df_messages_weekday = df_messages_weekday.reindex(weekdats_order, fill_value=0).reset_index()
    return df_messages_weekday.rename(columns={"datetime": "Days", "count": "Messages count"})

_URL_RE = re.compile(r"http[s]?://\S+")

def link_sharing(df: pd.DataFrame) -> pd.Series:
    df_links = df["message"].str.findall(_URL_RE).explode().value_counts().reset_index()
    return df_links.rename(columns={"message": "Links"})

def remove_links(df: pd.DataFrame) -> pd.DataFrame:
    mask = ~df["message"].str.contains(_URL_RE, na=False)
    return df.loc[mask].copy()

