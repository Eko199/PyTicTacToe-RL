from abc import ABC, abstractmethod
from typing import Any
import asyncio
import numpy as np
from .board import Board
from ..players.player import Player
from ..saving.save_manager import save_json

class Game(ABC):
    def __init__(self, mode: int, *, test_mode: bool = False, is_o: bool = True, auto_save: bool = True):
        self.test_mode: bool = test_mode
        self.mode = mode

        self.player1: int = 1
        self.player2: int = 2

        self.players: dict[int, Player] = {}

        self.board: Board = Board()
        self.next: tuple[int, int] = -1, -1

        self.current_player: int = self.player1 if is_o else self.player2
        self.winner: int | None = None

        self.auto_save: bool = auto_save
        self.turns: int = 0
        self.tasks: set[asyncio.Task] = set()

    def switch_player(self) -> None:
        self.current_player = self.player1 + self.player2 - self.current_player

    async def play_turn(self) -> tuple[int, int, int, int]:
        #Turn is guaranteed to be valid by Player
        turn: tuple[int, int, int, int] | None = self.players[self.current_player].get_turn(self.next, self.board)

        if turn is None:
            await self.save()
            exit()
        
        big_x, big_y, small_x, small_y = turn
        if not self.board.play_turn(self.current_player, big_x, big_y, small_x, small_y):
            raise RuntimeError("An unknown error occurred!")

        if self.board.check_small_win(self.current_player, big_x, big_y):
            if self.board.check_big_win(self.current_player):
                self.winner = self.current_player

        self.next = (small_x, small_y) if not self.test_mode and self.board.check_small_board_valid(small_x, small_y) else (-1, -1)

        if self.auto_save and self.turns > 0 and self.turns % 5 == 0:
            self.tasks.add(asyncio.create_task(Game.save(self, "autosave.json")))
            await asyncio.sleep(0.1)
        
        self.turns += 1
        return big_x, big_y, small_x, small_y
    
    def to_json(self) -> dict[str, list | tuple | int]:
        return {
            "board": self.board.board.tolist(), 
            "big_board": self.board.big_board.tolist(), 
            "current_player": self.current_player,
            "next": self.next,
            "mode": self.mode
        }

    async def save(self, file_name: str | None = None) -> None:
        try:
            await save_json(self.to_json(), file_name)

            if file_name is None or not file_name.startswith("autosave"):
                self.successful_save()
        except OSError as e:
            print(e)

    @abstractmethod
    async def play(self) -> None:
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
        game.next = (data["next"][0], data["next"][1])

        return game