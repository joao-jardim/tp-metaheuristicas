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

for inst in instances:
    name = inst.stem
    print(f'-> Executando instância: {name} ({inst})')
    try:
        # Medir tempo com perf_counter e capturar peak memory via /usr/bin/time -l (macOS)
        start = time.perf_counter()
        # Usamos /usr/bin/time -l para obter informações de memória no stderr
        cmd = ['/usr/bin/time', '-l', str(BIN), inst.name]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        end = time.perf_counter()
        duration = end - start
        # Extrair pico de memória (max resident set size) do stderr
        max_rss_kb = ''
        for line in proc.stderr.splitlines():
            if 'maximum resident set size' in line.lower() or 'maximum resident set size (kbytes)' in line.lower():
                # extrai o último número na linha
                parts = line.split()
                for p in reversed(parts):
                    try:
                        max_rss_kb = int(p)
                        break
                    except:
                        continue
                break
        # fallback: se não achou, deixar em branco
    except subprocess.CalledProcessError as e:
        print(f'Erro ao executar {BIN} para {inst}: {e}')
        continue

    # Após execução, deve existir greedy_stats.csv
    stats = ROOT / 'greedy_stats.csv'
    if not stats.exists():
        print(f'Arquivo greedy_stats.csv não foi gerado para {name}. Pulando.')
        continue

    dest = CSV_DIR / f'greedy_stats_{name}.csv'
    shutil.move(str(stats), str(dest))
    print(f'  -> Movido para data/results/{dest.name}')

    # Ler métricas básicas do CSV
    allocated = total = alloc_rate = demand_alloc = demand_total = demand_rate = avg_waste = ''
    # preferˆencias
    pref_total = 0
    pref_satisfied = 0
    with open(dest, 'r') as f:
        reader = csv.reader(f)
        lines = [row for row in reader]
    # converter para dicionário simples (procura por Metrica,Valor) e também preferências
    section = 'metrics'
    for row in lines:
        if not row:
            continue
        # detectar mudança de seção por cabeçalho textual
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
            # formato: Categoria,Total,Satisfeitas,Taxa (%)
            try:
                total_p = int(row[1])
                sat = int(row[2])
                pref_total += total_p
                pref_satisfied += sat
            except:
                pass

    summary_rows.append({
        'instance': name,
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
    })

# Escrever summary CSV em data/results/
summary_file = CSV_DIR / 'summary_instances.csv'
with open(summary_file, 'w', newline='') as f:
    fieldnames=['instance','Encontros Alocados','Encontros Total','Taxa Alocacao (%)','Demanda Alocada','Demanda Total','Taxa Demanda (%)','Desperdicio Medio','Runtime(s)','MaxRSS(kB)','PrefTotal','PrefSatisfeitas','PrefSat(%)']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in summary_rows:
        writer.writerow(row)

print('\n✔️ Processamento concluído.')
print(f'Arquivo de resumo gerado: {summary_file}')
print('Arquivos por instância:')
for inst in instances:
    p = CSV_DIR / f'greedy_stats_{inst.stem}.csv'
    if p.exists():
        print('  -', p.name)
