import gymnasium as gym
from typing import Any

MODELS_PATH = "src\\agent\\models"
env: gym.Env[Any, Any] = gym.make('CartPole-v0')