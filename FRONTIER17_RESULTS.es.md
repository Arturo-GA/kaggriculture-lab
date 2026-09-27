# Frontier17: resultados del candidato de mercado

Puerta registrada: **SUPERADA**. Ganancia emparejada frente a F16: **+10 puntos de partida** en 128 por agente (victoria = 1, empate = 0,5). Son puntos de esta evaluación, no puntos del leaderboard.

El holdout contiene 256 partidas completas, ocho rivales, ocho semillas nuevas y ambos asientos. Las semillas son la unidad de diversidad; los asientos del mismo mundo están correlacionados.

| Rival | F17 V/E/D | F16 V/E/D | Diferencia de puntuación |
|---|---:|---:|---:|
| f16_repaired | 16/0/0 | 1/14/1 | +8 |
| g25_mooman0222_a62376 | 16/0/0 | 16/0/0 | +0 |
| g25_mooman0222_baf0d3 | 16/0/0 | 16/0/0 | +0 |
| g25_wangyh_v44 | 16/0/0 | 16/0/0 | +0 |
| n25_abhinav0370_127ed3 | 16/0/0 | 14/0/2 | +2 |
| n23_prvsiyan_178ae0 | 16/0/0 | 16/0/0 | +0 |
| n23_kenanzhang9_b52378 | 16/0/0 | 16/0/0 | +0 |
| v43 | 16/0/0 | 16/0/0 | +0 |

Ganancia excluyendo el enfrentamiento contra F16: **+2**. Máxima llamada del candidato: **458.0 ms** frente al límite de 1000 ms. Partidas con errores registrados: **0**.

Las doce pruebas unitarias de F16/F17 pasaron. Incluyen conservación de inventario y compras frente al mercado oficial, rechazo por caja/capacidad insuficiente y conservación de comandos físicos.

## Prueba adicional frente a otra estrategia de compras

En cuatro semillas nuevas (17301–17304), F17 puntuó **4/8** y F16 **0/8** contra `f17_robust`. Resultado de la prueba: **superada**. Este rival es una variante original creada para someter a prueba la hipótesis de órdenes similares; no se presenta como un agente del top 100.

## Diagnóstico de las pérdidas reales

Se reconstruyeron exactamente 28 partidas originales. En el panel contrafactual de F16, el candidato convierte **4 de 17 derrotas** y pierde **0 de cuatro victorias**. Mejora 15, empeora 2 y deja 4 iguales. Los rivales grabados no pueden responder; esas cifras no estiman la tasa de victoria real.

Después de congelar el código llegaron cinco derrotas nuevas de F16. El candidato mejora las cinco y convierte **2/5** en victorias al repetir esos rivales grabados. El control reproduce las cinco exactamente; no se retocó el candidato después de verlas. Este segundo panel tampoco sustituye una evaluación competitiva en Kaggle.

La derrota de −8488 contra trantrikien239 pasa a −306. Las derrotas amplias frente a keiz, Smackaveli y ShunkiKyoya siguen presentes; requieren mejorar la composición productiva. Detalles, contabilidad y fuentes en [FRONTIER17_RESEARCH.es.md](FRONTIER17_RESEARCH.es.md).

## Estado y alcance

Arturo autorizó una plaza con «Y lanza una plaza a kaggle». Submission **56615489**, estado **SubmissionStatus.PENDING** al 2026-09-27T17:54:58.532074+00:00. [Notebook privado](https://www.kaggle.com/code/jarturo/kaggriculture-frontier17-input-market), versión 1. La verificación en Kaggle completó 16 partidas: F17 ganó 8/8 contra F16, con cero errores y máximo 248.4 ms. El paquete exportado coincide byte por byte con el local. Se realizó un solo envío. El estado del par activo se conserva en `results/frontier17/active_after_submission.json`.

Consulta previa al envío (2026-09-27T17:33:58.058397+00:00): corte top 100 **2621.9**, Frontier16 **2449.8**, puesto **273**. No hay una conversión validada entre este panel público y el rating. Tampoco se dispone del código privado de los mejores rivales. La duda del foro sobre versiones públicas posteriores al cierre de publicación sigue registrada en el informe de investigación.

## Reproducción

```powershell
.venv/Scripts/python.exe -X utf8 build_f17.py
.venv/Scripts/python.exe -X utf8 -m unittest test_frontier17 test_frontier16 -v
.venv/Scripts/python.exe -X utf8 analyze_f17.py
.venv/Scripts/python.exe -X utf8 report_f17.py
.venv/Scripts/python.exe -X utf8 pack_frontier17.py
.venv/Scripts/python.exe -X utf8 make_frontier17_notebook.py
```

La regeneración no reejecuta el holdout ni realiza solicitudes a Kaggle. La matriz, semillas, hashes y umbrales están en [plan.json](results/frontier17/plan.json).

SHA-256 del candidato: `62b766886208e572462c19f45706cf9d0eded7d048c39a55a6093212bd72426f`.
