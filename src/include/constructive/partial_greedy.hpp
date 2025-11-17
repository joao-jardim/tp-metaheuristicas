#ifndef PARTIAL_GREEDY_HPP
#define PARTIAL_GREEDY_HPP

#include "../problem.hpp"

// Heurística parcialmente gulosa (RCL - Restricted Candidate List)
// alpha: 0.0 -> comportamento determinístico (igual ao greedy)
// alpha: 1.0 -> RCL máximo (mais aleatoriedade)
// seed == 0 -> usa random_device (não determinístico). seed != 0 -> reprodutível
void partiallyGreedyConstruct(Problem& p, double alpha, unsigned int seed);

#endif
