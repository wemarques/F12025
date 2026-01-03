# F1 2025 Backend

Este diretório contém o backend da aplicação F1 2025.

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

Para rodar a API (se aplicável):
```bash
uvicorn app.main:app --reload
```

## Estrutura

- `app/api`: Endpoints da API.
- `app/ml`: Módulos de Machine Learning.
- `app/core`: Configurações e utilitários centrais.
- `app/services`: Lógica de negócio e integrações (FastF1).
