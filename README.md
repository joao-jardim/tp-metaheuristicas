#Trabalho Prático: Alocação de Salas com Metaheurísticas

## 📋 Descrição do Projeto

Este projeto implementa uma **solução para o problema de alocação de salas de aula** usando técnicas de otimização combinatória. A solução inclui:

- 🎯 **Heurística Construtiva Gulosa**: alocação eficiente de encontros em salas disponíveis
- 📊 **Análise Detalhada**: coleta de estatísticas e métricas de qualidade
- 📈 **Visualizações**: gráficos comparativos e detalhados de múltiplas instâncias
- ⚡ **Medição de Performance**: coleta de tempo de execução e uso de memória

## 🏗️ Estrutura do Projeto

tp-metaheuristicas/
├── src/                              # Código-fonte C++
│   ├── main.cpp                      # Entrada principal
│   ├── problem.cpp                   # Parsing e gerenciamento de instâncias
│   ├── constructive/
│   │   └── constructive_heuristic.cpp  # Implementação da heurística gulosa
│   └── include/
│       ├── problem.hpp
│       └── constructive/
│           └── constructive_heuristic.hpp
│
├── data/
│   ├── generated_instances/          # Instâncias JSON de entrada
│   │   ├── instance1.json
│   │   ├── instance2.json
│   │   └── ...
│   └── results/                      # 📊 CSVs gerados (saída)
│       ├── greedy_stats_instance1.csv
│       ├── greedy_stats_instance2.csv
│       └── summary_instances.csv
│
├── results/                          # 📈 Gráficos PNG gerados
│   ├── compare_allocation_rate.png
│   ├── compare_demand_rate.png
│   ├── compare_runtime.png
│   ├── compare_memory.png
│   └── [mais visualizações]
│
├── scripts/plotting/                 # 📉 Scripts de análise
│   ├── plot_greedy_results.py       # Gráficos por instância
│   └── plot_compare_instances.py    # Gráficos comparativos
│
├── bin/                              # Binário compilado
│   └── app                           # Executável
│
├── Makefile                          # Compilação
├── run_and_aggregate.py              # Automação de múltiplas instâncias
├── plot_requirements.txt             # Dependências Python
├── SETUP_MAC.md                      # Setup para macOS
├── VISUALIZACOES.md                  # Guia de visualizações
└── README.md                         # Este arquivo
```

---

### Pré-requisitos

**macOS:**
```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Xcode Command Line Tools
xcode-select --install

# Instalar Python 3
brew install python3
```

**Dependências Python:**
```bash
pip3 install -r plot_requirements.txt
```

### Compilar

Ao executar `make` o processo solicitará que você escolha qual heurística construtiva será usada como padrão no binário:

- Digite `1` para a heurística gulosa (padrão)
- Digite `2` para a heurística parcialmente gulosa (RCL)

Exemplo:
```bash
make clean && make
# durante a execução, digite 1 ou 2 e pressione Enter
```

O `Makefile` definirá macros de compilação que ajustam o comportamento padrão do binário (`DEFAULT_HEUR`, `DEFAULT_ALPHA`, `DEFAULT_SEED`).

Isto gera o binário `bin/app`.

### Executar

**Para uma única instância:**
```bash
./bin/app instance1.json
```

Isto gera: `greedy_stats.csv` no diretório atual.

**Para todas as instâncias (recomendado):**
```bash
python3 run_and_aggregate.py
```

Isto:
- Executa o binário para cada instância em `data/generated_instances/`
- Salva CSVs individuais em `data/results/greedy_stats_*.csv`
- Gera resumo agregado em `data/results/summary_instances.csv`
- Mede tempo de execução e pico de memória

### Gerar Gráficos

```bash
# Gráficos comparativos entre instâncias
python3 scripts/plotting/plot_compare_instances.py
```

Isto gera PNGs em `results/`:
- Comparação de taxas de alocação/demanda
- Análise de desperdício vs eficiência
- Gráficos de performance (runtime, memória)
- Scatter plots e boxplots

---

## 📊 Saídas e Dados

### CSVs Gerados

**`data/results/greedy_stats_<instance>.csv`**
Estatísticas detalhadas por instância:
- Métricas: encontros alocados, taxa de alocação, taxa de demanda, desperdício médio
- Ocupação por sala, por dia, por horário
- Distribuição de desperdício
- Satisfação de preferências (se aplicável)

**`data/results/summary_instances.csv`**
Resumo consolidado de todas as instâncias:
```
instance | Encontros Alocados | Taxa Alocacao (%) | Demanda Alocada | ... | Runtime(s) | MaxRSS(kB) | PrefSat(%)
---------|-------------------|-------------------|-----------------|-----|------------|------------|----------
instance1| 974                | 97.4              | 39264           | ... | 0.0311     | 4800512    | [%]
instance2| 983                | 98.3              | 38732           | ... | 0.0212     | 5046272    | [%]
```

### Gráficos Gerados

**Comparativos:**
- `compare_allocation_rate.png` — Taxa de alocação por instância
- `compare_demand_rate.png` — Taxa de demanda atendida
- `compare_waste_vs_allocation.png` — Desperdício vs eficiência
- `compare_runtime.png` — Tempo de execução com linha de média
- `compare_runtime_with_std.png` — Runtime com desvio padrão
- `compare_runtime_vs_allocation_scatter.png` — Relação runtime × alocação
- `compare_runtime_boxplot.png` — Distribuição de runtime
- `compare_memory.png` — Pico de memória por instância

**Detalhados (por instância):**
- `greedy_allocation.png` — Pizza + barras de alocação
- `greedy_metrics.png` — Métricas principais em dashboard
- `greedy_classroom_occupancy.png` — Utilização de salas (top/bottom 10)
- `greedy_daily_occupancy.png` — Carga por dia da semana
- `greedy_waste_distribution.png` — Histograma + boxplot de desperdício
- `greedy_schedule_heatmap.png` — Demanda por dia e horário
- `greedy_preferences.png` — Satisfação de preferências (se houver)

---

## 🔧 Desenvolvimento

### Arquitetura

**C++ (src/)**
- `main.cpp`: Entrada; aceita nome da instância como argumento
- `problem.cpp/hpp`: Estruturas de dados e parsing de JSON
- `constructive_heuristic.cpp/hpp`: Algoritmo de alocação gulosa

**Python (scripts/plotting/)**
- `plot_compare_instances.py`: Comparativos entre instâncias
- `plot_greedy_results.py`: Gráficos detalhados por instância

**Automação**
- `run_and_aggregate.py`: Wrapper que executa todas as instâncias, agrega CSVs e mede performance

### Algoritmo: Greedy Best-Fit

1. Ordena encontros por demanda decrescente
2. Para cada encontro, tenta alocar na sala que:
   - Tem capacidade suficiente
   - Minimiza desperdício (ou respeita preferências com penalidade)
3. Coleta estatísticas detalhadas por sala, dia e horário

**Penalidade por Preferência:** 10.000 (grande, força respeito quando possível)

### Métricas Coletadas

- **Por encontro**: se foi alocado, sala, desperdício
- **Por sala**: número de encontros, demanda, ocupação, taxa de utilização
- **Por dia**: encontros e demanda total
- **Por dia/horário**: demanda agregada
- **Global**: taxa de alocação, taxa de demanda, desperdício médio, preferências satisfeitas

---

## 📈 Análise de Resultados

Veja **[VISUALIZACOES.md](VISUALIZACOES.md)** para interpretação detalhada dos gráficos e insights por métrica.

### Resumo Executivo (Exemplo)

| Métrica | Valor | Avaliação |
|---------|-------|-----------|
| Taxa Alocação | 97.4% | ✅ Excelente |
| Taxa Demanda | 96.1% | ✅ Excelente |
| Desperdício Médio | 11.69 vagas | ✅ Baixo |
| Tempo Médio | ~0.025s | ✅ Muito rápido |
| Pico de Memória | ~5MB | ✅ Eficiente |

---

## 🛠️ Troubleshooting

### Erro: "nlohmann/json.hpp: No such file"

O header JSON single-header já deve estar incluído. Se faltar:
```bash
curl -o src/include/nlohmann/json.hpp https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp
```

### Erro: "ImportError: No module named matplotlib"

Reinstale as dependências Python:
```bash
pip3 install --upgrade --force-reinstall matplotlib seaborn pandas
```

### Gráficos não são gerados

Verifique se:
1. `data/results/summary_instances.csv` existe (rode `run_and_aggregate.py`)
2. Python tem permissão de escrita em `results/`
3. Dependências estão instaladas: `pip3 list | grep -E "matplotlib|pandas|seaborn"`

---

## 📚 Referências Técnicas

- **Linguagem de Programação:** C++17
- **Build System:** Make
- **JSON Parsing:** nlohmann/json (single-header)
- **Visualização:** Python 3 + Matplotlib + Seaborn + Pandas
- **Plataforma Suportada:** macOS (Linux/Windows com ajustes)

---

## 📝 Notas

- O arquivo `greedy_stats.csv` é gerado na raiz ou em `data/results/` (conforme configuração)
- CSVs com sufixo `_<instance>` indicam que o programa processou múltiplas instâncias
- Gráficos sempre salvam em `results/` para centralizar visualizações
- Performance é medida com `time.perf_counter()` (Python) e `/usr/bin/time -l` (macOS)

---

## 👤 Autores

Joao Victor Ramalho de Sousa Pereira Jardim e Maria Eduarda Bessa Teixeira
Desenvolvido como Trabalho Prático para a disciplina de Metaheurísticas.

---

## 📄 Licença

Projeto acadêmico. Sem licença específica.

---

Para dúvidas sobre:
- **Visualizações:** veja [VISUALIZACOES.md](VISUALIZACOES.md)
- **Setup macOS:** veja [SETUP_MAC.md](SETUP_MAC.md)
- **Código C++:** consulte comentários em `src/constructive/constructive_heuristic.cpp`
