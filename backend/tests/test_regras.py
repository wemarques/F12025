import unittest
import sys
import os

# Adiciona o diretório backend ao path para importação correta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core import regras_qualifying, regras_sprint, regras_corrida

class TestRegrasFantasy(unittest.TestCase):
    
    # --- Testes de Qualifying ---
    def test_qualifying_points(self):
        # 1º lugar = 10 pts
        self.assertEqual(regras_qualifying.calculate_qualifying_position_points(1), 10)
        # 10º lugar = 1 pt
        self.assertEqual(regras_qualifying.calculate_qualifying_position_points(10), 1)
        # 11º lugar = 0 pts
        self.assertEqual(regras_qualifying.calculate_qualifying_position_points(11), 0)

    def test_qualifying_bonus(self):
        # Bateu companheiro (+2) + Q3 (+1) = 3
        self.assertEqual(regras_qualifying.calculate_qualifying_bonus(True, True), 3)
        # Só Q3 = 1
        self.assertEqual(regras_qualifying.calculate_qualifying_bonus(False, True), 1)
        # Nenhum = 0
        self.assertEqual(regras_qualifying.calculate_qualifying_bonus(False, False), 0)

    # --- Testes de Sprint ---
    def test_sprint_points(self):
        # 1º = 8 pts
        self.assertEqual(regras_sprint.calculate_sprint_position_points(1), 8)
        # 8º = 1 pt
        self.assertEqual(regras_sprint.calculate_sprint_position_points(8), 1)
        # 9º = 0 pts
        self.assertEqual(regras_sprint.calculate_sprint_position_points(9), 0)

    def test_sprint_overtake(self):
        # Grid 10 -> Chegada 5 (Ganhou 5)
        self.assertEqual(regras_sprint.calculate_sprint_overtake_points(10, 5), 5)
        # Grid 5 -> Chegada 10 (Perdeu 5)
        self.assertEqual(regras_sprint.calculate_sprint_overtake_points(5, 10), -5)

    # --- Testes de Corrida (Feature Race) ---
    def test_race_points(self):
        # 1º = 25 pts
        self.assertEqual(regras_corrida.calculate_race_position_points(1), 25)
        # 10º = 1 pt
        self.assertEqual(regras_corrida.calculate_race_position_points(10), 1)
        # 11º = 0 pts
        self.assertEqual(regras_corrida.calculate_race_position_points(11), 0)

    def test_race_bonuses(self):
        # FL (+5) + DOTD (+5) + Teammate (+3) = 13
        self.assertEqual(regras_corrida.calculate_race_bonuses(True, True, True), 13)
        # Só FL = 5
        self.assertEqual(regras_corrida.calculate_race_bonuses(True, False, False), 5)

    def test_completion_status(self):
        # Finished = 1
        self.assertEqual(regras_corrida.calculate_completion_points("Finished"), 1)
        self.assertEqual(regras_corrida.calculate_completion_points("+1 Lap"), 1)
        # DNF = -10
        self.assertEqual(regras_corrida.calculate_completion_points("Collision"), -10)
        # DSQ = -20
        self.assertEqual(regras_corrida.calculate_completion_points("Disqualified"), -20)

if __name__ == '__main__':
    unittest.main()
