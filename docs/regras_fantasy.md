# Regras de Pontuação e Mecânicas - Fantasy F1 2025

Este documento detalha as regras implementadas no backend (`backend/app/core/`) para cálculo de pontuação e gerenciamento de times.

## 1. Pilotos

### 1.1. Qualifying (Classificação)
| Critério | Pontos | Detalhes |
| :--- | :---: | :--- |
| **Posição (Top 10)** | 10 a 1 | 1º=10, 2º=9, ..., 10º=1 |
| **Superar Companheiro** | +2 | Se terminar à frente do teammate |
| **Chegar ao Q3** | +1 | Bônus por performance |
| **Não Classificado** | -5 | Desclassificação (DSQ) ou sem tempo |

### 1.2. Corrida (Feature Race)
| Critério | Pontos | Detalhes |
| :--- | :---: | :--- |
| **Posição (Top 10)** | 25 a 1 | Padrão FIA (25, 18, 15, 12, 10, 8, 6, 4, 2, 1) |
| **Ultrapassagens** | +/- 1 | Pontos por posição ganha/perdida (Grid vs Chegada) |
| **Volta Mais Rápida** | +5 | Bônus (maior que a F1 real) |
| **Piloto do Dia (DOTD)** | +5 | Votação oficial |
| **Superar Companheiro** | +3 | Se terminar à frente |
| **Terminar a Corrida** | +1 | Classificado (mesmo com voltas a menos) |
| **DNF** | -10 | Did Not Finish |
| **DSQ** | -20 | Disqualified |

### 1.3. Sprint
| Critério | Pontos | Detalhes |
| :--- | :---: | :--- |
| **Posição (Top 8)** | 8 a 1 | Padrão FIA (8, 7, 6, 5, 4, 3, 2, 1) |
| **Ultrapassagens** | +/- 1 | Diferença Grid vs Chegada |
| **DNF** | -5 | Did Not Finish na Sprint |
| **Volta Mais Rápida** | +1 | Bônus pequeno (se aplicável) |

---

## 2. Construtores

A pontuação base é a **soma dos pontos dos dois pilotos**. Adicionalmente:

| Critério | Pontos | Detalhes |
| :--- | :---: | :--- |
| **Pit Stop Mais Rápido** | +10 / +5 / +3 | Para os 3 tempos mais rápidos da corrida |
| **Pódio Duplo** | +10 | Ambos pilotos no Top 3 |
| **Q3 Duplo** | +5 | Ambos pilotos no Q3 |
| **DNF Duplo** | -10 | Ambos não terminam a corrida |

---

## 3. Curingas (Chips)

Apenas um chip pode ser usado por rodada (exceto Wildcard/Limitless que afetam transferências).

- **Autopilot**: Atribui automaticamente o DRS (bônus 2x) ao piloto com maior pontuação no time.
- **Extra DRS**: Triplica (3x) a pontuação de um piloto selecionado (substitui o 2x padrão).
- **No Negative**: Se a pontuação total (ou de uma categoria) for negativa, ela é zerada.
- **Wildcard**: Transferências ilimitadas gratuitas na rodada ativa.
- **Limitless**: Orçamento infinito e transferências ilimitadas para montar o "Dream Team" apenas naquela rodada.
- **Final Fix**: Permite 1 substituição entre o Qualifying e a Corrida (mantendo pontos já ganhos, regra dependente da liga).

---

## 4. Transferências e Orçamento

- **Orçamento (Budget Cap)**: Limite de $100M (valor inicial, flutua com o mercado).
- **Transferências Gratuitas**:
    - **2 por semana** (padrão).
    - Pode acumular 1 transferência não usada para a próxima semana (máximo de 3 disponíveis).
- **Penalidade**: **-10 pontos** por cada transferência extra além do limite gratuito.

---

## Referência de Código

As implementações dessas regras encontram-se em:
- `backend/app/core/regras_qualifying.py`
- `backend/app/core/regras_corrida.py`
- `backend/app/core/regras_sprint.py`
- `backend/app/core/regras_construtores.py`
- `backend/app/core/curingas.py`
- `backend/app/core/transferencias.py`
