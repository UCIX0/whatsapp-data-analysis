import streamlit as st
import hydralit_components as hc
import app.analysis.stats as stats
import pandas as pd

def cards_show(df: pd.DataFrame) -> None:
    """
    Renderiza tarjetas informativas (info cards) con métricas clave del chat analizado.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame limpio con columnas 'datetime', 'user' y 'message'.

    Métricas mostradas:
    - Total de mensajes.
    - Número de usuarios únicos.
    - Período cubierto por el chat.
    - Cantidad total de enlaces compartidos.
    """
    total = len(df)
    users = df["user"].nunique()
    period = f'{df["datetime"].dt.date.min()} → {df["datetime"].dt.date.max()}'
    links = int(stats.link_sharing(df)["count"].sum())

    # Definir temas personalizados para cada tarjeta
    theme_messages = {
        'bgcolor': '#E8F0FE',
        'title_color': '#1A73E8',
        'content_color': '#1A73E8',
        'icon_color': '#1A73E8',
        'icon': 'fa fa-comment-dots'
    }
    theme_users = {
        'bgcolor': '#E8F5E9',
        'title_color': '#34A853',
        'content_color': '#34A853',
        'icon_color': '#34A853',
        'icon': 'fa fa-users'
    }
    theme_links = {
        'bgcolor': '#FFF3E0',
        'title_color': '#FB8C00',
        'content_color': '#FB8C00',
        'icon_color': '#FB8C00',
        'icon': 'fa fa-link'
    }
    theme_period = {
        'bgcolor': '#F3E5F5',
        'title_color': '#8E24AA',
        'content_color': '#8E24AA',
        'icon_color': '#8E24AA',
        'icon': 'fa fa-calendar-alt'
    }

    # Crear columnas
    c1, c2, c3, c4 = st.columns(4)

    # Mostrar tarjeta: total de mensajes
    with c1:
        hc.info_card(
            title='Messages',
            content=f"{total:,}",
            theme_override=theme_messages
        )

    # Mostrar tarjeta: usuarios únicos
    with c2:
        hc.info_card(
            title='Users',
            content=f"{users}",
            theme_override=theme_users
        )

    # Mostrar tarjeta: enlaces compartidos
    with c3:
        hc.info_card(
            title='Links',
            content=f"{links:,}",
            theme_override=theme_links
        )

    # Mostrar tarjeta: periodo del chat
    with c4:
        hc.info_card(
            title='Period',
            content=period,
            theme_override=theme_period
        )