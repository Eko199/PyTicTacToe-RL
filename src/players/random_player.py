"""
This module contains the RandomPlayer class, 
which represents a player that makes random valid moves.
"""

import random
from src.players.bot_player import BotPlayer
from src.tictactoe.board import Board

class RandomPlayer(BotPlayer):
    """
    A player that selects random moves.
    """
    def get_turn(self, next_board: tuple[int, int], board: Board) -> tuple[int, int, int, int]:
        """
        Selects a random valid move from the board.

        Args:
            next_board (tuple[int, int]): The coordinates of the board to play on.
            board (Board): The current game board.

        Returns:
            tuple[int, int, int, int]: The coordinates of the selected move.
        """
        return random.choice(list(board.valid_moves(next_board)))

    def get_type(self) -> str:
        """Returns the type of the player as a string."""
        return "Random"
