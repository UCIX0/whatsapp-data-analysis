import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from app.analysis.stats import messages_per_dates


def messages_over_time_fig(df: pd.DataFrame) -> plt.Figure:
    """
    Genera una gráfica de líneas que muestra la cantidad de mensajes enviados por día.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame que debe contener una columna 'datetime' y 'message'.

    Retorna:
    -------
    matplotlib.figure.Figure
        Objeto de figura con la gráfica de mensajes por fecha.
    """
    daily_df = messages_per_dates(df)
    daily_df = daily_df.sort_values("Dates")

    # Crear la figura de línea
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(daily_df["Dates"], daily_df["Messages count"])
    plt.xlabel("Date")
    plt.ylabel("Number of Messages")
    plt.title("Messages Over Time")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


def build_wordcloud_fig(df: pd.DataFrame) -> plt.Figure:
    """
    Genera una nube de palabras a partir de los mensajes del DataFrame,
    excluyendo enlaces y palabras de 4 caracteres o menos.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame con una columna 'message'.

    Retorna:
    -------
    matplotlib.figure.Figure
        Objeto de figura con la nube de palabras.
    """
    text = " ".join(df.loc[~df["message"].str.contains(r"http[s]?://", na=False), "message"])

    text = " ".join([w for w in text.split() if len(w) > 4])

    # Generar la nube de palabras
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)

    # Crear figura de WordCloud
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")

    return fig