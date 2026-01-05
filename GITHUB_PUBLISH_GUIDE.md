# 📤 Guia: Como Publicar no GitHub

Este guia explica passo a passo como publicar seu projeto F1 Fantasy 2025 no GitHub.

## Pré-requisitos

1. **Conta no GitHub**: Crie uma conta em [github.com](https://github.com) se ainda não tiver
2. **Git instalado**: Verifique se o Git está instalado:
   ```bash
   git --version
   ```
   Se não estiver, baixe em: https://git-scm.com/downloads

---

## 📝 Passo a Passo

### 1. Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito → **"New repository"**
3. Preencha:
   - **Repository name**: `f1-fantasy-2025` (ou outro nome de sua escolha)
   - **Description**: "Plataforma avançada de simulação e otimização para Fantasy F1 2025"
   - **Visibility**: Escolha **Public** ou **Private**
   - **NÃO marque** "Initialize this repository with a README" (já temos um)
4. Clique em **"Create repository"**

### 2. Inicializar Git no Projeto (se ainda não estiver inicializado)

Abra o terminal/PowerShell na pasta do projeto:

```bash
cd C:\F1\setup\f1_race_traces_2021\F12025

# Verificar se já é um repositório Git
git status
```

**Se aparecer erro "not a git repository":**

```bash
# Inicializar repositório Git
git init
```

### 3. Configurar Git (primeira vez apenas)

Se for a primeira vez usando Git no seu computador:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

### 4. Adicionar Arquivos ao Git

```bash
# Adicionar todos os arquivos (exceto os ignorados pelo .gitignore)
git add .

# Verificar o que será commitado
git status
```

### 5. Fazer o Primeiro Commit

```bash
git commit -m "Initial commit: F1 Fantasy 2025 - Plataforma completa de simulação e otimização"
```

### 6. Conectar com o Repositório GitHub

No GitHub, após criar o repositório, você verá instruções. Use a opção **"push an existing repository"**:

```bash
# Substitua 'SEU_USUARIO' pelo seu nome de usuário do GitHub
# Substitua 'f1-fantasy-2025' pelo nome do repositório que você criou

git remote add origin https://github.com/SEU_USUARIO/f1-fantasy-2025.git

# Verificar se foi adicionado corretamente
git remote -v
```

### 7. Enviar Código para o GitHub

```bash
# Renomear branch principal para 'main' (se necessário)
git branch -M main

# Enviar código para o GitHub
git push -u origin main
```

**Nota**: Se pedir autenticação:
- **GitHub não aceita mais senha** via HTTPS
- Use **Personal Access Token** ou configure **SSH**

---

## 🔐 Autenticação no GitHub

### Opção 1: Personal Access Token (Recomendado para HTTPS)

1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Dê um nome (ex: "F1 Fantasy Project")
4. Selecione escopos: **`repo`** (acesso completo aos repositórios)
5. Clique em **"Generate token"**
6. **COPIE O TOKEN** (você só verá uma vez!)
7. Ao fazer `git push`, use o token como senha (nome de usuário = seu usuário GitHub)

### Opção 2: SSH (Mais Seguro)

1. **Gerar chave SSH**:
   ```bash
   ssh-keygen -t ed25519 -C "seu.email@example.com"
   ```
   (Pressione Enter para aceitar local padrão e senha vazia se preferir)

2. **Copiar chave pública**:
   ```bash
   # Windows PowerShell
   cat ~/.ssh/id_ed25519.pub
   
   # Ou copie manualmente de: C:\Users\SeuUsuario\.ssh\id_ed25519.pub
   ```

3. **Adicionar no GitHub**:
   - Acesse: https://github.com/settings/keys
   - Clique em **"New SSH key"**
   - Cole a chave pública
   - Salve

4. **Usar SSH no lugar de HTTPS**:
   ```bash
   git remote set-url origin git@github.com:SEU_USUARIO/f1-fantasy-2025.git
   git push -u origin main
   ```

---

## 📋 Comandos Úteis (Depois da Publicação)

### Atualizar o Repositório

Quando fizer mudanças no código:

```bash
# Verificar status
git status

# Adicionar arquivos alterados
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push
```

### Ver Histórico

```bash
git log --oneline
```

### Criar Branch para Nova Feature

```bash
git checkout -b feature/nova-funcionalidade
# Faça suas alterações
git add .
git commit -m "Adiciona nova funcionalidade"
git push -u origin feature/nova-funcionalidade
```

---

## ⚠️ Arquivos Importantes a Verificar

Antes de fazer o commit, verifique se o `.gitignore` está configurado corretamente para **não** enviar:

- ❌ Arquivos de cache (`__pycache__/`, `backend/cache/`)
- ❌ Dados sensíveis (`.env`, senhas)
- ❌ Arquivos temporários
- ❌ Database local (`.db`, `.sqlite`)

---

## 🎯 Resumo Rápido

```bash
# 1. Criar repositório no GitHub (via site)

# 2. No terminal do projeto:
git init  # (se necessário)
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/SEU_USUARIO/f1-fantasy-2025.git
git branch -M main
git push -u origin main
```

---

## 🆘 Problemas Comuns

### Erro: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/f1-fantasy-2025.git
```

### Erro: "Authentication failed"
- Use Personal Access Token ao invés de senha
- Ou configure SSH

### Erro: "refusing to merge unrelated histories"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Esqueceu de adicionar arquivo no commit
```bash
git add arquivo_esquecido.py
git commit --amend --no-edit  # Adiciona ao último commit
git push --force  # Cuidado: só use se você tiver certeza!
```

---

## 📚 Recursos Adicionais

- [Documentação oficial do Git](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Boa sorte publicando seu projeto! 🚀**


