import numpy as np
import numpy.typing as npt

class Board:
    def __init__(self):
        self.board: npt.NDArray[np.str_] = np.full((3, 3, 3, 3), " ")

    def play_turn(self, player: str, bigX: int, bigY: int, smallX: int, smallY: int) -> bool:
        if self.board[bigX, bigY, smallX, smallY] != " ":
            return False
        
        self.board[bigX, bigY, smallX, smallY] = player
        return True
    
    def check_small_win(self, player: str, bigX: int, bigY: int) -> bool:
        small_board: npt.NDArray[np.str_] = self.board[bigX, bigY]

        for i in range(3):
            if np.all(small_board[i] == player) \
                or np.all(small_board[:, i] == player) \
                or np.all(np.diag(small_board) == player) \
                or np.all(np.diag(np.fliplr(small_board)) == player):

                return True

        return False
    
    def print(self) -> None:
        for bigX in range(3):
            for smallX in range(3):
                for bigY in range(3):
                    print(" | ".join(self.board[bigX, bigY, smallX]), end=" || ")
                print()
            print("-" * 40)