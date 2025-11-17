# Guia de Instalação no macOS

## Pré-requisitos

### 1️⃣ Instalar Homebrew (se ainda não tiver)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2️⃣ Instalar Xcode Command Line Tools (necessário para compilar C++)
```bash
xcode-select --install
```

### 3️⃣ Instalar Python 3 via Homebrew
```bash
brew install python3
```

Verificar instalação:
```bash
python3 --version
pip3 --version
```

## Instalação das Dependências Python

### Opção A: Usar o arquivo requirements.txt (RECOMENDADO)
```bash
cd /Users/joaojardim/Documents/UFOP/8periodo/MEH/tp-metaheuristicas
pip3 install -r plot_requirements.txt
```

### Opção B: Instalar pacotes individualmente
```bash
pip3 install matplotlib seaborn pandas
```

### Verificar instalação
```bash
python3 -c "import matplotlib; import pandas; import seaborn; print('✅ Todas as bibliotecas estão instaladas!')"
```

## Compilar e Executar o Projeto

### 1️⃣ Compilar o programa C++
```bash
cd /Users/joaojardim/Documents/UFOP/8periodo/MEH/tp-metaheuristicas
make clean
make
```

### 2️⃣ Executar a heurística (gera greedy_stats.csv)
```bash
./bin/app
```

Para processar **todas as instâncias** e agregar resultados (salva CSVs em `data/results/`):
```bash
python3 run_and_aggregate.py
```
Isto criará:
- `data/results/greedy_stats_<instance>.csv` (para cada instância)
- `data/results/summary_instances.csv` (resumo agregado)

### 3️⃣ Gerar gráficos
```bash
# Gráficos por instância (salvos em results/)
python3 scripts/plotting/plot_greedy_results.py

# Gráficos comparativos entre instâncias (summary_instances.csv -> results/)
python3 scripts/plotting/plot_compare_instances.py
```

## ✅ Checklist de Instalação

- [ ] Homebrew instalado (`brew --version`)
- [ ] Xcode Command Line Tools instalado (`xcode-select -p`)
- [ ] Python 3.8+ instalado (`python3 --version`)
- [ ] Matplotlib instalado (`python3 -c "import matplotlib"`)
- [ ] Pandas instalado (`python3 -c "import pandas"`)
- [ ] Seaborn instalado (`python3 -c "import seaborn"`)
- [ ] C++ compilado sem erros (`make` retorna sucesso)
- [ ] Arquivo `greedy_stats.csv` gerado após executar `./bin/app`
- [ ] Gráficos PNG gerados após executar `python3 plot_greedy_results.py`

