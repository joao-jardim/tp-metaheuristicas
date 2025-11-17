#ifndef CONSTRUCTIVE_HEURISTIC_HPP
#define CONSTRUCTIVE_HEURISTIC_HPP

#include "../problem.hpp"

void greedyConstruct(Problem& p);
// Heurística parcialmente gulosa (RCL - Restricted Candidate List)
// alpha: 0.0 -> comportamento determinístico (igual ao greedy)
// alpha: 1.0 -> RCL máximo (mais aleatoriedade)
// partiallyGreedyConstruct: alpha em [0,1] controla o tamanho da RCL.
// seed == 0 -> usa random_device para semear (não determinístico)
// seed != 0 -> usa seed fornecida para permitir reprodutibilidade
void partiallyGreedyConstruct(Problem& p, double alpha, unsigned int seed = 0);

#endif 
// Ambos os algoritmos usados neste trabalho (NSGA-II e MOLA) precisam de soluc¸
// ˜
// oes
// iniciais e para isso foi desenvolvido um algoritmo gerador guloso de soluc¸
// ˜ oes. Para a construc¸
// ˜ ao da
// soluc¸
// ˜ ao gulosa, primeiro ordena-se de forma decrescente os encontros de acordo com a sua demanda
// e as salas de acordo com a capacidade de cada sala. Ap´ os este processo, para cada encontro aloca-se
// a melhor opc¸
// ˜ ao dispon´ ıvel (aquela com o n´ umero de vagas dispon´ ıvel mais pr´ oximo da demanda
// necess
// ´ aria).