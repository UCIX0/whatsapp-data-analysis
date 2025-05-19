### Pseudocódigo – `compute_data.py`

#### 1. Función `compute_dataframes`

```
1  Iniciar
2  Construir y devolver diccionario:
    • 'user_counts'         ← stats.user_message_counts(df)
    • 'per_day'             ← stats.messages_per_dates(df)
    • 'per_hour'            ← stats.messages_per_hour(df)
    • 'per_weekday'         ← stats.messages_per_weekday(df)
    • 'start_conversations' ← analizar_inicios(df)
    • 'links'               ← stats.link_sharing(df)
3  Fin
```

#### 2. Función `compute_figures`

```
1  Iniciar
2  Construir y devolver diccionario:
    • 'messages_over_time' ← visualization.messages_over_time_fig(df)
    • 'wordcloud'          ← visualization.build_wordcloud_fig(df)
3  Fin
```

---

### Pseudocódigo – `data_manager.py`

#### 3. Función `get_data`

```
1  Iniciar
2  file_bytes ← uploaded_file.getvalue()
3  file_hash  ← MD5(file_bytes)

4  Si st.session_state['file_hash'] ≠ file_hash entonces          # archivo nuevo
    4.1  Mostrar loader “Processing chat…”
    4.2  Intentar
         a. df ← chat_to_dataframe(BytesIO(file_bytes))
         b. df ← clean_dataframe(df)
        Capturar ValueError   →  st.error, st.stop()
        Capturar Exception    →  st.error, st.stop()
    4.3  dict_dframes ← compute_dataframes(df)
    4.4  dict_figs    ← compute_figures(df)
    4.5  Guardar en st.session_state:
         • 'file_hash'   = file_hash
         • 'df'          = df
         • 'dict_dframes' = dict_dframes
         • 'dict_figs'    = dict_figs
5  Fin Si

6  Devolver tupla desde caché:
    (st.session_state.df,
     st.session_state.dict_dframes,
     st.session_state.dict_figs)
7  Fin
```
