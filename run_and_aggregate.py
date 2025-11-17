#!/usr/bin/env python3
"""
Executa o binário para todas as instâncias JSON em data/generated_instances/
Renomeia o greedy_stats.csv gerado para greedy_stats_<instance>.csv
E cria summary_instances.csv com métricas chave por instância.
"""

import subprocess
import shutil
from pathlib import Path
import csv
import sys
import time
import shlex

ROOT = Path(__file__).resolve().parent
INST_DIR = ROOT / 'data' / 'generated_instances'
BIN = ROOT / 'bin' / 'app'
CSV_DIR = ROOT / 'data' / 'results'  # Pasta para armazenar CSVs gerados
CSV_DIR.mkdir(exist_ok=True)

if not BIN.exists():
    print('Erro: binário ./bin/app não encontrado. Compile o projeto primeiro (make).')
    sys.exit(1)

instances = sorted(INST_DIR.glob('*.json'))
if not instances:
    print('Nenhuma instância JSON encontrada em data/generated_instances/')
    sys.exit(1)

summary_rows = []

# Experiment configuration: by default compare greedy (once) and partial for multiple alphas/seeds.
HEUR_CONFIG = [
    {'name': 'greedy'},
    {'name': 'partial', 'alphas': [0.25, 0.5, 0.75], 'seeds': [0, 12345]}
]

for inst in instances:
    name = inst.stem
    for heur in HEUR_CONFIG:
        if heur['name'] == 'greedy':
            runs = [ {'heur': 'greedy'} ]
        else:
            runs = []
            alphas = heur.get('alphas', [0.5])
            seeds = heur.get('seeds', [0])
            for a in alphas:
                for s in seeds:
                    runs.append({'heur': 'partial', 'alpha': a, 'seed': s})

        for run_cfg in runs:
            descr = f"{name} | {run_cfg['heur']}"
            if run_cfg['heur'] == 'partial':
                descr += f" alpha={run_cfg['alpha']} seed={run_cfg['seed']}"
            print(f"-> Executando: {descr}")
            try:
                start = time.perf_counter()
                if run_cfg['heur'] == 'greedy':
                    cmd = ['/usr/bin/time', '-l', str(BIN), inst.name]
                else:
                    # build heuristic string: partial:<alpha>[:seed]
                    alpha_s = str(run_cfg['alpha'])
                    if run_cfg['seed'] and int(run_cfg['seed']) != 0:
                        heur_arg = f"partial:{alpha_s}:{run_cfg['seed']}"
                    else:
                        heur_arg = f"partial:{alpha_s}"
                    cmd = ['/usr/bin/time', '-l', str(BIN), inst.name, f"--heuristic={heur_arg}"]

                proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                end = time.perf_counter()
                duration = end - start
                max_rss_kb = ''
                for line in proc.stderr.splitlines():
                    if 'maximum resident set size' in line.lower() or 'maximum resident set size (kbytes)' in line.lower():
                        parts = line.split()
                        for p in reversed(parts):
                            try:
                                max_rss_kb = int(p)
                                break
                            except:
                                continue
                        break
            except subprocess.CalledProcessError as e:
                print(f'Erro ao executar {BIN} para {inst}: {e}')
                continue

            stats = ROOT / 'greedy_stats.csv'
            if not stats.exists():
                print(f'Arquivo greedy_stats.csv não foi gerado para {name}. Pulando.')
                continue

            # destination filename includes heuristic info
            if run_cfg['heur'] == 'greedy':
                dest_name = f'greedy_stats_{name}_greedy.csv'
            else:
                alpha_str = str(run_cfg['alpha']).replace('.', '_')
                seed_str = str(run_cfg['seed'])
                dest_name = f'greedy_stats_{name}_partial_a{alpha_str}_s{seed_str}.csv'

            dest = CSV_DIR / dest_name
            shutil.move(str(stats), str(dest))
            print(f'  -> Movido para data/results/{dest.name}')

            # Ler métricas básicas do CSV (mesma lógica que antes)
            allocated = total = alloc_rate = demand_alloc = demand_total = demand_rate = avg_waste = ''
            pref_total = 0
            pref_satisfied = 0
            with open(dest, 'r') as f:
                reader = csv.reader(f)
                lines = [row for row in reader]
            section = 'metrics'
            for row in lines:
                if not row:
                    continue
                first = row[0].strip() if len(row) > 0 else ''
                if 'Preferencias por Categoria' in first:
                    section = 'prefs'
                    continue
                if 'Ocupacao por Sala' in first:
                    section = 'other'
                    continue

                if section == 'metrics' and len(row) >= 2:
                    key = row[0].strip()
                    val = row[1].strip()
                    if key == 'Encontros Alocados':
                        allocated = val
                    elif key == 'Encontros Total':
                        total = val
                    elif key == 'Taxa Alocacao (%)':
                        alloc_rate = val
                    elif key == 'Demanda Alocada':
                        demand_alloc = val
                    elif key == 'Demanda Total':
                        demand_total = val
                    elif key == 'Taxa Demanda (%)':
                        demand_rate = val
                    elif key == 'Desperdicio Medio':
                        avg_waste = val

                elif section == 'prefs' and len(row) >= 4:
                    try:
                        total_p = int(row[1])
                        sat = int(row[2])
                        pref_total += total_p
                        pref_satisfied += sat
                    except:
                        pass

            summary = {
                'instance': name,
                'heuristic': run_cfg['heur'],
                'alpha': run_cfg.get('alpha', ''),
                'seed': run_cfg.get('seed', ''),
                'Encontros Alocados': allocated,
                'Encontros Total': total,
                'Taxa Alocacao (%)': alloc_rate,
                'Demanda Alocada': demand_alloc,
                'Demanda Total': demand_total,
                'Taxa Demanda (%)': demand_rate,
                'Desperdicio Medio': avg_waste,
                'Runtime(s)': f"{duration:.4f}",
                'MaxRSS(kB)': max_rss_kb,
                'PrefTotal': pref_total,
                'PrefSatisfeitas': pref_satisfied,
                'PrefSat(%)': f"{(100.0 * pref_satisfied / pref_total):.2f}" if pref_total > 0 else "",
            }
            summary_rows.append(summary)

# Escrever summary CSV em data/results/
summary_file = CSV_DIR / 'summary_instances.csv'
with open(summary_file, 'w', newline='') as f:
    fieldnames=['instance','heuristic','alpha','seed','Encontros Alocados','Encontros Total','Taxa Alocacao (%)','Demanda Alocada','Demanda Total','Taxa Demanda (%)','Desperdicio Medio','Runtime(s)','MaxRSS(kB)','PrefTotal','PrefSatisfeitas','PrefSat(%)']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in summary_rows:
        # garantir que todas as chaves existam
        out = {k: row.get(k, '') for k in fieldnames}
        writer.writerow(out)

print('\n✔️ Processamento concluído.')
print(f'Arquivo de resumo gerado: {summary_file}')
print('Arquivos por instância:')
print('\nArquivos CSV gerados:')
for p in sorted(CSV_DIR.glob('greedy_stats_*.csv')):
    print('  -', p.name)
