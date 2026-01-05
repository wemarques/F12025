"""
Componente Team Builder para montar time de Fantasy F1.
"""
import streamlit as st
import pandas as pd
import json
import sys
import os
import requests
from pathlib import Path

# Adiciona o backend ao path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.services.fantasy_rules import validate_team
from config_env import API_BASE_URL

# Constantes
TOTAL_BUDGET = 100.0
MAX_DRIVERS = 5
MAX_CONSTRUCTORS = 2


def load_prices_data():
    """Carrega dados de preços do arquivo f1_prices.json"""
    backend_dir = backend_path
    prices_file = backend_dir / "data" / "f1_prices.json"
    
    if not prices_file.exists():
        raise FileNotFoundError(f"Arquivo {prices_file} não encontrado")
    
    with open(prices_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def init_session_state():
    """Inicializa o estado da sessão se necessário."""
    if 'selected_drivers' not in st.session_state:
        st.session_state.selected_drivers = []
    if 'selected_constructors' not in st.session_state:
        st.session_state.selected_constructors = []


def calculate_total_cost(drivers: list, constructors: list, prices_data: list) -> float:
    """Calcula o custo total do time."""
    data_dict = {item["id"]: item for item in prices_data}
    total = 0.0
    
    for driver_id in drivers:
        if driver_id in data_dict:
            total += data_dict[driver_id]["price"]
    
    for constructor_id in constructors:
        if constructor_id in data_dict:
            total += data_dict[constructor_id]["price"]
    
    return total


def render_team_builder():
    """
    Renderiza o componente Team Builder completo.
    """
    init_session_state()
    
    try:
        prices_data = load_prices_data()
    except FileNotFoundError as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        st.info("💡 Certifique-se de que o arquivo backend/data/f1_prices.json existe.")
        return
    except Exception as e:
        st.error(f"❌ Erro inesperado: {e}")
        return
    
    # Separa pilotos e construtores
    drivers_data = [item for item in prices_data if item["type"] == "DRIVER"]
    constructors_data = [item for item in prices_data if item["type"] == "CONSTRUCTOR"]
    
    # Calcula custo total e orçamento restante
    total_cost = calculate_total_cost(
        st.session_state.selected_drivers,
        st.session_state.selected_constructors,
        prices_data
    )
    budget_remaining = TOTAL_BUDGET - total_cost
    
    # Botão de Otimização no topo
    st.markdown("### 🪄 Otimização Automática")
    col_opt1, col_opt2 = st.columns([3, 1])
    
    with col_opt1:
        st.info("💡 Clique no botão para encontrar automaticamente o melhor time com base nos pontos esperados.")
    
    with col_opt2:
        # Verifica se existem pontos simulados disponíveis
        use_simulated_points = 'simulated_points' in st.session_state and st.session_state.get('simulated_points')
        
        if use_simulated_points:
            st.info("💡 Usando dados da sua simulação recente!")
        
        if st.button("🪄 Sugerir Melhor Time ($100M)", type="primary", use_container_width=True):
            with st.spinner('Calculando melhor time possível...'):
                try:
                    url = f"{API_BASE_URL}/api/v1/fantasy/optimize"
                    payload = {"budget": TOTAL_BUDGET}
                    
                    # Se existirem pontos simulados, adiciona ao payload
                    if use_simulated_points:
                        payload["custom_points_projections"] = st.session_state['simulated_points']
                    
                    response = requests.post(url, json=payload, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Atualiza o session_state com os IDs retornados
                        st.session_state.selected_drivers = result["drivers"]
                        st.session_state.selected_constructors = result["constructors"]
                        
                        st.success(f"✅ Time otimizado! Pontos esperados: {result['total_points']:.1f}")
                        st.rerun()
                    else:
                        try:
                            error_detail = response.json().get("detail", "Erro desconhecido")
                        except:
                            error_detail = f"Erro HTTP {response.status_code}"
                        st.error(f"❌ Erro ao otimizar: {error_detail}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Não foi possível conectar à API. Certifique-se de que o backend está rodando em http://localhost:8000")
                except requests.exceptions.Timeout:
                    st.error("❌ A otimização demorou muito. Tente novamente.")
                except Exception as e:
                    st.error(f"❌ Erro inesperado: {str(e)}")
    
    st.divider()
    
    # Layout em 2 colunas
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("### 🛒 Mercado")
        
        # Tabs para Pilotos e Construtores
        tab_drivers, tab_constructors = st.tabs(["Pilotos", "Construtores"])
        
        with tab_drivers:
            st.markdown("#### Selecionar Pilotos")
            
            # Cria botões para cada piloto
            for driver in sorted(drivers_data, key=lambda x: x["price"], reverse=True):
                driver_id = driver["id"]
                driver_name = driver["name"]
                driver_price = driver["price"]
                driver_team = driver["team"]
                is_selected = driver_id in st.session_state.selected_drivers
                is_disabled = len(st.session_state.selected_drivers) >= MAX_DRIVERS and not is_selected
                
                # Botão para adicionar/remover piloto
                col_btn, col_info = st.columns([1, 3])
                
                with col_btn:
                    if is_selected:
                        if st.button("➖", key=f"remove_driver_{driver_id}", help="Remover piloto"):
                            st.session_state.selected_drivers.remove(driver_id)
                            st.rerun()
                    else:
                        if st.button("➕", key=f"add_driver_{driver_id}", disabled=is_disabled, help="Adicionar piloto"):
                            if len(st.session_state.selected_drivers) < MAX_DRIVERS:
                                st.session_state.selected_drivers.append(driver_id)
                                st.rerun()
                            else:
                                st.warning(f"❌ Limite de {MAX_DRIVERS} pilotos atingido!")
                
                with col_info:
                    status_text = "✅" if is_selected else ""
                    disabled_text = " (Máximo atingido)" if is_disabled else ""
                    st.markdown(f"{status_text} **{driver_name}** ({driver_team}) - ${driver_price:.1f}M{disabled_text}")
        
        with tab_constructors:
            st.markdown("#### Selecionar Construtores")
            
            # Cria botões para cada construtor
            for constructor in sorted(constructors_data, key=lambda x: x["price"], reverse=True):
                constructor_id = constructor["id"]
                constructor_name = constructor["name"]
                constructor_price = constructor["price"]
                is_selected = constructor_id in st.session_state.selected_constructors
                is_disabled = len(st.session_state.selected_constructors) >= MAX_CONSTRUCTORS and not is_selected
                
                # Botão para adicionar/remover construtor
                col_btn, col_info = st.columns([1, 3])
                
                with col_btn:
                    if is_selected:
                        if st.button("➖", key=f"remove_constructor_{constructor_id}", help="Remover construtor"):
                            st.session_state.selected_constructors.remove(constructor_id)
                            st.rerun()
                    else:
                        if st.button("➕", key=f"add_constructor_{constructor_id}", disabled=is_disabled, help="Adicionar construtor"):
                            if len(st.session_state.selected_constructors) < MAX_CONSTRUCTORS:
                                st.session_state.selected_constructors.append(constructor_id)
                                st.rerun()
                            else:
                                st.warning(f"❌ Limite de {MAX_CONSTRUCTORS} construtores atingido!")
                
                with col_info:
                    status_text = "✅" if is_selected else ""
                    disabled_text = " (Máximo atingido)" if is_disabled else ""
                    st.markdown(f"{status_text} **{constructor_name}** - ${constructor_price:.1f}M{disabled_text}")
    
    with col_right:
        st.markdown("### 👥 Meu Time")
        
        # Orçamento Restante com barra de progresso
        st.markdown("#### 💰 Orçamento")
        budget_percent = min(max(budget_remaining / TOTAL_BUDGET * 100, 0), 100)
        st.progress(budget_percent / 100)
        
        col_budget1, col_budget2 = st.columns(2)
        with col_budget1:
            st.metric("Restante", f"${budget_remaining:.2f}M")
        with col_budget2:
            st.metric("Gasto", f"${total_cost:.2f}M")
        
        # Alertas visuais
        if budget_remaining < 0:
            st.error(f"⚠️ **Orçamento estourado!** Faltam ${abs(budget_remaining):.2f}M")
        elif budget_remaining < 10:
            st.warning(f"⚠️ Orçamento restante baixo: ${budget_remaining:.2f}M")
        
        st.divider()
        
        # Lista de Pilotos Selecionados
        st.markdown("#### 🏎️ Pilotos (5)")
        if len(st.session_state.selected_drivers) == 0:
            st.info("Nenhum piloto selecionado")
        else:
            data_dict = {item["id"]: item for item in prices_data}
            for i, driver_id in enumerate(st.session_state.selected_drivers, 1):
                if driver_id in data_dict:
                    driver = data_dict[driver_id]
                    st.markdown(f"{i}. **{driver['name']}** ({driver['team']}) - ${driver['price']:.1f}M")
                else:
                    st.markdown(f"{i}. {driver_id} (erro ao carregar)")
        
        st.divider()
        
        # Lista de Construtores Selecionados
        st.markdown("#### 🏭 Construtores (2)")
        if len(st.session_state.selected_constructors) == 0:
            st.info("Nenhum construtor selecionado")
        else:
            data_dict = {item["id"]: item for item in prices_data}
            for i, constructor_id in enumerate(st.session_state.selected_constructors, 1):
                if constructor_id in data_dict:
                    constructor = data_dict[constructor_id]
                    st.markdown(f"{i}. **{constructor['name']}** - ${constructor['price']:.1f}M")
                else:
                    st.markdown(f"{i}. {constructor_id} (erro ao carregar)")
        
        st.divider()
        
        # Botão Limpar Time
        if st.button("🗑️ Limpar Time", type="secondary", use_container_width=True):
            st.session_state.selected_drivers = []
            st.session_state.selected_constructors = []
            st.rerun()
        
        # Validação do time
        is_valid, validation_message = validate_team(
            st.session_state.selected_drivers,
            st.session_state.selected_constructors,
            prices_data
        )
        
        if is_valid:
            st.success(f"✅ {validation_message}")
        else:
            st.error(f"❌ {validation_message}")
