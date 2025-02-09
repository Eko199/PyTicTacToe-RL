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
        self.board = Board()

    def test_initial_is_empty(self):
        npt.assert_array_equal(self.board.board, Board.EMPTY)
        npt.assert_array_equal(self.board.big_board, Board.EMPTY)

    def test_play_turn_places_move(self):
        result: bool = self.board.play_turn(1, 0, 0, 0, 0)

        self.assertTrue(result)
        self.assertEqual(self.board.board[0, 0, 0, 0], 1)

    def test_play_invalid_turn_returns_false(self):
        self.assertFalse(self.board.play_turn(1, -1, 0, 0, 0))
        self.assertFalse(self.board.play_turn(1, 1, 1, 1, 3))

    def test_play_turn_already_taken_returns_false(self):
        self.board.play_turn(1, 0, 0, 0, 0)
        result: bool = self.board.play_turn(2, 0, 0, 0, 0)

        self.assertFalse(result)
        self.assertEqual(self.board.board[0, 0, 0, 0], 1)

    def test_check_small_win(self):
        self.win_small_board(1, 0, 0)

        self.assertTrue(self.board.check_small_win(1, 0, 0))
        self.assertFalse(self.board.check_small_win(2, 0, 0))
        self.assertEqual(self.board.big_board[0, 0], 1)

    def test_check_small_empty_board_is_valid(self):
        self.assertTrue(self.board.check_small_board_valid(0, 0))

    def test_check_small_won_board_is_invalid(self):
        self.win_small_board(1, 0, 0)
        self.assertFalse(self.board.check_small_board_valid(0, 0))

    def test_check_small_full_board_is_invalid(self):
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
        self.win_small_board(1, 0, 0)
        self.assertFalse(self.board.play_turn(1, 0, 0, 1, 0))

    def test_check_big_win_works(self):
        for i in range(3):
            self.win_small_board(1, 0, i)

        self.assertTrue(self.board.check_big_win(1))
        self.assertFalse(self.board.check_big_win(2))

    def test_check_big_win_empty_returns_false(self):
        self.assertFalse(self.board.check_big_win(1))

    def test_is_full_on_empty_returns_false(self):
        self.assertFalse(self.board.is_full())

    def test_is_full_when_full_returns_true(self):
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
        all_moves: set[tuple[int, int, int, int]] = set(it.product(range(3), range(3), range(3), range(3)))
        valid_moves: set[tuple[int, int, int, int]] = set(self.board.valid_moves((-1, -1)))

        self.assertCountEqual(valid_moves, all_moves)
        self.assertSetEqual(valid_moves, all_moves)

    def test_valid_moves_next_are_correct(self):
        all_moves: set[tuple[int, int, int, int]] = set(it.product([0], [0], range(3), range(3)))
        valid_moves: set[tuple[int, int, int, int]] = set(self.board.valid_moves((0, 0)))

        self.assertCountEqual(valid_moves, all_moves)
        self.assertSetEqual(valid_moves, all_moves)

    def test_to_string_works(self):
        board_str_len: int = len(self.board.to_string())
        self.assertGreater(board_str_len, 81)

    def win_small_board(self, player: int, x: int, y: int):
        self.board.play_turn(player, x, y, 0, 0)
        self.board.play_turn(player, x, y, 1, 1)
        self.board.play_turn(player, x, y, 2, 2)

if __name__ == '__main__':
    unittest.main()
