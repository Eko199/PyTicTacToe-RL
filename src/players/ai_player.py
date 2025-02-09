"""
This module contains the AIPlayer class, which represents a player controlled by a trained AI model.
"""

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
    """
    A player controlled by a trained AI model using a DQN to predict the next move.
    """
    def __init__(self, model_name: str):
        """
        Initializes the AIPlayer with a trained model.

        Args:
            model_name (str): The name of the trained model to load.
        """
        self.model: DQN = DQN.load(os.path.join(MODELS_PATH, model_name))

    def get_turn(self, next: tuple[int, int], board: Board) -> tuple[int, int, int, int]:
        """
        Predicts the next move from the AI model.

        Args:
            next (tuple[int, int]): The coordinates of the big board to play on.
            board (Board): The current game board.

        Returns:
            tuple[int, int, int, int]: The coordinates of the selected move.
        """
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
