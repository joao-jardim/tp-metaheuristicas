#!/usr/bin/env python3
"""Gera gráficos comparativos entre heurísticas a partir de data/results/summary_instances.csv
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CSV_DIR = ROOT / 'data' / 'results'
OUT_DIR = ROOT / 'results'
OUT_DIR.mkdir(exist_ok=True)

summary_file = CSV_DIR / 'summary_instances.csv'
if not summary_file.exists():
    print('Arquivo summary_instances.csv não encontrado. Rode run_and_aggregate.py primeiro.')
    raise SystemExit(1)

# Ler o summary que foi gerado pela versão atualizada do run_and_aggregate.py
df = pd.read_csv(summary_file)
# Se 'heuristic' não existir (antigo), tenta inferir a partir dos filenames
if 'heuristic' not in df.columns and 'file' in df.columns:
    df['heuristic'] = df['file'].apply(lambda x: 'partial' if 'partial' in x else 'greedy')

# Converter colunas numéricas
for col in ['Taxa Alocacao (%)','Taxa Demanda (%)','Desperdicio Medio','Runtime(s)']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Boxplot de Desperdicio Medio por heuristica
plt.figure(figsize=(8,6))
sns.boxplot(data=df, x='heuristic', y='Desperdicio Medio')
plt.title('Desperdício médio por heurística')
plt.savefig(OUT_DIR / 'compare_waste_boxplot.png')
print('Gerado:', OUT_DIR / 'compare_waste_boxplot.png')

# Boxplot de Taxa Alocacao
plt.figure(figsize=(8,6))
sns.boxplot(data=df, x='heuristic', y='Taxa Alocacao (%)')
plt.title('Taxa de alocação por heurística')
plt.savefig(OUT_DIR / 'compare_allocation_boxplot.png')
print('Gerado:', OUT_DIR / 'compare_allocation_boxplot.png')

# Runtime comparativo
plt.figure(figsize=(8,6))
sns.boxplot(data=df, x='heuristic', y='Runtime(s)')
plt.title('Tempo de execução por heurística')
plt.savefig(OUT_DIR / 'compare_runtime_boxplot.png')
print('Gerado:', OUT_DIR / 'compare_runtime_boxplot.png')

print('Pronto.')
