"""
This module contains the Board class, which represents the 3x3x3x3 board for Mega Tic Tac Toe.
"""

from typing import Generator
import numpy as np
from numpy.typing import NDArray
from colorama import Fore, Style
from collections import defaultdict

class Board:
    """
    Represents the game board of zeroes (empty), ones (player 1) and twos (player 2). 
    Also provides the big 3x3 board which can also have -1 as a value, representing a small draw game.
    """
    EMPTY: int = 0
    FULL: int = -1

    def __init__(self, player1: str = "O", player2: str = "X"):
        """
        Initializes the game board.

        Args:
            player1 (str, optional): The symbol for player 1. Defaults to "O".
            player2 (str, optional): The symbol for player 2. Defaults to "X".
        """
        self.board: NDArray[np.int8] = np.full((3, 3, 3, 3), self.EMPTY)
        self.big_board: NDArray[np.int8] = np.full((3, 3), self.EMPTY)

        self.player_symbols: defaultdict[int, str] = defaultdict(str, {
            self.EMPTY: ".",
            1: player1,
            2: player2
        })

    def play_turn(self, player: int, big_x: int, big_y: int, small_x: int, small_y: int) -> bool:
        """
        Plays a turn for the specified player.

        Args:
            player (int): The player number (1 or 2).
            big_x (int): The big board x-coordinate.
            big_y (int): The big board y-coordinate.
            small_x (int): The small board x-coordinate.
            small_y (int): The small board y-coordinate.

        Returns:
            bool: True if the turn was successful, False otherwise.
        """
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
        """
        Checks if the specified small board is valid. A small board is valid if it was not taken by a player and is not full.

        Args:
            big_x (int): The big board x-coordinate of the small board.
            big_y (int): The big board y-coordinate of the small board.

        Returns:
            bool: True if the small board is valid, False otherwise.
        """
        return self.big_board[big_y, big_x] == self.EMPTY
    
    def check_small_win(self, player: int, big_x: int, big_y: int) -> bool:
        """
        Checks if the specified player has won the small board.

        Args:
            player (int): The player number.
            big_x (int): The big board x-coordinate of the small board.
            big_y (int): The big board y-coordinate of the small board.

        Returns:
            bool: True if the player has won the small board, False otherwise.
        """
        return self.big_board[big_y, big_x] == player
    
    def check_big_win(self, player: int) -> bool:
        """
        Checks if the specified player has won the big board.

        Args:
            player (int): The player number.

        Returns:
            bool: True if the player has won the big board, False otherwise.
        """
        return Board.check_board_win(self.big_board, player)
    
    def is_full(self) -> bool:
        """
        Checks if the board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return all(not self.check_small_board_valid(big_x, big_y) for big_x in range(3) for big_y in range(3))
    
    def valid_moves(self, next: tuple[int, int]) -> Generator[tuple[int, int, int, int], None, None] :
        """
        Generates valid moves for the specified small board. If next is (-1, -1) then for all small boards.

        Args:
            next (tuple[int, int]): The next board to play on.

        Returns:
            Generator[tuple[int, int, int, int], None, None]: A generator of valid moves.
        """
        return ((int(big_x), int(big_y), int(small_x), int(small_y))
                for big_y, big_x, small_y, small_x in np.argwhere(self.board == Board.EMPTY)
                if next in { (-1, -1), (big_x, big_y) } and self.big_board[big_y, big_x] == self.EMPTY)

    def to_string(self, *, last_turn: tuple[int, int, int, int] | None = None, next: tuple[int, int] | None = None) -> str:
        """
        Converts the board to a string representation.

        Args:
            last_turn (tuple[int, int, int, int] | None, optional): The last played move, used for coloring. Defaults to None.
            next (tuple[int, int] | None, optional): The next board to play on, used for coloring. Defaults to None.

        Returns:
            str: The string representation of the board.
        """
        last_big_x, last_big_y, last_small_x, last_small_y = last_turn if last_turn is not None else (-1, -1, -1, -1)

        big_str_map: dict[tuple[str, int], str] = {
            ("X", 0): "\\   /",
            ("X", 1):  "  X  ",
            ("X", 2):  "/   \\",
            ("O", 0): "⌈ ‾ ⌉",
            ("O", 1): "⎸   |",
            ("O", 2): "⌊ _ ⌋"
        }

        horizontal: str = "     " + "-" * 23 + "\n"

        result: str = "        1       2       3\n"
        result += "      1 2 3   1 2 3   1 2 3\n"
        result += horizontal
    
        for big_y in range(3):
            for small_y in range(3):
                result += str(big_y + 1) if small_y == 1 else " "
                result += f" {small_y + 1} | "

                for big_x in range(3):
                    if self.player_symbols[self.big_board[big_y, big_x]] in { "X", "O" }:
                        mapped: str = big_str_map[self.player_symbols[self.big_board[big_y, big_x]], small_y]
                        result += Fore.GREEN + mapped + Style.RESET_ALL if (big_x, big_y) == (last_big_x, last_big_y) else mapped
                        result += " | "
                        continue

                    board_str: list[str] = [self.player_symbols[cell]
                                            if (cell := self.board[big_y, big_x, small_y, small_x]) != self.EMPTY
                                                or next not in { (-1, -1), (big_x, big_y) } 
                                            else Fore.YELLOW + self.player_symbols[cell] + Style.RESET_ALL
                                            for small_x in range(3)]

                    if (big_x, big_y, small_y) == (last_big_x, last_big_y, last_small_y):
                        board_str[last_small_x] = Fore.GREEN + board_str[last_small_x] + Style.RESET_ALL

                    result += " ".join(board_str) + " | "

                result += "\n"

            result += horizontal

        return result

    def __str__(self) -> str:
        """
        Converts the board to a string representation.

        Returns:
            str: The string representation of the board.
        """
        return self.to_string()

    @staticmethod
    def check_board_win(board: NDArray[np.int8], player: int) -> bool:
        """
        Checks if the specified player has won a board.

        Args:
            board (NDArray[np.int8]): The board to check.
            player (int): The player number.

        Returns:
            bool: True if the player has won the board, False otherwise.
        """
        for i in range(3):
            if (board[i] == player).all() \
                or (board[:, i] == player).all() \
                or (np.diag(board) == player).all() \
                or (np.diag(np.fliplr(board)) == player).all():

                return True

        return False