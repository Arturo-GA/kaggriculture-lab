# Cómo juegan los de 2700-3000 y qué haría falta para ganarles — 27 de septiembre de 2026

Petición de Arturo: "Busca una estrategia que pueda ganar también a los de 2700 considerando todo lo aprendido y
revisando las estrategias actuales en kaggle utilizadas".

## 1. Fuentes revisadas

- Los 12 replays en vivo del par activo contra rivales de 2600+ (`vendor/live_f14`) y sus líneas de tiempo económicas
  día a día (`scratchpad/econ_timeline.py`): dinero, manos, terreno, animales, cultivos, alimentación, compras y ventas.
- El archivo público de replays del top-10 diario (dataset `ashok205/kaggriculture-top10-replay-archive`, lote del 25 de
  septiembre, 575 partidas): huellas económicas de DSM (1.º, 3089), Boey (2.º, 3040), Vadim Vasilenko (3.º), M & M & P &
  Q (4.º), DECEM (6.º), Unknown Mother-Goose (8.º), Fourth Quadrant (10.º), Majkel1337, mtmr_s1 y 吃白饭的大肥鱼
  (`outputs/session/gold/top10_econ_0925.json`, 5 partidas por equipo).
- La tabla completa del leaderboard (10.060 equipos, `outputs/session/gold/lb0927/`): cortes 30.º = 2788, 50.º = 2727,
  100.º = 2624, 200.º = 2507, 500.º = 2357. Nuestro equipo: 539.º con 2341 (antes de que Frontier15 suba).
- Las reglas de producción del motor (`kaggriculture.py`: cuidado, alimentación, rendimientos, coste de manos).
- Notebooks públicos actualizados tras el cierre (`vendor/pub0927`): "What 2600+ Farms Do Differently" (georgymamarin),
  "God's mode: hacked stores" (leoprovorov), el calendario de cultivos, la guía de evgendvorkin con el análisis de tres
  replays del campeón; y el foro (hilos sobre el cuadrante sudeste, RL con PPO y clonación de comportamiento, "Six
  things I wish I'd known").

## 2. Hechos del motor que explican la economía

- **Cuidado + alimentación multiplican la producción**: un animal alimentado y cuidado cada día acumula +1 de bonus por
  día y lo cobra en su día de producción. Vaca: 3 leches cada 2 días (×3); oveja: 4 lanas cada 3 días (×4); ganso: 2
  huevos al día (×2). Dos días sin comer y el animal se escapa.
- **Manos**: se contratan cada día; la n-ésima contratación del día cuesta fib(n): 11 manos = 232/día, 12 = 376, 13 =
  609, 14 = 986. Las manos 12 y 13 cuestan casi tanto como las 11 primeras juntas.
- **Terreno**: NE 1000, SW 2000, SE 4000 (en ese orden). Con 4 cuadrantes hay 100 casillas.
- **Mercado**: cada producto tiene su propia curva; huevo y trigo apenas bajan con la saturación (logarítmica), leche y
  fresa bajan linealmente, lana y melón cuadráticamente. El pueblo consume por tienda: 6 unidades/día por producto (12 en
  YARN_STORE y PET_CAFE) más 1 al día del centro. Con 8 tiendas al azar, la demanda esperada es ~13/día de huevo, lana y
  tomate, ~19/día de leche, fresa y zanahoria, ~31/día de trigo.
- Valor neto por casilla y día a precios de final de partida: vaca cuidada 85, ganso cuidado 63, melón 42, zanahoria
  abonada 41, oveja cuidada 41 (lana saturada), tomate abonado 34, trigo abonado 21, fresa 14-18.

## 3. Qué hacen los de 2700-3000 (evidencia)

| Equipo (puesto) | Banco medio | Manos | SE comprado | Animales día 12 (gansos / ovejas / vacas) | Tomates día 12 | Zanahorias día 12 |
|---|---:|---:|---|---|---:|---:|
| Boey (2.º) | 125.539 | 11,8 | no | 20 (7 / 6 / 7) | 0 | 1 |
| Majkel1337 (5.º) | 115.092 | 12,0 | no | 18 (3 / 7 / 8) | 2 | 1 |
| 吃白饭的大肥鱼 (21.º) | 111.187 | 12,6 | no | 19 (5 / 4 / 10) | 5 | 1 |
| Unknown Mother-Goose (8.º) | 110.899 | 12,4 | día 10 | 21 (6 / 5 / 10) | 13 | 0 |
| mtmr_s1 (16.º) | 110.391 | 13,0 | día 10 | 20 (5 / 5 / 11) | 18 | 0 |
| Vadim Vasilenko (3.º) | 109.819 | 12,4 | día 10 | 22 (7 / 6 / 9) | 9 | 7 |
| M & M & P & Q (4.º) | 107.060 | 13,0 | día 12 | 22 (8 / 5 / 9) | 1 | 7 |
| Fourth Quadrant (10.º) | 94.225 | 12,4 | día 10 | 15 (0 / 4 / 11) | 0 | 15 |
| DECEM (6.º) | 93.984 | 12,2 | día 10 | 21 (8 / 6 / 7) | 11 | 9 |
| DSM (1.º) | 89.620 | 12,2 | día 10 | 24 (8 / 7 / 10) | 14 | 4 |
| **Nuestra línea (cha22)** | ~105.000 | 11 | no (solo V219 día 18) | 17 (0-6 / 6-11 / 6-9) | 0 | 0 |

Patrón común: NE el día 6, SW el día 8-9, **SE el día 10-13** (7 de 10 equipos), **12-13 manos**, **20-25 animales el
día 12** con la mezcla ligada a las tiendas (DSM llega a 15 gansos con tres panaderías; Vadim y DECEM a 13-15 ovejas
con dos o tres tiendas de lana; mtmr_s1 a 14 vacas con tiendas de leche), **tomates desde el día ~10** con pizzerías o
mercados, zanahorias con pet cafés, trigo como cultivo de caja (30-50 casillas) y las fresas como relleno. Ingresos
de 5-10k por día desde el día 12 (nosotros 4-8k). Al final dejan de alimentar (las ovejas se escapan a propósito).

En nuestras 12 partidas contra 2600+: kuengo (2685) con 3 tiendas de lana subió a **24 ovejas** y 16 tomates y nos
sacó 35.486; ymg_aq (2814) compró los 4 cuadrantes en los días 6-10, 11 vacas, 10 ovejas, 5 gansos y 18 tomates;
arutyunoff, feel the agi y by usan gansos y tomates. Nuestra granja se congela el día 11 (8 vacas, 9 ovejas, 33 fresas,
24 trigos, 3 cuadrantes, 11 manos) porque la cinta de cha22 lo fija.

## 4. Lo que probamos para copiarlo y por qué no sirve antes del 30

1. **Bloque de expansión en el SE** (gansos u ovejas con manos dedicadas, al estilo de la inversión en tomates de cha22):
   las manos 12 y 13 cuestan 377/día; un bloque de 8-10 gansos deja +1-4k por partida; nuestras 11 manos ya están al
   95 % de uso. El propio cha22 trae estos bloques con puertas muy estrictas (tomates con ≥ 3 pizzerías-mercados desde
   el día 18; 6 ovejas con ≥ 2 tiendas de lana y lana ≥ 220 el día 11): aflojar la puerta de tomates dio −1 en el holdout.
2. **Trasplante de cintas grabadas del top-10** (la misma técnica que usa la línea pública con las rutas de yhay81):
   las cintas adaptativas (DSM, Vadim) se derrumban fuera de su mundo, porque el sorteo de tiendas cambia con la granja
   del rival (cada casilla vacía consume un número aleatorio antes del sorteo) y sus decisiones dependen de las tiendas.
   La cinta de Boey (2.º) reproduce su granja en otros mundos y **gana a nuestro f15_e81 por +4.400 a +13.400 en 4 de 12
   mundos, pero pierde por −20.000 a −61.000 en los otros 8** cuando una compra falla y la cadena se rompe
   (`scratchpad/frozen_top.py`). Hacerlo robusto requiere reconstruir los guardas del chasis para una cinta ajena: días
   de trabajo, sin garantía.
3. **Dirigir el sorteo de tiendas** (notebook "God's mode"): real (una casilla vacía de más cambia el 77 % de los
   sorteos), pero exige inferir la semilla oculta; su autor mide 10-18 % de cobertura y en sus pruebas forzar tiendas
   sin cambiar la producción empeoró el resultado.

## 5. Conclusión y estrategia

- **Para ganar a los de 2700 hace falta otra economía, no otros tiempos de venta**: 4 cuadrantes hacia el día 10, 12-13
  manos, 20-25 animales el día 12 elegidos por las tiendas, tomates y zanahorias tempranos, trigo de caja. Los equipos
  que están ahí lo hacen con planificadores propios o con RL (PPO con clonación de comportamiento sobre los replays
  oficiales del top, 300k-1M partidas). No se puede construir y validar antes del cierre del 30 de septiembre.
- **Lo que sí tenemos** (Frontier15, enviada como 56592376): la mejor ejecución de la línea pública contra sus
  clones (34/36 en bucle cerrado, holdout +33) y una economía ~3-7 % por debajo de los 2700 normales (5k por partida
  contra Boey en mundos limpios). Expectativa realista: 2500-2650; los 2700+ seguirán ganándonos casi siempre.
- **Después del cierre** (si quieres seguir): clonación de comportamiento sobre `ashok205/kaggriculture-top10-replay-
  archive` y `kaggle/kaggriculture-episodes-*` (acciones macro por día: compras, contrataciones, cultivos por casilla) y
  luego PPO contra un panel de clones; el simulador Rust público (`Debmalya`, 550k pasos/s) permite el volumen.
- Ajuste menor probado: incluir huevos (y melón) en la liquidación al abrir ventana (`f15_e81e`, `f15_e81em`): 24/24
  contra 6 clones, igual que `f15_e81` (24/24), delta emparejado −23 por partida y ningún cambio de resultado → no se
  adopta (`outputs/session/gold/screen_f15c_0927.json`).
