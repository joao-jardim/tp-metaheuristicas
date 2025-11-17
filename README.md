#Trabalho Prático: Alocação de Salas com Metaheurísticas

## 📋 Descrição do Projeto

Este projeto implementa uma **solução para o problema de alocação de salas de aula** usando técnicas de otimização combinatória. A solução inclui:

- **Heurística Construtiva Gulosa**: alocação eficiente de encontros em salas disponíveis
- **Análise Detalhada**: coleta de estatísticas e métricas de qualidade
- **Visualizações**: gráficos comparativos e detalhados de múltiplas instâncias
- **Medição de Performance**: coleta de tempo de execução e uso de memória

## Estrutura do Projeto

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

## Saídas e Dados

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