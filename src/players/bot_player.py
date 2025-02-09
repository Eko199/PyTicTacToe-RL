"""
This module defines the BotPlayer class, an abstract base class for bot players in the game.
"""

from abc import ABC, abstractmethod
from ..game.board import Board
from .player import Player

class BotPlayer(Player, ABC):
    """
    Abstract base class for bot players in the game.
    """
    @abstractmethod
    def get_turn(self, next: tuple[int, int], board: Board) -> tuple[int, int, int, int]:
        """
        Abstract method to get the next turn for the bot player.

        Args:
            next (tuple[int, int]): The coordinates of the small board to play on.
            board (Board): The current state of the game board.

        Returns:
            tuple[int, int, int, int]: The coordinates for the next move.
        """
        pass