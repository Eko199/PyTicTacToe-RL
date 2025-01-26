from .board import Board
from .player import Player

class Game:
    def __init__(self, *, test_mode: bool = False):
        self.test_mode: bool = test_mode
        self.player1: str = "O"
        self.player2: str = "X"

        self.board: Board = Board()
        self.next_x: int = -1
        self.next_y: int = -1

        self.players: dict[str, Player] = {
            self.player1: Player(),
            self.player2: Player()
        }

        self.current_player: str = self.player1
        self.winner: str | None = None

    def play(self) -> None:
        while not self.board.is_full() and not self.winner:
            self.print()
            if self.play_turn() and not self.test_mode:
                self.switch_player()

        self.print()
        print(f"{self.winner} wins!" if self.winner else "It's a tie!")

    def switch_player(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play_turn(self) -> bool:
        print(f"{self.current_player}'s turn!")
        (bigX, bigY, smallX, smallY) = self.players[self.current_player].get_turn(self.next_x, self.next_y)

        if not self.board.play_turn(self.current_player, bigX, bigY, smallX, smallY):
            print("Invalid move! Try again.")
            return False

        if self.board.check_small_win(self.current_player, bigX, bigY):
            print(f"{self.current_player} wins small board ({bigX},{bigY})!")

            if self.board.check_big_win(self.current_player):
                print(f"{self.current_player} wins the game!")
                self.winner = self.current_player

        if not self.test_mode and self.board.check_small_board_valid(smallX, smallY):
            self.next_x = smallX
            self.next_y = smallY
            return True

        self.next_x = -1
        self.next_y = -1
        return True

    def print(self) -> None:
        self.board.print()