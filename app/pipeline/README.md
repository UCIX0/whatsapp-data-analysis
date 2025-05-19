### Pseudocódigo del módulo **pipeline**

---

#### 1. **Función `extract_line`**

```
1  Iniciar
2  Si la línea comienza con '[' entonces            ──► (formato Apple)
	2.1  Definir patrón Apple (fecha, hora, usuario, mensaje)
3  En caso contrario                               ──► (formato Android)
	3.1  Definir patrón Android (fecha, hora, usuario, mensaje)
4  Buscar el patrón en la línea
5  Si hay coincidencia
	5.1  Devolver (date_str, time_str, user, message)
6  Si no hay coincidencia
	6.1  Devolver (None, None, None, None)
7  Fin
```

---

#### 2. **Función `parse_datetime`**

```
1  Iniciar
2  Limpiar la cadena de hora:
	2.1  Remover puntos
	2.2  Compactar espacios
	2.3  Unir 'a m' / 'p m'  →  'am' / 'pm'
3  Detectar:
	3.1  Si contiene AM/PM
	3.2  Si contiene segundos
	3.3  Si el año es de 2 dígitos
4  Construir formato de fecha (%d/%m/%y ó %d/%m/%Y)
5  Construir formato de hora:
	5.1  12 h  →  %I:%M[:%S] %p
	5.2  24 h  →  %H:%M[:%S]
6  Concatenar formatos → `dt_format`
7  Concatenar date_str + clean_time → `date_time_str`
8  Intentar convertir a `pd.to_datetime`
9  Si falla  →  lanzar ValueError
10 Devolver Timestamp
11 Fin
```

---

#### 3. **Función `chat_to_dataframe`**

```
1  Iniciar
2  Si file_obj es bytes
	2.1  Convertir a BytesIO
3  Si file_obj es BytesIO o BufferedReader
	3.1  Envolver en TextIOWrapper (UTF-8 estricto)

4  Definir lista vacía `records`
5  Definir patrones:
	5.1  pattern_Android  (sólo fecha y hora, sin usuario/mensaje)
	5.2  pattern_Apple    (sólo fecha y hora, sin usuario/mensaje)

6  Leer archivo línea por línea
	6.1  Eliminar saltos de línea y caracteres invisibles
	6.2  (date, time, user, msg) ← extract_line(línea)

	6.3  Si date y time y user existen
		6.3.1  Intentar convertir date+time → Timestamp
			Si falla  →  imprimir error, continuar
		6.3.2  Añadir dict{datetime, user, message} a `records`

	6.4  Si la línea NO coincide con pattern_Android NI pattern_Apple
	     **y** `records` no está vacío
		6.4.1  Añadir texto a `records[-1]["message"]`        ← (mensaje multilínea)

7  Manejo de errores:
	7.1  UnicodeDecodeError  →  ValueError “archivo no UTF-8”
	7.2  Otro Exception      →  propagar

8  Construir DataFrame con columnas [datetime, user, message]
9  Si DataFrame está vacío  →  ValueError
10 Devolver DataFrame
11 Fin
```

---

#### 4. **Función `clean_dataframe`**

```
1  Iniciar
2  Crear copia del DataFrame original
3  Eliminar filas con valores NaN

4  Leer archivo YAML de configuración
5  Extraer lista `patterns` de mensajes de sistema a omitir
6  Si `patterns` está vacía
	6.1  Devolver DataFrame limpio (reset_index)

7  Escapar cada patrón  →  lista `escaped`
8  Unir patrones con OR  →  regex global

9  Crear máscara:
	9.1  TRUE si 'message' contiene alguno de los patrones
10 Filtrar DataFrame con ~máscara  (quitar mensajes de sistema)
11 Resetear índice
12 Devolver DataFrame filtrado
13 Manejar excepciones genéricas →  lanzar con mensaje descriptivo
14 Fin
```

---
