import random
from .player import Player, Board

class RandomPlayer(Player):
    def get_turn(self, next: tuple[int, int], board: Board) -> tuple[int, int, int, int]:
        return random.choice(list(board.valid_moves(next)))