# F1 2025 Prediction System

**Repositório**: [https://github.com/wemarques/F12025](https://github.com/wemarques/F12025)

Sistema completo de prognósticos para Fantasy F1, utilizando Machine Learning, dados históricos e telemetria em tempo real.

## 📋 Funcionalidades

- **Dashboard Interativo**: Interface Streamlit protegida por senha para visualização de dados.
- **Machine Learning**: Modelos de regressão (RandomForest) para prever pontuação de pilotos.
- **Integração FastF1**: Extração de dados de telemetria e tempos de volta reais.
- **Dados Históricos**: Download automatizado de datasets do Kaggle.
- **Simulador de Times**: Ferramenta para montar e validar times dentro do teto orçamentário.
- **API REST**: Backend FastAPI estruturado para servir dados e predições.

## 🏗️ Arquitetura

O projeto segue uma arquitetura modular dividida em camadas:

```text
F12025/
├── backend/            # Lógica de Negócio e API
│   ├── app/
│   │   ├── api/        # Endpoints (FastAPI)
│   │   ├── core/       # Regras de Negócio e Configurações
│   │   ├── ml/         # Pipeline de Machine Learning
│   │   └── services/   # Integrações (FastF1, Kaggle)
├── streamlit_app/      # Frontend (Streamlit)
│   ├── app.py          # Dashboard Principal
│   └── auth.py         # Módulo de Autenticação
└── data/               # Armazenamento de Dados
```

Para mais detalhes, consulte [docs/architecture.md](docs/architecture.md).

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- Conta no Kaggle (para download de datasets)

### Passo a Passo

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/wemarques/F12025.git
   cd F12025
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure as credenciais do Kaggle**:
   - Coloque seu arquivo `kaggle.json` na pasta `.kaggle` do seu usuário ou configure as variáveis de ambiente `KAGGLE_USERNAME` e `KAGGLE_KEY`.

5. **Baixe os dados iniciais**:
   ```bash
   python data/download_kaggle.py
   ```

## ▶️ Execução

### Rodar o Dashboard (Streamlit)
Este é o modo principal de uso.
```bash
streamlit run streamlit_app/app.py
```
Acesse no navegador: `http://localhost:8501`

**Credenciais Padrão**:
- **Admin**: `admin` / `password123`
- **User**: `user` / `user123`

### Rodar a API (Backend)
Para desenvolvimento ou integração via API.
```bash
cd backend
uvicorn app.main:app --reload
```
Documentação da API (Swagger): `http://localhost:8000/docs`

## 🧪 Desenvolvimento

### Regras de Negócio
As regras de pontuação (Qualifying, Sprint, Corrida, Construtores) estão implementadas em `backend/app/core/` como funções puras, facilitando testes unitários.

### Machine Learning
O pipeline de ML está em `backend/app/ml/`:
1. `clean_data.py`: Limpeza e padronização.
2. `feature_engineering.py`: Criação de variáveis preditivas.
3. `train_regressor.py`: Treinamento do modelo.
4. `predict.py`: Inferência.

## 📄 Licença

Este projeto é distribuído sob a licença MIT.
