import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from app.analysis.stats import messages_per_day

def messages_over_time_fig(df: pd.DataFrame):
    series = messages_per_day(df)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(series.index, series.values)
    plt.xlabel("Date")
    plt.ylabel("Number of Messages")
    plt.title("Messages Over Time")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def build_wordcloud_fig(df: pd.DataFrame):
    # Filtra links y palabras cortas
    text = " ".join(df.loc[~df["message"].str.contains(r"http[s]?://", na=False), "message"])
    text = " ".join([w for w in text.split() if len(w) > 4])

    wc = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    return fig
