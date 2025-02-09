"""
Unit tests for the Board class.
"""

import unittest
import itertools as it
import numpy.testing as npt
from src.tictactoe.board import Board

class TestBoard(unittest.TestCase):
    """
    Test cases for the Board class.
    """

    def setUp(self):
        """Set up a new Board instance for each test."""
        self.board = Board()

    def test_initial_is_empty(self):
        """Test that the initial board is empty."""
        npt.assert_array_equal(self.board.board, Board.EMPTY)
        npt.assert_array_equal(self.board.big_board, Board.EMPTY)

    def test_play_turn_places_move(self):
        """Test that a move is placed correctly on the board."""
        result: bool = self.board.play_turn(1, 0, 0, 0, 0)

        self.assertTrue(result)
        self.assertEqual(self.board.board[0, 0, 0, 0], 1)

    def test_play_invalid_turn_returns_false(self):
        """Test that an invalid move returns false."""
        self.assertFalse(self.board.play_turn(1, -1, 0, 0, 0))
        self.assertFalse(self.board.play_turn(1, 1, 1, 1, 3))

    def test_play_turn_already_taken_returns_false(self):
        """Test that a move on an already taken spot returns false."""
        self.board.play_turn(1, 0, 0, 0, 0)
        result: bool = self.board.play_turn(2, 0, 0, 0, 0)

        self.assertFalse(result)
        self.assertEqual(self.board.board[0, 0, 0, 0], 1)

    def test_check_small_win(self):
        """Test checking for a win on a small board."""
        self.win_small_board(1, 0, 0)

        self.assertTrue(self.board.check_small_win(1, 0, 0))
        self.assertFalse(self.board.check_small_win(2, 0, 0))
        self.assertEqual(self.board.big_board[0, 0], 1)

    def test_check_small_empty_board_is_valid(self):
        """Test that an empty small board is valid."""
        self.assertTrue(self.board.check_small_board_valid(0, 0))

    def test_check_small_won_board_is_invalid(self):
        """Test that a won small board is invalid."""
        self.win_small_board(1, 0, 0)
        self.assertFalse(self.board.check_small_board_valid(0, 0))

    def test_check_small_full_board_is_invalid(self):
        """Test that a full small board is invalid."""
        # o x x
        # x x o
        # o o x

        self.board.play_turn(1, 0, 0, 0, 0)
        self.board.play_turn(2, 0, 0, 1, 0)
        self.board.play_turn(2, 0, 0, 2, 0)
        self.board.play_turn(2, 0, 0, 0, 1)
        self.board.play_turn(2, 0, 0, 1, 1)
        self.board.play_turn(1, 0, 0, 2, 1)
        self.board.play_turn(1, 0, 0, 0, 2)
        self.board.play_turn(1, 0, 0, 1, 2)
        self.board.play_turn(2, 0, 0, 2, 2)

        self.assertFalse(self.board.check_small_board_valid(0, 0))
        self.assertEqual(self.board.big_board[0, 0], Board.FULL)

    def test_play_turn_on_won_returns_false(self):
        """Test that a move on a won board returns false."""
        self.win_small_board(1, 0, 0)
        self.assertFalse(self.board.play_turn(1, 0, 0, 1, 0))

    def test_check_big_win_works(self):
        """Test checking for a win on the big board."""
        for i in range(3):
            self.win_small_board(1, 0, i)

        self.assertTrue(self.board.check_big_win(1))
        self.assertFalse(self.board.check_big_win(2))

    def test_check_big_win_empty_returns_false(self):
        """Test that an empty big board does not have a win."""
        self.assertFalse(self.board.check_big_win(1))

    def test_is_full_on_empty_returns_false(self):
        """Test that an empty board is not full."""
        self.assertFalse(self.board.is_full())

    def test_is_full_when_full_returns_true(self):
        """Test that a full board is detected correctly."""
        self.win_small_board(1, 0, 0)
        self.win_small_board(2, 1, 0)
        self.win_small_board(2, 2, 0)
        self.win_small_board(2, 0, 1)
        self.win_small_board(2, 1, 1)
        self.win_small_board(1, 2, 1)
        self.win_small_board(1, 0, 2)
        self.win_small_board(1, 1, 2)
        self.win_small_board(2, 2, 2)

        self.assertTrue(self.board.is_full())

    def test_valid_moves_empty_are_all(self):
        """Test that all moves are valid on an empty board."""
        all_moves: set[tuple[int, int, int, int]] = \
            set(it.product(range(3), range(3), range(3), range(3)))

        valid_moves: set[tuple[int, int, int, int]] = set(self.board.valid_moves((-1, -1)))

        self.assertCountEqual(valid_moves, all_moves)
        self.assertSetEqual(valid_moves, all_moves)

    def test_valid_moves_next_are_correct(self):
        """Test that valid moves are correct for the next board."""
        all_moves: set[tuple[int, int, int, int]] = set(it.product([0], [0], range(3), range(3)))
        valid_moves: set[tuple[int, int, int, int]] = set(self.board.valid_moves((0, 0)))

        self.assertCountEqual(valid_moves, all_moves)
        self.assertSetEqual(valid_moves, all_moves)

    def test_to_string_works(self):
        """Test converting the board to a string."""
        board_str_len: int = len(self.board.to_string())
        self.assertGreater(board_str_len, 81)

    def win_small_board(self, player: int, x: int, y: int):
        """Helper method to win a small board for a player."""
        self.board.play_turn(player, x, y, 0, 0)
        self.board.play_turn(player, x, y, 1, 1)
        self.board.play_turn(player, x, y, 2, 2)

if __name__ == '__main__':
    unittest.main()
