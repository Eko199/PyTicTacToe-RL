import random
from .bot_player import BotPlayer
from ..game.board import Board

class RandomPlayer(BotPlayer):
    def get_turn(self, next: tuple[int, int], board: Board) -> tuple[int, int, int, int]:
        return random.choice(list(board.valid_moves(next)))