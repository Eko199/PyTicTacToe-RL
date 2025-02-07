import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from ..players.bot_player import BotPlayer
from ..players.random_player import RandomPlayer
from ..game.game import Game

def action_coordinates(action):
    """Converts flat coordinate (0 - 80) to board coordinates (big_x, big_y, small_x, small_y)"""
    return (action % 9) // 3, (action // 9) // 3, action % 3, (action // 9) % 3

class TicTacToeEnv(gym.Env):
    def __init__(self, opponents=[RandomPlayer()], train_x=False):
        super(TicTacToeEnv, self).__init__()
        
        self.action_space = spaces.Discrete(81)

        self.observation_space = spaces.Dict({
            "board": spaces.Box(low=-1, high=1, shape=(3,3,3,3), dtype=np.int8),
            "big_board": spaces.Box(low=-1, high=2, shape=(3,3), dtype=np.int8),
            "next": spaces.Box(low=-1, high=2, shape=(2,), dtype=np.int8)
        })

        self.opponents: list[BotPlayer] = opponents
        self.train_x = train_x
        
        self.reset()

    def _get_obs(self):
        return {
            "board": self.game.board.board.copy(),
            "big_board": self.game.board.big_board.copy(),
            "next": self.game.next
        }

    def reset(self, seed=None, options=None):
        self.game = Game(2, auto_save=False)
        self.opponent = random.choice(self.opponents)
        self.win_reward = 100

        if not self.train_x:
            big_x, big_y, small_x, small_y = self.opponent.get_turn(self.game.next, self.game.board)
            self.game.take_turn(big_x, big_y, small_x, small_y)

        return self._get_obs(), {}

    def step(self, action):
        big_x, big_y, small_x, small_y = action_coordinates(action)
        current_player = self.game.current_player

        # Check for illegal moves
        try:
            self.game.take_turn(big_x, big_y, small_x, small_y)
        except RuntimeError:
            return self._get_obs(), -100, True, False, {}
        
        if self.game.winner is not None:
            return self._get_obs(), self.win_reward, True, False, {}

        reward = 1

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
        self.game.render()