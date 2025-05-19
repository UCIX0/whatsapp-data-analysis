### Pseudocódigo – UI módulos

---

#### 1. **Función `draw_optionbar`** (`optionbar.py`)

```
1	Iniciar
2	Mostrar barra de opciones horizontal (Hydralit):
		• Datos  : OPTION_DATA  (icono + etiqueta)
		• Tema   : THEME
		• key    : 'NavBarOption'
3	Devolver etiqueta seleccionada ('Tables' o 'Visualization')
4	Fin
```

---

#### 2. **Función `render_tables`** (`render_pages.py`)

```
1	Iniciar
2	Crear 4 columnas superiores (st.columns)
3	En columna-1
		3.1	Subtítulo “Messages per User”
		3.2	Mostrar dict_dframes['user_counts']  (sin índice)
4	En columna-2
		4.1	Subtítulo “Messages per Day”
		4.2	Mostrar dict_dframes['per_day']
		     • Formato de fecha “DD MMM YYYY”
5	En columna-3
		5.1	Subtítulo “Messages per Hour”
		5.2	Mostrar dict_dframes['per_hour']
6	En columna-4
		6.1	Subtítulo “Messages per Weekday”
		6.2	Mostrar dict_dframes['per_weekday']
7	Dibujar línea divisoria
8	Crear 2 columnas inferiores
9	En columna-1
		9.1	Subtítulo “Probability of Starting a Conversation”
		9.2	Mostrar dict_dframes['start_conversations']
		     • Formato numérico “%.1f%%”
10	En columna-2
		10.1	Subtítulo “Most Shared Links”
		10.2	Mostrar dict_dframes['links']
		     • Columna “Links” como hipervínculo
11	Fin
```

---

#### 3. **Función `render_charts`** (`render_pages.py`)

```
1	Iniciar
2	Subtítulo “Messages over Time”
3	Mostrar figura dict_figs['messages_over_time']
4	Subtítulo “Word Cloud”
5	Mostrar figura dict_figs['wordcloud']
6	Fin
```

---

#### 4. **Función `cards_show`** (`stats_cards.py`)

```
1	Iniciar
2	Calcular métricas básicas:
		• total  = número de filas (mensajes)
		• users  = número de usuarios únicos
		• period = fecha mínima  → fecha máxima
		• links  = total de enlaces (stats.link_sharing)
3	Definir 4 temas de color (messages, users, links, period)
4	Crear 4 columnas
5	En columna-1
		5.1	Mostrar tarjeta “Messages”  (total)
6	En columna-2
		6.1	Mostrar tarjeta “Users”     (users)
7	En columna-3
		7.1	Mostrar tarjeta “Links”     (links)
8	En columna-4
		8.1	Mostrar tarjeta “Period”    (periodo)
9	Fin
```

---
