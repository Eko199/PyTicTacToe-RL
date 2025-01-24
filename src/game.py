from .board import Board

class Game:
    def __init__(self):
        self.player1: str = "O"
        self.player2: str = "X"
        self.current_player: str = self.player1
        self.board: Board = Board()
        self.winner: str | None = None

    # def play(self):
    #     while not self.board.is_full() and not self.winner:
    #         self.current_player.move(self.board)
    #         self.winner = self.board.get_winner()

    #         if self.current_player == self.player1:
    #             self.current_player = self.player2
    #         else:
    #             self.current_player = self.player1

    #     if not self.winner:
    #         print("It's a tie!")
    #     else:
    #         print(f"{self.winner} wins!")

    def print(self):
        self.board.print()