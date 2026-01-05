"""
Configuração de ambiente para o Streamlit.
Suporta variáveis de ambiente, Streamlit Secrets e fallback para localhost.
"""
import os
import streamlit as st

def get_api_base_url():
    """
    Obtém a URL base da API em ordem de prioridade:
    1. Streamlit Secrets (produção no Streamlit Cloud)
    2. Variável de ambiente API_BASE_URL
    3. Fallback para localhost (desenvolvimento local)
    """
    # Tenta pegar do Streamlit Secrets (produção)
    try:
        if hasattr(st, 'secrets') and 'API_BASE_URL' in st.secrets:
            return st.secrets['API_BASE_URL']
    except Exception:
        pass
    
    # Tenta pegar da variável de ambiente
    env_url = os.getenv("API_BASE_URL")
    if env_url:
        return env_url
    
    # Fallback para localhost (desenvolvimento)
    return "http://localhost:8000"

# Exporta a URL da API
API_BASE_URL = get_api_base_url()

