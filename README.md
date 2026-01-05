# 🏎️ F1 Fantasy 2025 - Plataforma Avançada de Simulação e Otimização

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)

Uma plataforma completa de análise, simulação e otimização para Fantasy F1 2025, integrando dados reais do FastF1, simulação Monte Carlo avançada, e otimização de equipes baseada em estratégia.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Como Rodar](#-como-rodar)
- [Documentação da API](#-documentação-da-api)
- [Roadmap e Status](#-roadmap-e-status)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Visão Geral

O **F1 Fantasy 2025** é uma aplicação full-stack desenvolvida para auxiliar entusiastas de Formula 1 Fantasy a tomar decisões estratégicas baseadas em dados. A plataforma combina:

- **Análise de Dados Reais**: Integração com FastF1 para acesso a telemetria e dados históricos
- **Simulação Monte Carlo**: Motor de simulação avançado com modelagem de clima, pneus e estratégias
- **Otimização de Equipes**: Algoritmo de otimização que maximiza pontos esperados respeitando orçamento e regras
- **Visualizações Interativas**: Dashboards e gráficos Race Trace para análise visual
- **Interface Moderna**: Frontend Streamlit intuitivo e responsivo

---

## ✨ Funcionalidades Principais

### 🔮 Simulador Monte Carlo (Fase 2.0 - 2.3)

Simulação avançada de corridas usando dados reais do FastF1:

- **Integração com FastF1**: Carrega dados reais de sessões (Race/Qualifying) para cada GP
- **Modelagem Realista**: 
  - Sistema de pneus (SOFT, MEDIUM, HARD, INTER, WET)
  - Degradação de pneus e estratégias de pit stop
  - Impacto climático (DRY, MIXED, WET)
  - Variação de performance baseada em consistência
- **Simulação Monte Carlo**: Executa centenas de iterações para calcular probabilidades
- **Métricas de Saída**:
  - Probabilidade de vitória por piloto
  - Posição média esperada
  - Pontos de Fantasy F1 projetados
- **Visualização Race Trace**: Gráfico interativo mostrando evolução das posições volta a volta

### 🏗️ Team Builder e Otimizador (Fase 1.5, Fase 3)

Construção e otimização de equipes seguindo regras oficiais do F1 Fantasy:

- **Regras Oficiais 2025**:
  - Orçamento máximo: $100M
  - 5 pilotos obrigatórios
  - 2 construtores obrigatórios
  - Máximo 3 pilotos da mesma equipe
- **Otimização Automática**:
  - Algoritmo de força bruta otimizado usando `itertools.combinations`
  - Maximiza pontos esperados respeitando todas as regras
  - Integração com resultados de simulação (Fase 3)
- **Interface Interativa**:
  - Seleção visual de pilotos e construtores
  - Validação em tempo real
  - Sugestão automática de melhor time
  - Indicadores visuais de orçamento e conformidade

### 📊 Analytics e Telemetria

Análise comparativa de performance:

- **Comparativo Head-to-Head**: Compara telemetria de dois pilotos
- **Visualização de Velocidade**: Gráficos de velocidade vs distância
- **Análise de Voltas Rápidas**: Extração e comparação de melhores voltas

### 🌧️ Sistema de Clima (Fase 4)

Simulação de condições climáticas variáveis:

- **Condições Climáticas**: DRY (seco), MIXED (misto), WET (molhado)
- **Impacto na Performance**:
  - Chuva: Aumenta tempo de volta em 15-20%
  - Condições mistas: Alta variabilidade simulando Safety Car
- **Configuração via UI**: Slider para definir probabilidade de chuva (0-100%)

### 🛞 Sistema de Pneus (Fase 5)

Modelagem completa de estratégias de pneus:

- **Compostos Disponíveis**: SOFT, MEDIUM, HARD, INTER, WET
- **Características por Composto**:
  - Bônus de velocidade (SOFT mais rápido)
  - Taxa de degradação
  - Durabilidade máxima
- **Estratégia Automática**:
  - Decisão inteligente de pit stops baseada em custo-benefício
  - Respeita regra de 2 compostos diferentes por corrida
  - Escolha de composto baseada em clima e voltas restantes

### 📈 Race Trace Visualization (Fase 6)

Visualização avançada da evolução da corrida:

- **Gráfico Interativo**: Evolução das posições volta a volta
- **Cores Oficiais**: Linhas coloridas conforme equipe
- **Iteração Representativa**: Mostra a simulação mais próxima do resultado médio
- **Tooltips Informativos**: Informações detalhadas ao passar o mouse

---

## 🏗️ Arquitetura

### Backend (FastAPI)

```
backend/
├── app/
│   ├── api/endpoints/        # Endpoints REST
│   │   ├── analytics.py      # Comparativo de telemetria
│   │   ├── fantasy.py        # Otimização de equipes
│   │   ├── simulation.py     # Simulação Monte Carlo
│   │   └── optimization.py   # Otimização alternativa
│   ├── simulation/           # Motor de simulação
│   │   ├── engine.py         # Lógica principal de simulação
│   │   ├── models.py         # DriverSim, RaceResult
│   │   ├── tyres.py          # Sistema de pneus
│   │   └── weather.py        # Sistema climático
│   ├── services/             # Serviços de negócio
│   │   ├── fastf1_adapter.py # Integração FastF1
│   │   ├── fantasy_optimizer.py # Algoritmo de otimização
│   │   ├── race_setup.py     # Configuração de corrida
│   │   └── fantasy_rules.py  # Validação de regras
│   └── data/                 # Dados mock
│       └── f1_prices.json    # Preços e pontos esperados
└── main.py                   # Aplicação FastAPI
```

### Frontend (Streamlit)

```
streamlit_app/
├── app.py                    # Aplicação principal
├── components/
│   ├── charts.py            # Visualizações (Plotly)
│   └── team_builder.py      # Interface Team Builder
└── config.yaml              # Configuração de autenticação
```

---

## 🛠️ Instalação

### Pré-requisitos

- **Python 3.9 ou superior**
- **Conexão com internet** (para baixar dados do FastF1 na primeira execução)
- **Git** (para clonar o repositório)

### Passo a Passo

1. **Clone o repositório:**

```bash
git clone <url-do-repositorio>
cd F12025
```

2. **Crie um ambiente virtual (recomendado):**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure o cache do FastF1 (opcional):**

O sistema criará automaticamente o diretório `backend/cache` na primeira execução para armazenar dados do FastF1 localmente.

---

## 🚀 Como Rodar

### Opção 1: Script Automático (Recomendado)

Para facilitar, incluímos scripts que iniciam tanto o Backend (API) quanto o Frontend (Dashboard) simultaneamente.

**No Windows:**
```bash
# Duplo clique no arquivo ou execute:
run_app.bat
```

**No Linux/Mac:**
```bash
chmod +x run_app.sh
./run_app.sh
```

### Opção 2: Manual

**Terminal 1 - Backend (API):**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend (Dashboard):**
```bash
cd streamlit_app
streamlit run app.py
```

### Acessos

- **Frontend (Dashboard)**: http://localhost:8501
- **Backend API (Docs)**: http://localhost:8000/docs
- **Backend API (Health)**: http://localhost:8000/health

---

## 📚 Documentação da API

A documentação interativa da API está disponível em http://localhost:8000/docs (Swagger UI).

### Principais Endpoints

#### Simulação

- `POST /api/v1/simulation/run/{year}/{gp}`
  - Executa simulação Monte Carlo
  - Parâmetros: `year`, `gp`, `iterations`, `rain_probability`
  - Retorna: Probabilidades, posições médias, pontos esperados, race trace

#### Otimização de Equipes

- `POST /api/v1/fantasy/optimize`
  - Otimiza equipe baseado em pontos esperados
  - Body: `budget`, `custom_points_projections` (opcional)
  - Retorna: Melhor combinação de pilotos e construtores

#### Analytics

- `GET /api/v1/analytics/compare-laps`
  - Compara telemetria de dois pilotos
  - Parâmetros: `year`, `gp`, `session_type`, `driver1`, `driver2`
  - Retorna: Dados de velocidade e distância

---

## 🗺️ Roadmap e Status

O projeto encontra-se em **estágio MVP Completo**. Todas as fases principais foram implementadas:

### ✅ Fases Concluídas

- [x] **Fase 1**: Coleta de Dados e Cache (FastF1)
  - Integração com FastF1 API
  - Sistema de cache local persistente
  - Tratamento robusto de erros

- [x] **Fase 1.5**: Team Builder e Regras Oficiais
  - Interface visual de construção de equipes
  - Validação de regras ($100M, 5 Drivers, 2 Constructors, max 3 por equipe)
  - Mock data completo (20 pilotos, 10 construtores)

- [x] **Fase 2.0**: Motor de Simulação Monte Carlo (Core)
  - Modelos `DriverSim` e `RaceResult`
  - Função `simulate_race` com geração de tempos de volta
  - Degradação de pneus e pit stops básicos

- [x] **Fase 2.1**: Refinamento da Simulação
  - Adição de `pit_stop_loss` individual por piloto
  - Rastreamento de voltas completadas
  - Lógica aprimorada de pit stops

- [x] **Fase 2.2**: Integração com Dados Reais
  - Serviço `race_setup.py` para carregar dados do FastF1
  - Cálculo de `base_lap_time` e `consistency` a partir de dados reais
  - Endpoint `/api/v1/simulation/run/{year}/{gp}` funcional

- [x] **Fase 2.3**: Interface Frontend
  - Aba "🔮 Simulador Monte Carlo" no Streamlit
  - Seleção de ano, GP e iterações
  - Visualização de resultados (tabela e gráfico)

- [x] **Fase 3**: Integração Simulador → Otimizador
  - Sistema de pontuação F1 integrado ao motor
  - `average_fantasy_points` nos resultados
  - Otimizador aceita `custom_points_projections`
  - Frontend integra resultados de simulação ao otimizador

- [x] **Fase 4**: Variáveis de Clima
  - Módulo `weather.py` com `WeatherCondition` (DRY, MIXED, WET)
  - `WeatherEngine` aplicando impacto climático
  - Parâmetro `rain_probability` no simulador
  - Indicador visual de condição simulada

- [x] **Fase 5**: Estratégia de Pneus e Pit Stops
  - Módulo `tyres.py` com 5 compostos
  - Modelagem de degradação por composto
  - Decisão inteligente de pit stops
  - Escolha de composto baseada em clima e estratégia

- [x] **Fase 6**: Visualização Avançada (Race Trace)
  - Rastreamento de posições a cada volta
  - `lap_history` e `position_history` em `RaceResult`
  - Função `render_lap_chart()` com Plotly
  - Exibição da iteração mais representativa

### 🔮 Próximas Fases (Futuro)

- [ ] **Fase 7**: Modelagem de Safety Car / VSC
- [ ] **Fase 8**: Machine Learning para Previsão de Performance
- [ ] **Fase 9**: Sistema de Usuários e Histórico de Equipes
- [ ] **Fase 10**: Comparação de Estratégias (Multi-Strategy Analysis)

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido para APIs
- **FastF1**: Biblioteca para acesso a dados oficiais da F1
- **Pydantic**: Validação de dados e models
- **NumPy / Pandas**: Processamento de dados

### Frontend
- **Streamlit**: Framework para criação de dashboards interativos
- **Plotly**: Visualizações interativas avançadas
- **Requests**: Comunicação HTTP com backend

### Simulação e Otimização
- **itertools**: Geração de combinações para otimização
- **random**: Simulação estocástica (Monte Carlo)
- **dataclasses**: Modelos de dados Python

---

## 📁 Estrutura do Projeto

```
F12025/
├── backend/                  # Backend FastAPI
│   ├── app/
│   │   ├── api/endpoints/    # Endpoints REST
│   │   ├── simulation/       # Motor de simulação
│   │   ├── services/         # Serviços de negócio
│   │   └── data/             # Dados mock
│   ├── cache/                # Cache FastF1 (criado automaticamente)
│   └── requirements.txt
├── streamlit_app/            # Frontend Streamlit
│   ├── app.py
│   ├── components/
│   └── config.yaml
├── docs/                     # Documentação adicional
├── run_app.bat              # Script de inicialização (Windows)
├── start_backend.bat        # Script backend apenas
└── README.md                # Este arquivo
```

---

## 📸 Screenshots

### 1. Simulador Monte Carlo & Race Trace

Visualização completa dos resultados da simulação, incluindo:
- Gráfico de barras horizontal com probabilidades de vitória
- Race Trace mostrando evolução das posições volta a volta
- Tabela detalhada com métricas de cada piloto

![Race Trace Visualization](docs/screenshots/race_trace.png)

### 2. Otimizador de Equipes

Interface interativa para construção e otimização de equipes:
- Seleção visual de pilotos e construtores
- Validação em tempo real das regras
- Sugestão automática do melhor time

![Team Builder Optimizer](docs/screenshots/team_builder.png)

### 3. Comparativo Head-to-Head

Análise comparativa de telemetria entre dois pilotos:
- Gráfico de velocidade vs distância
- Comparação de melhores voltas
- Visualização interativa com Plotly

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autores

Desenvolvido com 🏁 e 🐍 por entusiastas de Formula 1.

---

## 🙏 Agradecimentos

- **FastF1** pela excelente biblioteca de acesso a dados da F1
- **Formula 1** pelos dados oficiais
- Comunidade de Fantasy F1 pela inspiração e feedback

---

## 📞 Contato

Para questões, sugestões ou problemas, abra uma [Issue](../../issues) no repositório.

---

**Made with 🏁 and 🐍**
