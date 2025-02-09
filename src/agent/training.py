"""
This module contains functions for training AI models for Mega Tic Tac Toe.
"""

import os.path
from stable_baselines3 import DQN
from gymnasium.wrappers import FlattenObservation
from src.agent.models_path import MODELS_PATH
from src.agent.tictactoe_env import TicTacToeEnv
from src.players.random_player import RandomPlayer
from src.players.ai_player import AIPlayer

def train_model(name: str, steps: int, is_o: bool):
    """
    Trains an AI model to play Mega Tic Tac Toe using a Deep Q-Network.

    Args:
        name (str): The name of the model.
        steps (int): The number of training games.
        is_o (bool): Whether the model is trained as player O.
    """
    # DQN doesn't support environments with a dictionary observations
    env = FlattenObservation(TicTacToeEnv([RandomPlayer()], train_x=False)) \
        if is_o \
        else FlattenObservation(TicTacToeEnv([RandomPlayer(), AIPlayer("o_trainer1")], train_x=True))

    # Train the model (3M+ timesteps recommended)
    model = DQN(
        "MlpPolicy", env, verbose=1,
        learning_rate=3e-4,
        exploration_fraction=0.1,
        exploration_final_eps=0.01,
        buffer_size=100000,
        batch_size=64,
        train_freq=4,
        target_update_interval=1000
    )

    model.learn(total_timesteps=steps)
    model.save(os.path.join(MODELS_PATH, ("o_" if is_o else "x_") + name))
