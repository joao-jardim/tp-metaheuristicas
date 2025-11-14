//Implementação das definições do problema 
//O problema consiste em alocar encontros em salas e horários, respeitando restrições de capacidade e disponibilidade.
#include "include/problem.hpp"
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
// Definições das funções membro da classe Problem
// ... (implementações específicas das funções vão aqui)
// Exemplo de função para carregar dados do problema a partir de um arquivo na pasta data/generated_instances

struct Schedule {
    int id = 0;
    std::string startTime = "";
    std::string endTime = "";
};

struct Building {
    int id = 0;
    std::string name = "";
};

struct Classroom {
    int id = 0;
    bool isLab = false;
    int capacity = 0;
    int buildingId = 0;
    std::string description = "";
    int floor = 0;
    std::string board = "";
    bool projector = false;
};

struct Professor {
    std::string code = "";
    std::string name = "";
};

struct Subject {
    std::string code = "";
    std::string name = "";
};

struct Meeting { 
    std::string id = "";
    bool isPractical = false;
    std::vector<std::string> professorCodes;  // IDs dos professores
    std::string subjectCode = "";             // ID do assunto
    std::vector<std::string> classIds;        // IDs das turmas (se existir)
    std::vector<int> scheduleIds;             // IDs dos horários
    int demand = 0;
    int vacancies = 0;
    int dayOfWeek = 0;
};

struct Preference {
    std::string id = "";
    std::string category = "";
    std::string categoryCode = "";
    std::string buildingId = "";  // ID ou vazio se null
    int floor = -1;               // -1 significa não especificado
    std::string board = "";
    bool projector = false;
};

struct Restriction {
    std::string id = "";
    std::string category = "";
    std::string categoryCode = "";
    std::string buildingId = "";
    int floor = -1;               // -1 significa não especificado
    std::string board = "";
    bool projector = false;
};

struct Reservation {
    std::string id = "";
    int classroomId = 0;
    int dayOfWeek = 0;
    int scheduleId = 0;
};

void Problem::loadInstance(const std::string& filename) {
    std::ifstream file("data/generated_instances/" + filename);
    if (!file.is_open()) {
        std::cerr << "Erro ao abrir o arquivo: " << filename << std::endl;
        return;
    }

    // TODO: Implementar parsing com nlohmann::json
    file.close();
}
