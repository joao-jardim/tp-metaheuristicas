
#include "include/constructive/constructive_heuristic.hpp"
#include <algorithm>
#include <iostream>
#include <climits>

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

	auto classroom_free = [&](int classroomId, int day, int scheduleId) {
		for (const auto& r : p.reservations) {
			if (r.classroomId == classroomId && r.dayOfWeek == day && r.scheduleId == scheduleId) return false;
		}
		return true;
	};

	int placed = 0;
	for (int mi : idx) {
		const Meeting& m = p.meetings[mi];
		if (m.scheduleIds.empty()) continue;

		// busca melhor combinação schedule + classroom
		for (int sched : m.scheduleIds) {
			// escolher sala: melhor-fit (menor desperdício) que esteja livre
			int bestClassroom = 0;
			int bestWaste = INT_MAX;
			for (const auto& c : p.classrooms) {
				if (!classroom_free(c.id, m.dayOfWeek, sched)) continue;
				if (m.isPractical && !c.isLab) continue;
				if (c.capacity < m.demand) continue;
				int waste = c.capacity - m.demand;
				if (waste < bestWaste) { bestWaste = waste; bestClassroom = c.id; }
			}

			if (bestClassroom != 0) {
				Reservation r;
				r.id = m.id;
				r.classroomId = bestClassroom;
				r.dayOfWeek = m.dayOfWeek;
				r.scheduleId = sched;
				p.reservations.push_back(std::move(r));
				++placed;
				break;
			}
		}
	}

	std::cout << "Greedy placed " << placed << " meetings\n";
}

