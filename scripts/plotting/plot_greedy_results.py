"""
Script para visualizar estatísticas da heurística gulosa com Matplotlib.
Lê o arquivo greedy_stats.csv gerado por constructive_heuristic.cpp
e gera gráficos profissionais.
Arquivo movido para scripts/plotting; paths relativos usam a raiz do projeto.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

# Raiz do projeto (um nível acima desta pasta)
ROOT = Path(__file__).resolve().parent.parent


def load_stats(csv_file=None):
    """Carrega estatísticas do arquivo CSV."""
    if csv_file is None:
        csv_file = ROOT / 'greedy_stats.csv'
    else:
        csv_file = Path(csv_file)

    if not csv_file.exists():
        print(f"Erro: arquivo '{csv_file}' não encontrado.")
        print("   Execute primeiro o programa C++ para gerar o arquivo.")
        sys.exit(1)
    
    # Ler as linhas do arquivo
    with open(csv_file, 'r') as f:
        lines = f.readlines()
    
    # Encontrar onde começa a seção de preferências
    metrics_lines = []
    prefs_lines = []
    in_prefs = False
    
    for line in lines:
        if 'Preferencias por Categoria' in line:
            in_prefs = True
            continue
        
        if in_prefs:
            prefs_lines.append(line)
        else:
            metrics_lines.append(line)
    
    # Converter para DataFrames
    from io import StringIO
    df_metrics = pd.read_csv(StringIO(''.join(metrics_lines)))
    
    # Processar preferências se existirem e tiverem dados
    df_prefs = pd.DataFrame()
    if prefs_lines:
        prefs_content = ''.join(prefs_lines).strip()
        if prefs_content and 'Categoria' in prefs_lines[0]:
            try:
                df_prefs = pd.read_csv(StringIO(prefs_content))
                # Remover linhas vazias
                df_prefs = df_prefs.dropna(how='all')
                if len(df_prefs) == 0 or (len(df_prefs) == 1 and df_prefs.iloc[0].isna().all()):
                    df_prefs = pd.DataFrame()
            except:
                df_prefs = pd.DataFrame()
    
    return df_metrics, df_prefs

def plot_allocation_overview(df_metrics, results_dir):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Visão Geral de Alocação', fontsize=14, fontweight='bold')
    
    allocated = df_metrics[df_metrics['Metrica'] == 'Encontros Alocados']['Valor'].values[0]
    total = df_metrics[df_metrics['Metrica'] == 'Encontros Total']['Valor'].values[0]
    not_allocated = int(total - allocated)
    
    sizes = [allocated, not_allocated]
    labels = [f'Alocados\n({allocated})', f'Não alocados\n({not_allocated})']
    colors = ['#2ecc71', '#e74c3c']
    axes[0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, 
                textprops={'fontsize': 10, 'weight': 'bold'})
    axes[0].set_title('Distribuição de Encontros')
    
    demand_allocated = df_metrics[df_metrics['Metrica'] == 'Demanda Alocada']['Valor'].values[0]
    demand_total = df_metrics[df_metrics['Metrica'] == 'Demanda Total']['Valor'].values[0]
    
    categories = ['Alocado', 'Não Alocado']
    values = [demand_allocated, demand_total - demand_allocated]
    colors_bar = ['#3498db', '#95a5a6']
    
    bars = axes[1].bar(categories, values, color=colors_bar, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_ylabel('Demanda (alunos)', fontweight='bold')
    axes[1].set_title('Distribuição de Demanda')
    axes[1].set_ylim(0, demand_total * 1.1)
    for bar, val in zip(bars, values):
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(val)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(results_dir / 'greedy_allocation.png', dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo: {results_dir / 'greedy_allocation.png'}")
    plt.close()


def plot_metrics(df_metrics, results_dir):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Métricas Principais da Heurística Gulosa', fontsize=14, fontweight='bold')
    
    taxa_aloc = df_metrics[df_metrics['Metrica'] == 'Taxa Alocacao (%)']['Valor'].values[0]
    ax = axes[0, 0]
    ax.barh(['Taxa Alocação'], [taxa_aloc], color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_xlim(0, 100)
    ax.text(taxa_aloc/2, 0, f'{taxa_aloc:.1f}%', ha='center', va='center', 
            fontweight='bold', fontsize=12, color='white')
    ax.set_xlabel('Percentual (%)', fontweight='bold')
    ax.set_title('Taxa de Alocação')
    ax.grid(axis='x', alpha=0.3)
    
    taxa_dem = df_metrics[df_metrics['Metrica'] == 'Taxa Demanda (%)']['Valor'].values[0]
    ax = axes[0, 1]
    ax.barh(['Taxa Demanda'], [taxa_dem], color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_xlim(0, 100)
    ax.text(taxa_dem/2, 0, f'{taxa_dem:.1f}%', ha='center', va='center', 
            fontweight='bold', fontsize=12, color='white')
    ax.set_xlabel('Percentual (%)', fontweight='bold')
    ax.set_title('Taxa de Demanda Alocada')
    ax.grid(axis='x', alpha=0.3)
    
    desp_med = df_metrics[df_metrics['Metrica'] == 'Desperdicio Medio']['Valor'].values[0]
    ax = axes[1, 0]
    ax.barh(['Desperdício Médio'], [desp_med], color='#e67e22', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.text(desp_med/2, 0, f'{desp_med:.2f}', ha='center', va='center', 
            fontweight='bold', fontsize=12, color='white')
    ax.set_xlabel('Vagas/Encontro', fontweight='bold')
    ax.set_title('Desperdício Médio de Capacidade')
    ax.grid(axis='x', alpha=0.3)
    
    ax = axes[1, 1]
    ax.axis('off')
    summary_text = f"""
    RESUMO EXECUTIVO
    
    • Encontros alocados: {int(df_metrics[df_metrics['Metrica'] == 'Encontros Alocados']['Valor'].values[0])} 
      de {int(df_metrics[df_metrics['Metrica'] == 'Encontros Total']['Valor'].values[0])}
    
    • Taxa de alocação: {taxa_aloc:.1f}%
    
    • Demanda alocada: {int(df_metrics[df_metrics['Metrica'] == 'Demanda Alocada']['Valor'].values[0])} 
      de {int(df_metrics[df_metrics['Metrica'] == 'Demanda Total']['Valor'].values[0])} alunos
    
    • Taxa de demanda: {taxa_dem:.1f}%
    
    • Desperdício médio: {desp_med:.2f} vagas por encontro
    """
    ax.text(0.1, 0.5, summary_text, fontsize=11, verticalalignment='center',
            family='monospace', bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(results_dir / 'greedy_metrics.png', dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo: {results_dir / 'greedy_metrics.png'}")
    plt.close()


def plot_preferences(df_prefs, results_dir):
    if df_prefs.empty or len(df_prefs) == 0:
        print("⚠️  Nenhuma preferência encontrada para plotar.")
        return
    
    df_prefs = df_prefs.dropna()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Análise de Preferências', fontsize=14, fontweight='bold')
    
    ax = axes[0]
    categories = df_prefs['Categoria'].values
    satisfaction = df_prefs['Taxa (%)'].values
    colors = ['#2ecc71' if x >= 80 else '#f39c12' if x >= 50 else '#e74c3c' for x in satisfaction]
    
    bars = ax.barh(categories, satisfaction, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_xlim(0, 105)
    ax.set_xlabel('Taxa de Satisfação (%)', fontweight='bold')
    ax.set_title('Taxa de Satisfação por Categoria')
    ax.axvline(x=80, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Excelente (80%)')
    ax.axvline(x=50, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Aceitável (50%)')
    ax.legend()
    ax.grid(axis='x', alpha=0.3)
    
    for bar, val in zip(bars, satisfaction):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2., f'{val:.1f}%',
                ha='left', va='center', fontweight='bold', fontsize=9)
    
    ax = axes[1]
    satisfied = df_prefs['Satisfeitas'].values
    violated = df_prefs['Total'].values - satisfied
    
    x_pos = range(len(categories))
    ax.bar(x_pos, satisfied, label='Satisfeitas', color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.bar(x_pos, violated, bottom=satisfied, label='Violadas', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel('Quantidade', fontweight='bold')
    ax.set_title('Preferências Satisfeitas vs Violadas')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    for i, (s, v) in enumerate(zip(satisfied, violated)):
        total = s + v
        if s > 0:
            ax.text(i, s/2, str(int(s)), ha='center', va='center', fontweight='bold', color='white')
        if v > 0:
            ax.text(i, s + v/2, str(int(v)), ha='center', va='center', fontweight='bold', color='white')
    
    plt.tight_layout()
    plt.savefig(results_dir / 'greedy_preferences.png', dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo: {results_dir / 'greedy_preferences.png'}")
    plt.close()


def load_detailed_data(csv_file=None):
    if csv_file is None:
        csv_file = ROOT / 'greedy_stats.csv'
    else:
        csv_file = Path(csv_file)
    with open(csv_file, 'r') as f:
        lines = f.readlines()
    
    sections = {}
    current_section = None
    section_data = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line in ['Ocupacao por Sala', 'Ocupacao por Dia', 'Distribuicao Desperdicio', 'Ocupacao por Dia e Horario']:
            if current_section:
                sections[current_section] = section_data
            current_section = line
            section_data = []
        elif current_section and (line.startswith('ClassroomId') or line.startswith('DiaSemanaSemana') or 
                                  line.startswith('Desperdicio') or line.startswith('DiaSchedule')):
            continue
        elif current_section:
            section_data.append(line)
    
    if current_section:
        sections[current_section] = section_data
    
    return sections


def plot_classroom_occupancy(sections, results_dir):
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Análise de Ocupação por Sala', fontsize=14, fontweight='bold')
    
    classrooms = []
    occupancy = []
    utilization = []
    capacity = []
    
    for line in sections.get('Ocupacao por Sala', []):
        parts = line.split(',')
        if len(parts) >= 5:
            classrooms.append(f"S{parts[0]}")
            occupancy.append(int(parts[1]))
            utilization.append(float(parts[4]))
            capacity.append(int(parts[3]))
    
    ax = axes[0, 0]
    colors = ['#2ecc71' if u <= 100 else '#f39c12' if u <= 200 else '#e74c3c' for u in utilization]
    ax.bar(range(len(classrooms)), occupancy, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    ax.set_xticks(range(len(classrooms)))
    ax.set_xticklabels(classrooms, rotation=90, fontsize=7)
    ax.set_ylabel('Número de Encontros', fontweight='bold')
    ax.set_title('Encontros Alocados por Sala')
    ax.grid(axis='y', alpha=0.3)
    
    ax = axes[0, 1]
    colors_util = ['#2ecc71' if u <= 100 else '#f39c12' if u <= 150 else '#e74c3c' for u in utilization]
    bars = ax.bar(range(len(classrooms)), utilization, color=colors_util, alpha=0.8, edgecolor='black', linewidth=0.5)
    ax.axhline(y=100, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Capacidade (100%)')
    ax.set_xticks(range(len(classrooms)))
    ax.set_xticklabels(classrooms, rotation=90, fontsize=7)
    ax.set_ylabel('Taxa de Utilização (%)', fontweight='bold')
    ax.set_title('Taxa de Utilização por Sala')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    ax = axes[1, 0]
    sorted_idx = sorted(range(len(utilization)), key=lambda i: utilization[i], reverse=True)[:10]
    top_classrooms = [classrooms[i] for i in sorted_idx]
    top_util = [utilization[i] for i in sorted_idx]
    ax.barh(top_classrooms, top_util, color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Taxa de Utilização (%)', fontweight='bold')
    ax.set_title('Top 10 Salas Mais Utilizadas')
    ax.grid(axis='x', alpha=0.3)
    
    ax = axes[1, 1]
    sorted_idx = sorted(range(len(utilization)), key=lambda i: utilization[i])[:10]
    bottom_classrooms = [classrooms[i] for i in sorted_idx]
    bottom_util = [utilization[i] for i in sorted_idx]
    ax.barh(bottom_classrooms, bottom_util, color='#95a5a6', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Taxa de Utilização (%)', fontweight='bold')
    ax.set_title('Top 10 Salas Menos Utilizadas')
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(results_dir / 'greedy_classroom_occupancy.png', dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo: {results_dir / 'greedy_classroom_occupancy.png'}")
    plt.close()


def plot_daily_occupancy(sections, results_dir):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Análise de Ocupação por Dia da Semana', fontsize=14, fontweight='bold')
    
    days = {0: 'Domingo', 1: 'Segunda', 2: 'Terça', 3: 'Quarta', 4: 'Quinta', 5: 'Sexta', 6: 'Sábado'}
    day_occupancy = {}
    day_demand = {}
    
    for line in sections.get('Ocupacao por Dia', []):
        parts = line.split(',')
        if len(parts) >= 3:
            day_id = int(parts[0])
            day_occupancy[day_id] = int(parts[1])
            day_demand[day_id] = int(parts[2])
    
    sorted_days = sorted(day_occupancy.keys())
    day_names = [days.get(d, f'Dia {d}') for d in sorted_days]
    occupancies = [day_occupancy[d] for d in sorted_days]
    demands = [day_demand[d] for d in sorted_days]
    
    ax = axes[0]
    bars = ax.bar(day_names, occupancies, color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Número de Encontros', fontweight='bold')
    ax.set_title('Encontros Alocados por Dia')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, occupancies):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, str(int(val)), 
                ha='center', va='bottom', fontweight='bold')
    
    ax = axes[1]
    bars = ax.bar(day_names, demands, color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Demanda (alunos)', fontweight='bold')
    ax.set_title('Demanda Alocada por Dia')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, demands):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, str(int(val)), 
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(results_dir / 'greedy_daily_occupancy.png', dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo: {results_dir / 'greedy_daily_occupancy.png'}")
    plt.close()


def plot_waste_distribution(sections, results_dir):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Análise de Desperdício de Capacidade', fontsize=14, fontweight='bold')
    
    waste_values = []
    for line in sections.get('Distribuicao Desperdicio', []):
        try:
            waste_values.append(int(line))
        except:
            pass
    
    if waste_values:
        ax = axes[0]
        ax.hist(waste_values, bins=30, color='#f39c12', alpha=0.8, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Desperdício (vagas)', fontweight='bold')
        ax.set_ylabel('Frequência', fontweight='bold')
        ax.set_title('Histograma de Desperdício')
        ax.grid(axis='y', alpha=0.3)
        
        ax = axes[1]
        bp = ax.boxplot(waste_values, vert=True, patch_artist=True, widths=0.5)
        bp['boxes'][0].set_facecolor('#f39c12')
        ax.set_ylabel('Desperdício (vagas)', fontweight='bold')
        ax.set_title('Boxplot de Desperdício')
        ax.grid(axis='y', alpha=0.3)
        
        median = sorted(waste_values)[len(waste_values)//2]
        mean = sum(waste_values) / len(waste_values)
        ax.text(1.3, median, f'Mediana: {median}', fontsize=10, fontweight='bold')
        ax.text(1.3, mean, f'Média: {mean:.2f}', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(results_dir / 'greedy_waste_distribution.png', dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo: {results_dir / 'greedy_waste_distribution.png'}")
    plt.close()


def plot_schedule_heatmap(sections, results_dir):
    import numpy as np
    
    schedule_data = {}
    for line in sections.get('Ocupacao por Dia e Horario', []):
        parts = line.split(',')
        if len(parts) >= 2:
            key = parts[0]
            demand = int(parts[1])
            schedule_data[key] = demand
    
    days = {}
    schedules = set()
    
    for key, demand in schedule_data.items():
        day, sched = key.split('_')
        day_id = int(day)
        sched_id = int(sched)
        schedules.add(sched_id)
        
        if day_id not in days:
            days[day_id] = {}
        days[day_id][sched_id] = demand
    
    sorted_days = sorted(days.keys())
    sorted_schedules = sorted(schedules)
    
    matrix = []
    day_names = {0: 'Dom', 1: 'Seg', 2: 'Ter', 3: 'Qua', 4: 'Qui', 5: 'Sex', 6: 'Sab'}
    day_labels = [day_names.get(d, f'D{d}') for d in sorted_days]
    
    for day_id in sorted_days:
        row = []
        for sched_id in sorted_schedules:
            demand = days[day_id].get(sched_id, 0)
            row.append(demand)
        matrix.append(row)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    
    ax.set_xticks(range(len(sorted_schedules)))
    ax.set_yticks(range(len(sorted_days)))
    ax.set_xticklabels([f'H{s}' for s in sorted_schedules])
    ax.set_yticklabels(day_labels)
    ax.set_xlabel('Horário (Schedule)', fontweight='bold')
    ax.set_ylabel('Dia da Semana', fontweight='bold')
    ax.set_title('Heatmap: Demanda por Dia e Horário', fontsize=14, fontweight='bold')
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Demanda (alunos)', fontweight='bold')
    
    for i in range(len(sorted_days)):
        for j in range(len(sorted_schedules)):
            value = matrix[i][j]
            text = ax.text(j, i, int(value), ha="center", va="center", color="black", fontsize=8)
    
    plt.tight_layout()
    plt.savefig(results_dir / 'greedy_schedule_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo: {results_dir / 'greedy_schedule_heatmap.png'}")
    plt.close()


def main():
    print("\nGerando gráficos detalhados das estatísticas da heurística gulosa...\n")
    ROOT = Path(__file__).resolve().parent.parent
    RESULTS_DIR = ROOT / 'results'
    RESULTS_DIR.mkdir(exist_ok=True)

    df_metrics, df_prefs = load_stats(ROOT / 'greedy_stats.csv')
    sections = load_detailed_data(ROOT / 'greedy_stats.csv')

    try:
        plot_allocation_overview(df_metrics, RESULTS_DIR)
        plot_metrics(df_metrics, RESULTS_DIR)
        plot_classroom_occupancy(sections, RESULTS_DIR)
        plot_daily_occupancy(sections, RESULTS_DIR)
        plot_waste_distribution(sections, RESULTS_DIR)
        plot_schedule_heatmap(sections, RESULTS_DIR)
        if not df_prefs.empty:
            plot_preferences(df_prefs, RESULTS_DIR)
        
        print("\n Todos os gráficos foram gerados com sucesso!\n")
    except Exception as e:
        import traceback
        print(f"Erro ao gerar gráficos: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
