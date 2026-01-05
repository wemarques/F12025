import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import requests

# Adiciona o diretório raiz ao path para importar módulos do backend se necessário
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))

from auth import Authenticator
from components.charts import render_telemetry_chart, render_simulation_results
from components.team_builder import render_team_builder

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
page = st.sidebar.radio("Navegação", ["Dashboard", "Prognóstico por Piloto", "Simulação de Time", "⚔️ Comparativo de Pilotos", "🏗️ Montar Time", "🔮 Simulador Monte Carlo"])

# --- Páginas ---

if page == "Dashboard":
    st.title("🏎️ Dashboard F1 2025")
    st.markdown("### Visão Geral da Temporada")
    
    # Lista de Grandes Prêmios 2025
    gp_options = [
        "Australian Grand Prix", "Chinese Grand Prix", "Japanese Grand Prix", "Bahrain Grand Prix",
        "Saudi Arabian Grand Prix", "Miami Grand Prix", "Emilia Romagna Grand Prix", "Monaco Grand Prix",
        "Spanish Grand Prix", "Canadian Grand Prix", "Austrian Grand Prix", "British Grand Prix",
        "Belgian Grand Prix", "Hungarian Grand Prix", "Dutch Grand Prix", "Italian Grand Prix",
        "Azerbaijan Grand Prix", "Singapore Grand Prix", "United States Grand Prix", "Mexican Grand Prix",
        "São Paulo Grand Prix", "Las Vegas Grand Prix", "Qatar Grand Prix", "Abu Dhabi Grand Prix"
    ]
    
    # Inicializa session state para corrida selecionada
    if 'selected_race' not in st.session_state:
        st.session_state.selected_race = gp_options[0]
    
    # Selectbox para selecionar a corrida
    selected_race = st.selectbox(
        "🏁 Selecionar Corrida",
        options=gp_options,
        index=gp_options.index(st.session_state.selected_race) if st.session_state.selected_race in gp_options else 0,
        help="Selecione a corrida para visualizar os dados"
    )
    
    # Atualiza session state
    st.session_state.selected_race = selected_race
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Corrida Selecionada", selected_race.split(" Grand Prix")[0] if " Grand Prix" in selected_race else selected_race)
    col2.metric("Líder do Campeonato", "Max Verstappen", "25 pts")
    col3.metric("Construtor Líder", "Red Bull Racing", "40 pts")
    
    st.subheader(f"Tendências de Pontuação - {selected_race.split(' Grand Prix')[0] if ' Grand Prix' in selected_race else selected_race}")
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
    
    # Configuração da API
    API_BASE_URL = "http://localhost:8000"
    
    # Lista de Grandes Prêmios 2025
    gp_options = [
        "Miami Grand Prix", "Australian Grand Prix", "Chinese Grand Prix", "Japanese Grand Prix", "Bahrain Grand Prix",
        "Saudi Arabian Grand Prix", "Emilia Romagna Grand Prix", "Monaco Grand Prix",
        "Spanish Grand Prix", "Canadian Grand Prix", "Austrian Grand Prix", "British Grand Prix",
        "Belgian Grand Prix", "Hungarian Grand Prix", "Dutch Grand Prix", "Italian Grand Prix",
        "Azerbaijan Grand Prix", "Singapore Grand Prix", "United States Grand Prix", "Mexican Grand Prix",
        "São Paulo Grand Prix", "Las Vegas Grand Prix", "Qatar Grand Prix", "Abu Dhabi Grand Prix"
    ]
    
    # Inicializa session state para corrida selecionada
    if 'sim_race' not in st.session_state:
        st.session_state.sim_race = "Miami Grand Prix"
    if 'sim_strategy' not in st.session_state:
        st.session_state.sim_strategy = "balanced"
    
    # Seção de Controles de Otimização
    col_race, col_strategy, col_button = st.columns([2, 2, 1.5])
    
    with col_race:
        selected_race = st.selectbox(
            "🏁 Selecionar Corrida",
            options=gp_options,
            index=gp_options.index(st.session_state.sim_race) if st.session_state.sim_race in gp_options else 0,
            help="Selecione a corrida para simulação"
        )
        st.session_state.sim_race = selected_race
    
    with col_strategy:
        strategy_options = {
            "Equilibrado": "balanced",
            "Agressivo (Maximizar Pontos)": "points",
            "Seguro (Maximizar Valorização)": "value"
        }
        strategy_labels = list(strategy_options.keys())
        # Encontra o índice da estratégia atual
        current_strategy_label = next(
            (k for k, v in strategy_options.items() if v == st.session_state.sim_strategy),
            "Equilibrado"
        )
        current_index = strategy_labels.index(current_strategy_label) if current_strategy_label in strategy_labels else 0
        
        strategy_label = st.selectbox(
            "Estratégia de Otimização",
            options=strategy_labels,
            index=current_index,
            help="Escolha a estratégia de otimização"
        )
        st.session_state.sim_strategy = strategy_options[strategy_label]
    
    with col_button:
        st.write("")  # Espaçamento
        st.write("")  # Espaçamento
        if st.button("🪄 Sugerir Melhor Time", type="primary", use_container_width=True):
            with st.spinner('Calculando melhor time possível...'):
                try:
                    url = f"{API_BASE_URL}/api/v1/optimization/optimize"
                    payload = {
                        "budget": 100.0,
                        "strategy": st.session_state.sim_strategy
                    }
                    
                    response = requests.post(url, json=payload, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(
                            f"✅ Time otimizado sugerido! "
                            f"Score: {result['total_score']:.2f}, "
                            f"Custo: ${result['total_cost']:.2f}M"
                        )
                        # Aqui você poderia preencher os selects automaticamente se necessário
                        st.session_state.optimized_result = result
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
    
    budget = st.number_input("Orçamento Disponível ($M)", value=100.0, step=0.5)
    
    st.subheader("Seleção de Pilotos")
    c1, c2, c3, c4, c5 = st.columns(5)
    p1 = c1.selectbox("Piloto 1", ["Verstappen ($30M)", "Norris ($25M)", "Hamilton ($20M)"], index=0)
    p2 = c2.selectbox("Piloto 2", ["Leclerc ($22M)", "Piastri ($18M)", "Russell ($18M)"], index=1)
    p3 = c3.selectbox("Piloto 3", ["Alonso ($15M)", "Sainz ($15M)", "Gasly ($10M)"], index=0)
    p4 = c4.selectbox("Piloto 4", ["Albon ($8M)", "Tsunoda ($8M)", "Ocon ($9M)"], index=0)
    p5 = c5.selectbox("Piloto 5", ["Bearman ($5M)", "Antonelli ($6M)", "Lawson ($5M)"], index=1)
    
    st.subheader("Seleção de Construtores")
    const1_col, const2_col = st.columns(2)
    constructor_options = ["Red Bull ($25M)", "Ferrari ($22M)", "McLaren ($23M)", "Mercedes ($24M)", "Aston Martin ($21M)", "Alpine ($19M)", "Williams ($18M)", "RB ($17M)", "Haas ($16M)", "Sauber ($15M)"]
    constructor_choice_1 = const1_col.selectbox("Construtor 1", constructor_options, index=0)
    constructor_choice_2 = const2_col.selectbox("Construtor 2", constructor_options, index=1)
    
    st.divider()
    
    if st.button("Validar e Simular Pontuação"):
        total_cost = 95.5 # Valor simulado
        st.info(f"Custo Total do Time: ${total_cost}M")
        
        if total_cost <= budget:
            st.success("✅ Time dentro do orçamento!")
            st.metric("Pontuação Projetada da Rodada", "145 pts")
        else:
            st.error(f"❌ Orçamento estourado em ${total_cost - budget:.1f}M")

elif page == "⚔️ Comparativo de Pilotos":
    st.title("⚔️ Comparativo de Pilotos")
    st.markdown("Compare a telemetria de dois pilotos em uma sessão específica.")
    
    # Configuração da API
    API_BASE_URL = "http://localhost:8000"
    
    # Lista de Grandes Prêmios (exemplos)
    gp_options = [
        "Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami",
        "Emilia Romagna", "Monaco", "Spain", "Canada", "Austria", "Great Britain",
        "Hungary", "Belgium", "Netherlands", "Italy", "Azerbaijan", "Singapore",
        "United States", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"
    ]
    
    # Lista de pilotos (códigos de 3 letras)
    driver_options = [
        "VER", "NOR", "HAM", "LEC", "PIA", "RUS", "PER", "SAI", "ALO", "STR",
        "OCO", "GAS", "ALB", "TSU", "BOT", "ZHO", "HUL", "MAG", "RIC", "LAW"
    ]
    
    # Inputs do usuário
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.number_input("Ano", min_value=2020, max_value=2030, value=2025, step=1)
        gp = st.selectbox("Grande Prêmio", gp_options, index=0)
        session_type = st.selectbox(
            "Tipo de Sessão",
            ["R", "Q", "FP1", "FP2", "FP3", "S", "SS"],
            index=0,
            format_func=lambda x: {
                "R": "Race (Corrida)",
                "Q": "Qualifying (Classificação)",
                "FP1": "Free Practice 1",
                "FP2": "Free Practice 2",
                "FP3": "Free Practice 3",
                "S": "Sprint",
                "SS": "Sprint Shootout"
            }.get(x, x)
        )
    
    with col2:
        driver1 = st.selectbox("Piloto 1", driver_options, index=0)
        driver2 = st.selectbox("Piloto 2", driver_options, index=1)
    
    if st.button("Comparar Telemetria", type="primary"):
        with st.spinner(f'Carregando dados de {year} {gp} {session_type}...'):
            try:
                url = f"{API_BASE_URL}/api/v1/analytics/compare-laps"
                params = {
                    "year": year,
                    "gp": gp,
                    "session_type": session_type,
                    "driver1": driver1,
                    "driver2": driver2
                }
                
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    fig = render_telemetry_chart(data)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    try:
                        error_detail = response.json().get("detail", "Erro desconhecido")
                    except:
                        error_detail = f"Erro HTTP {response.status_code}"
                    st.error(f"❌ Erro ao comparar pilotos: {error_detail}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Não foi possível conectar à API. Certifique-se de que o backend está rodando em http://localhost:8000")
            except requests.exceptions.Timeout:
                st.error("❌ A requisição demorou muito. Tente novamente.")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {str(e)}")

elif page == "🏗️ Montar Time":
    st.title("🏗️ Montar Time Fantasy F1")
    st.markdown("Monte seu time ideal seguindo as regras do F1 Fantasy 2025.")
    
    render_team_builder()

elif page == "🔮 Simulação de Corrida":
    st.title("🔮 Simulação de Corrida")
    st.markdown("Execute simulações Monte Carlo para prever resultados de corridas.")
    
    # Configuração da API
    API_BASE_URL = "http://localhost:8000"
    
    # Lista de Grandes Prêmios 2025
    gp_options = [
        "Miami Grand Prix", "Australian Grand Prix", "Chinese Grand Prix", "Japanese Grand Prix", "Bahrain Grand Prix",
        "Saudi Arabian Grand Prix", "Emilia Romagna Grand Prix", "Monaco Grand Prix",
        "Spanish Grand Prix", "Canadian Grand Prix", "Austrian Grand Prix", "British Grand Prix",
        "Belgian Grand Prix", "Hungarian Grand Prix", "Dutch Grand Prix", "Italian Grand Prix",
        "Azerbaijan Grand Prix", "Singapore Grand Prix", "United States Grand Prix", "Mexican Grand Prix",
        "São Paulo Grand Prix", "Las Vegas Grand Prix", "Qatar Grand Prix", "Abu Dhabi Grand Prix"
    ]
    
    # Seleção de GP
    selected_gp = st.selectbox(
        "🏁 Selecionar Grande Prêmio",
        options=gp_options,
        index=0,
        help="Selecione o GP para simular"
    )
    
    # Botão para rodar simulação
    if st.button("🔄 Rodar Simulação Monte Carlo (100x)", type="primary", use_container_width=True):
        with st.spinner(f'Executando {100} simulações Monte Carlo...'):
            try:
                url = f"{API_BASE_URL}/api/v1/simulation/simulate"
                payload = {
                    "gp_name": selected_gp,
                    "num_simulations": 100
                }
                
                response = requests.post(url, json=payload, timeout=120)
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.simulation_result = result
                    st.success(f"✅ Simulação concluída com sucesso!")
                else:
                    try:
                        error_detail = response.json().get("detail", "Erro desconhecido")
                    except:
                        error_detail = f"Erro HTTP {response.status_code}"
                    st.error(f"❌ Erro ao executar simulação: {error_detail}")
                    st.session_state.simulation_result = None
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Não foi possível conectar à API. Certifique-se de que o backend está rodando em http://localhost:8000")
                st.session_state.simulation_result = None
            except requests.exceptions.Timeout:
                st.error("❌ A simulação demorou muito. Tente novamente.")
                st.session_state.simulation_result = None
            except Exception as e:
                st.error(f"❌ Erro inesperado: {str(e)}")
                st.session_state.simulation_result = None
    
    # Exibe resultados se disponíveis
    if 'simulation_result' in st.session_state and st.session_state.simulation_result:
        result = st.session_state.simulation_result
        
        st.divider()
        st.subheader(f"📊 Resultados da Simulação - {result['gp_name']}")
        st.caption(f"Baseado em {result['num_simulations']} simulações Monte Carlo")
        
        # Obtém lista de pilotos do "Meu Time" se disponível
        my_team_drivers = []
        if 'selected_drivers' in st.session_state:
            try:
                backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
                sys.path.insert(0, backend_path)
                from app.services.fantasy_data import load_assets
                df_drivers, _ = load_assets()
                for driver_id in st.session_state.selected_drivers:
                    driver = df_drivers[df_drivers['id'] == driver_id]
                    if not driver.empty:
                        my_team_drivers.append(driver.iloc[0]['name'])
            except Exception as e:
                # Se não conseguir carregar, continua sem destacar
                pass
        
        # Tabela de probabilidades de vitória
        st.markdown("### 🏆 Probabilidade de Vitória")
        sorted_winners = result.get('sorted_winners', [])
        
        if sorted_winners:
            # Cria DataFrame para exibição
            table_data = []
            for item in sorted_winners:
                driver_name = item['driver']
                win_prob = item['probability']
                podium_prob = result['podium_probabilities'].get(driver_name, 0)
                avg_pos = result['avg_positions'].get(driver_name, 0)
                is_my_team = driver_name in my_team_drivers
                
                table_data.append({
                    'Piloto': driver_name,
                    'Prob. Vitória (%)': f"{win_prob:.2f}",
                    'Prob. Pódio (%)': f"{podium_prob:.2f}",
                    'Pos. Média': f"{avg_pos:.2f}",
                    'Meu Time': '✅' if is_my_team else ''
                })
            
            df_results = pd.DataFrame(table_data)
            st.dataframe(df_results, use_container_width=True, hide_index=True)
        
        # Gráfico de barras - Chance de Pódio
        st.markdown("### 📈 Chance de Pódio por Piloto")
        
        try:
            import plotly.graph_objects as go
            
            # Prepara dados do gráfico
            drivers_list = list(result['podium_probabilities'].keys())
            podium_probs = list(result['podium_probabilities'].values())
            
            # Cores: verde para pilotos do "Meu Time", azul para outros
            colors = ['#22c55e' if driver in my_team_drivers else '#3b82f6' for driver in drivers_list]
            
            # Ordena por probabilidade (maior primeiro)
            sorted_data = sorted(zip(drivers_list, podium_probs, colors), key=lambda x: x[1], reverse=True)
            drivers_sorted, probs_sorted, colors_sorted = zip(*sorted_data) if sorted_data else ([], [], [])
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(drivers_sorted),
                    y=list(probs_sorted),
                    marker_color=list(colors_sorted),
                    text=[f"{p:.1f}%" for p in probs_sorted],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Prob. Pódio: %{y:.2f}%<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title="Probabilidade de Pódio (Top 3) por Piloto",
                xaxis_title="Piloto",
                yaxis_title="Probabilidade (%)",
                height=500,
                xaxis={'tickangle': -45},
                hovermode='closest'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Legenda
            if my_team_drivers:
                st.info(f"💚 **Pilotos do Meu Time destacados em verde**: {', '.join(my_team_drivers)}")
        
        except ImportError:
            st.warning("⚠️ Plotly não está instalado. Instale com: pip install plotly")
        except Exception as e:
            st.error(f"❌ Erro ao gerar gráfico: {str(e)}")
        
        # Resumo dos pilotos do "Meu Time"
        if my_team_drivers:
            st.divider()
            st.markdown("### 👥 Performance dos Pilotos do Meu Time")
            
            team_summary = []
            for driver_name in my_team_drivers:
                if driver_name in result['win_probabilities']:
                    win_prob = result['win_probabilities'][driver_name]
                    podium_prob = result['podium_probabilities'][driver_name]
                    avg_pos = result['avg_positions'][driver_name]
                    
                    team_summary.append({
                        'Piloto': driver_name,
                        'Prob. Vitória': f"{win_prob:.2f}%",
                        'Prob. Pódio': f"{podium_prob:.2f}%",
                        'Pos. Média': f"{avg_pos:.2f}"
                    })
            
            if team_summary:
                df_team = pd.DataFrame(team_summary)
                st.dataframe(df_team, use_container_width=True, hide_index=True)

elif page == "🔮 Simulador Monte Carlo":
    st.title("🔮 Simulador Monte Carlo")
    st.markdown("Execute simulações Monte Carlo usando dados reais do FastF1 para prever resultados de corridas.")
    
    # Configuração da API
    API_BASE_URL = "http://localhost:8000"
    
    # Lista de anos disponíveis
    year_options = [2024, 2023, 2022, 2021]
    
    # Lista de Grandes Prêmios (hardcoded para teste rápido)
    gp_options = [
        "Bahrain", "Saudi Arabia", "Australia", "Brazil",
        "Monaco", "Spain", "Canada", "Austria", "Great Britain",
        "Hungary", "Belgium", "Netherlands", "Italy", "Singapore",
        "Japan", "United States", "Mexico", "Abu Dhabi"
    ]
    
    # Layout de inputs em colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_year = st.selectbox(
            "📅 Ano",
            options=year_options,
            index=0,
            help="Selecione o ano da temporada"
        )
    
    with col2:
        selected_gp = st.selectbox(
            "🏁 Grande Prêmio",
            options=gp_options,
            index=0,
            help="Selecione o GP para simular"
        )
    
    with col3:
        iterations = st.slider(
            "🔄 Número de Iterações",
            min_value=100,
            max_value=1000,
            value=100,
            step=50,
            help="Número de simulações Monte Carlo a executar"
        )
    
    # Slider para probabilidade de chuva
    st.markdown("### 🌧️ Condições Climáticas")
    rain_probability = st.slider(
        "🌧️ Probabilidade de Chuva",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
        help="Probabilidade de chuva na corrida (0% = seco, 100% = chuva garantida)"
    )
    
    st.divider()
    
    # Botão para rodar simulação
    if st.button("🚀 Rodar Simulação", type="primary", use_container_width=True):
        with st.spinner(f'Simulando corrida {iterations} vezes...'):
            try:
                url = f"{API_BASE_URL}/api/v1/simulation/run/{selected_year}/{selected_gp}"
                params = {"iterations": iterations, "rain_probability": rain_probability}
                
                response = requests.post(url, params=params, timeout=300)
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.monte_carlo_result = result
                    
                    # Salva os pontos simulados no session_state para uso no otimizador
                    if result.get('predictions'):
                        simulated_points = {}
                        for pred in result['predictions']:
                            driver_name = pred['driver']
                            avg_points = pred.get('average_fantasy_points', 0)
                            simulated_points[driver_name] = avg_points
                        st.session_state['simulated_points'] = simulated_points
                    
                    st.success(f"✅ Simulação concluída com sucesso!")
                else:
                    try:
                        error_detail = response.json().get("detail", "Erro desconhecido")
                    except:
                        error_detail = f"Erro HTTP {response.status_code}"
                    
                    if "404" in error_detail or "não encontrado" in error_detail.lower() or "insuficientes" in error_detail.lower():
                        st.error(f"❌ Dados insuficientes para esta pista neste ano. Tente outro GP ou ano.")
                    else:
                        st.error(f"❌ Erro ao executar simulação: {error_detail}")
                    st.session_state.monte_carlo_result = None
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Não foi possível conectar à API. Certifique-se de que o backend está rodando em http://localhost:8000")
                st.session_state.monte_carlo_result = None
            except requests.exceptions.Timeout:
                st.error("❌ A simulação demorou muito. Tente reduzir o número de iterações.")
                st.session_state.monte_carlo_result = None
            except Exception as e:
                st.error(f"❌ Erro inesperado: {str(e)}")
                st.session_state.monte_carlo_result = None
    
    # Exibe resultados se disponíveis
    if 'monte_carlo_result' in st.session_state and st.session_state.monte_carlo_result:
        result = st.session_state.monte_carlo_result
        
        st.divider()
        st.subheader(f"📊 Resultados da Simulação - {result['track']}")
        st.caption(f"Baseado em {result['iterations']} simulações Monte Carlo")
        
        # Indicador de condição climática
        weather_condition = result.get('weather_condition', 'DRY')
        weather_display = {
            'DRY': '☀️ SECO',
            'WET': '🌧️ CHUVA',
            'MIXED': '🌦️ MISTO'
        }
        weather_text = weather_display.get(weather_condition, f'❓ {weather_condition}')
        st.info(f"**Condição Simulada:** {weather_text}")
        
        # Métricas principais no topo
        if result.get('predictions'):
            winner = result['predictions'][0]  # Primeiro é o mais provável vencedor
            st.markdown("### 🏆 Vencedor Mais Provável")
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric(
                    "Piloto",
                    winner['driver'],
                    f"{winner['win_probability']*100:.1f}% de chance"
                )
            with col_metric2:
                st.metric(
                    "Posição Média",
                    f"{winner['avg_position']:.2f}",
                    "posição esperada"
                )
            
            st.divider()
            
            # Gráfico de barras horizontal
            st.markdown("### 📈 Probabilidade de Vitória por Piloto")
            try:
                fig = render_simulation_results(result['predictions'])
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Erro ao gerar gráfico: {str(e)}")
            
            # Race Trace (se disponível)
            if result.get('race_trace'):
                st.divider()
                st.markdown("### 🏁 Race Trace - Evolução das Posições")
                try:
                    from components.charts import render_lap_chart
                    trace_fig = render_lap_chart(result['race_trace'])
                    st.plotly_chart(trace_fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"⚠️ Não foi possível exibir o Race Trace: {str(e)}")
            
            st.divider()
            
            # Tabela com dados brutos
            st.markdown("### 📋 Dados Completos")
            df_predictions = pd.DataFrame(result['predictions'])
            # Renomeia colunas para português e formata
            df_display = df_predictions.copy()
            df_display['win_probability'] = (df_display['win_probability'] * 100).round(2).astype(str) + '%'
            df_display = df_display.rename(columns={
                'driver': 'Piloto',
                'win_probability': 'Prob. Vitória',
                'avg_position': 'Pos. Média',
                'average_fantasy_points': 'Pontos Média'
            })
            st.dataframe(df_display, use_container_width=True, hide_index=True)
