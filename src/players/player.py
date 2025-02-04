from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def get_turn(self, next: tuple[int, int]) -> tuple[int, int, int, int] | None:
        pass