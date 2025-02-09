"""
Unit tests for the TicTacToeEnv class.
"""

import unittest
from src.agent.tictactoe_env import TicTacToeEnv

class TestTicTacToeEnv(unittest.TestCase):
    """
    Test cases for the TicTacToeEnv class.
    """

    def setUp(self):
        """Set up a new TicTacToeEnv instance for each test."""
        self.env = TicTacToeEnv()
        self.env.reset()

    def test_valid_move_gives_positive_reward(self):
        """Test that a positive reward is given for a valid move."""
        _, reward, _, _, _ = self.env.step(1)

        self.assertGreater(reward, 0)

    def test_negative_reward(self):
        """Test that a negative reward is given for an invalid move."""
        self.env.step(0)
        _, reward, _, _, _ = self.env.step(0)  # Invalid move, same spot

        self.assertLess(reward, 0)
