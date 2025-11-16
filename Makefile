
CC := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -O2
INCLUDES := -Isrc -Iinclude -I/opt/homebrew/include

SRCS := $(wildcard src/*.cpp) $(wildcard src/constructive/*.cpp)
TARGET := bin/app

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(SRCS)
	@mkdir -p $(dir $@)
	$(CC) $(CXXFLAGS) $(INCLUDES) $(SRCS) -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	-rm -f $(TARGET)

install-deps:
	@echo "If you need nlohmann/json install via apt (Ubuntu):"
	@echo "  sudo apt update && sudo apt install -y nlohmann-json3-dev"
