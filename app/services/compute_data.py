from app.analysis import stats, visualization
from app.analysis.analizar_inicios import analizar_inicios

def compute_dataframes(df):
    return {
        "user_counts":  stats.user_message_counts(df),
        "per_day":      stats.messages_per_dates(df),
        "per_hour":     stats.messages_per_hour(df),
        "per_weekday":  stats.messages_per_weekday(df),
        "start_conversations": analizar_inicios(df),
        "links":        stats.link_sharing(df),
    }

def compute_figures(df):
    return {
        "messages_over_time": visualization.messages_over_time_fig(df),
        "wordcloud":          visualization.build_wordcloud_fig(df),
    }
