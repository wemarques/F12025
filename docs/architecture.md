# Arquitetura do Sistema F1 2025

**Repositório Oficial**: [https://github.com/wemarques/F12025](https://github.com/wemarques/F12025)

## 1. Visão Geral

O **F1 2025 Prediction System** é uma aplicação modular projetada para auxiliar jogadores de Fantasy F1 com prognósticos baseados em dados. O sistema integra dados históricos (Kaggle) e telemetria em tempo real (FastF1) para alimentar modelos de Machine Learning e regras de pontuação complexas.

## 2. Stack Tecnológico

- **Linguagem**: Python 3.8+
- **Backend API**: FastAPI + Uvicorn
- **Frontend**: Streamlit
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Dados Externos**: FastF1 API, Kaggle API
- **Persistência**: Arquivos locais (CSV/Parquet), Joblib (Modelos), YAML (Configurações)

## 3. Estrutura de Diretórios

```text
F12025/
├── backend/                  # Núcleo da aplicação
│   ├── app/
│   │   ├── api/              # Endpoints REST (Routers)
│   │   │   ├── pilotos.py
│   │   │   ├── corridas.py
│   │   │   └── prognosticos.py
│   │   ├── core/             # Regras de Negócio (Pure Functions)
│   │   │   ├── config.py
│   │   │   ├── regras_qualifying.py
│   │   │   ├── regras_sprint.py
│   │   │   ├── regras_corrida.py
│   │   │   ├── regras_construtores.py
│   │   │   ├── curingas.py
│   │   │   └── transferencias.py
│   │   ├── ml/               # Pipeline de Machine Learning
│   │   │   ├── clean_data.py
│   │   │   ├── feature_engineering.py
│   │   │   ├── encode_scale.py
│   │   │   ├── train_regressor.py
│   │   │   └── predict.py
│   │   └── services/         # Integrações e Serviços de Dados
│   │       ├── fastf1_extractor.py
│   │       ├── kaggle_downloader.py
│   │       ├── pilotos_service.py
│   │       └── corridas_service.py
│   ├── requirements.txt
│   └── main.py               # Entrypoint da API
├── streamlit_app/            # Interface do Usuário
│   ├── app.py                # Dashboard Principal
│   ├── auth.py               # Lógica de Login
│   └── config.yaml           # Credenciais e Configurações de UI
├── data/                     # Data Lake Local
│   ├── raw/                  # Dados brutos (Kaggle .csv, FastF1 Cache)
│   ├── processed/            # Dados limpos e features geradas
│   └── external/             # Dados complementares
└── docs/                     # Documentação
```

## 4. Componentes do Backend

### 4.1. Camada de Regras de Negócio (`app.core`)
Implementa a lógica do Fantasy F1 de forma isolada, facilitando testes e ajustes sem impactar o resto do sistema.
- **Pontuação**: Módulos específicos para Qualifying, Sprint e Corrida Principal.
- **Gerenciamento de Time**: Regras para transferências, penalidades e teto orçamentário.
- **Curingas (Chips)**: Lógica para Chips como Wildcard, Limitless, Autopilot, etc.

### 4.2. Pipeline de Machine Learning (`app.ml`)
O fluxo de ML é linear e reprodutível:
1.  **Limpeza (`clean_data`)**: Tratamento de nulos (`\N`), conversão de tipos e remoção de duplicatas.
2.  **Engenharia de Features (`feature_engineering`)**: Criação de variáveis preditivas (ex: ganho de posições, performance em qualificação).
3.  **Pré-processamento (`encode_scale`)**: Pipeline `ColumnTransformer` com `StandardScaler` (numéricos) e `OneHotEncoder` (categóricos).
4.  **Modelo (`train_regressor`)**: `RandomForestRegressor` treinado e persistido via `joblib`.
5.  **Inferência (`predict`)**: Carregamento do pipeline salvo para gerar prognósticos em tempo real.

### 4.3. Serviços de Dados (`app.services`)
- **FastF1**: Abstração para carregar sessões com cache automático.
- **Kaggle**: Script de download automático do dataset histórico.
- **Mock Services**: Serviços de pilotos e corridas para fornecer dados estruturados à API/Frontend.

## 5. Arquitetura do Frontend (Streamlit)

O frontend é construído como uma aplicação *Single Page App* (SPA) com navegação via Sidebar.

- **Autenticação**:
    - Sistema baseado em `session_state`.
    - Credenciais armazenadas em `config.yaml`.
    - Bloqueia renderização do conteúdo principal até o login.
- **Módulos**:
    - **Dashboard**: Visão macro da temporada.
    - **Prognósticos**: Interface para input de parâmetros e chamada ao modelo de ML.
    - **Simulador**: Ferramenta interativa para seleção de pilotos e validação de orçamento.

## 6. Fluxo de Dados

1.  **Ingestão**: `kaggle_downloader.py` baixa dados históricos -> `data/raw`.
2.  **Treinamento**: `train_regressor.py` lê `data/raw`, processa e salva `model.pkl`.
3.  **Consumo**:
    - O Usuário acessa o Streamlit.
    - Solicita uma previsão.
    - O Streamlit (ou API) carrega `model.pkl`.
    - O modelo retorna a pontuação prevista.
    - O resultado é exibido no Dashboard.
