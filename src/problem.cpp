//Implementação das definições do problema 
//O problema consiste em alocar encontros em salas e horários, respeitando restrições de capacidade e disponibilidade.
#include "include/problem.hpp"
#include <vector>
#include <string>
#include <unordered_map> 
#include <utility>
#include <limits>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <random>
#include <ctime>
#include <cmath>
#include <cstdlib>
#include <iomanip>
// Definições das funções membro da classe Problem
// ... (implementações específicas das funções vão aqui)
// Exemplo de função para carregar dados do problema a partir de um arquivo na pasta data/generated_instances
void Problem::loadInstance(const std::string& filename) {
    std::ifstream file("data/generated_instances/" + filename);
    if (!file.is_open()) {
        std::cerr << "Erro ao abrir o arquivo: " << filename << std::endl;
        return;
    }

    std::string line;
    while (std::getline(file, line)) {

    file.close();
}
