"""
This module contains the abstract HumanPlayer class, 
which represents a human player for distinction.
"""

from abc import ABC
from src.players.player import Player

class HumanPlayer(Player, ABC):
    """A human player."""
