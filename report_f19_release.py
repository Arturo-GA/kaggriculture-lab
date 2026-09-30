"""Add verified results and actual submission receipts to the Spanish handoff."""
import json
from pathlib import Path

ROOT = Path('results/frontier19')
MARKER = '\n## Resultado verificado y envíos\n'


def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def main():
    assessment = read('holdout_summary.json')
    decision = read('release_selection.json')
    release = read('release.json')
    cloud = read('kaggle_verified.json')
    private = read('kaggle_private_verified.json')
    assert cloud['verified'] and private['is_private'] is True
    assert release['candidates'] == decision['selected'] and len(release['candidates']) == 2
    receipts = {n: read(n + '_submission_receipt.json') for n in release['candidates']}
    assert len({r['id'] for r in receipts.values()}) == 2
    assert all(r['leaderboard_submitted'] for r in receipts.values())
    lines = [MARKER, '| Política | V/D/E | Puntos | Delta frente a F18 | Pasa |',
             '|---|---:|---:|---:|---|']
    for n, r in assessment['candidates'].items():
        lines.append(f"| {n} | {'/'.join(map(str,r['wlt']))} | {assessment['scores'][n]:g} | {r['score_delta']:+g} | {'Sí' if r['pass_gate'] else 'No'} |")
    rows = read('holdout.json')['rows']
    base = [r for r in rows if r['candidate'] == release['control']]
    lines.append(f"| F18 control | {sum(r['win'] for r in base)}/{sum(r['margin']<0 for r in base)}/{sum(r['tie'] for r in base)} | {assessment['scores'][release['control']]:g} | — | Referencia |")
    lines += ['', 'Se evaluaron todos los requisitos del plan, incluyendo deterioro máximo por rival,',
              'semillas con mejora, errores y latencia. Los resultados completos de los cuatro',
              'candidatos permanecen guardados, incluidos los rechazados.', '',
              f"Kaggle completó **{cloud['games']} juegos nuevos**, con cero errores, y confirmó",
              'que ambos archivos exportados coinciden byte por byte con los archivos locales.',
              'Los resultados de nube son comprobaciones adicionales, no pronósticos del rating.', '']
    if decision.get('supplemental_panel'):
        extra=read('supplement/holdout_summary.json')
        lines += ['La segunda plaza se estudió en **144 juegos adicionales**, con ocho semillas',
                  'nuevas 19301–19308 y tres rivales: F18, F17 y Lynn. Se conservaron los mismos',
                  'umbrales. El fallo original de Robust no fue borrado ni reinterpretado.', '',
                  '| Política, panel adicional | V/D/E | Puntos | Delta frente a F18 | Pasa |',
                  '|---|---:|---:|---:|---|']
        for n, r in extra['candidates'].items():
            lines.append(f"| {n} | {'/'.join(map(str,r['wlt']))} | {extra['scores'][n]:g} | {r['score_delta']:+g} | {'Sí' if r['pass_gate'] else 'No'} |")
        lines += [f"| F18 control | — | {extra['scores']['f18_small']:g} | — | Referencia |", '',
                  'Los porcentajes brutos de los dos paneles no son comparables: cambian semillas',
                  'y rivales. Es una campaña adaptativa de investigación, no una única prueba',
                  'confirmatoria sin selección de candidatos.', '']
        lines += ['**Decisión explícita para la segunda plaza:** Market1 se envía como experimento,',
                  'con la autorización actual de Arturo para dos plazas. Gana 44/48 frente a 38/48',
                  'del control y 16/16 contra F18, pero pierde dos puntos adicionales contra Lynn;',
                  'el límite fuera del duelo directo era −1. Su puerta sigue marcada **No**.',
                  'Se conserva la selección estricta original en `selection_decision.json` y la',
                  'decisión de envío con este riesgo en `release_selection.json`. No se cambia',
                  'el umbral ni se sigue buscando una muestra favorable para ocultar el fallo.', '']
    for n in release['candidates']:
        r = receipts[n]
        source_plan=Path(decision['source_plans'][n])
        policy_assessment=json.loads(source_plan.with_name('holdout_summary.json').read_text())
        head = policy_assessment['candidates'][n]['head_to_head_score']
        lines += [f"- **{n}**, submission **{r['id']}**, estado `{r['status']}`",
                  f"  comprobado en {r['checked_utc']}. Contra F18: {head:g}/16 puntos locales;",
                  f"  {cloud['scores'][n]:g}/8 puntos en nube. Máximo de llamada en nube: {cloud['max_call_ms'][n]:.1f} ms.",
                  f"  SHA de fuente: `{release['source_sha256'][n]}`.",
                  f"  SHA de paquete: `{r['archive_sha256']}`."]
    lines += ['', '[Notebook privado](https://www.kaggle.com/code/jarturo/kaggriculture-frontier19-policy-validation).',
              'Se verificó la privacidad descargando metadatos y comparando las celdas del notebook.',
              'Se realizaron exactamente dos envíos. Las intenciones previas al POST y los recibos',
              'están separados para evitar duplicados tras una desconexión.', '',
              'La mejora demostrada corresponde a este panel. El objetivo top 200–300 sigue',
              'pendiente de confirmación por las partidas del leaderboard.']
    p = Path('FRONTIER19_RESULTS.es.md')
    body = p.read_text(encoding='utf-8').split(MARKER)[0]
    body = body.replace('Los resultados definitivos y los dos recibos se incorporan al terminar la\nvalidación. El repositorio y el notebook se mantienen privados.',
                        'Los resultados y recibos verificados figuran a continuación. El repositorio y\nel notebook se mantienen privados.')
    p.write_text(body.rstrip() + '\n' + '\n'.join(lines) + '\n', encoding='utf-8')
    resume = Path('RESUME_FRONTIER19.es.md')
    text = resume.read_text(encoding='utf-8').split(MARKER)[0].rstrip() + '\n' + MARKER
    for n, r in receipts.items():
        text += f"\n- {n}: **{r['id']}**, `{r['status']}`, {r['checked_utc']}.\n"
    text += '\nDos envíos efectuados; consultar los recibos antes de cualquier acción. No queda una plaza pendiente de esta autorización.\n'
    resume.write_text(text, encoding='utf-8')
    ids = ' y '.join(str(r['id']) for r in receipts.values())
    note = (f'**30 de septiembre: Frontier19, submissions {ids}.** '
            'Cuatro partidas por cada equipo del puesto 200–300, veinte contabilidades propias exactas, '
            '544 juegos de comparación y dos estrategias verificadas funcionalmente en un notebook privado. '
            'Market2 pasa su puerta; Market1 es una segunda plaza experimental con un retroceso documentado. '
            '[Resultados](FRONTIER19_RESULTS.es.md) y [estado para continuar](RESUME_FRONTIER19.es.md). '
            'La mejora local no garantiza top 300.\n\n')
    readme = Path('README.md'); original = readme.read_text(encoding='utf-8')
    if '**30 de septiembre: Frontier19,' not in original:
        original = original.replace('# Kaggriculture Lab\n\n', '# Kaggriculture Lab\n\n' + note, 1)
        readme.write_text(original, encoding='utf-8')
    guide = Path('GUIA_PARA_EL_PROXIMO_CHAT.es.md'); original = guide.read_text(encoding='utf-8')
    if '**30 de septiembre: Frontier19,' not in original:
        title, rest = original.split('\n', 1)
        guide.write_text(title + '\n\n' + note + 'Los estados anteriores que siguen son históricos.\n' + rest, encoding='utf-8')


if __name__ == '__main__':
    main()
