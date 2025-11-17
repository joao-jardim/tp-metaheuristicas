#include "include/constructive/partial_greedy.hpp"
#include <random>
#include <algorithm>
#include <iostream>
#include <climits>
#include <string>
#include <iomanip>
#include <map>
#include <fstream>

void partiallyGreedyConstruct(Problem& p, double alpha, unsigned int seed) {
    if (alpha < 0.0) alpha = 0.0;
    if (alpha > 1.0) alpha = 1.0;

    std::mt19937 rng;
    if (seed == 0) {
        std::random_device rd;
        rng.seed(rd());
    } else {
        rng.seed(seed);
    }
    auto classroom_free = [&](int classroomId, int day, int scheduleId) {
        for (const auto& r : p.reservations) {
            if (r.classroomId == classroomId && r.dayOfWeek == day && r.scheduleId == scheduleId) return false;
        }
        return true;
    };

    auto applicable_preferences = [&](const Meeting& m) {
        std::vector<Preference> out;
        for (const auto &pref : p.preferences) {
            if (pref.category == "professor") {
                for (const auto &pc : m.professorCodes) if (pc == pref.categoryCode) { out.push_back(pref); break; }
            } else if (pref.category == "subject") {
                if (pref.categoryCode == m.subjectCode) out.push_back(pref);
            } else if (pref.category == "class") {
                for (const auto &cid : m.classIds) if (cid == pref.categoryCode) { out.push_back(pref); break; }
            }
        }
        return out;
    };

    int placed = 0;
    int notPlaced = 0;
    int totalDemand = 0;
    int demandPlaced = 0;
    int wasteTotal = 0;
    int underUtilizedWaste = 0;  // vagas ociosas em salas com <50% ocupação
    int standingStudents = 0;    // alunos em pé (demanda > capacidade)
    std::map<std::string, int> prefSatisfied;
    std::map<std::string, int> prefViolated;
    std::map<std::string, int> prefCategoryCount;

    std::map<int, int> classroomOccupancy;
    std::map<int, int> classroomDemand;
    std::map<int, int> classroomCapacity;
    std::map<int, int> dayOccupancy;
    std::map<int, int> dayDemand;
    std::vector<int> wasteValues;
    std::map<std::string, std::vector<int>> scheduleOccupancy;

    // penalidade por preferência reduzida para a heurística parcialmente gulosa
    const int PARTIAL_PREF_PENALTY = 1000; // antes era 10000 no greedy

    std::vector<int> idx(p.meetings.size());
    for (size_t i = 0; i < idx.size(); ++i) idx[i] = static_cast<int>(i);
    std::sort(idx.begin(), idx.end(), [&](int a, int b){
        return p.meetings[a].demand > p.meetings[b].demand;
    });

    for (int mi : idx) {
        const Meeting& m = p.meetings[mi];
        if (m.scheduleIds.empty()) continue;

        totalDemand += m.demand;
        auto prefs = applicable_preferences(m);

        bool allocated = false;
        for (int sched : m.scheduleIds) {
            if (allocated) break;

            struct Cand { int id; int score; int violated; int waste; };
            std::vector<Cand> cands;

            for (const auto& c : p.classrooms) {
                if (!classroom_free(c.id, m.dayOfWeek, sched)) continue;
                if (m.isPractical && !c.isLab) continue;
                if (c.capacity < m.demand) continue;  // Sala não cabe: não é candidata
                int waste = c.capacity - m.demand;

                int prefPenalty = 0;
                int violatedCount = 0;
                for (const auto &pf : prefs) {
                    if (!pf.buildingId.empty()) {
                        try {
                            int bid = std::stoi(pf.buildingId);
                            if (bid != c.buildingId) { prefPenalty += PARTIAL_PREF_PENALTY; ++violatedCount; }
                        } catch (...) {}
                    }
                    if (pf.floor != -1 && pf.floor != c.floor) { prefPenalty += PARTIAL_PREF_PENALTY; ++violatedCount; }
                    if (!pf.board.empty() && pf.board != c.board) { prefPenalty += PARTIAL_PREF_PENALTY; ++violatedCount; }
                    if (pf.projector && !c.projector) { prefPenalty += PARTIAL_PREF_PENALTY; ++violatedCount; }
                }
                int score = waste + prefPenalty;
                cands.push_back({c.id, score, violatedCount, waste});
            }

            if (cands.empty()) continue;

            int minScore = INT_MAX, maxScore = INT_MIN;
            for (const auto &cc : cands) {
                if (cc.score < minScore) minScore = cc.score;
                if (cc.score > maxScore) maxScore = cc.score;
            }

            int threshold = minScore;
            if (maxScore > minScore) {
                double t = minScore + alpha * (double)(maxScore - minScore);
                threshold = static_cast<int>(std::floor(t + 0.5));
            }

            std::vector<Cand> rcl;
            for (const auto &cc : cands) if (cc.score <= threshold) rcl.push_back(cc);

            if (rcl.empty()) {
                Cand best = cands[0];
                for (const auto &cc : cands) if (cc.score < best.score) best = cc;
                rcl.push_back(best);
            }

            std::uniform_int_distribution<size_t> dist(0, rcl.size() - 1);
            size_t choice = dist(rng);
            int chosenId = rcl[choice].id;
            int chosenViol = rcl[choice].violated;
            int chosenWaste = rcl[choice].waste;

            Reservation r;
            r.id = m.id;
            r.classroomId = chosenId;
            r.dayOfWeek = m.dayOfWeek;
            r.scheduleId = sched;
            p.reservations.push_back(std::move(r));

            const Classroom* chosenClassroom = nullptr;
            for (const auto& c : p.classrooms) if (c.id == chosenId) { chosenClassroom = &c; break; }

            ++placed;
            demandPlaced += m.demand;
            int realWaste = chosenWaste;
            wasteTotal += realWaste;
            wasteValues.push_back(realWaste);

            // Verificar alunos em pé APENAS após alocação: se demanda > capacidade
            if (chosenClassroom && m.demand > chosenClassroom->capacity) {
                standingStudents += (m.demand - chosenClassroom->capacity);
            }

            classroomOccupancy[chosenId]++;
            classroomDemand[chosenId] += m.demand;
            if (chosenClassroom) classroomCapacity[chosenId] = chosenClassroom->capacity;

            dayOccupancy[m.dayOfWeek]++;
            dayDemand[m.dayOfWeek] += m.demand;

            std::string daySchedKey = std::to_string(m.dayOfWeek) + "_" + std::to_string(sched);
            scheduleOccupancy[daySchedKey].push_back(m.demand);

            for (const auto &pf : prefs) {
                prefCategoryCount[pf.category]++;
                if (chosenViol == 0) prefSatisfied[pf.category]++; else prefViolated[pf.category]++;
            }

            allocated = true;
            break;
        }

        if (!allocated) ++notPlaced;
    }

    int total = placed + notPlaced;
    double placementRate = total > 0 ? (100.0 * placed / total) : 0.0;
    double demandRate = totalDemand > 0 ? (100.0 * demandPlaced / totalDemand) : 0.0;
    double avgWaste = placed > 0 ? (double)wasteTotal / placed : 0.0;
    
    // Calcular vagas ociosas em salas com ocupação < 50%
    for (const auto& [cid, dem] : classroomDemand) {
        int cap = classroomCapacity[cid];
        if (cap > 0 && dem < cap / 2.0) {
            underUtilizedWaste += (cap - dem);
        }
    }
    
    int unallocatedStudents = totalDemand - demandPlaced;

    std::cout << "\n";
    std::cout << "  Parâmetros: alpha = " << std::fixed << std::setprecision(2) << alpha 
              << ", seed = " << seed << "\n\n";

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "ALOCAÇÃO GERAL:\n";
    std::cout << "  Encontros alocados:    " << placed << " / " << total 
              << " (" << placementRate << "%)\n";
    std::cout << "  Encontros não alocados: " << notPlaced << "\n";
    std::cout << "  Demanda alocada:        " << demandPlaced << " / " << totalDemand 
              << " alunos (" << demandRate << "%)\n";
    std::cout << "  Desperdício médio:      " << avgWaste << " vagas/encontro\n";

    std::cout << "\nMÉTRICAS DE REFERÊNCIA:\n";
    std::cout << "  Alunos desalocados:                      " << unallocatedStudents << "\n";
    std::cout << "  Vagas ociosas (<50% ocupação):           " << underUtilizedWaste << "\n";
    std::cout << "  Alunos em pé (demanda > capacidade):     " << standingStudents << "\n";

    if (!prefCategoryCount.empty()) {
        std::cout << "\nPREFERÊNCIAS:\n";
        for (const auto &[cat, count] : prefCategoryCount) {
            int sat = prefSatisfied[cat];
            int viol = prefViolated[cat];
            double satRate = count > 0 ? (100.0 * sat / count) : 0.0;
            std::cout << "  " << cat << ":\n";
            std::cout << "    Total:       " << count << "\n";
            std::cout << "    Satisfeitas: " << sat << " (" << satRate << "%)\n";
            std::cout << "    Violadas:    " << viol << "\n";
        }
    }

    std::cout << "\n========================================\n\n";

    std::ofstream csv("greedy_stats.csv");
    if (csv.is_open()) {
        csv << "Metrica,Valor\n";
        csv << "Encontros Alocados," << placed << "\n";
        csv << "Encontros Total," << total << "\n";
        csv << "Taxa Alocacao (%)," << placementRate << "\n";
        csv << "Demanda Alocada," << demandPlaced << "\n";
        csv << "Demanda Total," << totalDemand << "\n";
        csv << "Taxa Demanda (%)," << demandRate << "\n";
        csv << "Desperdicio Medio," << avgWaste << "\n";
        csv << "Alunos Desalocados," << unallocatedStudents << "\n";
        csv << "Vagas Ociosas SubUtilizadas," << underUtilizedWaste << "\n";
        csv << "Alunos em Pe," << standingStudents << "\n";

        csv << "\nPreferencias por Categoria\n";
        csv << "Categoria,Total,Satisfeitas,Taxa (%)\n";
        for (const auto &[cat, count] : prefCategoryCount) {
            int sat = prefSatisfied[cat];
            double satRate = count > 0 ? (100.0 * sat / count) : 0.0;
            csv << cat << "," << count << "," << sat << "," << satRate << "\n";
        }

        csv << "\nOcupacao por Sala\n";
        csv << "ClassroomId,Encontros,Demanda,Capacidade,TaxaUtilizacao(%)\n";
        for (const auto &[cid, occ] : classroomOccupancy) {
            int cap = classroomCapacity[cid];
            int dem = classroomDemand[cid];
            double util = cap > 0 ? (100.0 * dem / cap) : 0.0;
            csv << cid << "," << occ << "," << dem << "," << cap << "," << util << "\n";
        }

        csv << "\nOcupacao por Dia\n";
        csv << "DiaSemanaSemana,Encontros,Demanda\n";
        for (int d = 0; d < 7; ++d) {
            if (dayOccupancy.count(d) > 0) csv << d << "," << dayOccupancy[d] << "," << dayDemand[d] << "\n";
        }

        csv << "\nDistribuicao Desperdicio\n";
        csv << "Desperdicio\n";
        for (int w : wasteValues) csv << w << "\n";

        csv << "\nOcupacao por Dia e Horario\n";
        csv << "DiaSchedule,Demanda\n";
        for (const auto &[key, demands] : scheduleOccupancy) {
            int totalDemandSched = 0; for (int d : demands) totalDemandSched += d;
            csv << key << "," << totalDemandSched << "\n";
        }

        csv.close();
    }
}
