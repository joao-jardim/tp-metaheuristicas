#!/usr/bin/env python3
"""
Gera um heatmap (dia x horario) a partir de um arquivo `greedy_stats.csv` gerado
pelas heurísticas. Salva um PNG com o heatmap.

Usage:
  python3 heatmap_from_stats.py --csv path/to/greedy_stats.csv --out path/to/out.png

If --out is a directory, file will be saved as <dirname>/heatmap_<basename>.png
"""
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import sys


def extract_schedule_section(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as fh:
        lines = [l.strip() for l in fh]

    in_section = False
    section = []
    for line in lines:
        if not line:
            continue
        if line == 'Ocupacao por Dia e Horario':
            in_section = True
            continue
        if in_section:
            # stop if next section header appears
            if line in ('Preferencias por Categoria', 'Ocupacao por Sala', 'Ocupacao por Dia', 'Distribuicao Desperdicio'):
                break
            # skip header row
            if line.startswith('DiaSchedule') or line.startswith('DiaSchedule,'):
                continue
            section.append(line)
    return section


def build_matrix(section_lines):
    schedule_data = {}
    schedules = set()
    days = {}
    for line in section_lines:
        parts = line.split(',')
        if len(parts) >= 2:
            key = parts[0]
            try:
                demand = int(parts[1])
            except:
                try:
                    demand = int(float(parts[1]))
                except:
                    demand = 0
            schedule_data[key] = demand

    for key, demand in schedule_data.items():
        if '_' not in key:
            continue
        day, sched = key.split('_')
        try:
            day_id = int(day)
            sched_id = int(sched)
        except:
            continue
        schedules.add(sched_id)
        if day_id not in days:
            days[day_id] = {}
        days[day_id][sched_id] = demand

    sorted_days = sorted(days.keys())
    sorted_schedules = sorted(schedules)

    matrix = np.zeros((len(sorted_days), len(sorted_schedules)), dtype=int)
    for i, day_id in enumerate(sorted_days):
        for j, sched_id in enumerate(sorted_schedules):
            matrix[i, j] = days.get(day_id, {}).get(sched_id, 0)

    return matrix, sorted_days, sorted_schedules


def plot_heatmap(matrix, days, schedules, out_path, title=None):
    day_names = {0: 'Dom', 1: 'Seg', 2: 'Ter', 3: 'Qua', 4: 'Qui', 5: 'Sex', 6: 'Sab'}
    day_labels = [day_names.get(d, f'D{d}') for d in days]

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')

    ax.set_xticks(range(len(schedules)))
    ax.set_yticks(range(len(days)))
    ax.set_xticklabels([f'H{s}' for s in schedules], rotation=45)
    ax.set_yticklabels(day_labels)
    ax.set_xlabel('Horário (Schedule)')
    ax.set_ylabel('Dia da Semana')
    if title:
        ax.set_title(title)

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Demanda (alunos)')

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            val = matrix[i, j]
            ax.text(j, i, int(val), ha='center', va='center', fontsize=8, color='black')

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', '-c', required=True)
    parser.add_argument('--out', '-o', required=True)
    parser.add_argument('--title', '-t', default=None)
    args = parser.parse_args()

    csvp = Path(args.csv)
    outp = Path(args.out)
    if not csvp.exists():
        print(f"CSV not found: {csvp}")
        sys.exit(1)

    section = extract_schedule_section(csvp)
    if not section:
        print("No 'Ocupacao por Dia e Horario' section found in CSV.")
        sys.exit(2)

    matrix, days, schedules = build_matrix(section)
    plot_heatmap(matrix, days, schedules, outp, title=args.title)
    print(f"Saved heatmap to: {outp}")


if __name__ == '__main__':
    main()
