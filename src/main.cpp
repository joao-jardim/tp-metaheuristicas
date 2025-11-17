#include "include/problem.hpp"
#include "include/constructive/constructive_heuristic.hpp"
#include <iostream>
#include <string>
#include <sstream>

// If Makefile defines DEFAULT_HEUR at compile time, use it to set binary default.
#ifndef DEFAULT_HEUR
#define DEFAULT_HEUR 1
#endif
#ifndef DEFAULT_ALPHA
#define DEFAULT_ALPHA 0.0
#endif
#ifndef DEFAULT_SEED
#define DEFAULT_SEED 0
#endif

int main(int argc, char** argv) {
    Problem p;

    std::string instancePath = "instance1.json"; // nome relativo a data/generated_instances/
    std::string heuristicArg;
    double alpha = 0.0;
    unsigned int seed = 0;

#if DEFAULT_HEUR == 2
    heuristicArg = "partial";
    alpha = DEFAULT_ALPHA;
    seed = DEFAULT_SEED;
#else
    heuristicArg = "greedy";
    alpha = DEFAULT_ALPHA;
    seed = DEFAULT_SEED;
#endif

// Parsear argumentos: primeiro argumento posicional não-flag é o instancePath
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a.rfind("--heuristic=", 0) == 0) {
            heuristicArg = a.substr(std::string("--heuristic=").size());
        } else if (a == "--heuristic" && i + 1 < argc) {
            heuristicArg = argv[++i];
        } else if (!a.empty() && a[0] == '-') {
            // ignorar outras flags por enquanto
        } else {
            // primeiro posicional não-flag -> instancePath
            instancePath = a;
            // se começar com "data/generated_instances/", remover o prefixo (será re-adicionado em loadInstance)
            const std::string prefix = "data/generated_instances/";
            if (instancePath.rfind(prefix, 0) == 0) {
                instancePath = instancePath.substr(prefix.size());
            }
        }
    }

    if (heuristicArg.rfind("partial", 0) == 0) {
        if (heuristicArg == "partial") {
            if (alpha <= 0.0) alpha = 0.5; // default razoável se não veio do compile-time
        } else {
            std::string tail;
            if (heuristicArg.size() > 8 && heuristicArg[7] == ':') tail = heuristicArg.substr(8);
            else if (heuristicArg.size() > 7 && heuristicArg[7] != '\0') tail = heuristicArg.substr(7);
            // split tail por ':'
            std::istringstream ss(tail);
            std::string part;
            if (std::getline(ss, part, ':')) {
                try { alpha = std::stod(part); } catch(...) { if (alpha <= 0.0) alpha = 0.5; }
            }
            if (std::getline(ss, part, ':')) {
                try { seed = static_cast<unsigned int>(std::stoul(part)); } catch(...) { /* keep previous seed */ }
            }
        }
    } else if (heuristicArg == "greedy") {
        // nada adicional
    } else {
        if (!heuristicArg.empty()) {
            if (heuristicArg.find(':') != std::string::npos) {
                std::istringstream ss(heuristicArg);
                std::string part;
                if (std::getline(ss, part, ':')) {
                    try { alpha = std::stod(part); heuristicArg = "partial"; }
                    catch(...) { heuristicArg = "greedy"; }
                }
                if (std::getline(ss, part, ':')) {
                    try { seed = static_cast<unsigned int>(std::stoul(part)); } catch(...) { /* keep previous seed */ }
                }
            }
        }
    }

    p.loadInstance(instancePath);

    if (heuristicArg.rfind("partial", 0) == 0) {
        std::cout << "Executando heuristica parcialmente gulosa (alpha=" << alpha << ", seed=" << seed << ")\n";
        partiallyGreedyConstruct(p, alpha, seed);
    } else {
        std::cout << "Executando heuristica gulosa deterministica\n";
        greedyConstruct(p);
    }

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