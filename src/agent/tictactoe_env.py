"""
This module defines the TicTacToeEnv class, 
a custom OpenAI Gym environment for the Mega Tic Tac Toe game, 
used for training agents.
"""

import random
from typing import NewType
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from src.players.bot_player import BotPlayer
from src.players.random_player import RandomPlayer
from src.tictactoe.game import Game

Observation = NewType("Observation", dict[str, np.ndarray | tuple[int, int]])

def action_coordinates(action: int) -> tuple[int, int, int, int]:
    """
    Converts a flat coordinate (0 - 80) to board coordinates (big x, big y, small x, small y).

    Args:
        action (int): The flat action coordinate.

    Returns:
        tuple[int, int, int, int]: The board coordinates.
    """
    return (action % 9) // 3, (action // 9) // 3, action % 3, (action // 9) % 3

class TicTacToeEnv(gym.Env):
    """
    Custom OpenAI Gym environment for the Mega Tic Tac Toe game.
    """
    def __init__(self, opponents: list[BotPlayer] | None = None, train_x: bool = False):
        """
        Initializes the TicTacToeEnv.

        Args:
            opponents (list[BotPlayer]): List of opponent bot players to train with.
            train_x (bool): Whether to train as the X player.
        """
        super().__init__()

        self.action_space: gym.Space = spaces.Discrete(81)

        self.observation_space: gym.Space = spaces.Dict({
            "board": spaces.Box(low=-1, high=1, shape=(3,3,3,3), dtype=np.int8),
            "big_board": spaces.Box(low=-1, high=2, shape=(3,3), dtype=np.int8),
            "next": spaces.Box(low=-1, high=2, shape=(2,), dtype=np.int8)
        })

        self.opponents: list[BotPlayer] = opponents if opponents is not None else [RandomPlayer()]
        self.train_x: bool = train_x

        self.reset()

    def _get_obs(self) -> Observation:
        """
        Gets the current observation of the game. 
        An observartion is a dictionary pf the current 3x3x3x3 board, 
        the 3x3 big board and the small board coordinates of the next turn.

        Returns:
            dict: The current observation.
        """
        return Observation({
            "board": self.game.board.board.copy(),
            "big_board": self.game.board.big_board.copy(),
            "next": self.game.next
        })

    def reset(self,
              seed: int | None = None,
              options: dict | None = None) -> tuple[Observation, dict]:
        """
        Resets the environment to the initial state.

        Args:
            seed (int, optional): 
                The seed for random number generation. Comes from the base Env class.
            options (dict, optional): 
                Additional options for resetting. Comes from the base Env class.

        Returns:
            tuple: The initial observation and an empty dictionary as info.
        """
        self.game: Game = Game(2, auto_save=False)
        self.opponent: BotPlayer = random.choice(self.opponents)
        self.win_reward: int = 100

        if self.train_x:
            big_x, big_y, small_x, small_y = self.opponent.get_turn(self.game.next, self.game.board)
            self.game.take_turn(big_x, big_y, small_x, small_y)

        return self._get_obs(), {}

    def step(self, action: int) -> tuple[Observation, int, bool, bool, dict]:
        """
        Takes a step in the environment with the given action and 
        plays the opponent's turn, producing a reward.

        Args:
            action (int): The action to take.

        Returns:
            tuple: The new observation, reward, done flag, truncated flag, and additional info.
        """
        big_x, big_y, small_x, small_y = action_coordinates(action)
        current_player: int = self.game.current_player

        # Check for illegal moves
        try:
            self.game.take_turn(big_x, big_y, small_x, small_y)
        except RuntimeError:
            return self._get_obs(), -100, True, False, {}

        if self.game.winner is not None:
            return self._get_obs(), self.win_reward, True, False, {}

        reward: int = 1

        if self.game.board.check_small_win(current_player, big_x, big_y):
            reward += 5

        if self.game.board.is_full():
            return self._get_obs(), reward, True, False, {}

        if self.game.next == (-1, -1):
            reward -= 7

        current_player = self.game.current_player

        big_x, big_y, small_x, small_y = self.opponent.get_turn(self.game.next, self.game.board)
        self.game.take_turn(big_x, big_y, small_x, small_y)

        if self.game.winner is not None:
            return self._get_obs(), -60, True, False, {}

        if self.game.board.is_full():
            return self._get_obs(), 0, True, False, {}

        if self.game.board.check_small_win(current_player, big_x, big_y):
            reward -= 5

        if self.game.next == (-1, -1):
            reward += 7

        self.win_reward -= 1
        return self._get_obs(), reward, False, False, {}

    def render(self):
        """Renders the current state of the environment."""
        self.game.render()
