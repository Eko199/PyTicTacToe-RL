"""
Unit tests for the Game class.
"""

import asyncio
import unittest

import numpy as np
from src.players.random_player import RandomPlayer
from src.tictactoe.game import Game
from src.tictactoe.board import Board

class TestGame(unittest.TestCase):
    """
    Test cases for the Game class.
    """

    def setUp(self):
        """Set up a new game instance for each test."""
        self.game = Game(mode=1)

    def test_initial_state(self):
        """Test the initial state of the game."""
        self.assertEqual(self.game.current_player, self.game.player1)
        self.assertIsNone(self.game.winner)
        self.assertEqual(self.game.next, (-1, -1))
        self.assertIsInstance(self.game.board, Board)

    def test_switch_player(self):
        """Test switching the current player."""
        self.game.switch_player()
        self.assertEqual(self.game.current_player, self.game.player2)
        self.game.switch_player()
        self.assertEqual(self.game.current_player, self.game.player1)

    def test_take_turn(self):
        """Test taking a turn correctly."""
        self.game.take_turn(0, 0, 0, 0)

        self.assertEqual(self.game.board.board[0, 0, 0, 0], self.game.player1)
        self.assertEqual(self.game.next, (0, 0))
        self.assertEqual(self.game.current_player, self.game.player2)

    def test_take_turn_used_space_raises_error(self):
        """Test handling a move that's already taken."""
        self.game.take_turn(0, 0, 0, 0)

        with self.assertRaises(RuntimeError):
            self.game.take_turn(0, 0, 0, 0)  # Invalid move, same spot

    def test_take_turn_invalid_move_raises_error(self):
        """Test handling an invalid move."""
        with self.assertRaises(RuntimeError):
            self.game.take_turn(-1, 0, 0, 0)

    def test_take_turn_wrong_board_raises_error(self):
        """Test taking turn on the wrong small board."""
        self.game.take_turn(0, 0, 0, 0)

        with self.assertRaises(RuntimeError):
            self.game.take_turn(1, 1, 0, 0)

    def test_take_turn_changes_next(self):
        """Test next player should play in the correct board"""
        self.game.take_turn(0, 0, 0, 0)
        self.assertEqual(self.game.next, (0, 0))

    def test_take_turn_next_full_can_play_anywhere(self):
        """Test next player should play in the correct board"""
        self.game.test_mode = True

        self.game.take_turn(0, 0, 0, 0)
        self.game.take_turn(0, 0, 1, 0)
        self.game.take_turn(0, 0, 2, 0)
        self.assertEqual(self.game.next, (-1, -1))

    def test_winner(self):
        """Test winning the game."""
        self.game.test_mode = True

        self.game.take_turn(0, 0, 0, 0)
        self.game.take_turn(0, 0, 1, 0)
        self.game.take_turn(0, 0, 2, 0)
        
        self.game.take_turn(1, 0, 0, 0)
        self.game.take_turn(1, 0, 1, 0)
        self.game.take_turn(1, 0, 2, 0)
        
        self.game.take_turn(2, 0, 0, 0)
        self.game.take_turn(2, 0, 1, 0)
        self.game.take_turn(2, 0, 2, 0)

        self.assertEqual(self.game.winner, self.game.player1)

    def test_play_turn(self):
        self.game.players[1] = RandomPlayer()
        asyncio.run(self.game.play_turn())

        self.assertEqual(self.game.current_player, self.game.player2)
        self.assertEqual(np.count_nonzero(self.game.board.board == 1), 1)

    def test_to_json(self):
        """Test converting the game state to JSON."""
        game_json = self.game.to_json()
        self.assertIn("board", game_json)
        self.assertIn("big_board", game_json)
        self.assertIn("current_player", game_json)
        self.assertIn("next", game_json)
        self.assertIn("mode", game_json)
        self.assertIn("agent_name", game_json)

    def test_load(self):
        """Test loading the game state from JSON."""
        game_json = self.game.to_json()
        loaded_game = Game.load(game_json)
        self.assertEqual(loaded_game.current_player, self.game.current_player)
        self.assertEqual(loaded_game.next, self.game.next)
        self.assertEqual(loaded_game.mode, self.game.mode)
        self.assertEqual(loaded_game.agent_name, self.game.agent_name)

if __name__ == "__main__":
    unittest.main()
