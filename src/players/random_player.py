import random
from .player import Player

class RandomPlayer(Player):
    def get_turn(self, next: tuple[int, int]) -> tuple[int, int, int, int]:
        possibilites: range = range(3)
        big_x, big_y = next if next != (-1, -1) else (random.choice(possibilites), random.choice(possibilites))

        return big_x, big_y, random.choice(possibilites), random.choice(possibilites)