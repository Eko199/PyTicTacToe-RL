"""
This module contains the ConsolePlayer class, 
which represents a human player interacting through the console.
"""

from src.players.human_player import HumanPlayer
from src.tictactoe.board import Board

class ConsolePlayer(HumanPlayer):
    """
    A human player that interacts through the console.
    """
    def get_int_or_quit(self, prompt: str) -> int | None:
        """
        Prompts the user for an integer input and allows them to quit.

        Args:
            prompt (str): The prompt message.

        Returns:
            int | None: The entered integer or None if the user quits.
        """
        entered: str = input(prompt)

        while not entered.isdigit() or int(entered) < 1 or int(entered) > 3:
            if entered != "" and entered.lower()[0] == "q":
                return None

            print("Invalid input! (1 - 3)")
            entered = input(prompt)

        return int(entered)

    def get_coordinates(self, coord_type: str) -> tuple[int, int] | None:
        """
        Prompts the user for coordinates input.

        Args:
            coord_type (str): The type of coordinates (big or small).

        Returns:
            tuple[int, int] | None: The entered coordinates or None if the user quits.
        """
        x: int | None = self.get_int_or_quit(f"Enter {coord_type} X: ")

        if x is None:
            return None

        y: int | None = self.get_int_or_quit(f"Enter {coord_type} Y: ")

        if y is None:
            return None

        return x - 1, y - 1

    def get_all_coordinates(self,
                            next_board: tuple[int, int],
                            board: Board) -> tuple[int, int, int, int] | None:
        """
        Prompts the user for all coordinates needed for a move.

        Args:
            next_board (tuple[int, int]): The coordinates of the small board to play on.
            board (Board): The current game board.

        Returns:
            tuple[int, int, int, int] | None: The entered coordinates or None if the user quits.
        """
        if next_board == (-1, -1):
            print("You can play anywhere!")
            big_coord: tuple[int, int] | None = self.get_coordinates("big")

            if big_coord is None:
                return None

            big_x, big_y = big_coord

            while board.big_board[big_y, big_x] != Board.EMPTY:
                print(f"Big board ({big_x + 1}, {big_y + 1}) is already taken!")
                big_coord: tuple[int, int] | None = self.get_coordinates("big")

                if big_coord is None:
                    return None

                big_x, big_y = big_coord
        else:
            big_x, big_y = next_board
            print(f"You must play in the ({big_x + 1}, {big_y + 1}) board!")

        small_coord: tuple[int, int] | None = self.get_coordinates("small")

        if small_coord is None:
            return None

        small_x, small_y = small_coord
        return big_x, big_y, small_x, small_y

    def get_turn(self,
                 next_board: tuple[int, int],
                 board: Board) -> tuple[int, int, int, int] | None:
        """
        Gets the user's turn until a valid one is entered.

        Args:
            next_board (tuple[int, int]): The next board to play on.
            board (Board): The current game board.

        Returns:
            tuple[int, int, int, int] | None: 
                The coordinates of the selected move or None if the user quits.
        """
        coordinates: tuple[int, int, int, int] | None = self.get_all_coordinates(next_board, board)

        if coordinates is None:
            return None

        big_x, big_y, small_x, small_y = coordinates

        while board.board[big_y, big_x, small_y, small_x] != Board.EMPTY:
            print("Invalid move!")
            coordinates: tuple[int, int, int, int] | None = \
                self.get_all_coordinates(next_board, board)

            if coordinates is None:
                return None

            big_x, big_y, small_x, small_y = coordinates

        return coordinates
