# 📊 Guia de Visualizações - Análise de Alocação de Salas

## Visão Geral

Documentação dos gráficos gerados pelo pipeline de análise. Existem **dois tipos** de visualizações:

1. **Gráficos por Instância** (greedy_*): Análise detalhada de uma instância específica com a heurística gulosa
2. **Gráficos de Comparação** (compare_*): Comparação entre heurísticas (Greedy vs Partial com diferentes alphas/seeds)

---

## 📈 GRÁFICOS POR INSTÂNCIA (Heurística Gulosa)

### 1️⃣ **greedy_allocation.png** - Visão Geral de Alocação

**Conteúdo:**
- **Pizza (esquerda)**: Distribuição de encontros alocados vs não alocados
- **Barras (direita)**: Distribuição de demanda de alunos

**O que observar:**
- Taxa de alocação **97.4%** → excelente!
- 974 de 1000 encontros alocados
- 39.264 de 40.861 alunos acomodados (96.1%)

**Interpretação:**
✅ A heurística gulosa conseguiu alocar quase todos os encontros.

---

### 2️⃣ **greedy_metrics.png** - Métricas Principais

**Conteúdo:**
- **Taxa de Alocação**: % de encontros alocados
- **Taxa de Demanda**: % de alunos acomodados
- **Desperdício Médio**: Vagas não ocupadas/encontro
- **Resumo Executivo**: Números-chave

**O que observar:**
- Desperdício médio: **11.69 vagas/encontro**
- Taxa de demanda: **96.09%** → muito bom!

**Interpretação:**
✅ Baixo desperdício + alta taxa de acomodação = boa eficiência.

---

### 3️⃣ **greedy_classroom_occupancy.png** - Distribuição por Sala

**Conteúdo** (4 sub-gráficos):
1. **Encontros/Sala**: Quantos encontros cada sala recebeu
2. **Taxa de Utilização/Sala**: % da capacidade utilizada
3. **Top 10 Mais Utilizadas**: Salas com maior demanda
4. **Top 10 Menos Utilizadas**: Salas com baixa ocupação

**O que observar:**
- Distribuição desigual: algumas salas super-utilizadas, outras sub-utilizadas
- Identifica gargalos e oportunidades de rebalanceamento

**Interpretação:**
⚠️ Desigualdade sugere potencial para otimização futura.

---

### 4️⃣ **greedy_daily_occupancy.png** - Distribuição por Dia

**Conteúdo:**
- **Esquerda**: Número de encontros por dia da semana
- **Direita**: Demanda de alunos por dia

**O que observar:**
- Picos e vales de demanda ao longo da semana
- Distribuição relativa entre dias

**Interpretação:**
📈 Permite identificar dias críticos e planejamento de recursos.

---

### 5️⃣ **greedy_waste_distribution.png** - Distribuição de Desperdício

**Conteúdo** (2 sub-gráficos):
1. **Histograma**: Distribuição de desperdício por encontro
2. **Boxplot**: Resumo estatístico (mediana, quartis, outliers)

**O que observar:**
- Pico em 0-5 vagas = alocações muito eficientes
- Alguns outliers com desperdício 15-40 vagas

**Interpretação:**
✅ Distribuição positiva indica boa eficiência geral.

---

### 6️⃣ **greedy_schedule_heatmap.png** - Mapa de Calor Dia × Horário

**Conteúdo:**
- Heatmap: Dias (linhas) × Horários (colunas)
- Cores: Vermelho (alta demanda) → Branco (baixa)

**O que observar:**
- Horários mais procurados (picos de cor)
- Dias de maior congestionamento
- Padrões de concentração (manhã vs tarde/noite)

**Interpretação:**
💡 Identifica oportunidades para distribuição de carga horária.

---

## 🔄 GRÁFICOS DE COMPARAÇÃO (Greedy vs Partial)

### compare_waste_boxplot.png - Desperdício Médio

**Compara:** Greedy vs Partial (todos os alphas/seeds agregados)

**O que observar:**
- Mediana: valor central da distribuição
- Caixa: 50% dos dados (quartis 25-75%)
- Linhas: mín/máx dos valores
- Pontos: outliers individuais

**Interpretação:**
- Se Partial < Greedy → partial tem menos desperdício (melhor)
- Se distribuições se sobrepõem → sem diferença significativa

---

### compare_allocation_boxplot.png - Taxa de Alocação

**Compara:** % de encontros alocados em cada heurística

**O que observar:**
- Centro da distribuição (mediana)
- Variabilidade entre instâncias/configurações

**Interpretação:**
- Se Partial ≈ Greedy → ambas têm mesma taxa de sucesso
- Diferenças grandes indicam dependência de parâmetros (alpha/seed)

---

### compare_runtime_boxplot.png - Tempo de Execução

**Compara:** Tempo em segundos para cada heurística

**O que observar:**
- Partial geralmente mais rápido que Greedy
- Variação por instância

**Interpretação:**
- Trade-off: Partial é mais rápido mas com qual qualidade?
- Usar em conjunto com desperdício/alocação para avaliar custo-benefício

---

## 📊 Resumo da Interpretação

| Métrica | Greedy | Partial | Melhor Para |
|---------|--------|---------|-----------|
| Taxa Alocação | ~97% | ~97% | Ambos similares |
| Desperdício | Basal | Aumenta c/ alpha | Greedy (menos desperdício) |
| Tempo | ~0.02s | ~0.02s | Ambos rápidos |

**Conclusão:**
- ✅ Greedy tem melhor desperdício
- ✅ Partial oferece diversidade (múltiplas soluções via alpha/seed)
- ⚖️ Trade-off qualidade vs. exploração

---

## 🔧 Como Regenerar os Gráficos

### Instâncias Individuais (Greedy)
```bash
# Compilar
make clean && make

# Executar para uma instância
./bin/app data/generated_instances/instance1.json

# Gerar gráficos por instância
python3 scripts/plotting/plot_greedy_results.py
```

**Saída:** `results/greedy_*.png`

### Comparação Entre Heurísticas
```bash
# Executar pipeline de agregação (roda greedy e partial em múltiplas instâncias)
python3 run_and_aggregate.py

# Gerar gráficos comparativos
python3 scripts/plotting/compare_heuristics.py
```

**Saída:** `results/compare_*_boxplot.png`

### Comparação Entre Instâncias
```bash
# Após run_and_aggregate.py
python3 scripts/plotting/plot_compare_instances.py
```

**Saída:** `results/compare_*.png` (gráficos por instância agregada)

---

## 📁 Arquivos Gerados

```
results/
├── greedy_allocation.png                  # Visão geral (1 instância)
├── greedy_metrics.png                     # Métricas resumidas
├── greedy_classroom_occupancy.png         # Distribuição por sala
├── greedy_daily_occupancy.png             # Distribuição por dia
├── greedy_waste_distribution.png          # Histograma + boxplot desperdício
├── greedy_schedule_heatmap.png            # Mapa de calor dia × horário
│
├── compare_waste_boxplot.png              # Comparação desperdício
├── compare_allocation_boxplot.png         # Comparação taxa alocação
└── compare_runtime_boxplot.png            # Comparação tempo execução

data/results/
├── greedy_stats_instance1.csv             # Dados brutos (1 instância)
├── greedy_stats_instance1_greedy.csv      # Dados greedy (agregação)
├── greedy_stats_instance1_partial_a*.csv  # Dados partial c/ alpha/seed
└── summary_instances.csv                  # Resumo todas as instâncias/heurísticas
```

---

## 📚 Referências Técnicas

**Algoritmo Greedy:**
- Estratégia: Largest-First, Best-Fit
- Penalidade de preferência: 10.000 (peso alto)
- Objetivo: Maximizar alocação, minimizar desperdício

**Algoritmo Partial (RCL):**
- Estratégia: Reduced Cost List com parâmetro alpha ∈ [0,1]
- Penalidade de preferência (RCL): 1.000 (reduzida)
- Objetivo: Explorar múltiplas soluções mantendo qualidade
- Parâmetros testados: alpha ∈ {0.25, 0.5, 0.75}, seed ∈ {0, 12345}

**Métricas Coletadas:**
- Taxa de alocação: % de encontros alocados
- Taxa de demanda: % de alunos acomodados
- Desperdício médio: vagas não utilizadas/encontro
- Runtime: tempo de execução (segundos)
- MaxRSS: memória máxima utilizada

---

## ❓ Dúvidas?

Consulte os dados brutos:
- `data/results/*.csv` — detalhes por execução
- `src/constructive/constructive_heuristic.cpp` — algoritmo Greedy
- `src/constructive/partial_greedy.cpp` — algoritmo Partial
- `scripts/plotting/*.py` — código de visualização
