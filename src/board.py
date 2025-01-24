import numpy as np
import numpy.typing as npt

class Board:
    def __init__(self):
        self.board: npt.NDArray[np.str_] = np.full((3, 3, 3, 3), " ")

    def play_turn(self, player: str, bigX: int, bigY: int, smallX: int, smallY: int) -> bool:
        if self.board[bigY, bigX, smallY, smallX] != " ":
            return False
        
        self.board[bigY, bigX, smallY, smallX] = player
        return True
    
    def check_small_win(self, player: str, bigX: int, bigY: int) -> bool:
        small_board: npt.NDArray[np.str_] = self.board[bigX, bigY]

        for i in range(3):
            if (small_board[i] == player).all() \
                or (small_board[:, i] == player).all() \
                or (np.diag(small_board) == player).all() \
                or (np.diag(np.fliplr(small_board)) == player).all():

                return True

        return False
    
    def check_big_win(self, player: str) -> bool:
        return False
    
    def is_full(self) -> bool:
        return False
    
    def print(self) -> None:
        print("-" * 41)

        for bigY in range(3):
            for smallY in range(3):
                print("|| ", end="")

                for bigX in range(3):
                    print(" | ".join(self.board[bigY, bigX, smallY]), end=" || ")

                print()

            print("-" * 41)