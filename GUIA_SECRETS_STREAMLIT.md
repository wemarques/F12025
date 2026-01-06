```markdown
# 🚀 Guia Definitivo: Secrets para o Deploy do F12025 no Streamlit Cloud

Olá! Analisei completamente o seu repositório `wemarques/F12025` e preparei um guia detalhado sobre quais `secrets` você precisa configurar para um deploy bem-sucedido no Streamlit Cloud. 

---

### 🎯 **Análise Rápida da Arquitetura**

Seu projeto é dividido em duas partes principais:

1.  **Backend (FastAPI)**: A inteligência do projeto, responsável por otimização, simulações e acesso a dados.
2.  **Frontend (Streamlit)**: A interface do usuário que consome os dados do backend.

Para que o deploy no Streamlit Cloud funcione, o frontend precisa saber onde encontrar o backend. É exatamente para isso que servem os `secrets`.

---

### 🔑 **Secrets Essenciais: O Que Você Precisa Adicionar**

Com base na análise do seu código, identifiquei **3 secrets principais** que você deve configurar no Streamlit Cloud. Eles substituem as informações que hoje estão fixas no arquivo `config.yaml` e garantem a segurança e o funcionamento da aplicação em produção.

#### **Secret 1: URL do Backend (Obrigatório)**

Este é o secret mais importante. Ele informa ao seu app Streamlit onde o backend está rodando.

-   **Nome do Secret**: `API_BASE_URL`
-   **Valor**: A URL pública do seu backend (ex: `https://seu-backend.onrender.com` ou `https://seu-backend.railway.app`).
-   **Por que é necessário?**: Seu código em `streamlit_app/config_env.py` já está preparado para ler esta variável, garantindo que o frontend se comunique com o backend correto em produção, em vez de `http://localhost:8000`.

#### **Secret 2: Credenciais de Acesso (Recomendado)**

Atualmente, suas credenciais de login estão no arquivo `config.yaml`. Em um ambiente de produção, isso não é seguro. O ideal é movê-las para os secrets.

-   **Nome do Secret**: `credentials`
-   **Valor**: A estrutura TOML completa das suas credenciais.
-   **Por que é necessário?**: Para proteger as senhas e nomes de usuário, evitando que fiquem expostos no repositório. O `auth.py` precisará ser ajustado para ler essas credenciais dos secrets.

#### **Secret 3: Configurações do Cookie (Recomendado)**

Assim como as credenciais, as configurações do cookie de autenticação também devem ser protegidas.

-   **Nome do Secret**: `cookie`
-   **Valor**: A estrutura TOML completa das configurações do cookie.
-   **Por que é necessário?**: Para centralizar e proteger as chaves e nomes dos cookies, facilitando a rotação de chaves de segurança se necessário.

---

### 📝 **Formato TOML para o Streamlit Cloud**

No painel do Streamlit Cloud (⚙️ → Secrets), você deve inserir os secrets no formato TOML. Abaixo está o conteúdo exato que você deve copiar e colar, substituindo apenas os valores necessários.

```toml
# Secrets para o App F1 Fantasy 2025

# 1. URL do Backend (Substitua pela URL real do seu backend no Render/Railway)
API_BASE_URL = "https://seu-backend-aqui.onrender.com"

# 2. Credenciais de Usuário (Movido do config.yaml)
[credentials.usernames.admin]
email = "admin@example.com"
name = "Administrador"
password = "SUA_SENHA_FORTE_AQUI" # Substitua por uma senha segura

# 3. Configurações do Cookie de Autenticação (Movido do config.yaml)
[cookie]
expiry_days = 30 # Aumentado para 30 dias para produção
key = "UMA_CHAVE_SECRETA_MUITO_FORTE_AQUI" # Gere uma chave aleatória
name = "f1_fantasy_session"

```

### 💡 **Ajuste Sugerido no Código**

Para que os secrets de `credentials` e `cookie` funcionem, você precisará fazer um pequeno ajuste no arquivo `streamlit_app/auth.py` para que ele leia as informações de `st.secrets` em vez de carregar o `config.yaml`.

**Exemplo de como ler as credenciais em `auth.py`:**

```python
# Em vez de carregar o config.yaml
# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# Use os secrets do Streamlit
config = {
    'credentials': st.secrets['credentials'],
    'cookie': st.secrets['cookie']
}

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
```

---

### ✅ **Checklist Final**

1.  **Faça o deploy do seu backend** em uma plataforma como Render ou Railway.
2.  **Copie a URL pública** do seu backend.
3.  **Acesse o painel do seu app no Streamlit Cloud** e vá para a seção de `Secrets`.
4.  **Copie e cole o bloco TOML acima**, substituindo a `API_BASE_URL`, a `password` e a `key` do cookie por valores seguros.
5.  **(Opcional, mas recomendado)** Atualize seu `auth.py` para usar `st.secrets`.
6.  **Clique em "Save" e reinicie o deploy** do seu app.

Seguindo estes passos, sua aplicação estará configurada de forma segura e funcional no Streamlit Cloud. Se tiver qualquer dúvida, pode perguntar!
```
