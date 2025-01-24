from .board import Board

class Game:
    def __init__(self):
        self.player1: str = "O"
        self.player2: str = "X"
        self.current_player: str = self.player1
        self.board: Board = Board()
        self.winner: str | None = None
        self.play()

    def play(self):
        while not self.board.is_full() and not self.winner:
            self.print()
            self.play_turn()
            #self.winner = self.board.get_winner()

            if self.current_player == self.player1:
                self.current_player = self.player2
            else:
                self.current_player = self.player1

        if not self.winner:
            print("It's a tie!")
        else:
            print(f"{self.winner} wins!")

    def switch_player(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play_turn(self) -> None:
        bigX: int = int(input("Enter big X: "))
        bigY: int = int(input("Enter big Y: "))
        smallX: int = int(input("Enter small X: "))
        smallY: int = int(input("Enter small Y: "))

        if not self.board.play_turn(self.current_player, bigX, bigY, smallX, smallY):
            print("Invalid move!")
            return

        if self.board.check_small_win(self.current_player, bigX, bigY):
            print(f"{self.current_player} wins the small board!")
            #self.board.big_board[bigY, bigX] = self.current_player

        if self.board.check_big_win(self.current_player):
            print(f"{self.current_player} wins the game!")
            self.winner = self.current_player

        self.switch_player()

    def print(self):
        self.board.print()