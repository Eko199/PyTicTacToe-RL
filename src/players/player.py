from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def get_turn(self, next_x: int, next_y: int) -> tuple[int, int, int, int]:
        pass