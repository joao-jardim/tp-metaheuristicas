Ambos os algoritmos usados neste trabalho (NSGA-II e MOLA) precisam de soluc¸
˜
oes
iniciais e para isso foi desenvolvido um algoritmo gerador guloso de soluc¸
˜ oes. Para a construc¸
˜ ao da
soluc¸
˜ ao gulosa, primeiro ordena-se de forma decrescente os encontros de acordo com a sua demanda
e as salas de acordo com a capacidade de cada sala. Ap´ os este processo, para cada encontro aloca-se
a melhor opc¸
˜ ao dispon´ ıvel (aquela com o n´ umero de vagas dispon´ ıvel mais pr´ oximo da demanda
necess
´ aria).