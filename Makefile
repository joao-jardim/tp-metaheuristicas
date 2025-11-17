
CC := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -O2
INCLUDES := -Isrc -Iinclude -I/opt/homebrew/include

SRCS := $(wildcard src/*.cpp) $(wildcard src/constructive/*.cpp)
TARGET := bin/app

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(SRCS)
	@mkdir -p $(dir $@)
	@echo "Escolha a heurística construtiva antes de compilar:";
	@echo "  1) Gulosa";
	@echo "  2) Parcialmente gulosa (RCL)";
	@printf "Digite 1 ou 2 e tecle Enter: "; \
	read choice; \
	if [ "$$choice" = "2" ]; then \
		DEFS="-DDEFAULT_HEUR=2 -DDEFAULT_ALPHA=0.25 -DDEFAULT_SEED=0"; \
		echo "Compilando com heurística parcialmente gulosa (DEFAULT_ALPHA=0.25)"; \
		$(CC) $(CXXFLAGS) $(INCLUDES) $(SRCS) $$DEFS -o $@; \
	else \
		DEFS="-DDEFAULT_HEUR=1 -DDEFAULT_ALPHA=0.0 -DDEFAULT_SEED=0"; \
		echo "Compilando com heurística gulosa"; \
		$(CC) $(CXXFLAGS) $(INCLUDES) $(SRCS) $$DEFS -o $@; \
	fi

run: $(TARGET)
	./$(TARGET)

clean:
	-rm -f $(TARGET)

install-deps:
	@echo "If you need nlohmann/json install via apt (Ubuntu):"
	@echo "  sudo apt update && sudo apt install -y nlohmann-json3-dev"
