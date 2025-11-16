#!/usr/bin/env python3
"""
Gera gráficos comparativos entre instâncias usando summary_instances.csv
(arquivo movido para scripts/plotting; paths relativos usam a raiz do projeto)
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent  # Navega até a raiz do projeto
RESULTS_DIR = ROOT / 'results'
RESULTS_DIR.mkdir(exist_ok=True)

summary = ROOT / 'data' / 'results' / 'summary_instances.csv'

if not summary.exists():
    print('Arquivo data/results/summary_instances.csv não encontrado. Execute run_and_aggregate.py primeiro.')
    sys.exit(1)

df = pd.read_csv(summary)

# Função utilitária para converter strings percentuais para float
def to_float(val):
    try:
        return float(str(val))
    except:
        try:
            return float(str(val).replace('%',''))
        except:
            return float('nan')

# Normalizar colunas
df['Taxa Alocacao (%)'] = df['Taxa Alocacao (%)'].apply(to_float)
df['Taxa Demanda (%)'] = df['Taxa Demanda (%)'].apply(to_float)

df['Desperdicio Medio'] = df['Desperdicio Medio'].apply(to_float)

instances = df['instance'].tolist()

# 1) Bar chart: Taxa de Alocação por instância
plt.figure(figsize=(10,6))
plt.bar(instances, df['Taxa Alocacao (%)'], color='#2ecc71', edgecolor='black')
plt.ylim(0, 100)
plt.xlabel('Instância')
plt.ylabel('Taxa de Alocação (%)')
plt.title('Comparativo: Taxa de Alocação por Instância')
for i, v in enumerate(df['Taxa Alocacao (%)']):
    plt.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig(RESULTS_DIR / 'compare_allocation_rate.png', dpi=300)
print(f'✅ {RESULTS_DIR / "compare_allocation_rate.png"} gerado')
plt.close()

# 2) Bar chart: Taxa de Demanda por instância
plt.figure(figsize=(10,6))
plt.bar(instances, df['Taxa Demanda (%)'], color='#3498db', edgecolor='black')
plt.ylim(0, 100)
plt.xlabel('Instância')
plt.ylabel('Taxa de Demanda (%)')
plt.title('Comparativo: Taxa de Demanda por Instância')
for i, v in enumerate(df['Taxa Demanda (%)']):
    plt.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig(RESULTS_DIR / 'compare_demand_rate.png', dpi=300)
print(f'✅ {RESULTS_DIR / "compare_demand_rate.png"} gerado')
plt.close()

# 3) Scatter: Desperdício Médio vs Taxa de Alocação
plt.figure(figsize=(10,6))
plt.scatter(df['Desperdicio Medio'], df['Taxa Alocacao (%)'], s=100, color='#e67e22', edgecolor='black')
for i, inst in enumerate(instances):
    plt.text(df['Desperdicio Medio'].iloc[i], df['Taxa Alocacao (%)'].iloc[i]+0.5, inst, ha='center')
plt.xlabel('Desperdício Médio (vagas)')
plt.ylabel('Taxa de Alocação (%)')
plt.title('Desperdício Médio vs Taxa de Alocação')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(RESULTS_DIR / 'compare_waste_vs_allocation.png', dpi=300)
print(f'✅ {RESULTS_DIR / "compare_waste_vs_allocation.png"} gerado')
plt.close()

# 4) Gráfico: Runtime por instância (com linha de média)
if 'Runtime(s)' in df.columns:
    plt.figure(figsize=(10,6))
    df['Runtime(s)'] = pd.to_numeric(df['Runtime(s)'], errors='coerce')
    plt.bar(instances, df['Runtime(s)'], color='#9b59b6', edgecolor='black')
    mean_rt = df['Runtime(s)'].mean()
    plt.axhline(mean_rt, color='red', linestyle='--', label=f'Média = {mean_rt:.3f}s')
    plt.xlabel('Instância')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Comparativo: Tempo de Execução por Instância')
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'compare_runtime.png', dpi=300)
    print(f'✅ {RESULTS_DIR / "compare_runtime.png"} gerado')
    plt.close()

    # 4b) Boxplot de runtime
    plt.figure(figsize=(6,6))
    plt.boxplot(df['Runtime(s)'].dropna(), vert=True, patch_artist=True, labels=['Runtime'])
    plt.title('Boxplot: Runtime (s) across instances')
    plt.ylabel('Tempo (s)')
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'compare_runtime_boxplot.png', dpi=300)
    print(f'✅ {RESULTS_DIR / "compare_runtime_boxplot.png"} gerado')
    plt.close()

    # 4c) Scatter: Runtime vs Taxa de Alocação
    if 'Taxa Alocacao (%)' in df.columns:
        plt.figure(figsize=(8,6))
        plt.scatter(df['Runtime(s)'], df['Taxa Alocacao (%)'], s=100, color='#8e44ad', edgecolor='black')
        for i, inst in enumerate(instances):
            plt.text(df['Runtime(s)'].iloc[i], df['Taxa Alocacao (%)'].iloc[i]+0.2, inst, ha='center', fontsize=8)
        plt.xlabel('Runtime (s)')
        plt.ylabel('Taxa de Alocação (%)')
        plt.title('Runtime vs Taxa de Alocação')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / 'compare_runtime_vs_allocation_scatter.png', dpi=300)
        print(f'✅ {RESULTS_DIR / "compare_runtime_vs_allocation_scatter.png"} gerado')
        plt.close()

    # 4d) Bar runtime com faixa média ± std
    plt.figure(figsize=(10,6))
    std_rt = df['Runtime(s)'].std()
    plt.bar(instances, df['Runtime(s)'], color='#9b59b6', edgecolor='black')
    plt.axhline(mean_rt, color='red', linestyle='--', label=f'Média = {mean_rt:.3f}s')
    plt.fill_between([-0.5, len(instances)-0.5], mean_rt-std_rt, mean_rt+std_rt, color='red', alpha=0.1, label=f'±1 σ = {std_rt:.3f}s')
    plt.xlabel('Instância')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Runtime por Instância (média ± desvio padrão)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'compare_runtime_with_std.png', dpi=300)
    print(f'✅ {RESULTS_DIR / "compare_runtime_with_std.png"} gerado')
    plt.close()

# 5) Gráfico: Memória (MaxRSS) por instância
if 'MaxRSS(kB)' in df.columns:
    plt.figure(figsize=(10,6))
    # tentar converter para numérico
    df['MaxRSS(kB)'] = pd.to_numeric(df['MaxRSS(kB)'], errors='coerce')
    plt.bar(instances, df['MaxRSS(kB)'], color='#16a085', edgecolor='black')
    mean_mem = df['MaxRSS(kB)'].mean()
    plt.axhline(mean_mem, color='red', linestyle='--', label=f'Média = {mean_mem:.1f} kB')
    plt.xlabel('Instância')
    plt.ylabel('Max RSS (kB)')
    plt.title('Comparativo: Pico de Memória por Instância')
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'compare_memory.png', dpi=300)
    print(f'✅ {RESULTS_DIR / "compare_memory.png"} gerado')
    plt.close()

print('\n✨ Gráficos comparativos gerados em results/:')
for p in RESULTS_DIR.iterdir():
    if p.suffix.lower() in ['.png']:
        print(' -', p.name)
