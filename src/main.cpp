#include "include/problem.hpp"
#include "include/constructive/constructive_heuristic.hpp"
#include <iostream>

int main(int argc, char** argv) {
    Problem p;

    // Permite passar caminho da instância como argumento: ./bin/app path/to/instance.json
    std::string instancePath = "instance1.json";
    if (argc > 1) {
        instancePath = argv[1];
    }

    p.loadInstance(instancePath);

    greedyConstruct(p);

    std::cout << "schedules: " << p.schedules.size() << "\n";
    std::cout << "buildings: " << p.buildings.size() << "\n";
    std::cout << "classrooms: " << p.classrooms.size() << "\n";
    std::cout << "professors: " << p.professors.size() << "\n";
    std::cout << "subjects: " << p.subjects.size() << "\n";
    std::cout << "meetings: " << p.meetings.size() << "\n";
    std::cout << "preferences: " << p.preferences.size() << "\n";
    std::cout << "restrictions: " << p.restrictions.size() << "\n";
    std::cout << "reservations: " << p.reservations.size() << "\n";
    return 0;
}