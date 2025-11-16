
#include "include/constructive/constructive_heuristic.hpp"
#include <algorithm>
#include <iostream>
#include <climits>
#include <string>
#include <iomanip>
#include <map>
#include <fstream>

// Heurística gulosa simples:
// - Ordena encontros por demanda decrescente (maiores primeiro)
// - Para cada encontro, tenta alocar em um dos horários permitidos
//   buscando a menor sala disponível que comporte a demanda e
//   satisfaça requisitos (laboratório para práticos, projetor, etc.)
// - Respeita reservas já existentes carregadas na instância

void greedyConstruct(Problem& p) {
	// Ordena índices de meetings por demanda (desc)
	std::vector<int> idx(p.meetings.size());
	for (size_t i = 0; i < idx.size(); ++i) idx[i] = static_cast<int>(i);
	std::sort(idx.begin(), idx.end(), [&](int a, int b){
		return p.meetings[a].demand > p.meetings[b].demand;
	});

	//verificar se a sala ta livre
	auto classroom_free = [&](int classroomId, int day, int scheduleId) {
		for (const auto& r : p.reservations) {
			if (r.classroomId == classroomId && r.dayOfWeek == day && r.scheduleId == scheduleId) return false;
		}
		return true;
	};

	// coleta preferências aplicáveis a um meeting
	auto applicable_preferences = [&](const Meeting& m) {
		std::vector<Preference> out;
		for (const auto &pref : p.preferences) {
			if (pref.category == "professor") {
				// verifica se o meeting contém o professor indicado
				for (const auto &pc : m.professorCodes) if (pc == pref.categoryCode) { out.push_back(pref); break; }
			} else if (pref.category == "subject") {
				if (pref.categoryCode == m.subjectCode) out.push_back(pref);
			} else if (pref.category == "class") {
				for (const auto &cid : m.classIds) if (cid == pref.categoryCode) { out.push_back(pref); break; }
			}
		}
		return out;
	};

	// Estatísticas
	int placed = 0;
	int notPlaced = 0;
	int totalDemand = 0;
	int demandPlaced = 0;
	int wasteTotal = 0;
	std::map<std::string, int> prefSatisfied;     // categoria -> quantidade satisfeitas
	std::map<std::string, int> prefViolated;      // categoria -> quantidade violadas
	std::map<std::string, int> prefCategoryCount; // categoria -> total de preferências
	
	// Dados detalhados para gráficos avançados
	std::map<int, int> classroomOccupancy;        // classroomId -> número de encontros alocados
	std::map<int, int> classroomDemand;           // classroomId -> demanda total alocada
	std::map<int, int> classroomCapacity;         // classroomId -> capacidade (para calcular utilização)
	std::map<int, int> dayOccupancy;              // dayOfWeek -> número de encontros alocados
	std::map<int, int> dayDemand;                 // dayOfWeek -> demanda total alocada
	std::vector<int> wasteValues;                 // desperdício de cada encontro alocado
	std::map<std::string, std::vector<int>> scheduleOccupancy; // "day_schedule" -> [demandas alocadas]

	for (int mi : idx) {
		const Meeting& m = p.meetings[mi];
		if (m.scheduleIds.empty()) continue;

		totalDemand += m.demand;
		auto prefs = applicable_preferences(m);

		// busca melhor combinação schedule + classroom
		bool allocated = false;
		for (int sched : m.scheduleIds) {
			if (allocated) break;

			// escolher sala: melhor-fit (menor desperdício) que esteja livre
			int bestClassroom = 0;
			int bestWaste = INT_MAX;
			int bestPrefViolated = 0;
			
			//procurando a melhor sala pra um meeting
			for (const auto& c : p.classrooms) {
				if (!classroom_free(c.id, m.dayOfWeek, sched)) continue;
				if (m.isPractical && !c.isLab) continue;
				if (c.capacity < m.demand) continue;
				int waste = c.capacity - m.demand;
				
				// calcula penalidade e número de preferências violadas
				int prefPenalty = 0;
				int violatedCount = 0;
				for (const auto &pf : prefs) {
					// buildingId em Preference é string (pode ser vazio)
					if (!pf.buildingId.empty()) {
						try {
							int bid = std::stoi(pf.buildingId);
							if (bid != c.buildingId) { prefPenalty += 10000; ++violatedCount; }
						} catch (...) { /* se não for número, não compara */ }
					}
					if (pf.floor != -1 && pf.floor != c.floor) { prefPenalty += 10000; ++violatedCount; }
					if (!pf.board.empty() && pf.board != c.board) { prefPenalty += 10000; ++violatedCount; }
					// só considera preferência positiva por projetor (se true)
					if (pf.projector && !c.projector) { prefPenalty += 10000; ++violatedCount; }
				}
				int score = waste + prefPenalty;
				if (score < bestWaste) { 
					bestWaste = score; 
					bestClassroom = c.id; 
					bestPrefViolated = violatedCount;
				}
			}

			// se achou sala, aloca
			if (bestClassroom != 0) {
				Reservation r;
				r.id = m.id;
				r.classroomId = bestClassroom;
				r.dayOfWeek = m.dayOfWeek;
				r.scheduleId = sched;
				p.reservations.push_back(std::move(r));
				
				// Encontra a sala para obter informações de capacidade
				const Classroom* chosenClassroom = nullptr;
				for (const auto& c : p.classrooms) {
					if (c.id == bestClassroom) { chosenClassroom = &c; break; }
				}
				
				// atualiza estatísticas
				++placed;
				demandPlaced += m.demand;
				int realWaste = bestWaste % 10000; // remove penalidades para calcular desperdício real
				wasteTotal += realWaste;
				wasteValues.push_back(realWaste);
				
				// Dados por sala
				classroomOccupancy[bestClassroom]++;
				classroomDemand[bestClassroom] += m.demand;
				if (chosenClassroom) {
					classroomCapacity[bestClassroom] = chosenClassroom->capacity;
				}
				
				// Dados por dia
				dayOccupancy[m.dayOfWeek]++;
				dayDemand[m.dayOfWeek] += m.demand;
				
				// Dados por dia/horário
				std::string daySchedKey = std::to_string(m.dayOfWeek) + "_" + std::to_string(sched);
				scheduleOccupancy[daySchedKey].push_back(m.demand);
				
				// coleta preferências satisfeitas/violadas
				for (const auto &pf : prefs) {
					prefCategoryCount[pf.category]++;
					// verifica satisfação (simplificado: apenas conta totais)
					if (bestPrefViolated == 0) {
						prefSatisfied[pf.category]++;
					} else {
						// nota: essa é uma aproximação; uma análise mais precisa
						// exigiria guardar referência à sala escolhida e comparar
						prefViolated[pf.category]++;
					}
				}
				
				allocated = true;
				break;
			}
		}
		
		if (!allocated) {
			++notPlaced;
		}
	}

	// ============= RELATÓRIO ESTATÍSTICO =============
	std::cout << "\n";
	std::cout << "========================================\n";
	std::cout << "         GREEDY HEURISTIC REPORT        \n";
	std::cout << "========================================\n\n";

	int total = placed + notPlaced;
	double placementRate = total > 0 ? (100.0 * placed / total) : 0.0;
	double demandRate = totalDemand > 0 ? (100.0 * demandPlaced / totalDemand) : 0.0;
	double avgWaste = placed > 0 ? (double)wasteTotal / placed : 0.0;

	std::cout << std::fixed << std::setprecision(2);
	std::cout << "ALOCAÇÃO GERAL:\n";
	std::cout << "  Encontros alocados:    " << placed << " / " << total 
	          << " (" << placementRate << "%)\n";
	std::cout << "  Encontros não alocados: " << notPlaced << "\n";
	std::cout << "  Demanda alocada:        " << demandPlaced << " / " << totalDemand 
	          << " alunos (" << demandRate << "%)\n";
	std::cout << "  Desperdício médio:      " << avgWaste << " vagas/encontro\n";

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

	// ============= EXPORTAR PARA CSV =============
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
		
		csv << "\nPreferencias por Categoria\n";
		csv << "Categoria,Total,Satisfeitas,Taxa (%)\n";
		for (const auto &[cat, count] : prefCategoryCount) {
			int sat = prefSatisfied[cat];
			double satRate = count > 0 ? (100.0 * sat / count) : 0.0;
			csv << cat << "," << count << "," << sat << "," << satRate << "\n";
		}
		
		// Ocupação por sala
		csv << "\nOcupacao por Sala\n";
		csv << "ClassroomId,Encontros,Demanda,Capacidade,TaxaUtilizacao(%)\n";
		for (const auto &[cid, occ] : classroomOccupancy) {
			int cap = classroomCapacity[cid];
			int dem = classroomDemand[cid];
			double util = cap > 0 ? (100.0 * dem / cap) : 0.0;
			csv << cid << "," << occ << "," << dem << "," << cap << "," << util << "\n";
		}
		
		// Ocupação por dia
		csv << "\nOcupacao por Dia\n";
		csv << "DiaSemanaSemana,Encontros,Demanda\n";
		for (int d = 0; d < 7; ++d) {
			if (dayOccupancy.count(d) > 0) {
				csv << d << "," << dayOccupancy[d] << "," << dayDemand[d] << "\n";
			}
		}
		
		// Distribuição de desperdício
		csv << "\nDistribuicao Desperdicio\n";
		csv << "Desperdicio\n";
		for (int w : wasteValues) {
			csv << w << "\n";
		}
		
		// Ocupação por dia/horário
		csv << "\nOcupacao por Dia e Horario\n";
		csv << "DiaSchedule,Demanda\n";
		for (const auto &[key, demands] : scheduleOccupancy) {
			int totalDemandSched = 0;
			for (int d : demands) totalDemandSched += d;
			csv << key << "," << totalDemandSched << "\n";
		}
		
		csv.close();
		std::cout << "Dados exportados para: greedy_stats.csv\n";
	}
}

