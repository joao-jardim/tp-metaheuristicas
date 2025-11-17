# 📚 Resumo Executivo - Modelo Matemático

## Problema: Alocação de Encontros em Salas (Classroom Timetabling)

### **Descrição Informal**
Você tem:
- 1000 encontros de aulas (com diferentes demandas de alunos)
- 36 salas (com diferentes capacidades e características)
- 16 horários possíveis em 7 dias da semana
- Preferências de localização (prédio, andar, equipamentos)

**Objetivo**: Alocar cada encontro a uma sala, horário e dia de forma que:
1. ✅ O máximo de encontros sejam alocados
2. ✅ O desperdício de espaço seja minimizado
3. ✅ As preferências sejam respeitadas

---

## Formulação Matemática Compacta

### Dados de Entrada
```
M = conjunto de encontros (|M| = 1000)
C = conjunto de salas (|C| = 36)  
H = conjunto de horários (|H| = 16)
D = 7 dias da semana

Para cada encontro i ∈ M:
  demand_i     = número de alunos
  dayOfWeek_i  = dia fixo (0-6)
  S_i ⊆ H      = horários permitidos
  isPractical_i = requer laboratório? (0/1)

Para cada sala j ∈ C:
  capacity_j  = número de lugares
  isLab_j     = é laboratório? (0/1)
  building_j  = prédio
  features_j  = {floor, board, projector}

Preferências = requisitos soft de localização/equipamento
```

### Variável de Decisão
```
x_{i,j,k,d} ∈ {0,1} para cada (encontro, sala, horário, dia)

x_{i,j,k,d} = 1 ⟺ encontro i alocado à sala j, horário k, dia d
```

### Restrições Hard (obrigatórias)
```
1. Cada encontro alocado no máximo uma vez:
   Σ_j Σ_k x_{i,j,k,d_i} ≤ 1  ∀i

2. Sala disponível em horário/dia (sem conflito):
   Σ_i x_{i,j,k,d} ≤ 1  ∀j,k,d

3. Capacidade: capacity_j ≥ demand_i

4. Compatibilidade: 
   - Se isPractical_i = 1 → isLab_j = 1
   - k ∈ S_i (horário permitido)
```

### Função Objetivo (Greedy)
```
Para cada encontro i, escolher sala j que minimiza:

  score_{i,j} = waste_{i,j} + penalty_{i,j}

Onde:
  waste_{i,j} = capacity_j - demand_i
  penalty_{i,j} = Σ_p violated_preferences(i,j) × W_pref
                (W_pref = 10000 para greedy, 1000 para partial)

Estratégia: Largest-First Best-Fit
  - Ordenar encontros por demanda decrescente
  - Para cada encontro, alocar na sala com menor score
  - Se nenhuma sala válida, deixar não alocado
```

### Função Objetivo (Partial/RCL)
```
Em vez de escolher a melhor sala, criar lista restrita (RCL):

  threshold = minScore + α(maxScore - minScore)
  RCL = {j : score_{i,j} ≤ threshold}
  
  Escolher j uniformemente aleatório de RCL

Parâmetros:
  α ∈ [0,1] : controla aleatoriedade
             (0 = greedy determinístico, 1 = completamente aleatório)
  seed : semente RNG
```

---

## Resultados Esperados

### Instância1 (1000 encontros, 36 salas)
```
Greedy:
  Encontros alocados: 974/1000 (97.4%)
  Demanda alocada: 39264/40861 (96.1%)
  Desperdício médio: 11.69 vagas/encontro
  Alunos em pé: 0 (nenhum - todas salas com capacidade ≥ demanda)

Partial (α=0.5, seed=12345):
  Encontros alocados: 974/1000 (97.4%)
  Demanda alocada: 39264/40861 (96.1%)
  Desperdício médio: 13.13 vagas/encontro
  Alunos em pé: 0 (idem)
```

---

## Análise Matemática

### Número de Soluções Possíveis (Espaço de Busca)
```
Limite superior: 
  |Soluções| ≈ (|C| × |H| × |D|)^|M|  
           = (36 × 16 × 7)^1000
           ≈ 4032^1000
           = astronomicamente grande!

Redução por restrições hard:
  - Apenas 974 encontros são alocáveis (26 infeasível)
  - Reduz espaço mas ainda NP-Difícil
```

### Otimalidade
```
Greedy é uma heurística construtiva:
  ✗ NÃO garante solução ótima
  ✗ NÃO garante aproximação com fator conhecido
  ✓ MAS converge rapidamente em tempo polinomial

Partial oferece:
  ✓ Exploração de múltiplas soluções via aleatoriedade
  ✓ Trade-off entre qualidade (desperdício) e diversidade
```

---

## Equações-Chave Resumidas

| Equação | Significado |
|---------|-----------|
| $\text{waste}_{i,j} = \text{cap}_j - \text{dem}_i$ | Espaço desperdiçado |
| $\text{score}_{i,j} = \text{waste}_{i,j} + W_p \cdot \text{penalidade}_p$ | Qualidade de alocação |
| $\text{Taxa Alocação (\%)} = \frac{\text{\# alocados}}{m} \times 100$ | Sucesso de cobertura |
| $\text{Taxa Demanda (\%)} = \frac{\sum \text{dem alocada}}{\sum \text{dem total}} \times 100$ | Cobertura de alunos |
| $\text{Desp. Médio} = \frac{1}{n_{\text{aloc}}} \sum \text{waste}$ | Eficiência de espaço |
| $\text{RCL threshold} = \text{min} + \alpha(\text{max} - \text{min})$ | Controle de aleatoriedade |

---

## Exemplos Visuais de Alocação

### Alocação Greedy (Best-Fit)
```
Encontro A: demand = 50 alunos, dia = 2 (terça)
  Salas viáveis: 
    Sala 10: cap=70, waste=20, score=20 ← ESCOLHIDA (menor score)
    Sala 12: cap=100, waste=50, score=50+penalty
    Sala 5: cap=60, waste=10, score=10+10000 (sem projetor, pen violada)
  
  Resultado: A → Sala 10, horário 9, terça-feira
```

### Alocação Partial (RCL, α=0.5)
```
Idem acima, mas:
  minScore = 20 (Sala 10)
  maxScore = 50 (Sala 12)
  threshold = 20 + 0.5×(50-20) = 35
  
  RCL = {Sala 10, Sala 12} (ambas score ≤ 35)
  
  Selecionar aleatório → Sala 10 ou Sala 12 com igual probabilidade
  
  → Resultado: A pode ir para Sala 10 OU Sala 12
     (oferece diversidade de soluções)
```

---

## Complexidade Computacional

| Operação | Tempo |
|----------|-------|
| Ordenar encontros | $O(m \log m)$ = $O(1000 \log 1000)$ ≈ $10^4$ |
| Loop: encontros × horários × salas × prefs | $O(m \cdot h \cdot c \cdot p)$ = $O(10^3 \cdot 10 \cdot 36 \cdot 6)$ ≈ $10^7$ |
| **Total** | $\approx O(10^7)$ operações ≈ **~10ms** em CPU moderno |

**Conclusão**: Heurística é muito rápida (tempo real) comparado a métodos exatos (NP-Difícil).

---

## Interpretação dos Resultados

### Por que Greedy ≈ Partial em alocação?
```
Ambos usam Largest-First + Best-Fit
→ Mesma taxa de sucesso (~97%)

Mas diferem em:
  - Desperdício: Greedy=11.69, Partial=13.13 
    (Greedy melhor por ser determinístico)
  - Tempo: Partial pode ser mais rápido (aleatório < score mín)
  - Diversidade: Partial gera múltiplas soluções
```

### Por que 26 encontros não são alocáveis?
```
Possíveis razões:
  1. Demanda > maior sala disponível (infeasível)
  2. Únicos horários viáveis conflitam com outros encontros
  3. Restrições de tipo (prático sem lab) bloqueiam
  4. Sequência greedy (Largest-First) deixa pequenos sem sala
```

---

## Código vs Matemática (Mapeamento)

| Variável C++ | Símbolo Matemático |
|--------------|-------------------|
| `demand_i` | $\text{demand}_i$ |
| `capacity_j` | $\text{capacity}_j$ |
| `waste` | $\text{waste}_{i,j}$ |
| `score` | $\text{score}_{i,j}$ |
| `prefPenalty` | $W_p \cdot \text{\#violações}$ |
| `x_{i,j,k,d}` | `reservations[].{id, classroomId, dayOfWeek, scheduleId}` |
| `placed` | $\sum x$ (conta alocações) |
| `threshold` (RCL) | $\text{min} + \alpha(\text{max} - \text{min})$ |

---

## Conclusão

**Tipo de Problema**: Classroom Timetabling (variante)
**Classe NP**: NP-Difícil (confirmado por literatura)
**Solução**: Heurística Construtiva (Greedy + Partial RCL)
**Garantias**: Nenhuma (heurística), mas prática (~97% em 10ms)
**Qualidade**: Muito bom para instâncias reais (trade-off qualidade vs tempo)

Para solver ótimo: use programação inteira (IP/MILP) + branch-and-bound (mas >> tempo)
Para qualidade melhor: use metaheurísticas (SA, GA, Tabu) + mais tempo computacional
