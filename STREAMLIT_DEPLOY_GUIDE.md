# 🚀 Guia: Deploy no Streamlit Cloud

Este guia explica passo a passo como fazer o deploy da aplicação F1 Fantasy 2025 no Streamlit Cloud.

---

## 📋 Pré-requisitos

1. **Conta no GitHub**: Seu código já está em https://github.com/wemarques/F12025 ✅
2. **Conta no Streamlit Cloud**: Crie em https://share.streamlit.io/ (grátis)
3. **Repositório público no GitHub**: O Streamlit Cloud precisa de acesso ao código

---

## ⚠️ Considerações Importantes

### Arquitetura Atual

Sua aplicação tem **duas partes**:
1. **Backend FastAPI** (roda em `localhost:8000`)
2. **Frontend Streamlit** (roda em `localhost:8501`)

O Streamlit Cloud **só hospeda o frontend**. Você tem 3 opções:

### Opção 1: Deploy Completo (Backend + Frontend) ⭐ Recomendado
- **Backend**: Deploy em [Railway](https://railway.app/), [Render](https://render.com/), ou [Fly.io](https://fly.io/)
- **Frontend**: Deploy no Streamlit Cloud
- **Vantagem**: Aplicação completa funcionando

### Opção 2: Apenas Frontend (Modo Standalone)
- Deploy apenas do Streamlit no Streamlit Cloud
- Remover dependências do backend ou criar versão simplificada
- **Limitação**: Funcionalidades que dependem do backend não funcionarão

### Opção 3: Tudo em Streamlit (Refatoração)
- Mover lógica do backend para dentro do Streamlit
- Usar `st.cache_data` e `st.cache_resource` para performance
- **Vantagem**: Um único deploy, sem backend separado

---

## 🎯 Opção 1: Deploy Completo (Recomendado)

### Passo 1: Deploy do Backend

#### 1.1. Escolha uma Plataforma (exemplo: Render)

1. Acesse https://render.com/ e faça login com GitHub
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório `wemarques/F12025`
4. Configure:
   - **Name**: `f1-fantasy-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Adicione variáveis de ambiente se necessário
6. Clique em **"Create Web Service"**
7. Aguarde o deploy (5-10 minutos)
8. **Copie a URL do backend** (ex: `https://f1-fantasy-backend.onrender.com`)

#### 1.2. Outras Opções de Backend

**Railway** (mais simples):
- Acesse https://railway.app/
- Conecte o repositório
- Configure: Root Directory = `backend`, Start Command = `uvicorn app.main:app`

**Fly.io** (mais controle):
- Requer `fly.toml` configurado
- Melhor para apps mais complexos

### Passo 2: Configurar Frontend para Usar Backend Remoto

Você precisa atualizar o código do Streamlit para usar a URL do backend em produção:

#### 2.1. Criar arquivo de configuração de ambiente

Crie `streamlit_app/config_env.py`:

```python
import os

# URL do backend - usar variável de ambiente em produção
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
```

#### 2.2. Atualizar componentes que usam API

No `streamlit_app/components/team_builder.py` e outros arquivos, substitua:
- `API_BASE_URL = "http://localhost:8000"` 
- Por: `from config_env import API_BASE_URL`

### Passo 3: Deploy no Streamlit Cloud

#### 3.1. Preparar arquivos necessários

**Criar `packages.txt` (se necessário)**:
Se você precisa de pacotes do sistema, crie na raiz:
```
packages.txt
```

**Verificar `requirements.txt` na raiz**:
Certifique-se de que contém todas as dependências do Streamlit:
```
streamlit
plotly
pandas
numpy
requests
pyyaml
fastf1
```

#### 3.2. Deploy no Streamlit Cloud

1. Acesse https://share.streamlit.io/
2. Faça login com sua conta GitHub
3. Clique em **"New app"**
4. Configure:
   - **Repository**: `wemarques/F12025`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app/app.py`
   - **App URL** (opcional): Escolha um nome customizado
5. **Adicione Secrets** (⚙️ → Secrets):
   ```toml
   API_BASE_URL = "https://seu-backend.onrender.com"
   ```
   (Substitua pela URL do seu backend deployado)
6. Clique em **"Deploy"**
7. Aguarde o build (2-5 minutos)

#### 3.3. Atualizar código para usar Secrets

No `streamlit_app/config_env.py`:

```python
import os
import streamlit as st

# Tenta pegar do secrets do Streamlit Cloud, senão usa variável de ambiente, senão localhost
if hasattr(st, 'secrets') and 'API_BASE_URL' in st.secrets:
    API_BASE_URL = st.secrets['API_BASE_URL']
elif os.getenv("API_BASE_URL"):
    API_BASE_URL = os.getenv("API_BASE_URL")
else:
    API_BASE_URL = "http://localhost:8000"
```

---

## 🎯 Opção 2: Deploy Standalone (Sem Backend)

Se você quer apenas visualizar o frontend sem backend:

1. Crie uma branch `streamlit-only` ou modifique o código para funcionar sem backend
2. Remova/comente chamadas à API
3. Use dados mockados ou carregue dados estáticos
4. Faça deploy normalmente no Streamlit Cloud

**Limitações**: 
- Simulador Monte Carlo não funcionará
- Otimizador de times não funcionará
- Comparativo de telemetria não funcionará

---

## 🔧 Configurações Adicionais

### Arquivo `.streamlit/config.toml` (Opcional)

Crie `streamlit_app/.streamlit/config.toml`:

```toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

### Arquivo `Procfile` (para Render/Railway)

Se usar Render ou Railway para o backend, pode ser necessário criar `backend/Procfile`:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 📝 Checklist de Deploy

### Antes do Deploy

- [ ] Código commitado e pushed para GitHub
- [ ] `requirements.txt` na raiz com todas as dependências
- [ ] Backend deployado (se usar Opção 1)
- [ ] URL do backend anotada
- [ ] Secrets configurados no Streamlit Cloud
- [ ] Código atualizado para usar variáveis de ambiente

### Durante o Deploy

- [ ] Streamlit Cloud conectado ao repositório correto
- [ ] Main file path correto: `streamlit_app/app.py`
- [ ] Secrets adicionados
- [ ] Build sem erros

### Após o Deploy

- [ ] App acessível e carregando
- [ ] Testar login/autenticação
- [ ] Testar funcionalidades que dependem do backend
- [ ] Verificar logs em caso de erros

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"

**Solução**: Verifique se todas as dependências estão em `requirements.txt` na raiz do projeto.

### Erro: "Connection refused" ao chamar API

**Solução**: 
1. Verifique se o backend está deployado e rodando
2. Confirme que a URL no Secrets está correta
3. Verifique CORS no backend (adicionar `CORSMiddleware` no FastAPI)

### Erro: "FileNotFoundError: config.yaml"

**Solução**: O arquivo `config.yaml` precisa estar no repositório. Se contém dados sensíveis, use Streamlit Secrets.

### Backend muito lento no Render/Railway

**Solução**: 
- Render/Railway free tier pode ter cold starts
- Considere upgrade para plano pago ou usar Fly.io
- Adicione health checks para manter o serviço "warm"

### CORS Error

No backend (`backend/app/main.py`), adicione:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique o domínio do Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📚 Recursos Adicionais

- [Documentação Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Secrets](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Deploy FastAPI no Render](https://render.com/docs/deploy-fastapi)
- [Deploy FastAPI no Railway](https://docs.railway.app/getting-started)

---

## 🎉 Próximos Passos

Após o deploy bem-sucedido:

1. Compartilhe o link da aplicação
2. Configure domínio customizado (se desejar)
3. Monitore logs e performance
4. Configure alertas (se necessário)

---

**Boa sorte com o deploy! 🚀**

