# Frontier9: búsqueda de una estrategia propia para acercarnos al oro — 20-21 de septiembre de 2026

Pregunta de Arturo: buscar una estrategia innovadora (en los datos, en papers recientes y en foros de juegos
con reglas parecidas) para tener un agente único que pueda llegar a oro. Este documento recoge qué se
investigó, qué se midió, qué se descartó y el candidato que sale.

## 1. Cómo se investigó

Se lanzó un flujo de seis investigadores en paralelo (derrotas en vivo, replays del top 10, mecánicas del
motor, papers, foro y notebooks de Kaggle, juegos análogos) con síntesis y verificación adversaria al
final. El límite de uso de la sesión cortó el flujo: terminaron tres (top 10, papers, foro) y dos dejaron
resultados parciales muy aprovechables (derrotas y juegos análogos); mecánicas, síntesis y verificación no
corrieron y las hice a mano. Notas completas en `outputs/session/gold/*.md` (fuera de Git).

La manipulación del sorteo de tiendas quedó descartada antes de empezar: Kaggle borra la semilla de la
configuración que ve el agente (31 bits) y las malas hierbas solo aparecen con probabilidad 0,005 por
casilla, así que dentro de una partida no hay información ni cómputo para inferirla.

## 2. Qué hace el top 10 (medido)

85 replays del 17 al 20 de septiembre de diez equipos del top (`outputs/session/gold/topteams.md`). El
ingreso se reconstruyó exacto, turno a turno (el banco reconstruido coincide en 169 de 170 asientos). Contra
27 rivales tipo v9/4 en la misma partida ganan 26 con **+9822 de media**, y todo el margen se hace después
del día 15 (v9/4 va +5,4k por delante el día 12):

| Producto | Top 10 (unidades a precio) | v9/4 | Diferencia |
|---|---|---|---:|
| Fresa | 231 a 154 | 244 a 119 | **+6541** (misma producción, mejor precio) |
| Tomate | 77 a 80 | 11 a 105 | **+5028** |
| Zanahoria | 159 a 51 | 109 a 48 | +2866 |
| Lana | 117 a 123 | 133 a 95 | +1760 |
| Huevo | 115 a 50 | 90 a 50 | +1227 |
| Melón | 77 a 168 | 73 a 224 | **−3463** (v9/4 gana la carrera del melón) |
| Fertilizante neto / contrataciones | | | −2578 / −1293 |

Tres mecanismos: (A) venta paciente: v9/4 regala 70 fresas por partida a 13 monedas de media y ellos solo
26; venden lotes de 2-4 justo después de cada consumo del pueblo y amanecen con 16-28 fresas guardadas
porque liquidan trigo, zanahoria, huevo y tomate antes de medianoche; (B) tomates y zanahorias en casillas
liberadas fertilizando el trigo, con la MISMA cuadrilla de 11 manos (nadie usa manos dedicadas; la mano 12
cuesta 144 al día y el programa con mano propia apenas da +2k); (C) tamaño de rebaño y cultivos según las
tiendas que van saliendo (15-22 ovejas con dos tiendas de hilo, 18-33 tomates con dos tiendas de tomate):
de ahí salen las partidas de +15k a +45k. Ninguno reproduce una cinta de 720 turnos: son planificadores.

## 3. Por qué perdemos en la franja 2800-2900 (medido)

Auditoría de 85 partidas en vivo de Frontier8 contra rivales de 2750 o más (`outputs/session/gold/f8_mechanisms.txt`),
clasificando al rival por cuántos turnos reproduce cada agente público:

| Familia rival | Nuestro balance | Pérdida mediana |
|---|---:|---:|
| Derivado de v9/4 con **capa de venta anticipada** (25 submissions) | 7-22 | −356 |
| Derivado de v9/4 con retoques de orden o cantidades (21) | 19-10 | −109 |
| Linaje V50 (11) | 5-7 | −1335 |
| Adaptativo, sin cinta (6) | 1-6 | −7642 |
| Clon público exacto (4) | 4-0 | — |

El mecanismo dominante es que **nos adelantan el mismo lote**: en un libro saturado (cotización por debajo
del precio base) la capa pública RACEGATE de v9/4 nunca adelanta la venta; el lote espera en el almacén el
turno de la ruta mientras el pueblo drena el exceso. Todos los clones hacen lo mismo, así que los dos
granjeros guardan lotes idénticos, y el derivado privado que vende uno o varios turnos antes se lleva el
precio. Ocurre en 34 de 47 derrotas (mediana −458 monedas) y en 22 de ellas supera el margen de la derrota.
Ejemplo (episodio 111104694, contra Tschinkel en vivo, 118 516 a 118 804): los dos guardábamos 18 fresas
desde el turno 624; él vendió 12 en el 645 a 91 y nosotros 9 en el 646 a 68 y 9 en el 647 a 51: 346
monedas en un lote, margen final −288.

## 4. Qué dice la literatura

- Juegos de anticipación (Fudenberg y Tirole 1985) y "predatory trading" (Brunnermeier y Pedersen 2005;
  Carlin, Lobo y Viswanathan 2007; Schied y Zhang, juegos de impacto de mercado): con impacto permanente
  el equilibrio es una carrera por vender primero, y los agentes esperan juntos mientras el premio es
  pequeño. En nuestro mercado, vender k turnos antes que un rival que vende en T vale
  `pendiente × lote × (lote − drenaje × k)` monedas relativas: máximo con k pequeño y negativo más allá de
  `lote / drenaje`. Con el precio exacto del motor: una fresa de lote 18 con tres tiendas da +595 con k=1,
  +294 con k=12 y −35 con k=24.
- Pago relativo (paradoja de Schaffer en el duopolio de Cournot; Amir y otros 2025): cuando solo cuenta
  ganar, cada unidad vendida antes que el rival vale su precio MÁS lo que le baja al rival. Por eso
  "retener" salió negativo en nuestras pruebas y en las de Tschinkel, y "repartirse el mercado" es un error.
- Evaluación: semillas emparejadas reducen la varianza de la diferencia de margen al 6,6 %; el cambio de
  asiento es redundante en el 95 % de los casos (medido sobre nuestros resultados).
- Lo que no se traslada: acaparar trigo o fertilizante (un viaje de ida y vuelta vale exactamente 0 y el
  almacén limita a 100), carry de trigo (+150 a +300 en el mejor caso), ganso/huevo (negativo, como ya
  medimos), TAC/Power TAC, Catan, Agricola.

## 5. Experimentos

**Panel de repetición con rival congelado (nuevo).** Cada replay en vivo guarda la semilla. Repetimos la
partida en el motor oficial con esa semilla, las acciones grabadas del rival y nuestro candidato jugando en
vivo. Con Frontier8 el panel reproduce las 85 partidas al céntimo (mismo margen, rival al 100 %), así que
mide directamente cuántas derrotas reales habría dado la vuelta un cambio. Limitación: el rival congelado
no reacciona; por eso todo se confirma después en circuito cerrado.

| Variante sobre Frontier8 | Victorias de 85 (Frontier8: 38) | Derrota→victoria / victoria→derrota | Margen medio |
|---|---:|---:|---:|
| Adelanto acotado K1 | 40 | 8 / 6 | +119 |
| K2 | 45 | 11 / 4 | +209 |
| K3 | 51 | 15 / 2 | +371 |
| **K4** | **51** | **15 / 2** | **+455** |
| K6 / K8 / K12 | 49 / 51 / 52 | 15/4, 18/5, 18/4 | +337 / +340 / +295 |
| K20 / K40 | 53 / 53 | 21 / 6 | +341 / +344 |
| Vender al llegar al almacén (sin puerta) | 49 | 18 / 7 | +137 |
| Planificador de mejor respuesta (simula el libro y decide vender o esperar) | 51 | 17 / 5 | +290 |
| K3 + planificador | 50 | 18 / 7 | +261 |
| Planificador solo a precio hundido (<45 % del base) | 44-48 | | +120 a +252 |
| Ventana adaptativa (responde al adelanto observado) | 50 | 15 / 3 | +436 |
| K8 + reserva de pienso de un día en zanahorias | 55 | 21 / 4 | +439 |
| K4 + reserva de pienso de un día | 54 | 18 / 2 | +556 |

**Circuito cerrado, motor oficial (semillas 7301-7306, 12 partidas por celda; fila = candidato):**

| | Frontier8 | K1 | K4 | K12 | K40 | al llegar | Tschinkel | tetsutani | total de 96 |
|---|---|---|---|---|---|---|---|---|---:|
| Frontier8 | — | 0/12 | | 2/10 | | 10/2 | 12/0 | 10/2 | |
| K4 | 12/0 | 12/0 | — | 2/10 | 4/8 | 8/4 | 12/0 | 10/2 | 66 |
| K8 | 12/0 | 12/0 | 12/0 | 2/10 | 8/4 | 8/4 | 12/0 | 10/2 | 76 |
| K12 | 10/2 | 10/2 | 10/2 | — | 4/8 | 6/6 | 12/0 | 12/0 | 70 |
| K20 | 6/6 | 8/4 | 10/2 | 8/4 | 2/10 | 8/4 | 12/0 | 12/0 | 66 |
| K40 | 6/6 | 6/6 | 8/4 | 8/4 | — | 6/6 | 12/0 | 12/0 | 64 |

Lectura: nuestro Frontier8 pierde 0/12 contra quien se adelanta un solo turno, que es justo lo que pasa en
vivo. Cada ventana gana a la inmediatamente más corta, pero las largas (K20, K40) dejan de ganar a los
clones sin adelanto (6/6) porque regalan el drenaje del pueblo, como predice la fórmula. El planificador de
mejor respuesta gana más contra Tschinkel en alguna semilla (+1918) pero en conjunto no supera a la ventana
fija (56 a 60 de 84) y pierde 2/10 contra el vendedor al llegar; la ventana adaptativa no recupera el
primer lote perdido (0/12 contra K8 y K12). La reserva de pienso de un día suma victorias en el panel
congelado pero en espejo reactivo cambia mundos en los dos sentidos (+1103, −105, −64, −1345 contra K4),
así que no entra.

**Primera elección: K4 (f9_pre4).** Era la más robusta en ese momento: 28 de 28 contra Frontier8 en 14 semillas
(K8: 24 de 28), 12/0 contra quien se adelanta un turno y mejor margen en el panel de rivales reales.

## 6. Aceptación: un candidato que falló en Kaggle y el que lo sustituye

La regla se registró antes de correr (`results/frontier9/plan.json`): control emparejado Frontier8 en el
motor OFICIAL, puntuación emparejada positiva, ninguna regresión por rival, 50 % o más en el espejo contra
Frontier8, sin errores y llamadas por debajo de 1000 ms. Los rivales emulados con ventana más larga (K8, K12,
K40, vender al llegar) se informan pero no deciden: cualquier ventana fija pierde contra una un poco más larga
por construcción. Un primer holdout (semillas 7401-7408) se gastó en K8 + reserva de zanahoria (10/6 contra
Frontier8, rechazado; `results/frontier9/rejected_pre8c_holdout*.json`).

**f9_pre4 pasó el holdout y falló en Kaggle.** Holdout 7421-7428: 137/160 (Frontier8 120), espejo 15/1,
emparejada +17; confirmación oficial 7431-7434: 6/2 en el espejo, +10. En el kernel de Kaggle (semillas
7441-7442) perdió **0/4 contra Frontier8** (−728 y −99) y no exportó nada. Reproduje las dos semillas en local
al céntimo: no era la plataforma, eran dos mundos malos. El rastro turno a turno (`outputs/session/gold/debt_trace.py`)
mostró la causa: la cadena de venta pública vende un lote pequeño de la ruta (1-4 unidades) y **al turno
siguiente suelta todo el stock**; adelantar solo la cantidad de la ruta rompía esa cadena y dejaba el grueso
del lote un turno tarde (20 leches a 89 en vez de 124).

**f9_pre4f: el adelanto se lleva todo el stock del producto.** Mismo cambio dentro de RACEGATE, ventana
`min(4, lote / drenaje)`, pero la venta adelantada es por todo el stock saturado, no solo por la cantidad de
la ruta. Panel de rivales reales: **38 → 54 victorias de 85** (19 derrotas dadas la vuelta, 3 victorias
perdidas, +543 de margen medio). Espejo contra Frontier8 en las 28 semillas de pantalla: 49/56 con +717 de media
(K4 simple: 49/56 con +407 y muchos márgenes de decenas de monedas). Quitar el libro de deudas de la capa no
cambió nada y no entra.

Segunda ronda, regla registrada antes de correr: los dos candidatos y el control juegan las mismas semillas
nuevas 7451-7458 contra los diez rivales que deciden; gana el de mayor total si pasa la misma puerta; la
verificación en Kaggle usa cuatro semillas en lugar de dos.

| Rival (16 partidas) | f9_pre4f | Frontier8 (control) | f9_pre4 |
|---|---:|---:|---:|
| Frontier8 (espejo) | **16/0** (+781) | — | 12/4 |
| Adelanto de un turno | **16/0** (+1046) | 6/10 | 14/2 |
| Tschinkel, Arlene, Gluzdov | **16/0** cada uno (+1350 a +1400) | 16/0 | 14/2 |
| tetsutani y V50 | **12/4** | 6/10 | 8/8 |
| V49 | 12/4 | 6/10 | 8/8 |
| Alperen (First in Line) | 12/4 | **14/2** | 14/2 |
| K0013 | 14/2 | 14/2 | 16/0 |
| **Total de 160** | **142** | 108 | 122 |

Emparejada +34, cero errores, 216 ms. **La puerta estricta falló en un rival**: contra Alperen el candidato
pierde un mundo más que el control. Lo repliqué con 16 semillas nuevas (7471-7486) y es real aunque pequeño:
27/5 frente a 29/3 contra "First in Line", 25/7 frente a 29/3 contra "Market Rhythm", 29/3 igual contra K0013
(`results/frontier9/replication_v48_lineage*.json`). Son agentes del linaje V48 con venta adelantada hasta 24
turnos, hoy en torno a 2750. El candidato es mejor contra todo lo demás y peor, por un mundo de cada dieciséis,
contra esa familia; queda escrito en `plan.json`, `selection.json` y `release.json` como excepción aceptada, y la
decisión es de Arturo.

Verificación en Kaggle (kernel privado `jarturo/kaggriculture-frontier9-preemption`, versión 3, semillas
7461-7464, ambos asientos, control Frontier8): **8/0 contra Frontier8 (+749), 8/0 contra Tschinkel (+1074),
8/0 contra tetsutani (+641; el control 3/5)**; emparejada +10, 215 ms, cero errores. `main.py` y
`submission.tar.gz` coinciden byte a byte con el candidato; SHA-256 del archivo
`a5a7814ff1fbd3d7acae24099f175f6aea1813d3aeb0e88a59aca6961e8ab05a` (`results/frontier9/kaggle_verified.json`).
Las seis pruebas de `test_frontier9.py` pasan. Envío autorizado por Arturo el 20 de septiembre ("envia una
plaza"): **submission 56404796**, una sola plaza; la otra sigue con Frontier8 (56372978) como cobertura. El
rating de las primeras horas no es el resultado final: juzgar a partir de unas 60 partidas.

## 7. Perspectiva honesta sobre el oro

El oro son unos 30 equipos (corte 2918) y casi todos son planificadores o RL que ganan a v9/4 por +9,8k
de media. Frontier9 no cambia eso: corrige la fuga que nos hacía perder contra derivados de nuestra misma
base (el 60 % de los rivales de la franja 2750-2900) y debería devolvernos a la zona de 2850-2900. Para
pasar de ahí hacen falta los mecanismos A-C de la sección 2, que son economía y no capas: el más abordable
es el intercambio neutral en trigo (convertir 8-10 casillas de trigo del borde en tomate entre los días
12 y 18 y fertilizar el trigo restante en sus riegos, con la mano 10 y 11 solo esos días), que los replays
valoran en hasta +4,5k y que Tschinkel no probó en esa forma. Es el siguiente experimento si Arturo quiere
seguir, con el panel de repetición y el circuito cerrado ya montados para medirlo en horas.
