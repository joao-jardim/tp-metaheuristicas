
CC := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -O2
INCLUDES := -Isrc -Iinclude -I/opt/homebrew/include

SRCS := $(wildcard src/*.cpp) $(wildcard src/constructive/*.cpp)
TARGET := bin/app

INSTANCE ?= data/generated_instances/instance0.json
HEURISTIC ?= greedy
DEFAULT_ALPHA ?= 0.25
DEFAULT_SEED ?= 0

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(SRCS)
	@mkdir -p $(dir $@)
	# If CHOICE is provided use it (non-interactive), otherwise ask interactively
	@if [ -n "$(CHOICE)" ]; then \
		choice="$(CHOICE)"; \
	else \
		echo "Escolha a heurística construtiva antes de compilar:"; \
		echo "  1) Gulosa"; \
		echo "  2) Parcialmente gulosa (RCL)"; \
		printf "Digite 1 ou 2 e tecle Enter: "; read choice; \
	fi; \
	if [ "$$choice" = "2" ]; then \
		DEFS="-DDEFAULT_HEUR=2 -DDEFAULT_ALPHA=$(DEFAULT_ALPHA) -DDEFAULT_SEED=$(DEFAULT_SEED)"; \
		echo "Compilando com heurística parcialmente gulosa (DEFAULT_ALPHA=$(DEFAULT_ALPHA))"; \
		$(CC) $(CXXFLAGS) $(INCLUDES) $(SRCS) $$DEFS -o $@; \
	else \
		DEFS="-DDEFAULT_HEUR=1 -DDEFAULT_ALPHA=$(DEFAULT_ALPHA) -DDEFAULT_SEED=$(DEFAULT_SEED)"; \
		echo "Compilando com heurística gulosa"; \
		$(CC) $(CXXFLAGS) $(INCLUDES) $(SRCS) $$DEFS -o $@; \
	fi

run: $(TARGET)
	./$(TARGET)

.PHONY: run-and-parse
run-and-parse: $(TARGET)
	@mkdir -p results/tmp
	@echo "Running: ./$(TARGET) $(INSTANCE) --heuristic=$(HEURISTIC)"
	@./$(TARGET) $(INSTANCE) --heuristic=$(HEURISTIC)
	@if [ -f greedy_stats.csv ]; then \
		outfile="results/tmp/greedy_stats_$(HEURISTIC).csv"; \
		jsonout="results/tmp/greedy_stats_$(HEURISTIC).json"; \
		mv greedy_stats.csv $$outfile; \
		python3 scripts/parse_greedy_stats.py --csv $$outfile --out $$jsonout || echo "Warning: parse script failed"; \
		echo "Wrote $$outfile and $$jsonout"; \
	else \
		echo "greedy_stats.csv not found after run"; \
	fi

.PHONY: run-all-and-parse
# Compile non-interactively (based on $(HEURISTIC)) and run the binary on all instances
# in `data/generated_instances/`, producing per-instance CSV+JSON files in `results/tmp/`.
run-all-and-parse:
	@mkdir -p results/tmp
	@hs=$(echo "$(HEURISTIC)" | tr ':' '_'); \
	# decide choice from HEURISTIC (partial -> 2, else 1)
	if echo "$(HEURISTIC)" | grep -q "partial"; then choice=2; else choice=1; fi; \
	echo "Compiling with CHOICE=$$choice"; \
	$(MAKE) CHOICE=$$choice DEFAULT_ALPHA=$(DEFAULT_ALPHA) DEFAULT_SEED=$(DEFAULT_SEED) $(TARGET); \
	for f in data/generated_instances/*.json; do \
		inst=$$(basename "$$f" .json); \
		echo "Running instance $$inst (heuristic=$(HEURISTIC))"; \
		./$(TARGET) "$$f" --heuristic="$(HEURISTIC)"; \
		if [ -f greedy_stats.csv ]; then \
			outfile="results/tmp/greedy_stats_$${inst}_$${hs}.csv"; \
			jsonout="results/tmp/greedy_stats_$${inst}_$${hs}.json"; \
			mv greedy_stats.csv $$outfile; \
			python3 scripts/parse_greedy_stats.py --csv $$outfile --out $$jsonout || echo "Warning: parse failed for $$outfile"; \
			echo "Wrote $$outfile and $$jsonout"; \
		else \
			echo "greedy_stats.csv not found for $$inst"; \
		fi; \
	done

clean:
	-rm -f $(TARGET)

install-deps:
	@echo "If you need nlohmann/json install via apt (Ubuntu):"
	@echo "  sudo apt update && sudo apt install -y nlohmann-json3-dev"
