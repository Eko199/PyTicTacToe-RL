from typing import Generator
import numpy as np
from numpy.typing import NDArray
from colorama import Fore, Style
from collections import defaultdict

class Board:
    EMPTY: int = 0
    FULL: int = -1

    def __init__(self, player1: str = "O", player2: str = "X"):
        self.board: NDArray[np.int8] = np.full((3, 3, 3, 3), self.EMPTY)
        self.big_board: NDArray[np.int8] = np.full((3, 3), self.EMPTY)

        self.player_symbols: defaultdict[int, str] = defaultdict(str, {
            self.EMPTY: ".",
            1: player1,
            2: player2
        })

    def play_turn(self, player: int, big_x: int, big_y: int, small_x: int, small_y: int) -> bool:
        if not { big_x, big_y, small_x, small_y } <= { 0, 1, 2 }:
            return False

        current_board: NDArray[np.int8] = self.board[big_y, big_x]

        if self.big_board[big_y, big_x] != self.EMPTY or current_board[small_y, small_x] != self.EMPTY:
            return False

        current_board[small_y, small_x] = player

        if Board.check_board_win(current_board, player):
            self.big_board[big_y, big_x] = player
        elif (current_board != self.EMPTY).all():
            self.big_board[big_y, big_x] = self.FULL

        return True
    
    def check_small_board_valid(self, big_x: int, big_y: int) -> bool:
        return self.big_board[big_y, big_x] == self.EMPTY
    
    def check_small_win(self, player: int, big_x: int, big_y: int) -> bool:
        return self.big_board[big_y, big_x] == player
    
    def check_big_win(self, player: int) -> bool:
        return Board.check_board_win(self.big_board, player)
    
    def is_full(self) -> bool:
        return all(not self.check_small_board_valid(big_x, big_y) for big_x in range(3) for big_y in range(3))
    
    def valid_moves(self, next: tuple[int, int]) -> Generator[tuple[int, int, int, int], None, None] :
        return ((big_x, big_y, small_x, small_y) 
                for big_x in (range(3) if next[0] == -1 else [next[0]]) 
                for big_y in (range(3) if next[1] == -1 else [next[1]])
                for small_x in range(3)
                for small_y in range(3)
                if self.big_board[big_y, big_x] == self.EMPTY and self.board[big_y, big_x, small_y, small_x] == self.EMPTY)

    def to_string(self, last_turn: tuple[int, int, int, int] | None = None) -> str:
        last_big_x, last_big_y, last_small_x, last_small_y = last_turn if last_turn is not None else (-1, -1, -1, -1)
        result: str = "-" * 25 + "\n"

        big_str_map: dict[tuple[str, int], str] = {
            ("X", 0): "\\   /",
            ("X", 1):  "  X  ",
            ("X", 2):  "/   \\",
            ("O", 0): "⌈ ‾ ⌉",
            ("O", 1): "|   |",
            ("O", 2): "⌊ _ ⌋"
        }

        for big_y in range(3):
            for small_y in range(3):
                result += "| "

                for big_x in range(3):
                    if self.player_symbols[self.big_board[big_y, big_x]] in { "X", "O" }:
                        mapped: str = big_str_map[(self.player_symbols[self.big_board[big_y, big_x]], small_y)]
                        result += Fore.GREEN + mapped + Style.RESET_ALL if (big_x, big_y) == (last_big_x, last_big_y) else mapped
                        result += " | "
                        continue

                    board_str: list[str] = [self.player_symbols[self.board[big_y, big_x, small_y, small_x]] for small_x in range(3)]

                    if (big_x, big_y, small_y) == (last_big_x, last_big_y, last_small_y):
                        board_str[last_small_x] = Fore.GREEN + board_str[last_small_x] + Style.RESET_ALL

                    result += " ".join(board_str) + " | "

                result += "\n"

            result += "-" * 25 + "\n"

        return result

    def __str__(self) -> str:
        return self.to_string()

    @staticmethod
    def check_board_win(board: NDArray[np.int8], player: int) -> bool:
        for i in range(3):
            if (board[i] == player).all() \
                or (board[:, i] == player).all() \
                or (np.diag(board) == player).all() \
                or (np.diag(np.fliplr(board)) == player).all():

                return True

        return False