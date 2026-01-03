import streamlit as st
import sys
import os
import pandas as pd
import numpy as np

# Adiciona o diretório raiz ao path para importar módulos do backend se necessário
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))

from streamlit_app.auth import Authenticator

# Configuração da Página
st.set_page_config(page_title="F1 2025 Fantasy Projections", layout="wide", page_icon="🏎️")

# --- Autenticação ---
auth = Authenticator(os.path.join(os.path.dirname(__file__), 'config.yaml'))

if not auth.login():
    st.stop()

# Sidebar - Informações do Usuário e Logout
with st.sidebar:
    st.write(f"Bem-vindo, **{st.session_state['name']}**!")
    auth.logout()
    st.divider()

# --- Navegação ---
page = st.sidebar.radio("Navegação", ["Dashboard", "Prognóstico por Piloto", "Simulação de Time"])

# --- Páginas ---

if page == "Dashboard":
    st.title("🏎️ Dashboard F1 2025")
    st.markdown("### Visão Geral da Temporada")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Próxima Corrida", "Australian GP", "16 Mar")
    col2.metric("Líder do Campeonato", "Max Verstappen", "25 pts")
    col3.metric("Construtor Líder", "Red Bull Racing", "40 pts")
    
    st.subheader("Tendências de Pontuação")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Verstappen', 'Norris', 'Hamilton']
    )
    st.line_chart(chart_data)

elif page == "Prognóstico por Piloto":
    st.title("🔮 Prognóstico de Performance")
    st.markdown("Estime a pontuação de um piloto para a próxima corrida.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        driver = st.selectbox("Selecione o Piloto", 
                            ["Max Verstappen", "Lando Norris", "Lewis Hamilton", "Charles Leclerc", "Oscar Piastri", "George Russell"])
        constructor = st.selectbox("Equipe", ["Red Bull Racing", "McLaren", "Ferrari", "Mercedes"])
        
    with col2:
        track = st.selectbox("Pista / GP", ["Bahrain", "Saudi Arabia", "Australia", "Japan"])
        grid_pos = st.slider("Posição de Largada Estimada", 1, 20, 1)
    
    if st.button("Gerar Prognóstico", type="primary"):
        with st.spinner('Calculando probabilidades com Machine Learning...'):
            # Simulação de chamada ao backend
            import time
            time.sleep(1) 
            predicted_points = np.random.randint(15, 30)
            confidence = np.random.randint(70, 95)
            
        st.success(f"Prognóstico gerado com sucesso!")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Pontos Previstos", f"{predicted_points} pts")
        res_col2.metric("Confiança do Modelo", f"{confidence}%")
        res_col3.metric("Variação Esperada", "±2.5 pts")

elif page == "Simulação de Time":
    st.title("🛠️ Simulação de Time Fantasy")
    st.markdown("Monte seu time ideal e verifique a viabilidade orçamentária.")
    
    budget = st.number_input("Orçamento Disponível ($M)", value=100.0, step=0.5)
    
    st.subheader("Seleção de Pilotos")
    c1, c2, c3, c4, c5 = st.columns(5)
    p1 = c1.selectbox("Piloto 1", ["Verstappen ($30M)", "Norris ($25M)", "Hamilton ($20M)"], index=0)
    p2 = c2.selectbox("Piloto 2", ["Leclerc ($22M)", "Piastri ($18M)", "Russell ($18M)"], index=1)
    p3 = c3.selectbox("Piloto 3", ["Alonso ($15M)", "Sainz ($15M)", "Gasly ($10M)"], index=0)
    p4 = c4.selectbox("Piloto 4", ["Albon ($8M)", "Tsunoda ($8M)", "Ocon ($9M)"], index=0)
    p5 = c5.selectbox("Piloto 5", ["Bearman ($5M)", "Antonelli ($6M)", "Lawson ($5M)"], index=1)
    
    constructor_choice = st.selectbox("Construtor", ["Red Bull ($25M)", "Ferrari ($22M)", "McLaren ($23M)"])
    
    st.divider()
    
    if st.button("Validar e Simular Pontuação"):
        total_cost = 95.5 # Valor simulado
        st.info(f"Custo Total do Time: ${total_cost}M")
        
        if total_cost <= budget:
            st.success("✅ Time dentro do orçamento!")
            st.metric("Pontuação Projetada da Rodada", "145 pts")
        else:
            st.error(f"❌ Orçamento estourado em ${total_cost - budget:.1f}M")
