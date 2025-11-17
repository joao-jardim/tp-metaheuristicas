# 📐 Modelo Matemático - Problema de Alocação de Encontros em Salas

## 1. Definição do Problema

Este é um **Problema de Alocação de Recursos** (Resource Allocation Problem) ou **Timetabling Problem**, especificamente um **Class Timetabling Problem** com restrições de capacidade e preferências.

### Caracterização
- **Classe**: Problema de Otimização Combinatória NP-Difícil
- **Objetivo**: Maximizar alocação de encontros minimizando desperdício de capacidade
- **Tipo**: Problema de Satisfação com Preferências (Constraint Satisfaction with Preferences)

---

## 2. Conjuntos e Índices

| Símbolo | Descrição |
|---------|-----------|
| $M$ | Conjunto de encontros (meetings), $\|M\| = m$ |
| $C$ | Conjunto de salas (classrooms), $\|C\| = c$ |
| $H$ | Conjunto de horários (schedules), $\|H\| = h$ |
| $D$ | Conjunto de dias da semana, $\|D\| = 7$ |
| $P$ | Conjunto de professores |
| $S$ | Conjunto de disciplinas (subjects) |
| $B$ | Conjunto de prédios (buildings) |
| $\text{Pref}$ | Conjunto de preferências |

### Índices
- $i \in M$ : índice de encontro
- $j \in C$ : índice de sala
- $k \in H$ : índice de horário
- $d \in D$ : índice de dia da semana

---

## 3. Parâmetros

### 3.1 Encontros (Meetings)
Para cada encontro $i \in M$:
- $\text{demand}_i$ : número de alunos requeridos (demanda)
- $\text{dayOfWeek}_i$ : dia da semana (fixo, $0 \leq \text{dayOfWeek}_i < 7$)
- $S_i \subseteq H$ : conjunto de horários disponíveis para o encontro $i$
- $\text{isPractical}_i$ : indicador se encontro é prático ($\text{isPractical}_i \in \{0,1\}$)
- $\text{prof}_i \subseteq P$ : conjunto de professores do encontro
- $\text{subj}_i \in S$ : disciplina do encontro

### 3.2 Salas (Classrooms)
Para cada sala $j \in C$:
- $\text{capacity}_j$ : capacidade da sala
- $\text{isLab}_j$ : indicador se é laboratório ($\text{isLab}_j \in \{0,1\}$)
- $\text{building}_j \in B$ : prédio onde está
- $\text{floor}_j$ : andar
- $\text{board}_j$ : tipo de quadro
- $\text{projector}_j$ : possui projetor ($\text{projector}_j \in \{0,1\}$)

### 3.3 Preferências
Para cada preferência $p \in \text{Pref}$:
- $\text{category}_p$ : categoria (professor, subject, class)
- $\text{categoryCode}_p$ : código da categoria
- $\text{building}_p$ : prédio preferido (ou $\emptyset$)
- $\text{floor}_p$ : andar preferido (ou $-1$ se não especificado)
- $\text{board}_p$ : tipo de quadro preferido (ou $\emptyset$)
- $\text{projector}_p$ : preferência por projetor ($\in \{0,1\}$)

### 3.4 Penalidades
- $W_{\text{pref}}$ : penalidade por preferência violada = **10000** (greedy) ou **1000** (partial)
- $\alpha \in [0,1]$ : parâmetro de aleatoriedade (heurística parcial)

---

## 4. Variáveis de Decisão

### Variável Binária de Alocação
$$x_{i,j,k,d} \in \{0,1\}$$

Onde:
- $x_{i,j,k,d} = 1$ se encontro $i$ é alocado à sala $j$, horário $k$, dia $d$
- $x_{i,j,k,d} = 0$ caso contrário

**Restrição implícita**: $d = \text{dayOfWeek}_i$ (dia é fixo por encontro)

### Variáveis Auxiliares (Métricas)
- $\text{waste}_{i,j}$ : desperdício = $\text{capacity}_j - \text{demand}_i$ (quando alocado)
- $\text{penalty}_{i,j}$ : penalidade por preferências violadas

---

## 5. Restrições (Hard Constraints)

### 5.1 Cada encontro é alocado no máximo uma vez
$$\sum_{j \in C} \sum_{k \in S_i} x_{i,j,k,d_i} \leq 1 \quad \forall i \in M$$

### 5.2 Compatibilidade de Horário
$$x_{i,j,k,d} = 0 \quad \text{se} \quad k \notin S_i$$

Ou equivalentemente, uma alocação só é válida se $k \in S_i$.

### 5.3 Compatibilidade de Tipo de Encontro
$$x_{i,j,k,d} = 0 \quad \text{se} \quad \text{isPractical}_i = 1 \text{ e } \text{isLab}_j = 0$$

(Encontros práticos só em laboratórios)

### 5.4 Restrição de Capacidade
$$x_{i,j,k,d} = 0 \quad \text{se} \quad \text{demand}_i > \text{capacity}_j$$

(A sala deve caber a demanda do encontro)

### 5.5 Sem Conflito de Sala-Horário-Dia
$$\sum_{i \in M} x_{i,j,k,d} \leq 1 \quad \forall j \in C, k \in H, d \in D$$

(Cada sala em cada horário em cada dia pode ter no máximo um encontro)

---

## 6. Restrições (Soft Constraints / Preferências)

Para cada encontro $i$ e sala $j$, calcular **penalidade de preferências violadas**:

$$\text{penalty}_{i,j} = \sum_{p \in \text{Pref}} \delta_{i,j,p} \cdot W_{\text{pref}}$$

Onde $\delta_{i,j,p} = 1$ se preferência $p$ aplicável a $i$ é violada pela sala $j$:

- $\delta_{i,j,p} = 1$ se $\text{category}_p = \text{"professor"}$ e professor do encontro prefere prédio $\text{building}_p \neq \text{building}_j$
- $\delta_{i,j,p} = 1$ se $\text{category}_p = \text{"subject"}$ e disciplina prefere prédio/andar/quadro/projetor e não corresponde
- $\delta_{i,j,p} = 1$ se $\text{projector}_p = 1$ e sala não tem projetor ($\text{projector}_j = 0$)
- Etc.

---

## 7. Função Objetivo

### Objetivo Primário: Maximizar Alocação
$$\text{maximize} \quad \sum_{i \in M} \sum_{j \in C} \sum_{k \in S_i} x_{i,j,k,d_i}$$

Ou equivalentemente: **Maximizar número de encontros alocados**

### Objetivo Secundário: Minimizar Desperdício (Best-Fit)

Para cada alocação válida de encontro $i$ à sala $j$:
$$\text{score}_{i,j} = \text{waste}_{i,j} + \text{penalty}_{i,j}$$

Onde:
- $\text{waste}_{i,j} = \text{capacity}_j - \text{demand}_i$
- $\text{penalty}_{i,j}$ = penalidade por preferências violadas

**Heurística Greedy**: Escolher sala com menor $\text{score}_{i,j}$ (minimizar desperdício + penalidades)

**Heurística Parcial (RCL)**: Criar lista restrita de candidatos com score próximo ao mínimo, selecionar aleatoriamente

---

## 8. Métricas Coletadas

### Métricas Primárias
| Métrica | Fórmula |
|---------|---------|
| Encontros Alocados | $\sum_{i,j,k,d} x_{i,j,k,d}$ |
| Taxa de Alocação (%) | $\frac{\text{Encontros Alocados}}{\|M\|} \times 100$ |
| Demanda Alocada | $\sum_{i: \text{alocado}} \text{demand}_i$ |
| Taxa de Demanda (%) | $\frac{\text{Demanda Alocada}}{\sum_i \text{demand}_i} \times 100$ |

### Métricas de Eficiência
| Métrica | Fórmula |
|---------|---------|
| Desperdício Médio | $\frac{1}{\text{#alocados}} \sum_{i: \text{alocado}} (\text{capacity}_{j_i} - \text{demand}_i)$ |
| Alunos Desalocados | $\sum_i \text{demand}_i - \text{Demanda Alocada}$ |
| Vagas Ociosas (<50%) | $\sum_{j: \text{dem}_j < 0.5 \cdot \text{cap}_j} (\text{cap}_j - \text{dem}_j)$ |
| Alunos em Pé | $\sum_{i: \text{alocado e dem}_i > \text{cap}_{j_i}} (\text{demand}_i - \text{capacity}_{j_i})$ |

---

## 9. Estratégias de Solução Implementadas

### 9.1 Heurística Gulosa (Greedy)
```
1. Ordenar encontros por demanda decrescente (Largest-First)
2. Para cada encontro i:
   a. Para cada horário k ∈ S_i:
      - Encontrar sala j com min(score_{i,j}) dentre salas viáveis
      - Se encontrou, alocar e quebrar
   b. Se nenhuma sala encontrada, encontro não alocado
3. Retornar alocação
```

**Característica**: Determinística, melhor-fit (minimiza desperdício)

### 9.2 Heurística Parcialmente Gulosa (RCL - Reduced Cost List)
```
1. Ordenar encontros por demanda decrescente
2. Para cada encontro i:
   a. Para cada horário k ∈ S_i:
      - Listar candidatos: salas j com score_{i,j} ≤ minScore + α(maxScore - minScore)
      - Se RCL vazia, usar melhor candidato
      - Selecionar aleatoriamente da RCL
      - Alocar e quebrar
   b. Se nenhuma sala encontrada, encontro não alocado
3. Retornar alocação
```

**Parâmetros**:
- $\alpha \in [0,1]$ : controla largura da RCL
  - $\alpha = 0$ : RCL = {melhor candidato} (greedy puro)
  - $\alpha = 1$ : RCL = todos os candidatos (aleatório puro)
- $\text{seed}$ : semente RNG para reprodutibilidade

---

## 10. Complexidade

### Análise de Complexidade Temporal

**Greedy**:
- Ordenar encontros: $O(m \log m)$
- Para cada encontro (m), cada horário ($\leq h$), cada sala ($c$):
  - Calcular score: $O(\text{|prefs|}) = O(p)$
  - Total: $O(m \cdot h \cdot c \cdot p)$
- **Complexidade total**: $O(m \log m + m \cdot h \cdot c \cdot p) = O(m \cdot h \cdot c \cdot p)$

**Heurística Parcial**: Mesma complexidade (RCL é construída em tempo linear)

### Espaço
- Armazenar alocações (reservações): $O(m)$
- Dados de entrada: $O(m + c + h + p)$
- **Total**: $O(m + c + h + p)$

---

## 11. Classificação do Problema

| Aspecto | Classificação |
|--------|---|
| **Tipo** | Timetabling / Scheduling / Resource Allocation |
| **Complexidade** | NP-Difícil |
| **Restrições Hard** | Capacidade, tipo de sala, compatibilidade horário-dia |
| **Restrições Soft** | Preferências de localização/equipamentos |
| **Objetivos** | Multi-objetivo: maximizar alocação + minimizar desperdício |
| **Abordagem** | Heurística Construtiva |

---

## 12. Variações e Extensões Possíveis

### 12.1 Variações Implementadas
- ✅ Encontros práticos (requerem laboratório)
- ✅ Preferências por localização/equipamento
- ✅ Múltiplos horários viáveis por encontro
- ✅ Diferentes penalidades para diferentes heurísticas

### 12.2 Extensões Propostas
- Permitir alunos em pé (relaxar restrição de capacidade)
- Considerar custos de deslocamento entre prédios
- Incluir restrições de professores (não podem ensinar simultaneamente)
- Incorporar metaheurísticas (SA, GA, NSGA-II)
- Multi-objetivo explícito (Pareto front)

---

## 13. Referências de Problemas Similares

Este problema é uma variante de:
- **University Course Timetabling Problem** (UCTP)
- **Exam Timetabling Problem** (ETP)
- **Bin Packing Problem** (minimizar desperdício)
- **Generalized Assignment Problem** (encontros → salas)

Literatura relevante:
- Schaerf, A. (1999). "A survey of automated timetabling"
- Carter, M. W., & Laporte, G. (1998). "Recent developments in practical course timetabling"
- Burke, E. K., & Petrovic, S. (2002). "Recent research directions in automated timetabling"
