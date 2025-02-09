"""
This module contains the abstract Player class, which defines the interface for all players.
"""

from abc import ABC, abstractmethod
from ..game.board import Board

class Player(ABC):
    """
    Abstract base class for all players defining a method to get the player's turn.
    """
    @abstractmethod
    def get_turn(self, next: tuple[int, int], board: Board) -> tuple[int, int, int, int] | None:
        """
        Gets the next move for the player.

        Args:
            next (tuple[int, int]): The coordinates of the big board to play on.
            board (Board): The current game board.

        Returns:
            tuple[int, int, int, int] | None: The coordinates of the selected move or None if the player quits.
        """
        pass