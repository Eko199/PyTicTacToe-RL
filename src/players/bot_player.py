from ..game.board import Board
from .player import Player, ABC, abstractmethod

class BotPlayer(Player, ABC):
    @abstractmethod
    def get_turn(self, next: tuple[int, int], board: Board) -> tuple[int, int, int, int]:
        pass