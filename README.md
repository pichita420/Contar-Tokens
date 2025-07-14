# Token Counter ChatGPT/Wolfram (Avanzado)

Contador de tokens para mensajes de ChatGPT y Wolfram, con funciones avanzadas:

- Leer mensajes desde `.txt` o `.json`
- Elegir modelo (`gpt-4o`, `gpt-4`, `gpt-3.5-turbo`)
- Ver tokens totales y por mensaje
- Guardar resultados
- Interfaz gráfica con menús
- Detección automática de roles y plugins (formato API/JSON o texto plano)

## Uso

1. Instala dependencias:
   ```sh
   pip install tiktoken
   ```

2. Ejecuta el script:
   ```sh
   python token_counter.py
   ```

3. Pega o abre tu historial (pueden ser líneas tipo `Usuario:`, `Asistente:`, `Wolfram:`, o formato JSON).

4. Elige el modelo y pulsa "Calcular tokens".

5. Guarda resultados si lo deseas.

## Ejemplo de entrada (texto)

```
Usuario: ¿Cuál es la derivada de x^2?
Asistente: Consultando Wolfram Alpha...
Wolfram: Output: 2x
Asistente: La derivada de x^2 es 2x.
```

## Ejemplo de entrada (JSON)

```json
{"role": "user", "content": "¿Cuál es la derivada de x^2?"}
{"role": "assistant", "content": "Consultando Wolfram Alpha..."}
{"role": "function", "name": "wolfram_alpha", "content": "Output: 2x"}
{"role": "assistant", "content": "La derivada de x^2 es 2x."}
```

## Exporta los resultados

Puedes guardar el cálculo en un archivo `.txt` para consulta o registro.

---

**Cualquier duda, mejora o sugerencia, crea un issue en el repo.**

Traduce tu conversacion al formato que lee para que funcione.
