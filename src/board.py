import numpy as np
import numpy.typing as npt

class Board:
    EMPTY: int = 0
    FULL: int = -1

    def __init__(self, player1: str = "X", player2: str = "O"):
        self.board: npt.NDArray[np.int8] = np.full((3, 3, 3, 3), self.EMPTY)
        self.big_board: npt.NDArray[np.int8] = np.full((3, 3), self.EMPTY)

        self.player_symbols: dict[int, str] = {
            self.EMPTY: ".",
            1: player1,
            2: player2
        }

    def play_turn(self, player: int, big_x: int, big_y: int, small_x: int, small_y: int) -> bool:
        if not { big_x, big_y, small_x, small_y } <= { 0, 1, 2 }:
            return False

        current_board: npt.NDArray[np.int8] = self.board[big_y, big_x]

        if self.big_board[big_y, big_x] != self.EMPTY or current_board[small_y, small_x] != self.EMPTY:
            return False
        
        current_board[small_y, small_x] = player

        if Board.check_board_win(current_board, player):
            self.big_board[big_y, big_x] = player
        elif (current_board != self.EMPTY).all():
            self.big_board[big_y, big_x] = self.FULL

        return True
    
    def check_small_board_valid(self, bigX: int, bigY: int) -> bool:
        return self.big_board[bigY, bigX] == self.EMPTY
    
    def check_small_win(self, player: int, bigX: int, bigY: int) -> bool:
        return self.big_board[bigY, bigX] == player
    
    def check_big_win(self, player: int) -> bool:
        return Board.check_board_win(self.big_board, player)
    
    def is_full(self) -> bool:
        return all(not self.check_small_board_valid(bigX, bigY) for bigX in range(3) for bigY in range(3))
    
    def print2(self) -> None:
        print("-" * 41)

        for bigY in range(3):
            for smallY in range(3):
                print("|| ", end="")

                for bigX in range(3):
                    print(" | ".join([self.player_symbols[cell] for cell in self.board[bigY, bigX, smallY]]), end=" || ")

                print()

            print("-" * 41)

    def print(self) -> None:
        print("-" * 25)

        for bigY in range(3):
            for smallY in range(3):
                print("| ", end="")

                for bigX in range(3):
                    print(" ".join([self.player_symbols[cell] for cell in self.board[bigY, bigX, smallY]]), end=" | ")

                print()

            print("-" * 25)

    @staticmethod
    def check_board_win(board: npt.NDArray[np.int8], player: int) -> bool:
        for i in range(3):
            if (board[i] == player).all() \
                or (board[:, i] == player).all() \
                or (np.diag(board) == player).all() \
                or (np.diag(np.fliplr(board)) == player).all():

                return True

        return False