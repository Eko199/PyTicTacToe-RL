import os
import random
import numpy as np
from numpy.typing import NDArray
from stable_baselines3 import DQN
from .bot_player import BotPlayer
from ..game.board import Board
from ..agent.models_path import MODELS_PATH
from ..agent.tictactoe_env import action_coordinates

class AIPlayer(BotPlayer):
    def __init__(self, model_name: str):
        self.model: DQN = DQN.load(os.path.join(MODELS_PATH, model_name))

    def get_turn(self, next: tuple[int, int], board: Board) -> tuple[int, int, int, int]:
        obs: NDArray[np.int8] = np.concatenate([
            board.board.flatten(),
            board.big_board.flatten(),
            np.array(next)
        ])

        action, _ = self.model.predict(obs)
        big_x, big_y, small_x, small_y = action_coordinates(int(action.item()))

        valid_moves: list[tuple[int, int, int, int]] = list(board.valid_moves(next))
        if (big_x, big_y, small_x, small_y) not in valid_moves:
            big_x, big_y, small_x, small_y = random.choice(valid_moves)

        return big_x, big_y, small_x, small_y
    