#!/usr/bin/env python3
"""
Gera gráficos comparativos entre heurísticas a partir de data/results/summary_instances.csv

Compara Greedy vs Partial (com diferentes alphas e seeds) através de boxplots para:
- Desperdício Médio (vagas não utilizadas por encontro)
- Taxa de Alocação (% de encontros alocados)
- Tempo de Execução (segundos)

Saídas: PNG em results/
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Setup
ROOT = Path(__file__).resolve().parent.parent.parent
CSV_DIR = ROOT / 'data' / 'results'
OUT_DIR = ROOT / 'results'
OUT_DIR.mkdir(exist_ok=True)

# Validar arquivo de entrada
summary_file = CSV_DIR / 'summary_instances.csv'
if not summary_file.exists():
    print(f'❌ Arquivo não encontrado: {summary_file}')
    print('   Rode run_and_aggregate.py primeiro.')
    raise SystemExit(1)

# Carregar dados
df = pd.read_csv(summary_file)
print(f'✓ Carregado {len(df)} linhas de {summary_file}')

# Garantir coluna 'heuristic' (fallback para dados antigos)
if 'heuristic' not in df.columns and 'file' in df.columns:
    df['heuristic'] = df['file'].apply(lambda x: 'partial' if 'partial' in x else 'greedy')

# Converter colunas numéricas
numeric_cols = ['Taxa Alocacao (%)', 'Taxa Demanda (%)', 'Desperdicio Medio', 'Runtime(s)']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Gerar boxplots comparativos
print('\n📊 Gerando gráficos comparativos...\n')

# 1. Desperdício Médio
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='heuristic', y='Desperdicio Medio', palette='Set2')
plt.title('Desperdício Médio por Heurística', fontsize=14, fontweight='bold')
plt.ylabel('Desperdício (vagas)', fontsize=12)
plt.xlabel('Heurística', fontsize=12)
plt.tight_layout()
plt.savefig(OUT_DIR / 'compare_waste_boxplot.png', dpi=150)
print('✓ Gerado: results/compare_waste_boxplot.png')
plt.close()

# 2. Taxa de Alocação
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='heuristic', y='Taxa Alocacao (%)', palette='Set2')
plt.title('Taxa de Alocação por Heurística', fontsize=14, fontweight='bold')
plt.ylabel('Taxa de Alocação (%)', fontsize=12)
plt.xlabel('Heurística', fontsize=12)
plt.tight_layout()
plt.savefig(OUT_DIR / 'compare_allocation_boxplot.png', dpi=150)
print('✓ Gerado: results/compare_allocation_boxplot.png')
plt.close()

# 3. Tempo de Execução
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='heuristic', y='Runtime(s)', palette='Set2')
plt.title('Tempo de Execução por Heurística', fontsize=14, fontweight='bold')
plt.ylabel('Tempo (segundos)', fontsize=12)
plt.xlabel('Heurística', fontsize=12)
plt.tight_layout()
plt.savefig(OUT_DIR / 'compare_runtime_boxplot.png', dpi=150)
print('✓ Gerado: results/compare_runtime_boxplot.png')
plt.close()

print('\n✅ Processamento concluído!')
