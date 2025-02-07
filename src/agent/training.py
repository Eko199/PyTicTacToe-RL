import os.path
from stable_baselines3 import DQN
from gymnasium.wrappers import FlattenObservation
from .tictactoe_env import TicTacToeEnv
from ..players.random_player import RandomPlayer
from ..players.ai_player import AIPlayer

MODELS_PATH = "src\\agent\\models"

def train_model(name: str, steps: int, is_o: bool):
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
    model.save(os.path.join(MODELS_PATH, name))
