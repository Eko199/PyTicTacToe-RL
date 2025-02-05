from abc import ABC, abstractmethod
from typing import Any
import numpy as np
from .board import Board
from ..players.player import Player
from ..players.console_player import HumanPlayer
from ..players.random_player import RandomPlayer
from ..saving.save_manager import save_json

class Game(ABC):
    def __init__(self, mode: int, *, test_mode: bool = False):
        self.test_mode: bool = test_mode
        self.mode = mode

        self.player1: int = 1
        self.player2: int = 2

        self.players: dict[int, Player] = {}

        self.board: Board = Board()
        self.next: tuple[int, int] = -1, -1

        self.current_player: int = self.player1
        self.winner: int | None = None

    def switch_player(self) -> None:
        self.current_player = self.player1 + self.player2 - self.current_player

    def play_turn(self) -> tuple[int, int, int, int]:
        turn: tuple[int, int, int, int] | None = self.players[self.current_player].get_turn(self.next)

        if turn is None:
            self.save()
            exit()
        
        big_x, big_y, small_x, small_y = turn

        while not self.board.play_turn(self.current_player, big_x, big_y, small_x, small_y):
            if isinstance(self.players[self.current_player], HumanPlayer):
                self.invalid_move()
                turn = self.players[self.current_player].get_turn(self.next)

                if turn is None:
                    self.save()
                    exit()
                
                big_x, big_y, small_x, small_y = turn
            else:
                big_x, big_y, small_x, small_y = RandomPlayer().get_turn(self.next)

        if self.board.check_small_win(self.current_player, big_x, big_y):
            if self.board.check_big_win(self.current_player):
                self.winner = self.current_player

        self.next = (small_x, small_y) if not self.test_mode and self.board.check_small_board_valid(small_x, small_y) else (-1, -1)
        return big_x, big_y, small_x, small_y

    def save(self) -> None:
        data: dict[str, Any] = {
            "board": self.board.board.tolist(), 
            "big_board": self.board.big_board.tolist(), 
            "current_player": self.current_player,
            "next": self.next,
            "mode": self.mode
        }
        
        try:
            save_json(data)
            self.successful_save()
        except OSError as e:
            print(e)

    @abstractmethod
    def play(self) -> None:
        pass

    @abstractmethod
    def invalid_move(self) -> None:
        pass

    @abstractmethod
    def render(self, last_turn: tuple[int, int, int, int] | None = None) -> None:
        pass

    @abstractmethod
    def successful_save(self):
        pass

    @classmethod
    def load(cls, data: dict[str, Any]):
        game = cls(data["mode"])
        game.board.board = np.array(data["board"])
        game.board.big_board = np.array(data["big_board"])
        game.current_player = data["current_player"]
        game.next = data["next"]

        return game