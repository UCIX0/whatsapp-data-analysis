### Pseudocódigo del módulo **analysis**

---

#### 1. **Función `analizar_inicios`**

```
1. Ordenar el DataFrame por la columna 'datetime'
2. Calcular la diferencia de tiempo ('time_diff') entre mensajes consecutivos
3. Crear columna 'new_convo'
	3.1  Marcar TRUE si 'time_diff' > umbral_minutos
4. Filtrar filas donde 'new_convo' es TRUE  →  guardar en `inicios`
5. Contar cuántas veces cada 'user' aparece en `inicios`
6. Calcular el porcentaje de inicio por usuario
7. Construir DataFrame con columnas
	7.1 'User'
	7.2 'Conversations Initiated'
	7.3 'Start %'
8. Devolver el nuevo DataFrame
```

---

#### 2. **Funciones de `stats.py`**

##### 2.1 `user_message_counts`

```
1. Agrupar el DataFrame por 'user'
2. Contar mensajes en la columna 'message'
3. Ordenar en orden descendente
4. Renombrar columnas a:
	4.1 'Users'
	4.2 'Messages count'
5. Devolver DataFrame resultante
```

##### 2.2 `messages_per_dates`

```
1. Agrupar por la fecha de 'datetime' (solo parte de la fecha)
2. Contar mensajes en la columna 'message'
3. Ordenar en orden descendente
4. Renombrar columnas a:
	4.1 'Dates'
	4.2 'Messages count'
5. Devolver DataFrame resultante
```

##### 2.3 `messages_per_hour`

```
1. Obtener la hora (0-23) de cada valor en 'datetime'
2. Contar frecuencia por hora
3. Asegurar que existan las 24 horas (rellenar con 0 donde falte)
4. Formatear la hora como "HH:00"
5. Renombrar columnas a:
	5.1 'Hour'
	5.2 'Messages count'
6. Devolver DataFrame resultante
```

##### 2.4 `messages_per_weekday`

```
1. Obtener el nombre del día de la semana de cada 'datetime'
2. Contar frecuencia por día
3. Reordenar en secuencia Monday→Sunday y rellenar con 0 si falta
4. Renombrar columnas a:
	4.1 'Days'
	4.2 'Messages count'
5. Devolver DataFrame resultante
```

##### 2.5 `link_sharing`

```
1. Buscar todas las URLs en cada mensaje usando expresión regular
2. Expandir resultados a una sola columna
3. Contar frecuencia de cada URL
4. Renombrar columnas a:
	4.1 'Links'
	4.2 'Count'
5. Devolver DataFrame resultante
```

##### 2.6 `remove_links`

```
1. Crear máscara booleana:
	1.1 TRUE si el mensaje **no** contiene una URL
2. Filtrar DataFrame usando la máscara
3. Devolver copia del DataFrame filtrado
```

---

#### 3. **Funciones de `visualization.py`**

##### 3.1 `messages_over_time_fig`

```
1. Llamar a `messages_per_dates` para obtener mensajes por día
2. Ordenar DataFrame por la columna 'Dates'
3. Crear figura y ejes (matplotlib)
4. Dibujar gráfica de línea:
	4.1 Eje X = 'Dates'
	4.2 Eje Y = 'Messages count'
5. Configurar etiquetas, título, rejilla y rotación de fechas
6. Ajustar diseño (`tight_layout`)
7. Devolver la figura
```

##### 3.2 `build_wordcloud_fig`

```
1. Concatenar todos los mensajes que **no** contienen URLs
2. Filtrar palabras con longitud > 4 caracteres
3. Generar nube de palabras (WordCloud)
4. Crear figura y ejes
5. Mostrar la nube de palabras en el eje
6. Ocultar ejes y bordes
7. Devolver la figura
```

---

> **Nota:** Cada función se puede invocar de forma independiente o como parte del pipeline completo de análisis dentro de la aplicación **WhatsApp Chat Analyzer**.
