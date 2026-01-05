"""
Componentes de visualização de gráficos usando Plotly.
"""
try:
    import plotly.graph_objects as go
except ImportError:
    import subprocess
    import sys
    import streamlit as st
    
    st.error("⚠️ Plotly não está instalado. Instalando agora...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
    import plotly.graph_objects as go
    st.success("✅ Plotly instalado com sucesso! Por favor, recarregue a página.")
    st.stop()


def _format_lap_time(lap_time_str: str) -> str:
    """
    Formata o tempo da volta para uma string mais legível.
    
    Args:
        lap_time_str: String no formato "0 days 01:28.123000" ou Timedelta string
    
    Returns:
        String formatada como "1:28.123" ou mantém o original se não conseguir parsear
    """
    try:
        # Tenta parsear se for string de Timedelta do pandas
        if "days" in lap_time_str:
            # Remove "0 days " se presente
            time_part = lap_time_str.replace("0 days ", "").strip()
            # Formata para remover segundos decimais extras
            parts = time_part.split(":")
            if len(parts) == 2:
                minutes = parts[0]
                seconds = parts[1].split(".")[0]
                milliseconds = parts[1].split(".")[1][:3] if "." in parts[1] else "000"
                return f"{minutes}:{seconds}.{milliseconds}"
        return lap_time_str
    except:
        return lap_time_str


def render_telemetry_chart(data: dict):
    """
    Renderiza um gráfico de telemetria comparando dois pilotos.
    
    Args:
        data: Dicionário com dados de telemetria no formato:
            {
                "driver1": {
                    "driver": "VER",
                    "lapTime": "0 days 01:28.123000",
                    "distance": [0.0, 10.5, ...],
                    "speed": [120.5, 125.3, ...]
                },
                "driver2": {
                    "driver": "HAM",
                    "lapTime": "0 days 01:28.456000",
                    "distance": [0.0, 10.3, ...],
                    "speed": [119.8, 124.9, ...]
                }
            }
    
    Returns:
        plotly.graph_objects.Figure: Gráfico interativo de telemetria
    """
    driver1_data = data["driver1"]
    driver2_data = data["driver2"]
    
    driver1_name = driver1_data["driver"]
    driver2_name = driver2_data["driver"]
    
    driver1_lap_time = _format_lap_time(str(driver1_data["lapTime"]))
    driver2_lap_time = _format_lap_time(str(driver2_data["lapTime"]))
    
    # Cria o gráfico
    fig = go.Figure()
    
    # Adiciona linha do piloto 1 (Vermelho)
    fig.add_trace(go.Scatter(
        x=driver1_data["distance"],
        y=driver1_data["speed"],
        mode='lines',
        name=f'{driver1_name} (Tempo: {driver1_lap_time})',
        line=dict(color='#DC143C', width=2),  # Vermelho
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Distância: %{x:.1f} m<br>' +
                      'Velocidade: %{y:.1f} km/h<extra></extra>'
    ))
    
    # Adiciona linha do piloto 2 (Azul)
    fig.add_trace(go.Scatter(
        x=driver2_data["distance"],
        y=driver2_data["speed"],
        mode='lines',
        name=f'{driver2_name} (Tempo: {driver2_lap_time})',
        line=dict(color='#1E90FF', width=2),  # Azul
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Distância: %{x:.1f} m<br>' +
                      'Velocidade: %{y:.1f} km/h<extra></extra>'
    ))
    
    # Configuração do layout
    fig.update_layout(
        title={
            'text': f'⚔️ Comparativo de Telemetria: {driver1_name} vs {driver2_name}',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title='Distância (metros)',
        yaxis_title='Velocidade (km/h)',
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600,
        template='plotly_white',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Configuração dos eixos
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray'
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray'
    )
    
    return fig


def render_simulation_results(predictions: list):
    """
    Renderiza um gráfico de barras horizontal com os resultados da simulação Monte Carlo.
    
    Args:
        predictions: Lista de dicionários com predições no formato:
            [
                {"driver": "VER", "win_probability": 0.85, "avg_position": 1.2},
                {"driver": "HAM", "win_probability": 0.10, "avg_position": 3.4},
                ...
            ]
    
    Returns:
        plotly.graph_objects.Figure: Gráfico de barras horizontal
    """
    # Ordena por probabilidade de vitória (maior primeiro)
    sorted_predictions = sorted(predictions, key=lambda x: x["win_probability"], reverse=True)
    
    # Extrai dados para o gráfico
    drivers = [p["driver"] for p in sorted_predictions]
    win_probs = [p["win_probability"] * 100 for p in sorted_predictions]  # Converte para porcentagem
    avg_positions = [p["avg_position"] for p in sorted_predictions]
    
    # Cria gráfico de barras horizontal
    fig = go.Figure(data=[
        go.Bar(
            y=drivers,
            x=win_probs,
            orientation='h',
            text=[f"{prob:.1f}%" for prob in win_probs],
            textposition='outside',
            marker=dict(
                color=win_probs,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Prob. Vitória (%)")
            ),
            hovertemplate='<b>%{y}</b><br>' +
                         'Prob. Vitória: %{x:.2f}%<br>' +
                         'Pos. Média: %{customdata:.2f}<extra></extra>',
            customdata=avg_positions
        )
    ])
    
    # Configuração do layout
    fig.update_layout(
        title={
            'text': '📊 Probabilidade de Vitória por Piloto',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title='Probabilidade de Vitória (%)',
        yaxis_title='Piloto',
        hovermode='closest',
        height=max(400, len(drivers) * 40),  # Altura dinâmica baseada no número de pilotos
        template='plotly_white',
        margin=dict(l=150, r=50, t=80, b=50),
        xaxis=dict(range=[0, max(win_probs) * 1.15])  # Adiciona espaço para o texto
    )
    
    # Configuração dos eixos
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray'
    )
    fig.update_yaxes(
        showgrid=False
    )
    
    return fig


def render_lap_chart(simulation_data: dict) -> go.Figure:
    """
    Renderiza um gráfico de Race Trace mostrando a evolução das posições por volta.
    
    Args:
        simulation_data: Dicionário com dados da simulação contendo:
            - 'lap_data': Lista de dicts com 'driver', 'lap_history', 'position_history'
            - 'total_laps': Número total de voltas
    
    Returns:
        Figura Plotly com o gráfico de posições por volta
    """
    lap_data = simulation_data.get('lap_data', [])
    total_laps = simulation_data.get('total_laps', 0)
    
    if not lap_data or total_laps == 0:
        # Retorna figura vazia se não houver dados
        fig = go.Figure()
        fig.add_annotation(text="Sem dados de volta disponíveis", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Cores oficiais das equipes (simplificado - pode ser expandido)
    team_colors = {
        'Verstappen': '#1E41FF',  # Red Bull - Azul
        'Hamilton': '#00D2BE',    # Mercedes - Ciano
        'Leclerc': '#DC143C',     # Ferrari - Vermelho
        'Norris': '#FF8700',      # McLaren - Laranja
        'Russell': '#00D2BE',     # Mercedes
        'Sainz': '#DC143C',       # Ferrari
        'Piastri': '#FF8700',     # McLaren
        'Perez': '#1E41FF',       # Red Bull
        'Alonso': '#00665E',      # Aston Martin - Verde
        'Stroll': '#00665E',      # Aston Martin
        'Albon': '#37BEDD',       # Williams - Azul claro
        'Gasly': '#FF87BC',       # Alpine - Rosa
        'Ocon': '#FF87BC',        # Alpine
        'Tsunoda': '#5E8FAA',     # RB - Azul acinzentado
        'Ricciardo': '#5E8FAA',   # RB
        'Bottas': '#9B0000',      # Sauber - Vermelho escuro
        'Hulkenberg': '#FFFFFF',  # Haas - Branco (preto no gráfico)
        'Magnussen': '#FFFFFF',   # Haas
        'Zhou': '#9B0000',        # Sauber
        'Sargeant': '#37BEDD',    # Williams
    }
    
    # Cores padrão (para pilotos não mapeados)
    default_colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'
    ]
    
    fig = go.Figure()
    
    # Filtra pilotos que estão muito atrás (opcional, para clareza)
    # Por enquanto, mostra todos os pilotos
    drivers_to_show = lap_data
    
    color_idx = 0
    for driver_data in drivers_to_show:
        driver_name = driver_data['driver']
        position_history = driver_data.get('position_history', [])
        
        if not position_history:
            continue
        
        # Escolhe cor
        if driver_name in team_colors:
            color = team_colors[driver_name]
        else:
            # Tenta pegar pela primeira palavra do nome (equipe)
            first_name = driver_name.split()[0] if ' ' in driver_name else driver_name
            color = team_colors.get(first_name, default_colors[color_idx % len(default_colors)])
            color_idx += 1
        
        # Prepara dados (eixo Y invertido: 1º lugar no topo)
        laps = list(range(1, len(position_history) + 1))
        positions = position_history
        
        # Adiciona linha
        fig.add_trace(go.Scatter(
            x=laps,
            y=positions,
            mode='lines+markers',
            name=driver_name,
            line=dict(color=color, width=2),
            marker=dict(size=4),
            hovertemplate=f'<b>{driver_name}</b><br>' +
                         'Volta %{x}<br>' +
                         'Posição: %{y}<extra></extra>'
        ))
    
    # Atualiza layout (eixo Y invertido: 1 no topo, 20 embaixo)
    max_position = max([max(d.get('position_history', [1])) for d in lap_data], default=20)
    
    fig.update_layout(
        title={'text': '📈 Race Trace - Evolução das Posições', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}},
        xaxis_title='Volta',
        yaxis_title='Posição',
        hovermode='closest',
        height=600,
        template='plotly_white',
        margin=dict(l=80, r=50, t=80, b=50),
        yaxis=dict(
            range=[max_position + 0.5, 0.5],  # Invertido: maior valor embaixo
            autorange='reversed',
            tickmode='linear',
            tick0=1,
            dtick=1
        ),
        xaxis=dict(
            range=[0.5, total_laps + 0.5],
            tickmode='linear',
            tick0=1,
            dtick=5
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01
        )
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig

