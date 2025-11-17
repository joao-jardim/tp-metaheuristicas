// legacy extra header removed; use partial_greedy.hpp instead
// This file kept for backward compatibility but intentionally left minimal.
#ifndef CONSTRUCTIVE_HEURISTIC_EXTRA_HPP
#define CONSTRUCTIVE_HEURISTIC_EXTRA_HPP

#include "../problem.hpp"

// Forward to new header (no default args here)
void partiallyGreedyConstruct(Problem& p, double alpha, unsigned int seed = 0);

#endif
