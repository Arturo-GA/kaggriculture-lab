# Kaggriculture: investigación y primer experimento

Fecha de consulta: 12 de septiembre de 2026. Las cifras 2700 y 3000 proceden del usuario; en esta primera investigación no se verificó una instantánea del leaderboard. La revisión posterior guarda una en `results/live/leaderboard.json` y el diagnóstico de nuestra submission en [LIVE_DIAGNOSIS.es.md](LIVE_DIAGNOSIS.es.md). Ningún paper demuestra por sí solo que una técnica supere esos ratings en Kaggriculture.

## Qué hay que optimizar

Gana el saldo final. La temporada tiene 720 estados, las órdenes de venta compiten en un mercado común y el inventario sin vender no suma al resultado. La mano de obra encarece progresivamente y el almacén limita la producción que puede conservarse. La granja rival es pública, pero su almacén es privado. El motor instalado establece un segundo por decisión; sus configuraciones y reglas se verificaron en `kaggle-environments==1.32.7`. [Motor oficial y reglas](https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture).

Mi interpretación: el problema reúne inversión, planificación de trabajo y competencia por precios. Producir más puede reducir el ingreso si la oferta deprime los precios o si la cosecha llega tarde. Conviene medir victorias, margen frente al rival, caja propia y coste de ejecución.

## Auditoría del notebook adjunto

El `main.py` extraído coincide exactamente con el SHA-256 declarado por el notebook: `94c1c2c05ae7cde8fca9ee3957b01112c1cbab82c7434aae6a5f24fa7485bc4c`. La primera extracción de Windows añadió CRLF; se normalizó a los saltos LF originales antes de construir los experimentos. La prueba inicial conservada en `results/smoke.json` corresponde a esa copia con CRLF, semánticamente equivalente; los experimentos posteriores usan el hash original.

V37 ya contiene rutas condicionadas por tiendas, reparaciones de acciones, proyectos de fertilización y trabajo, anticipación de ventas, protección de stock y planificación terminal. Sus comentarios conservan atribuciones a múltiples autores. El texto adjunto afirma mejoras en una evaluación y cero victorias netas adicionales en un panel élite distinto; son resultados del autor, no reproducidos aquí. Las rutas y controladores no son aportaciones nuevas de este repositorio.

Dos notebooks distintos pueden contener el mismo agente: el export de Tetsutani descargado hoy coincide byte por byte con V37. No se cuenta como evidencia independiente. Nagata y prvsiyan tienen hashes distintos y se usan como rivales que reaccionan a nuestras acciones. No representan necesariamente al líder actual. Los archivos de rivales quedan fuera del repositorio y del agente exportado; `results/opponents.json` registra sus fuentes y hashes.

## Lecciones de competencias similares

| Fuente primaria | Evidencia publicada | Aplicación propuesta aquí |
|---|---|---|
| [Lux AI S3, solución ganadora](https://github.com/tonykozlovsky/lux-ai3-pub) | IMPALA, memoria, predicción auxiliar del rival, profesores históricos y pool de oponentes. Sus autores reportan más de 20 mil millones de pasos entre experimentos. | Aprender un selector de decisiones de alto nivel y evaluar contra un pool; ese coste desaconseja empezar replicando toda su escala. |
| [Lux AI S3, tercer puesto](https://github.com/andreyd41/lux3-bot) | Solución de aprendizaje por imitación. | V37 y otras políticas públicas pueden generar demostraciones; comenzar con una política competente reduce exploración inútil. |
| [Lux AI S2, baseline](https://github.com/RoboEden/Luxai-s2-Baseline/blob/main/Luxai-s2-Baseline4Gym/README.md) | Baseline con PPO y flujo de behavior cloning desde replays. | Separar generación de partidas, entrenamiento y evaluación; evitar mezclar partidas de entrenamiento y validación. |
| [Halite IV, cuarto puesto](https://github.com/0Zeta/HaliteIV-Bot) | Heurísticas parametrizadas y búsqueda evolutiva inicial; los autores describen problemas de sobreajuste y simetría. | Optimizar parámetros pequeños es una vía razonable, pero una victoria contra una copia de uno mismo no prueba generalización. |

Estas son transferencias propuestas, no resultados medidos en Kaggriculture. La evidencia incluye enfoques neuronales y heurísticos: ser más reciente o complejo no garantiza ganar.

## Papers recientes y eficiencia

| Trabajo | Qué aporta | Decisión para este proyecto |
|---|---|---|
| [AlphaEvolve, 2025](https://arxiv.org/abs/2506.13131) | Generación y evolución de código guiadas por evaluadores automáticos. | Adoptar el ciclo hipótesis → modificación acotada → simulación → descarte. Este repositorio no implementa AlphaEvolve ni llama a Gemini. |
| [DreamerV3, Nature 2025](https://www.nature.com/articles/s41586-025-08744-2) | Un modelo de mundo permite mejorar políticas mediante futuros imaginados; resultados en más de 150 tareas con configuración común. | Referencia para aprender valores y políticas. Aquí el simulador exacto ya existe: aprenderlo entero podría añadir coste y error innecesarios. |
| [TD-M(PC)², L4DC 2026](https://proceedings.mlr.press/v331/lin26a.html) | Restricción de política para reducir problemas de sobreestimación en planificación con modelos aprendidos. | Inspira limitar cambios respecto a una política base. No trasladamos sus resultados de control continuo como garantía para este juego discreto. |
| [R2-Dreamer, marzo de 2026](https://arxiv.org/abs/2603.18202) | Reducción de redundancia en modelos visuales; el resumen reporta entrenamiento 1,59× más rápido que DreamerV3 en sus pruebas. | Baja prioridad inmediata: nuestra observación es estructurada, no una imagen. La cifra no permite estimar ahorro en Kaggriculture. |

## Experimentos implementados

Se conserva V37 y se interviene únicamente en el horizonte de reservas de ventas. Las reservas originales verifican stock disponible, compromisos de recogida, compras, deudas de ventas ya anticipadas, límite de órdenes y ventana terminal.

1. `h2`, `h6`, `h8`: horizontes de 2, 6 y 8 turnos frente a los 4 de V37.
2. `pressure`: horizonte 4/6/8 según exposición de nuestro stock a una posible oferta rival, calculada con producción madura visible y sensibilidad de precios. Es un escenario de presión, no una reconstrucción del almacén privado.
3. `matched6`: seis turnos solo tras seis observaciones consecutivas con semejanza de granjas ≥90%, entre pasos 336 y 647; en otro caso, conserva cuatro. Reutiliza la medida de semejanza existente de V37. Nace después de observar que `h6` mejora partidas similares pero reduce ligeramente caja contra Nagata; por ello requiere semillas nuevas.

El experimento inicial explora tres semillas y ambos asientos. La confirmación usa semillas separadas y compara las variantes con V37 contra los mismos rivales. Cada partida arranca políticas independientes y dura los 720 estados del motor. No hay oponentes que simplemente reproduzcan acciones grabadas ni lectura de observaciones privadas rivales.

Las semillas pueden generar malas hierbas diferentes por asiento. Por eso una partida entre políticas idénticas no tiene que empatar: el control correcto comprueba que intercambiar las etiquetas de los asientos invierte el margen. Los dos asientos de una misma semilla son observaciones relacionadas, no dos mundos independientes. El tamaño efectivo de la evidencia es pequeño.

## Próximas hipótesis priorizadas

1. **Planificación de ventas por escenarios:** comparar vender ahora, parcialmente o después usando consumo conocido de tiendas y varias ofertas rivales plausibles. Validar el modelo económico contra el motor antes de buscar políticas.
2. **Asignación diaria de trabajadores:** optimizar beneficio marginal por acción con fechas límite de riego, alimentación y cosecha. Empezar con un pequeño conjunto de proyectos factibles, no con todas las combinaciones de acciones.
3. **Selector aprendido de rutas:** entrenar con demostraciones y resultados simulados una política pequeña que elija inversiones y productos según tiendas, mercado y rival. Validar también frente a rutas no usadas para entrenar.
4. **Liga y distilación:** solo tras ampliar oponentes y acelerar simulación, entrenar con rivales históricos y destilar en una política CPU ligera. Medir ganancia por hora de cómputo y latencia por turno.

Los resultados de esta ejecución se documentan en `RESULTS.es.md` y en JSON por partida. El kernel produce un archivo de submission; un push de kernel no equivale a enviarlo al leaderboard ni proporciona un rating nuevo.
