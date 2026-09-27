"""Validate replay-derived evidence and produce an implementation-focused report."""
from collections import Counter
import gzip, hashlib, json
from pathlib import Path
from statistics import median

ROOT=Path('results/top100_0927')


def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def main():
    selection=read('selection.json');features=read('features.json');accounts=read('accounting.json');baseline=read('baseline.json')
    assert selection['complete'] and features['complete'] and accounts['complete'] and baseline['complete']
    rows=features['rows'];own=baseline['rows'];all_band=features['bands'][0]
    assert len(rows)==200 and len({r['team_id'] for r in rows})==100
    assert all(v==2 for v in Counter(r['team_id'] for r in rows).values())
    assert len({r['episode'] for r in rows})==184
    lookup={(r['episode'],r['seat']):r for r in rows}
    snapshot_checks=0
    for r in accounts['rows']:
        assert r['reproduced_exactly']
        f=lookup[(r['id'],r['seat'])]
        assert f['rewards']==r['recorded_rewards']
        for step in set(f['snapshots']) & set(r['snapshots']):
            actual=r['snapshots'][step][str(r['seat'])]
            for key in ('money','hands','layout','ripe','quadrants','shops','shed','carried'):
                assert f['snapshots'][step][key]==actual[key],(r['id'],step,key)
                snapshot_checks+=1
        for seat in (0,1):
            net=sum(v if k.startswith('SELL_') else -v for k,v in r['money'][seat].items())
            assert 3000+net==r['recorded_rewards'][seat]
    heavy=lambda r:sum(r['same_turn_buy_sell'].get(i+'_turns',0) for i in ('WHEAT','FERTILIZER'))>=10
    info=dict(snapshot_utc=selection['checked_utc'],teams=100,player_games=len(rows),unique_games=features['unique_games'],
        independent_seeds=len({r['seed'] for r in rows}),top100_cut=selection['leaderboard'][-1],
        baseline=dict(candidate=baseline['candidate'],submission=baseline['submission'],games=len(own),
            peak_hands_median=median(r['peak_hands_midgame'] for r in own),
            animals_step288_median=median(sum(r['snapshots']['288']['layout'].get(a,0) for a in ('GOOSE','COW','SHEEP')) for r in own),
            strawberry_step288_median=median(r['snapshots']['288']['layout'].get('STRAWBERRY',0) for r in own),
            sw_step_median=median(r['first_land_step']['SW'] for r in own)),
        bands=features['bands'],heavy_same_turn_input_games=sum(map(heavy,rows)),
        heavy_same_turn_input_teams=len({r['team_id'] for r in rows if heavy(r)}),
        sw_step_median=median(r['first_land_step']['SW'] for r in rows if 'SW' in r['first_land_step']),
        reconstructed_team_cases=len(accounts['rows']),reconstructed_unique_games=len({r['id'] for r in accounts['rows']}),
        exact_snapshot_field_checks=snapshot_checks,
        final_leftover_games=sum(sum(r['snapshots']['719']['shed'].values())+sum(r['snapshots']['719']['carried'].values())>0 for r in rows),
        own_final_leftover_games=sum(sum(r['snapshots']['719']['shed'].values())+sum(r['snapshots']['719']['carried'].values())>0 for r in own))
    case=next(r for r in accounts['rows'] if r['rank']==1)
    ledgers=case['money']; names=[a['team_name'] for a in sorted(case['agents'],key=lambda a:a['seat'])]
    def grouped(m):
        values={}
        for item in ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','FERTILIZER','EGG','MILK','WOOL'):
            animal={'EGG':'GOOSE','MILK':'COW','WOOL':'SHEEP'}.get(item)
            values[item]=m.get('SELL_'+item,0)-m.get('BUY_PRODUCT_'+item,0)-m.get('BUY_SEED_'+item,0)
            if animal:values[item]-=m.get('BUY_ANIMAL_'+animal,0)
        values['HIRE']=-m.get('HIRE',0);values['LAND']=-m.get('BUY_LAND',0)
        return values
    group=list(map(grouped,ledgers));seat=case['seat'];other=1-seat
    delta={k:group[seat][k]-group[other][k] for k in group[seat]}
    assert sum(delta.values())==case['recorded_rewards'][seat]-case['recorded_rewards'][other]
    info['decem_boey_case']=dict(episode=case['id'],teams=names,rewards=case['recorded_rewards'],
        decem_minus_boey=delta,margin=sum(delta.values()),tomato_sale=ledgers[seat]['SELL_TOMATO'],
        tomato_seed_cost=ledgers[seat]['BUY_SEED_TOMATO'],
        note='Accounting decomposition, not causal incremental profit. Fertilizer, feed, land and shared labor are reported separately.')
    profiles=[]
    for r in rows:
        profiles.append({k:r[k] for k in ('team','rank','submission','episode','seat','margin','seed','first_land_step','peak_hands_midgame','same_turn_buy_sell')} | {
            'layout_step288':r['snapshots']['288']['layout'],'shops_step288':r['snapshots']['288']['shops'],
            'plantings_by_crop':dict(Counter(p['crop'] for p in r['plantings'])),
            'late_plantings_by_crop':dict(Counter(p['crop'] for p in r['plantings'] if p['planted_day']>=12))})
    write('profiles.json',profiles);write('summary.json',info)
    blob=(ROOT/'features.json').read_bytes();(ROOT/'features.json.gz').write_bytes(gzip.compress(blob,mtime=0))
    write('verification.json',dict(verified=True,engine='1.32.7',exact_snapshot_field_checks=snapshot_checks,
        accounts_balanced=True,source_sha256=hashlib.sha256(Path('candidates/f17_selected.py').read_bytes()).hexdigest(),
        feature_sha256=hashlib.sha256(blob).hexdigest(),files={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [ROOT/n for n in ('selection.json','accounting.json','baseline.json','features.json.gz','profiles.json','summary.json')]}))
    lines=['# Qué aprender del top 100 — Kaggriculture, 27 de septiembre','',
        'La prioridad es una planificación de cultivos y producción más flexible dentro de la granja existente. '
        'La muestra actual no respalda comprar siempre el cuarto cuadrante ni aumentar siempre la plantilla. '
        'Frontier17 ya incorpora varias de las técnicas observadas; añadirlas otra vez no constituye una mejora.','',
        '## Muestra y comprobaciones','',
        f"Leaderboard fijado al **{selection['checked_utc']}**: corte top 100 **{info['top100_cut']['score']}**. "
        'Se consultó el agente activo con mayor rating de cada uno de los 100 equipos y se tomaron sus dos partidas '
        'públicas completas más recientes, sin seleccionar por victoria. Son **200 actuaciones en 184 partidas distintas** '
        f"y **{info['independent_seeds']} semillas distintas**. Los rangos se refieren a esa fotografía, no necesariamente al puesto cuando jugaron.",'',
        f"Se reconstruyeron **{info['reconstructed_unique_games']} partidas distintas**, que cubren 12 casos de equipos "
        'en los puestos 1, 3, 5, 8, 10, 20, 25, 29, 40, 60, 80 y 100. Todos los resultados coinciden exactamente '
        'con Kaggle y ambas contabilidades cierran: 3000 + ventas − compras − salarios − terrenos = dinero final. '
        f"Además pasaron {snapshot_checks} comparaciones de campos de estado entre el extractor y el motor oficial 1.32.7.",'',
        f"Referencia propia: las **{len(own)} primeras partidas públicas disponibles de Frontier17** ({baseline['submission']}). "
        'Son suficientes para mostrar su estructura actual, pero insuficientes para medir su fuerza y no constituyen '
        'una comparación emparejada de rating: rivales, tiendas y mundos difieren.','',
        '## Diferencias observadas','',
        '| Medida | Top 100 (200 actuaciones) | Frontier17 (4 actuaciones) |',
        '|---|---:|---:|',
        f"| Mediana de máximos diarios de trabajadores, días 10–26 del motor | {all_band['midgame_peak_hands_median']:g} | {info['baseline']['peak_hands_median']:g} |",
        f"| Mediana de animales al paso 288 | {all_band['animals_step288_median']:g} | {info['baseline']['animals_step288_median']:g} |",
        f"| Mediana de casillas de fresa al paso 288 | {all_band['crops_step288_median']['STRAWBERRY']:g} | {info['baseline']['strawberry_step288_median']:g} |",
        f"| Mediana del primer estado con SW abierto | {info['sw_step_median']:g} | {info['baseline']['sw_step_median']:g} |",
        f"| Actuaciones con cuarto cuadrante en algún momento | {all_band['any_se']}/200 | {sum('SE' in r['first_land_step'] for r in own)}/4 |",'',
        'El paso 288 corresponde a 12 días transcurridos (el motor cuenta desde el día 0). '
        'El pico de trabajadores no es una media de ocupación: se toma el máximo diario y después la mediana. '
        'Los números de cultivos son una fotografía; cero melones en ese instante no significa que nunca se cultivaran. '
        'F17 plantó 12 melones a lo largo de cada una de sus cuatro partidas.','',
        'En el top 10 la mediana también es 11 trabajadores y solo 6/20 actuaciones abren SE. '
        'En el top 100, 94/200 habían plantado tomate antes del paso 288 y 70/200 zanahoria. '
        'Son variantes de estrategia, no requisitos universales.','',
        '## Caso contable: DECEM frente a Boey','',
        f"Partida **{case['id']}**, ambos en el mismo mundo: DECEM gana **112302 a 106494**, diferencia **5808**. "
        'DECEM planta diez tomates el día 16 y otro el 18, con tres pizzerías observadas. '
        'Sus ventas de tomate suman **15990**, con **550** de gasto en semillas. '
        'El saldo de esas dos líneas es **15440**; no es beneficio marginal total porque también hay trabajo, '
        'fertilizante y costes de oportunidad.','',
        '| Componente contable | DECEM menos Boey |','|---|---:|']
    labels={'TOMATO':'Tomate: ventas menos semillas','WOOL':'Lana: ventas menos compra de ovejas',
            'WHEAT':'Trigo: ventas menos compras y semillas','HIRE':'Contratación','FERTILIZER':'Fertilizante: ventas menos compras'}
    for k,label in labels.items():lines.append(f'| {label} | {delta[k]:+g} |')
    lines += [f"| Resto de componentes | {sum(v for k,v in delta.items() if k not in labels):+g} |",
        f"| Diferencia final comprobada | {sum(delta.values()):+g} |",'',
        'Boey emplea muchas compras y reventas, pero termina perdiendo esta partida. '
        'Es un ejemplo de por qué facturación bruta o número de operaciones no equivalen a ventaja. '
        'En la muestra, 140/200 actuaciones tienen alguna compra y venta del mismo insumo en un turno; '
        f"solo **{info['heavy_same_turn_input_games']}/200**, de **{info['heavy_same_turn_input_teams']} equipos**, "
        'lo hacen en diez o más turnos. Incluso ese indicador describe órdenes, no ganancias realizadas.','',
        'Otros casos reconstruidos: Vadim vende 9967 de zanahoria; Smackaveli, 12731; '
        'Christoffer Thimsen, 19699 de tomate. Son ingresos brutos de casos concretos, no mejoras que podamos adjudicarnos.','',
        '## Qué podemos implementar y en qué orden','',
        '| Prioridad | Cambio concreto | Qué ya existe y qué falta | Validación necesaria |',
        '|---|---|---|---|',
        '| 1 | Previsión de cultivos por edad, producción restante y escenarios de resiembra | `_cxtb_their_supply` prolonga la oferta de cada tomate visible hasta el final. Es una hipótesis empírica de resiembra, no cuatro producciones seguras. Separar plantas actuales y futura resiembra; derivar aperturas de tiendas del calendario real. | Error de previsión en partidas reservadas y efecto sobre decisiones; después partidas completas contra F17. |',
        '| 2 | Rotación adaptable en casillas existentes, con tomate o zanahoria según demanda futura | Ya hay `_v9_carrot`, reservas de trigo y una inversión de tomates. Falta elegir por casilla y calendario de trabajo cuándo sustituir una plantación que termina, sin exigir SE ni alterar a ciegas las rutas. | Semillas nuevas; medir producción realmente entregada, alimento, costes, fallos de acciones y victorias. |',
        '| 3 | Adelantar producción del tercer cuadrante y aumentar densidad animal cuando resulte rentable | SW aparece unas 48 acciones antes en la mediana del top. F17 tiene 17 animales frente a mediana 19. Comprar antes sin mover colocación, alimento y recorridos no produce esa ventaja. | Cambiar un bloque coherente de trabajo; medir ROI tras salarios, varias tiendas y ambos asientos. |',
        '| 4 | Previsión del rival que contemple varias conductas de mercado | F16/F17 optimizan contra órdenes parecidas a las propias y condicionan su uso a semejanza de granjas. Hacen falta escenarios cuando el rival tiene otra producción, usando solo estado público e historial. | Rivales reactivos de varias familias; evitar usar sus órdenes simultáneas ocultas o puntuar solo contra grabaciones. |','',
        'La primera entrega viable es la previsión del punto 1, seguida de una rotación acotada del punto 2. '
        'Eso es más manejable que reemplazar todo el agente por RL. El aumento de animales necesita un planificador '
        'de recorridos y recursos; no basta cambiar una constante. Estas son propuestas de implementación respaldadas '
        'por la investigación, no cambios de política ya validados ni promesas de top 100.','',
        '## Restricciones del diseño que ya comprobamos','',
        '- Tomates: primera producción a edad 8, cuatro fechas consecutivas. Fresas: primera a edad 10, cuatro '
        'fechas separadas por dos días. Regar y fertilizar modifican el rendimiento; ignorar el fin de ciclo sesga el valor.',
        '- La mano 12 cuesta 144 monedas adicionales por día; la 13, 233. Sumarlas durante veinte días cuesta 7540, '
        'antes de terreno, semillas y alimento. La expansión tiene que pagar ese coste marginal.',
        '- El motor abre tiendas cada tres días, hasta ocho. La previsión heredada contiene incrementos fijos en '
        '22 y 24; hay que derivarlos de `townShopUnlockInterval`, la fecha y las tiendas ya observadas, y probar el cambio.',
        '- Las cuatro partidas propias terminan con almacén e inventarios vacíos. No hay evidencia aquí para priorizar '
        'otra capa genérica de liquidación final; varias ya están implementadas.',
        '- Una grabación revela conducta, no si el autor emplea PPO, búsqueda, reglas o una combinación. '
        'Tampoco hace falta trasplantar sus cintas de acciones para aprender estas decisiones.','',
        '## Revisión del análisis anterior','',
        'El informe `ANALISIS_2700.es.md` utilizaba otra muestra, del día 25, y generalizó en exceso la necesidad '
        'de cuatro cuadrantes y 12–13 trabajadores. La muestra actual demuestra diversidad y corrige esa recomendación. '
        'No podemos deducir el algoritmo privado ni afirmar, solo a partir de replays, que la solución requiera RL '
        'o que sea imposible construir una mejora antes del cierre.','',
        '## Evidencia y reproducción','',
        '- [Leaderboard público](https://www.kaggle.com/competitions/kaggriculture/leaderboard).',
        '- [Selección con equipos, submissions y episodios](results/top100_0927/selection.json).',
        '- [Resumen comprobado](results/top100_0927/summary.json), [200 perfiles](results/top100_0927/profiles.json).',
        '- [Contabilidad exacta](results/top100_0927/accounting.json), [referencia F17](results/top100_0927/baseline.json).',
        '- [Verificación y hashes](results/top100_0927/verification.json); eventos completos en `features.json.gz`.',
        '- Replays brutos comprimidos en `vendor/top100_0927/`, fuera de Git. No se incorporó código privado de rivales.','',
        '```powershell','.venv/Scripts/python.exe -X utf8 research_top100.py',
        '.venv/Scripts/python.exe -X utf8 analyze_top100.py','.venv/Scripts/python.exe -X utf8 baseline_top100.py',
        '.venv/Scripts/python.exe -X utf8 audit_top100.py','.venv/Scripts/python.exe -X utf8 report_top100.py','```','',
        'La selección queda fijada y las descargas se reanudan sin sustituir las partidas originales. '
        'Los errores iniciales de cuota quedaron resueltos con espera y reintento; el censo final está completo. '
        'F17 permanece congelado; esta investigación no realiza una nueva submission.','']
    Path('TOP100_ESTRATEGIAS.es.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({k:v for k,v in info.items() if k not in ('bands','decem_boey_case')},indent=2,ensure_ascii=False))


if __name__=='__main__':main()
