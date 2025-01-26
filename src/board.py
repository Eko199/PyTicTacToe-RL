import numpy as np
import numpy.typing as npt

class Board:
    EMPTY: str = " "
    FULL: str = "F"

    def __init__(self):
        self.board: npt.NDArray[np.str_] = np.full((3, 3, 3, 3), self.EMPTY)
        self.big_board: npt.NDArray[np.str_] = np.full((3, 3), self.EMPTY)

    def play_turn(self, player: str, bigX: int, bigY: int, smallX: int, smallY: int) -> bool:
        current_board: npt.NDArray[np.str_] = self.board[bigY, bigX]

        if self.big_board[bigY, bigX] != self.EMPTY or current_board[smallY, smallX] != self.EMPTY:
            return False
        
        current_board[smallY, smallX] = player

        if Board.check_board_win(current_board, player):
            self.big_board[bigY, bigX] = player
        elif (current_board != self.EMPTY).all():
            self.big_board[bigY, bigX] = self.FULL

        return True
    
    def check_small_board_valid(self, bigX: int, bigY: int) -> bool:
        return self.big_board[bigY, bigX] == self.EMPTY
    
    def check_small_win(self, player: str, bigX: int, bigY: int) -> bool:
        return self.big_board[bigY, bigX] == player
    
    def check_big_win(self, player: str) -> bool:
        return Board.check_board_win(self.big_board, player)
    
    def is_full(self) -> bool:
        return all(not self.check_small_board_valid(bigX, bigY) for bigX in range(3) for bigY in range(3))
    
    def print(self) -> None:
        print("-" * 41)

        for bigY in range(3):
            for smallY in range(3):
                print("|| ", end="")

                for bigX in range(3):
                    print(" | ".join(self.board[bigY, bigX, smallY]), end=" || ")

                print()

            print("-" * 41)

    @staticmethod
    def check_board_win(board: npt.NDArray[np.str_], player: str) -> bool:
        for i in range(3):
            if (board[i] == player).all() \
                or (board[:, i] == player).all() \
                or (np.diag(board) == player).all() \
                or (np.diag(np.fliplr(board)) == player).all():

                return True

        return False