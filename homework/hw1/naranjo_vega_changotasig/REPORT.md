# Duelo 1 — Búsqueda clásica frente a un modelo de lenguaje

**Autores:** Naranjo, Vega y Changotasig · **Curso:** Inteligencia Artificial · **Tarea 1**

## Resumen

Comparamos cinco algoritmos de búsqueda (BFS, DFS, UCS, IDS y A*) en dos dominios, y luego enfrentamos A* con un modelo de lenguaje pequeño (qwen2.5:3b), solo y con A* como herramienta. A* resolvió las 80 instancias de forma óptima en milisegundos. El modelo solo no acertó ninguna, y con la herramienta llegó a 70/80. Todos sus fallos fueron al copiar datos, no al buscar, y su rendimiento dependió mucho de cómo estaba escrito el prompt.

## 1. Introducción

La pregunta del trabajo es sencilla: ¿qué gana y qué pierde un modelo de lenguaje frente a un algoritmo con garantías, cuando ambos resuelven los mismos problemas? Primero medimos los algoritmos clásicos entre sí (Parte 1) y después los comparamos con el LLM (Parte 2). Para resumir la comparación usamos la tarjeta de puntuación del curso (§5).

## 2. Metodología

**Dominios e instancias.** Usamos el rompecabezas de 8 piezas, donde cada movimiento cuesta 1, y una cuadrícula ponderada con terreno `.`=1, `,`=3 y `~`=8. Trabajamos con los bancos del estudio (semilla 20260807): 10 instancias por nivel, con profundidades óptimas 4/8/12/16 y cuadrículas de 5×5, 8×8, 12×12 y 16×16.

**Algoritmos y medidas.** En el rompecabezas, A* usa fichas mal colocadas, Manhattan y Manhattan×3. En la cuadrícula usa Manhattan (admisible, porque el terreno más barato cuesta 1), ×3 y ×8. De cada ejecución medimos coste, longitud, expansiones, frontera máxima y tiempo real, y reportamos la mediana con su rango intercuartílico [Q1–Q3]. Pusimos un límite de 120 s, y las ejecuciones que lo agotan se registran como *timeout*, no como fallo. Los tests del estudio pasan sin modificar (5/5 y 5/5), y nuestro motor coincide con los del estudio (8/8).

**Duelo.** El LLM es qwen2.5:3b (Q4_K_M) en Ollama, con temperatura 0 y semilla 0, y recibe las instancias como texto. El sistema *híbrido* es el mismo modelo, que puede pedir `{"tool": "astar", …}`: nosotros ejecutamos A* y le devolvemos el resultado, sin reintentos. Un validador propio (`code/validator.py`), que nunca consulta al modelo, comprueba que la ruta sea legal, recalcula su coste y lo compara con el óptimo de A* y con el coste que reporta el modelo.

## 3. Resultados — Parte 1

### 3.1 Comparación general

**Tabla 1.** Rompecabezas a profundidad 16: todos menos DFS encuentran el óptimo, coste 16. Frontera y tiempo son medianas; en IDS, la frontera es la profundidad de la pila.

| Algoritmo | Expansiones [Q1–Q3] | Frontera | ms |
|---|---|---|---|
| A* + Manhattan | 128 [103–164] | 86 | 0,9 |
| A* + mal colocadas | 551 [519–627] | 350 | 3,2 |
| BFS = UCS | 9 442 [8 486–10 057] | 5 653 | 24 / 33 |
| IDS | 25 174 [21 467–26 216] | 17 | 55 |
| DFS (coste 24 835) | 25 284 [9 356–43 813] | 20 019 | 69 |

**Tabla 2.** Cuadrícula 16×16.

| Algoritmo | Coste [Q1–Q3] | Expansiones [Q1–Q3] | Frontera | ms | Resueltas |
|---|---|---|---|---|---|
| A* + Manhattan | 19,5 [18,3–23,5] | 65 [47–73] | 41 | 0,4 | 10 |
| UCS | 19,5 [18,3–23,5] | 177 [156–205] | 87 | 0,9 | 10 |
| BFS | 32 [28–43,8] | 208 [197–220] | 38 | 0,8 | 10 |
| IDS\* | 28 [27–28] | 639 565 [253 542–2 088 340] | 14 | 2 867 | **5** |
| DFS | 321 [307–371] | 138 [119–160] | 148 | 0,5 | 10 |

\* Las otras 5 instancias agotaron los 120 s, así que esta mediana usa solo las 5 más fáciles.

![](fig/fig1_expansions_puzzle.png) ![](fig/fig2_expansions_grid.png)
**Figuras 1 y 2.** Expansiones según el tamaño. En el rompecabezas, la búsqueda no informada crece exponencialmente, mientras que A* + Manhattan crece mucho más despacio: su ventaja sobre BFS pasa de 7× a 74×. En la cuadrícula, salvo IDS, nadie pasa de unas 200 expansiones, así que lo que separa a los algoritmos es la garantía de optimalidad, no el cómputo.

![](fig/fig6_wallclock.png)
**Figura 6.** El tiempo real sigue a las expansiones; solo IDS en la cuadrícula pasa claramente de 0,1 s.

IDS confirma el compromiso que esperábamos: ahorra memoria, no tiempo. En el rompecabezas usa una pila de 17 marcos frente a los 5 653 nodos de frontera de BFS, a cambio de 2,7 veces más expansiones. En la cuadrícula, al no tener tabla de transposición, los ciclos lo hacen explotar y agota el límite en 5 de las 10 instancias de 16×16. DFS siempre encuentra una solución, pero en la cuadrícula cuesta hasta 22 veces el óptimo, y en el rompecabezas llegó a devolver 94 280 movimientos.

### 3.2 Análisis 1: optimalidad

A* con heurística admisible obtuvo el mismo coste que UCS en las **80/80** instancias. BFS solo es óptimo cuando todos los costes son iguales. Coincidió con UCS en las 40 instancias del rompecabezas, pero fue **subóptimo en 33 de las 40 cuadrículas**, con un sobrecoste mediano por tamaño de 1,15× a 1,92× (máximo 2,91×). IDS se comportó igual que BFS, porque también minimiza el número de movimientos y no el coste.

El caso más claro es la cuadrícula 12×12 n.º 9. Las dos rutas tienen 11 movimientos. BFS se quedó con la primera que encontró, `DDDDDDRRRRR`, que cruza terreno caro y cuesta 32. UCS y A* encontraron `DRRRDDRRDDD`, que cuesta 11: BFS paga un 191 % de más.

### 3.3 Análisis 2: dominancia heurística

![](fig/fig3_dominance.png)
**Figura 3.** Ningún punto queda por encima de y = x: Manhattan expandió igual o menos nodos que mal colocadas en las 40/40 instancias, sin contraejemplos.

La ventaja crece con la profundidad: la mediana del cociente de expansiones (Manhattan / mal colocadas) pasa de 1,00 a 0,67, 0,43 y **0,22**.

### 3.4 Análisis 3: romper la admisibilidad

**Tabla 3.** Efecto de inflar la heurística. Aceleración = expansiones(admisible) / expansiones(inflada); el sobrecoste se mide sobre las soluciones subóptimas.

| Dominio | h | Aceleración [Q1–Q3] | Más lenta | Subóptimas | Sobrecoste mediano (máx.) |
|---|---|---|---|---|---|
| Cuadrícula | ×3 | **2,60× [1,78–3,08]** | 0/40 | 13/40 | 30 % (50 %) |
| Cuadrícula | ×8 | 2,92× [1,88–3,33] | 0/40 | 22/40 | 40 % (150 %) |
| Rompecabezas | ×3 | **1,00× [0,80–1,25]** | 12/40 | 7/40 | 17 % (50 %) |

![](fig/fig4_inadmissible.png)
**Figura 4.** En el rompecabezas, h×3 casi no aporta: a profundidad 16 expande más que A* admisible (0,77×) y empeora 6 de las 10 soluciones.

En la cuadrícula, inflar h sí acelera (de 1,65× en 5×5 a 3,67× en 16×16), pero se paga en calidad. Nos llamó la atención que cinco rutas subóptimas tienen *menos* movimientos y más coste: como h cuenta pasos, al darle tanto peso A* termina pareciéndose a BFS. En el rompecabezas, con f ≈ 3h la búsqueda se vuelve casi voraz y se mete en callejones, así que pierde a la vez en velocidad y en calidad.

### 3.5 Análisis 4: factor de ramificación efectivo

![](fig/fig5_bstar.png)
**Figura 5.** En el rompecabezas, Manhattan tiene un b* menor que mal colocadas, y la diferencia crece con la profundidad (1,22 frente a 1,37 a profundidad 16). En la cuadrícula se mantiene entre 1,15 y 1,20. El b* = 1,00 de ×8 refleja una búsqueda voraz, no eficiencia.

## 4. Resultados — Parte 2: el duelo

**Tabla 4.** Categorías de fallo según el validador, sobre 40 instancias por dominio.

| Categoría | LLM cuadr. | LLM rompec. | Híbrido cuadr. | Híbrido rompec. |
|---|---|---|---|---|
| Ruta ilegal | 36 | 40 | 2 | 7 |
| Legal pero subóptima | 3 | 0 | 0 | 0 |
| Óptima con coste mal reportado | 1 | 0 | 0 | 0 |
| JSON mal formado | 0 | 0 | 1 | 0 |

![](fig/fig7_duel_grid_scaling.png) ![](fig/fig10_duel_puzzle_scaling.png)
**Figuras 7 y 10.** Tasa de optimalidad por nivel, con IC de Wilson al 95 % (n = 10). El LLM solo no acierta nunca. El híbrido acierta 8/10/10/9 en la cuadrícula y 7/10/6/10 en el rompecabezas, sin tendencia con el tamaño.

![](fig/fig8_duel_grid_failures.png) ![](fig/fig11_duel_puzzle_failures.png)
**Figuras 8 y 11.** Casi todos los fallos del LLM solo son respuestas ilegales: casi nunca llega a una ruta válida que optimizar.

**El LLM solo no planifica.** En la cuadrícula, 10 respuestas fueron solo la casilla de salida y otras 26 terminaron a una mediana de 6 pasos de la meta. En el rompecabezas, para 40 tableros distintos el modelo produjo solo 7 secuencias de movimientos, y 4 de ellas cubren 35 respuestas (`R R D D` aparece diez veces). Su respuesta no depende del tablero.

**Los 10 fallos del híbrido son de interfaz, no de búsqueda.**
- **Entrada mal copiada (3):** en la cuadrícula transpuso la fila y la columna de S, y en el rompecabezas desplazó el hueco al copiar el tablero dos veces. A* resolvió bien un problema que no era el planteado.
- **Salida mal copiada (6):** recibió la solución correcta y la cortó (cuatro veces) o la alteró (dos).
- **JSON inválido (1):** escribió `[13, 9}}`.

![](fig/fig9_duel_grid_latency.png) ![](fig/fig12_duel_puzzle_latency.png)
**Figuras 9 y 12.** El híbrido tarda unas 2 veces lo que el LLM solo, y ambos quedan 3–5 órdenes de magnitud por encima de A*. Los tokens de salida del híbrido crecen con el tamaño porque copia rutas más largas.

**Reproducibilidad.** Hicimos 5 llamadas idénticas a una instancia por nivel y contamos las respuestas distintas del LLM solo (niveles 1 a 4):
- **Temperatura 0:** 2/2/1/1 en la cuadrícula y 2/2/2/1 en el rompecabezas.
- **Temperatura 0,7:** 5/5/5/2 y 4/4/5/5.

Es decir, el modelo no es determinista ni siquiera a temperatura 0. *[Confirmar la semilla.]* El híbrido y A*, medidos en el nivel 2, dieron siempre una única respuesta óptima.

## 5. Tarjeta de puntuación del duelo

**Tabla 5.** Clásico = A* + Manhattan; Híbrido = qwen2.5:3b con A* como herramienta. «a / b» = cuadrícula / rompecabezas.

| Eje | Clásico | LLM | Híbrido | Evidencia |
|---|---|---|---|---|
| Corrección | 80/80 óptimas | 0/80 (legales: 4/80) | 70/80 (37/40 y 33/40) | `results/duel/*/summary.csv` |
| Garantía | Coste mínimo **siempre que** h no sobreestime (Manhattan lo cumple en ambos dominios); completo en espacio finito. Nada sobre el tiempo. | Ninguna. Ruta válida en 4/80; nada sobre la instancia 81. | Ninguna propia: la de A* se pierde si el modelo copia mal (10/80). Óptimo solo si el validador lo confirma. | §3.2, §4 |
| Coste (mediana) | 26 / 16 expansiones | 542 + 59 / 317 + 25 tokens (entrada + salida) | 1 212 + 97 / 913 + 77 tokens, más 25 expansiones | `results/duel/*/raw.csv` |
| Latencia (mediana / p95) | 0,2 / 0,5 ms; 0,2 / 1,5 ms | 6,6 / 10,1 s; 2,7 / 2,7 s | 11,9 / 16,0 s; 5,6 / 5,8 s | Figs. 9 y 12 |
| Reproducibilidad (5 llamadas) | 1 respuesta | T = 0: 1–2; T = 0,7: 2–5; ninguna óptima | 1 respuesta, óptima | `repro_summary.csv` |
| Escalamiento | 100 % en los 4 tamaños; las expansiones crecen (Figs. 1–2) | 0 % en los 4: **no hay acantilado**, porque nunca despega del suelo | 80–100 % / 60–100 %, sin tendencia | Figs. 7 y 10 |
| Interpretabilidad | Ruta y coste verificables; optimalidad demostrable | Solo ruta y coste declarado (mal en sus 4 rutas legales) | Ruta + traza JSON: muestra si el error fue de entrada o de salida | `.llm_cache/` |
| Modo de fallo | Ninguno en 80/80; más allá de 16, sin medir | Erróneo pero seguro: 76/80 ilegales, siempre con un coste declarado | Errores de copia (9) y JSON inválido (1), todos detectados | `failures.md` |

## 6. Dónde pudimos haber sido injustos (*Where we may have been unfair*)

**Ajustamos el prompt después de ver los resultados, y eso pesó mucho.** En el rompecabezas, el prompt v1 traía el ejemplo de formato `["U", "L", ...]`. Con él, el híbrido acertó solo **4/40**: en 35 de sus 36 fallos recibió la solución correcta de A* y la cambió por una secuencia que empezaba como el ejemplo. Al cambiar únicamente ese ejemplo (v2) subió a **33/40**, mientras que el LLM solo se quedó en 0/40 con ambas versiones. El híbrido depende tanto del prompt como de A*. Manhattan, en cambio, no se tocó después de ver los datos. *[¿Una sola versión del prompt de la cuadrícula?]*

Tampoco dimos la misma información a todos. A* recibe la instancia ya estructurada, mientras que el modelo la recibe como texto y tiene que reconstruirla; justo ahí nacen 3 fallos del híbrido. Además, las instancias favorecen a lo clásico: el nivel más difícil le cuesta a A* menos de 2 ms, así que nunca lo ponemos a prueba, y para un modelo de 3B parámetros ese nivel ya es largo. La herramienta es nuestro propio A*, así que el híbrido no puede superar a lo clásico: lo que mide es la fiabilidad de la interfaz, y como no reintentamos, una llave de más cuenta como fallo. Un modelo más grande quizá copiaría mejor, pero no podemos saberlo sin probarlo. Por último, comparamos milisegundos con segundos sin contar las horas que nos tomó programar cada parte. *[Horas por brazo; hardware.]*

## 7. Lo que nuestra evidencia no respalda

- Nada fuera del rango medido: el 9/10 del híbrido en 16×16, o el 5/10 de IDS, no dicen nada sobre 20×20.
- El 0/80 corresponde a un solo modelo de 3B, cuantizado, con un solo prompt por dominio. Además, 0/10 por nivel es compatible con una tasa real de hasta el 28 % (IC de Wilson al 95 %).
- Las tasas por nivel del híbrido tienen intervalos amplios (6/10 → [31 %, 83 %]) y no permiten hablar de una tendencia.
- Que h×3 no acelere el rompecabezas vale para Manhattan y estas 40 instancias, no para A* ponderado en general.

## 8. Conclusiones

Para estos problemas, la búsqueda clásica es imbatible: es óptima, rápida y predecible. El modelo pequeño, por sí solo, no planifica. Con A* como herramienta acierta casi siempre, pero hereda la garantía de A* solo cuando copia bien los datos, y eso depende sobre todo del prompt. Por eso, la conclusión más útil de este trabajo no es que gane lo clásico, sino que en un sistema híbrido el punto débil es la interfaz entre el modelo y la herramienta.
