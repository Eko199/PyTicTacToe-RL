from abc import ABC, abstractmethod
from ..game.board import Board

class Player(ABC):
    @abstractmethod
    def get_turn(self, next: tuple[int, int], board: Board) -> tuple[int, int, int, int] | None:
        pass