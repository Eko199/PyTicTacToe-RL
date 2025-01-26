from .board import Board

class Game:
    def __init__(self):
        self.player1: str = "O"
        self.player2: str = "X"

        self.board: Board = Board()
        self.next_x: int = -1
        self.next_y: int = -1

        self.current_player: str = self.player1
        self.winner: str | None = None
        self.play()

    def play(self) -> None:
        while not self.board.is_full() and not self.winner:
            self.print()
            self.play_turn()
            self.switch_player()

        self.print()

        if not self.winner:
            print("It's a tie!")
        else:
            print(f"{self.winner} wins!")

    def switch_player(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def get_turn_coordinates(self) -> tuple[int, int, int, int]:
        if self.next_x == -1:
            print("You can play anywhere!")
            bigX: int = int(input("Enter big X: "))
            bigY: int = int(input("Enter big Y: "))
        else:
            print(f"You must play in the ({self.next_x}, {self.next_y}) board!")
            bigX: int = self.next_x
            bigY: int = self.next_y

        smallX: int = int(input("Enter small X: "))
        smallY: int = int(input("Enter small Y: "))

        return bigX, bigY, smallX, smallY

    def play_turn(self) -> None:
        print(f"{self.current_player}'s turn!")
        (bigX, bigY, smallX, smallY) = self.get_turn_coordinates()

        if not self.board.play_turn(self.current_player, bigX, bigY, smallX, smallY):
            print("Invalid move! Try again.")
            return

        if self.board.check_small_win(self.current_player, bigX, bigY):
            print(f"{self.current_player} wins small board ({bigX},{bigY})!")

        if self.board.check_big_win(self.current_player):
            print(f"{self.current_player} wins the game!")
            self.winner = self.current_player

        if self.board.check_small_board_valid(smallX, smallY):
            self.next_x = smallX
            self.next_y = smallY
            return

        self.next_x = -1
        self.next_y = -1

    def print(self) -> None:
        self.board.print()