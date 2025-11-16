# 📊 Guia de Visualizações - Análise de Alocação de Salas

## Visão Geral

Este documento explica os 6 gráficos gerados pela análise da heurística gulosa de alocação de salas de aula.

---

## 1️⃣ **greedy_allocation.png** - Visão Geral de Alocação

### Conteúdo:
- **Pizza (esquerda)**: Distribuição de encontros alocados vs não alocados
- **Barras (direita)**: Distribuição de demanda de alunos

### O que observar:
- Taxa de alocação **97.4%** - excelente resultado!
- 974 de 1000 encontros foram alocados
- 39.264 de 40.861 alunos acomodados (96.1%)

### Interpretação:
✅ A heurística gulosa conseguiu alocar quase todos os encontros, mostrando eficiência.

---

## 2️⃣ **greedy_metrics.png** - Métricas Principais

### Conteúdo:
- **Taxa de Alocação**: Percentual de encontros alocados
- **Taxa de Demanda**: Percentual de alunos acomodados
- **Desperdício Médio**: Vagas não ocupadas por encontro
- **Resumo Executivo**: Sumário com números-chave

### O que observar:
- Desperdício médio de **11.69 vagas/encontro** - indicador de quanto espaço sobra
- Taxa de demanda de **96.09%** - muito bom!

### Interpretação:
✅ Baixo desperdício indica que as salas foram bem aproveitadas. A taxa alta de demanda satisfeita é excelente.

---

## 3️⃣ **greedy_classroom_occupancy.png** ⭐ (NOVO)

### 4 Sub-gráficos:

#### Gráfico 1: Encontros Alocados por Sala
- Mostra quantos encontros cada sala recebeu
- Código de cores: Verde (normal) → Laranja/Vermelho (super-utilizadas)

#### Gráfico 2: Taxa de Utilização por Sala
- Mostra a percentagem da capacidade utilizada
- Linha verde = 100% (capacidade normal)
- Acima de 100% = superscrição necessária

#### Gráfico 3: Top 10 Salas Mais Utilizadas
- Identifica as salas que mais trabalham
- Vermelho = alta utilização

#### Gráfico 4: Top 10 Salas Menos Utilizadas
- Identifica salas sub-utilizadas
- Cinza = baixa utilização (oportunidades de otimização)

### O que observar:
- **Sala 1**: 82 encontros, 7807% utilização - super-cheia!
- **Sala 18**: 5 encontros, 331% utilização - praticamente vazia
- Distribuição desigual sugere ajustes possíveis

### Insights:
- ⚠️ Algumas salas ficaram super-utilizadas (demanda > capacidade × encontros)
- 💡 Algumas salas foram pouco aproveitadas
- 🎯 Oportunidade para rebalanceamento em futuras otimizações

---

## 4️⃣ **greedy_daily_occupancy.png** ⭐ (NOVO)

### Conteúdo:
- **Esquerda**: Número de encontros por dia da semana
- **Direita**: Demanda de alunos por dia

### O que observar:
- **Terça-feira (3)**: 175 encontros - pico de demanda
- **Quarta-feira (4)**: 162 encontros
- **Segunda-feira (2)**: 153 encontros - menor carga

### Interpretação:
📈 A carga é relativamente distribuída durante a semana, com pequenas variações.

### Insights para Planejamento:
- Terças-feiras estão mais congestionadas
- Possível reservar mais salas ou horários para terça
- Pode-se aproveitar segunda-feira para encontros opcionais

---

## 5️⃣ **greedy_waste_distribution.png** ⭐ (NOVO)

### 2 Sub-gráficos:

#### Histograma (esquerda):
- Mostra a distribuição de desperdício por encontro
- Pico em 0-5 vagas = alocações muito eficientes!

#### Boxplot (direita):
- **Mediana**: valor central
- **Caixa**: 50% dos dados (quartis)
- **Linhas**: mín/máx

### O que observar:
- Maioria dos encontros tem **desperdício de 0-5 vagas**
- Alguns encontros com desperdício **15-40 vagas**

### Estatística:
- Distribuição positiva (enviesada à direita)
- Indica boas alocações com alguns outliers

### Interpretação:
✅ A heurística gulosa fez bom trabalho na eficiência!

---

## 6️⃣ **greedy_schedule_heatmap.png** ⭐ (NOVO)

### Conteúdo:
- Mapa de calor: Dias (linhas) vs Horários (colunas)
- Cores: Vermelho = alta demanda, Amarelo = média, Branco = baixa

### O que observar:
- **Horários 2, 3, 7, 8, 11**: Mais procurados
- **Horários 1, 12, 16**: Menos procurados
- **Terça (Ter) e Quinta (Qui)**: Dias mais carregados

### Padrões Identificados:
- Manhã (H2-H8): Altamente utilizada
- Final de horário (H16): Pouca demanda
- Período concentrado em 2-3 horas do dia

### Ações Possíveis:
- 💡 Disponibilizar mais salas nos horários 2-8
- 💡 Oferecer incentivos para usar horários 12, 16
- 💡 Considerar aulas à noite em períodos críticos

---

## 📈 Resumo Executivo dos Insights

| Métrica | Valor | Avaliação |
|---------|-------|-----------|
| Taxa Alocação | 97.4% | ✅ Excelente |
| Taxa Demanda | 96.1% | ✅ Excelente |
| Desperdício Médio | 11.69 vagas | ✅ Baixo |
| Distribuição Diária | Equilibrada | ✅ Bom |
| Distribuição por Sala | Desigual | ⚠️ Oportunidade |
| Concentração Horária | Alta nos períodos matutinos | ⚠️ Requer atenção |

---

## 🎯 Recomendações

### Curto Prazo:
1. Validar as alocações da heurística gulosa contra restrições hard não capturadas
2. Analisar por que 26 encontros não foram alocados
3. Confirmar que superscrições (>100%) são viáveis

### Médio Prazo:
1. Implementar algoritmos avançados (NSGA-II, Simulated Annealing)
2. Balancear melhor a carga entre salas
3. Aproveitar horários menos congestionados (H12, H16)

### Longo Prazo:
1. Coletar feedback sobre qualidades das alocações (próximidade, conforto)
2. Incorporar preferências mais sofisticadas
3. Criar modelo preditivo de demanda por horário/dia

---

## 🔧 Como Regenerar os Gráficos

```bash
# Recompile C++
make clean && make

# Execute programa (gera greedy_stats.csv) para uma instância (ou configure main para receber o nome da instância):
./bin/app <instance.json>   # ou apenas ./bin/app para executar a instância padrão

# Para processar todas as instâncias e agregar resultados (CSVs salvos em data/results/):
python3 run_and_aggregate.py

# Gerar gráficos por instância (lê data/results/greedy_stats_*.csv, salva em results/)
python3 scripts/plotting/plot_greedy_results.py

# Gerar gráficos comparativos entre instâncias (lê data/results/summary_instances.csv -> salva em results/)
python3 scripts/plotting/plot_compare_instances.py
```

### Saídas Geradas
- **CSVs por instância**: `data/results/greedy_stats_<instance>.csv`
- **CSV agregado**: `data/results/summary_instances.csv` (resumo de todas as instâncias)
- **Gráficos**: `results/*.png` (comparativos e detalhados)

---

## 📚 Referências Técnicas

- **Algoritmo**: Greedy Best-Fit (First-Fit Decreasing)
- **Objetivo**: Maximizar taxa de alocação com mínimo desperdício
- **Constraints**: 
  - Capacidade da sala ≥ demanda do encontro
  - Sala deve estar livre (sem reserva prévia)
  - Lab para encontros práticos
  - Preferências: Building, Floor, Board, Projector
- **Estatísticas Coletadas**: 
  - Por sala (ocupação, demanda, utilização)
  - Por dia (encontros, demanda)
  - Por dia/horário (demanda)
  - Distribuição de desperdício

---

## ❓ Dúvidas?

Verifique os dados brutos em `greedy_stats.csv` ou explore o código em:
- `src/constructive/constructive_heuristic.cpp` - Algoritmo
- `scripts/plotting/plot_greedy_results.py` - Scripts de visualização
