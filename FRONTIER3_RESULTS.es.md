# Frontier3: apertura financiada y depósitos con capacidad compartida

**Estado: candidato experimental.** Mejora frente a nuestras versiones anteriores en estas pruebas, pero **no superó el criterio predefinido de 50 % frente a V41 en el bloque oficial local**. La decisión posterior de exportarlo queda explícita en `results/frontier3/release_decision.json`. El resultado original sigue marcado como fallido; no hay ajuste de código tras observar las semillas reservadas.

## Qué cambia y de dónde procede

- Apertura con órdenes solicitadas de trigo 5 / 10 / 60, tomada del V41 compartido por Arturo, que acredita a Rayk Kretzschmar. Las cantidades ejecutadas dependen del motor y la liquidez.
- Reserva de dinero para la contratación del primer amanecer y comprobación de semillas: cuatro helpers de Ahmed Berat Ozer, Apache-2.0, integrados sobre Frontier2. La validación de PLANT se generaliza al día actual antes del turno 696.
- Desde el turno 716, asignación conjunta de los 100 espacios del almacén: DROP completo, PLACE de un producto o conservación de carga. Se estima valor con precios visibles y se recalculan ventas a partir del estado propio proyectado.
- Se conserva el critic anterior, sin reentrenamiento. No es un modelo nuevo de RL ni una estrategia enteramente original. Los créditos completos están en NOTICE.md.

## Selección y validación

Exploración C++: 96 partidas totales, cuatro semillas y tres variantes más Frontier2. Cada variante obtuvo 20 victorias y 4 derrotas: 4/8 contra V41, 8/8 contra matched6 y 8/8 contra Frontier2. Las protecciones de recursos y capacidad **no añadieron victorias** respecto a cambiar solo la apertura; la capacidad redujo ligeramente el margen medio contra V41. Se eligió por sus contratos físicos probados, sin atribuirle una ventaja competitiva separada.

**Panel reservado C++:** 224 partidas totales, candidato y control, ocho semillas nuevas y siete rivales. Es exploratorio; no sustituye al motor oficial.

| Rival | Victorias | Empates | Derrotas | Cambio de resultado vs control | Margen medio |
|---|---:|---:|---:|---:|---:|
| v41_review | 13 | 0 | 3 | +13 | +1209.4 |
| matched6 | 16 | 0 | 0 | +1 | +31559.9 |
| frontier2_early | 16 | 0 | 0 | +8 | +29320.0 |
| router | 16 | 0 | 0 | +1 | +42230.1 |
| kaito | 16 | 0 | 0 | +0 | +21547.4 |
| nagata | 16 | 0 | 0 | +0 | +111285.4 |
| prvsiyan | 15 | 0 | 1 | +0 | +4947.8 |

Máximo observado C++: 1847.6 ms; incluye creación de observaciones y planificación del sistema. No cumple 1000 ms como medición bruta y no se oculta. El criterio temporal final usa el callback medido en el motor oficial.

**Confirmación oficial 1.32.7:** 112 partidas totales, candidato y control, cuatro semillas distintas y ambos asientos.

| Rival | Victorias | Empates | Derrotas | Cambio de resultado vs control | Margen medio |
|---|---:|---:|---:|---:|---:|
| v41_review | 3 | 0 | 5 | +3 | +542.8 |
| matched6 | 8 | 0 | 0 | +1 | +27296.4 |
| frontier2_early | 8 | 0 | 0 | +4 | +24832.1 |
| router | 8 | 0 | 0 | +0 | +39762.9 |
| kaito | 8 | 0 | 0 | +0 | +31726.8 |
| nagata | 8 | 0 | 0 | +0 | +112073.2 |
| prvsiyan | 8 | 0 | 0 | +0 | +4253.6 |

Máximo de callback del candidato: 381.7 ms. Errores/fallbacks o contratación inicial insuficiente reportados: 0. Todas las partidas completaron 720 estados y 719 llamadas.

Telemetría del candidato en ese bloque: 0 unidades de compra de semillas recortadas, 0 siembras rescatadas y confirmadas, 8 turnos con intervención de capacidad. La nueva apertura ya evita la escasez inicial en estas semillas; las protecciones de compra/siembra se comprobaron en casos dirigidos, sin atribuirles las victorias del panel. Se confirmaron las tres contrataciones previstas en cada partida.

La comparación de resultado asigna 1 a victoria, 0,5 a empate y 0 a derrota, y resta el control en el mismo rival, semilla y asiento. No equivale a rating de Kaggle. Los dos asientos de una semilla pueden producir partidas idénticas: no son muestras estadísticas independientes.

Las 31 pruebas de código pasaron: 30 en la ejecución conjunta y la de empaquetado al repetirla con acceso a su carpeta temporal, que el sandbox había bloqueado. Siete pruebas nuevas comprueban efectos del motor oficial: apertura, reserva de dinero, siembra factible, capacidad, retención de carga y descarga posterior. No se demuestra que toda la carga retenida llegue a venderse.

## Publicación y límites

Agente congelado: `candidates/frontier3_capacity.py`, SHA-256 `257a7248affaed0ef126474e6f19de3e23045cb911ea01b8b1ecfda582825981`.

Notebook privado: https://www.kaggle.com/code/jarturo/kaggriculture-frontier-joint-planner . El paquete v3 conserva los archivos v1/v2 y el archivo raíz de la primera submission.

El notebook exige 24 partidas oficiales adicionales con hashes exactos, ejecución válida y mejora emparejada frente al control antes de exportar. El criterio original contra V41 se sigue calculando y comunicando, incluso cuando falla. Esta excepción de publicación es posterior a los resultados locales, no una validación predefinida aprobada.

El panel contiene V41 y otros rivales públicos almacenados anteriormente; no representa todos los agentes actuales del top. La capacidad usa precios visibles, no anticipa perfectamente al rival y no garantiza monetizar inventario antes del final. No se garantiza superar 2797, mejorar el rating anterior ni conseguir medalla.

**Kaggle: ejecución y archivo verificados.**

| Rival | Victorias | Empates | Derrotas | Cambio de resultado vs control | Margen medio |
|---|---:|---:|---:|---:|---:|
| v41_review | 2 | 0 | 2 | +2 | +605.5 |
| matched6 | 4 | 0 | 0 | +0 | +19545.0 |
| frontier2_early | 4 | 0 | 0 | +2 | +18580.0 |

Máximo de callback: 374.4 ms; criterio original de este bloque: `True`; comprobaciones para exportación experimental: `True`.

Archivo: `results/frontier3/kaggle/submission.tar.gz`, SHA-256 `6531b8d948d374133ab070401d730635c9b51449a5b617a0fff45f0624ef0fdc`. El main.py descargado y el contenido del TAR coinciden por bytes con el candidato congelado.

Envío al leaderboard solicitado por Arturo: submission `56222986`, estado observado `SubmissionStatus.PENDING` a 2026-09-14T05:57:41.493740+00:00. El rating inicial no se toma como resultado final.
