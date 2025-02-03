import random
from .player import Player

class RandomPlayer(Player):
    def get_turn(self, next_x: int, next_y: int) -> tuple[int, int, int, int]:
        possibilites: range = range(3)
        big_x, big_y = (next_x, next_y) if (next_x, next_y) != (-1, -1) else (random.choice(possibilites), random.choice(possibilites))

        return big_x, big_y, random.choice(possibilites), random.choice(possibilites)