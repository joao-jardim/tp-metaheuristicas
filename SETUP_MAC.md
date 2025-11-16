# 🍎 Guia de Instalação no macOS

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

Os gráficos serão salvos no diretório `results/`, por exemplo:
- `greedy_allocation.png`
- `greedy_metrics.png`
- `greedy_classroom_occupancy.png`
- `greedy_daily_occupancy.png`
- `greedy_waste_distribution.png`
- `greedy_schedule_heatmap.png`
- `greedy_preferences.png` (se houver preferências)

## Troubleshooting

### ❌ Erro: "command not found: python3"
```bash
# Reinstalar Python
brew reinstall python3

# Ou criar alias para python
echo "alias python=python3" >> ~/.zshrc
source ~/.zshrc
```

### ❌ Erro: "pip3: command not found"
```bash
# Reinstalar pip
python3 -m ensurepip --upgrade
```

### ❌ Erro: "ImportError: No module named matplotlib"
```bash
# Reinstalar as dependências com force
pip3 install --upgrade --force-reinstall matplotlib seaborn pandas
```

### ❌ Erro ao compilar C++: "nlohmann/json.hpp: No such file"
```bash
# Certifique-se que o arquivo existe
ls -la src/include/nlohmann/json.hpp

# Se não existir, download do arquivo single-header
curl -o src/include/nlohmann/json.hpp https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp
```

## Dicas para macOS

- Se usar **M1/M2 (Apple Silicon)**, pode ser necessário instalar versões de arquitetura nativa:
  ```bash
  arch -arm64 brew install python3
  ```

- Se tiver problemas com permissões, use `sudo`:
  ```bash
  sudo pip3 install -r plot_requirements.txt
  ```

- Para usar um ambiente virtual (melhor prática):
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r plot_requirements.txt
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

Pronto! 🚀 Você está configurado para executar o projeto.
