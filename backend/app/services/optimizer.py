"""
Serviço de otimização para encontrar o melhor time de Fantasy F1.
"""
import itertools
from typing import Dict, List, Literal, Optional, Tuple
import pandas as pd

from app.services.fantasy_data import load_assets


class TeamOptimizer:
    """Otimizador de times de Fantasy F1."""
    
    def __init__(self):
        """Inicializa o otimizador carregando os dados."""
        self.df_drivers, self.df_constructors = load_assets()
    
    def _validate_team(self, driver_ids: List[str], constructor_ids: List[str], budget: float) -> bool:
        """
        Valida se um time está dentro das regras.
        
        Args:
            driver_ids: Lista de IDs dos pilotos
            constructor_ids: Lista de IDs dos construtores
            budget: Orçamento disponível
        
        Returns:
            bool: True se válido, False caso contrário
        """
        # Verifica orçamento
        total_cost = 0.0
        
        for driver_id in driver_ids:
            driver = self.df_drivers[self.df_drivers['id'] == driver_id]
            if driver.empty:
                return False
            total_cost += driver.iloc[0]['price']
        
        for constructor_id in constructor_ids:
            constructor = self.df_constructors[self.df_constructors['id'] == constructor_id]
            if constructor.empty:
                return False
            total_cost += constructor.iloc[0]['price']
        
        if total_cost > budget:
            return False
        
        # Verifica regra: máximo 3 pilotos da mesma equipe
        team_counts = {}
        for driver_id in driver_ids:
            driver = self.df_drivers[self.df_drivers['id'] == driver_id].iloc[0]
            team_id = driver['team_id']
            team_counts[team_id] = team_counts.get(team_id, 0) + 1
            if team_counts[team_id] > 3:
                return False
        
        return True
    
    def _calculate_score(
        self,
        driver_ids: List[str],
        constructor_ids: List[str],
        strategy: Literal["points", "value", "balanced"]
    ) -> float:
        """
        Calcula o score de um time baseado na estratégia.
        
        Args:
            driver_ids: Lista de IDs dos pilotos
            constructor_ids: Lista de IDs dos construtores
            strategy: Estratégia de otimização
        
        Returns:
            float: Score do time
        """
        total_points = 0.0
        total_sentiment = 0.0
        
        # Soma pontos e sentiment dos pilotos
        for driver_id in driver_ids:
            driver = self.df_drivers[self.df_drivers['id'] == driver_id].iloc[0]
            total_points += driver.get('predicted_points', 0.0)
            total_sentiment += driver.get('sentiment', 0.0)
        
        # Soma pontos e sentiment dos construtores
        for constructor_id in constructor_ids:
            constructor = self.df_constructors[self.df_constructors['id'] == constructor_id].iloc[0]
            total_points += constructor.get('predicted_points', 0.0)
            total_sentiment += constructor.get('sentiment', 0.0)
        
        if strategy == "points":
            return total_points
        elif strategy == "value":
            return total_sentiment
        elif strategy == "balanced":
            # Normaliza pontos e sentiment para 0-1 e soma
            max_points = self.df_drivers['predicted_points'].max() * 5 + self.df_constructors['predicted_points'].max() * 2
            max_sentiment = (self.df_drivers['sentiment'].max() * 5 + self.df_constructors['sentiment'].max() * 2)
            
            normalized_points = total_points / max_points if max_points > 0 else 0
            normalized_sentiment = total_sentiment / max_sentiment if max_sentiment > 0 else 0
            
            return normalized_points + normalized_sentiment
        else:
            raise ValueError(f"Estratégia inválida: {strategy}")
    
    def _calculate_cost(self, driver_ids: List[str], constructor_ids: List[str]) -> float:
        """Calcula o custo total de um time."""
        total_cost = 0.0
        
        for driver_id in driver_ids:
            driver = self.df_drivers[self.df_drivers['id'] == driver_id].iloc[0]
            total_cost += driver['price']
        
        for constructor_id in constructor_ids:
            constructor = self.df_constructors[self.df_constructors['id'] == constructor_id].iloc[0]
            total_cost += constructor['price']
        
        return total_cost
    
    def find_best_team(
        self,
        budget: float = 100.0,
        strategy: Literal["points", "value", "balanced"] = "points",
        max_drivers: int = 5,
        max_constructors: int = 2
    ) -> Dict:
        """
        Encontra o melhor time possível dado um orçamento e estratégia.
        
        Args:
            budget: Orçamento disponível (default: 100.0)
            strategy: Estratégia de otimização ("points", "value", "balanced")
            max_drivers: Número máximo de pilotos (default: 5)
            max_constructors: Número máximo de construtores (default: 2)
        
        Returns:
            Dict com as seguintes chaves:
                - drivers: Lista de IDs dos pilotos
                - constructors: Lista de IDs dos construtores
                - total_score: Score total do time
                - total_cost: Custo total do time
                - budget_remaining: Orçamento restante
        """
        driver_ids = self.df_drivers['id'].tolist()
        constructor_ids = self.df_constructors['id'].tolist()
        
        best_team = None
        best_score = float('-inf')
        
        # Gera todas as combinações possíveis
        driver_combinations = list(itertools.combinations(driver_ids, max_drivers))
        constructor_combinations = list(itertools.combinations(constructor_ids, max_constructors))
        
        # Combina todas as possibilidades
        total_combinations = len(driver_combinations) * len(constructor_combinations)
        
        for driver_combo in driver_combinations:
            for constructor_combo in constructor_combinations:
                driver_list = list(driver_combo)
                constructor_list = list(constructor_combo)
                
                # Valida o time
                if not self._validate_team(driver_list, constructor_list, budget):
                    continue
                
                # Calcula o score
                score = self._calculate_score(driver_list, constructor_list, strategy)
                
                # Atualiza melhor time se necessário
                if score > best_score:
                    best_score = score
                    best_team = {
                        'drivers': driver_list,
                        'constructors': constructor_list,
                        'total_score': score,
                        'total_cost': self._calculate_cost(driver_list, constructor_list),
                        'budget_remaining': budget - self._calculate_cost(driver_list, constructor_list)
                    }
        
        if best_team is None:
            raise ValueError(
                f"Não foi possível encontrar um time válido com orçamento de ${budget}M. "
                f"Tente aumentar o orçamento ou reduzir o número de pilotos/construtores."
            )
        
        return best_team


