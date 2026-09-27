# Qué aprender del top 100 — Kaggriculture, 27 de septiembre

La prioridad es una planificación de cultivos y producción más flexible dentro de la granja existente. La muestra actual no respalda comprar siempre el cuarto cuadrante ni aumentar siempre la plantilla. Frontier17 ya incorpora varias de las técnicas observadas; añadirlas otra vez no constituye una mejora.

## Muestra y comprobaciones

Leaderboard fijado al **2026-09-27T17:57:56.999211+00:00**: corte top 100 **2616.3**. Se consultó el agente activo con mayor rating de cada uno de los 100 equipos y se tomaron sus dos partidas públicas completas más recientes, sin seleccionar por victoria. Son **200 actuaciones en 184 partidas distintas** y **184 semillas distintas**. Los rangos se refieren a esa fotografía, no necesariamente al puesto cuando jugaron.

Se reconstruyeron **11 partidas distintas**, que cubren 12 casos de equipos en los puestos 1, 3, 5, 8, 10, 20, 25, 29, 40, 60, 80 y 100. Todos los resultados coinciden exactamente con Kaggle y ambas contabilidades cierran: 3000 + ventas − compras − salarios − terrenos = dinero final. Además pasaron 960 comparaciones de campos de estado entre el extractor y el motor oficial 1.32.7.

Referencia propia: las **4 primeras partidas públicas disponibles de Frontier17** (56615489). Son suficientes para mostrar su estructura actual, pero insuficientes para medir su fuerza y no constituyen una comparación emparejada de rating: rivales, tiendas y mundos difieren.

## Diferencias observadas

| Medida | Top 100 (200 actuaciones) | Frontier17 (4 actuaciones) |
|---|---:|---:|
| Mediana de máximos diarios de trabajadores, días 10–26 del motor | 11 | 11 |
| Mediana de animales al paso 288 | 19 | 17 |
| Mediana de casillas de fresa al paso 288 | 23 | 33 |
| Mediana del primer estado con SW abierto | 218 | 266 |
| Actuaciones con cuarto cuadrante en algún momento | 52/200 | 0/4 |

El paso 288 corresponde a 12 días transcurridos (el motor cuenta desde el día 0). El pico de trabajadores no es una media de ocupación: se toma el máximo diario y después la mediana. Los números de cultivos son una fotografía; cero melones en ese instante no significa que nunca se cultivaran. F17 plantó 12 melones a lo largo de cada una de sus cuatro partidas.

En el top 10 la mediana también es 11 trabajadores y solo 6/20 actuaciones abren SE. En el top 100, 94/200 habían plantado tomate antes del paso 288 y 70/200 zanahoria. Son variantes de estrategia, no requisitos universales.

## Caso contable: DECEM frente a Boey

Partida **114279609**, ambos en el mismo mundo: DECEM gana **112302 a 106494**, diferencia **5808**. DECEM planta diez tomates el día 16 y otro el 18, con tres pizzerías observadas. Sus ventas de tomate suman **15990**, con **550** de gasto en semillas. El saldo de esas dos líneas es **15440**; no es beneficio marginal total porque también hay trabajo, fertilizante y costes de oportunidad.

| Componente contable | DECEM menos Boey |
|---|---:|
| Tomate: ventas menos semillas | +15440 |
| Lana: ventas menos compra de ovejas | -6487 |
| Trigo: ventas menos compras y semillas | -970 |
| Contratación | -620 |
| Fertilizante: ventas menos compras | -379 |
| Resto de componentes | -1176 |
| Diferencia final comprobada | +5808 |

Boey emplea muchas compras y reventas, pero termina perdiendo esta partida. Es un ejemplo de por qué facturación bruta o número de operaciones no equivalen a ventaja. En la muestra, 140/200 actuaciones tienen alguna compra y venta del mismo insumo en un turno; solo **20/200**, de **12 equipos**, lo hacen en diez o más turnos. Incluso ese indicador describe órdenes, no ganancias realizadas.

Otros casos reconstruidos: Vadim vende 9967 de zanahoria; Smackaveli, 12731; Christoffer Thimsen, 19699 de tomate. Son ingresos brutos de casos concretos, no mejoras que podamos adjudicarnos.

## Qué podemos implementar y en qué orden

| Prioridad | Cambio concreto | Qué ya existe y qué falta | Validación necesaria |
|---|---|---|---|
| 1 | Previsión de cultivos por edad, producción restante y escenarios de resiembra | `_cxtb_their_supply` prolonga la oferta de cada tomate visible hasta el final. Es una hipótesis empírica de resiembra, no cuatro producciones seguras. Separar plantas actuales y futura resiembra; derivar aperturas de tiendas del calendario real. | Error de previsión en partidas reservadas y efecto sobre decisiones; después partidas completas contra F17. |
| 2 | Rotación adaptable en casillas existentes, con tomate o zanahoria según demanda futura | Ya hay `_v9_carrot`, reservas de trigo y una inversión de tomates. Falta elegir por casilla y calendario de trabajo cuándo sustituir una plantación que termina, sin exigir SE ni alterar a ciegas las rutas. | Semillas nuevas; medir producción realmente entregada, alimento, costes, fallos de acciones y victorias. |
| 3 | Adelantar producción del tercer cuadrante y aumentar densidad animal cuando resulte rentable | SW aparece unas 48 acciones antes en la mediana del top. F17 tiene 17 animales frente a mediana 19. Comprar antes sin mover colocación, alimento y recorridos no produce esa ventaja. | Cambiar un bloque coherente de trabajo; medir ROI tras salarios, varias tiendas y ambos asientos. |
| 4 | Previsión del rival que contemple varias conductas de mercado | F16/F17 optimizan contra órdenes parecidas a las propias y condicionan su uso a semejanza de granjas. Hacen falta escenarios cuando el rival tiene otra producción, usando solo estado público e historial. | Rivales reactivos de varias familias; evitar usar sus órdenes simultáneas ocultas o puntuar solo contra grabaciones. |

La primera entrega viable es la previsión del punto 1, seguida de una rotación acotada del punto 2. Eso es más manejable que reemplazar todo el agente por RL. El aumento de animales necesita un planificador de recorridos y recursos; no basta cambiar una constante. Estas son propuestas de implementación respaldadas por la investigación, no cambios de política ya validados ni promesas de top 100.

## Restricciones del diseño que ya comprobamos

- Tomates: primera producción a edad 8, cuatro fechas consecutivas. Fresas: primera a edad 10, cuatro fechas separadas por dos días. Regar y fertilizar modifican el rendimiento; ignorar el fin de ciclo sesga el valor.
- La mano 12 cuesta 144 monedas adicionales por día; la 13, 233. Sumarlas durante veinte días cuesta 7540, antes de terreno, semillas y alimento. La expansión tiene que pagar ese coste marginal.
- El motor abre tiendas cada tres días, hasta ocho. La previsión heredada contiene incrementos fijos en 22 y 24; hay que derivarlos de `townShopUnlockInterval`, la fecha y las tiendas ya observadas, y probar el cambio.
- Las cuatro partidas propias terminan con almacén e inventarios vacíos. No hay evidencia aquí para priorizar otra capa genérica de liquidación final; varias ya están implementadas.
- Una grabación revela conducta, no si el autor emplea PPO, búsqueda, reglas o una combinación. Tampoco hace falta trasplantar sus cintas de acciones para aprender estas decisiones.

## Revisión del análisis anterior

El informe `ANALISIS_2700.es.md` utilizaba otra muestra, del día 25, y generalizó en exceso la necesidad de cuatro cuadrantes y 12–13 trabajadores. La muestra actual demuestra diversidad y corrige esa recomendación. No podemos deducir el algoritmo privado ni afirmar, solo a partir de replays, que la solución requiera RL o que sea imposible construir una mejora antes del cierre.

## Evidencia y reproducción

- [Leaderboard público](https://www.kaggle.com/competitions/kaggriculture/leaderboard).
- [Selección con equipos, submissions y episodios](results/top100_0927/selection.json).
- [Resumen comprobado](results/top100_0927/summary.json), [200 perfiles](results/top100_0927/profiles.json).
- [Contabilidad exacta](results/top100_0927/accounting.json), [referencia F17](results/top100_0927/baseline.json).
- [Verificación y hashes](results/top100_0927/verification.json); eventos completos en `features.json.gz`.
- Replays brutos comprimidos en `vendor/top100_0927/`, fuera de Git. No se incorporó código privado de rivales.

```powershell
.venv/Scripts/python.exe -X utf8 research_top100.py
.venv/Scripts/python.exe -X utf8 analyze_top100.py
.venv/Scripts/python.exe -X utf8 baseline_top100.py
.venv/Scripts/python.exe -X utf8 audit_top100.py
.venv/Scripts/python.exe -X utf8 report_top100.py
```

La selección queda fijada y las descargas se reanudan sin sustituir las partidas originales. Los errores iniciales de cuota quedaron resueltos con espera y reintento; el censo final está completo. F17 permanece congelado; esta investigación no realiza una nueva submission.
