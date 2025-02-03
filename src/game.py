from .board import Board
from .players.human_player import HumanPlayer, Player
from .players.random_player import RandomPlayer

class Game:
    def __init__(self, opponent: Player, *, test_mode: bool = False):
        self.test_mode: bool = test_mode
        self.player1: int = 1
        self.player2: int = 2

        self.board: Board = Board()
        self.next_x: int = -1
        self.next_y: int = -1

        self.players: dict[int, Player] = {
            self.player1: HumanPlayer(),
            self.player2: opponent
        }

        self.current_player: int = self.player1
        self.winner: int | None = None

    def play(self) -> None:
        while not self.board.is_full() and not self.winner:
            self.print()
            self.play_turn()
            if not self.test_mode:
                self.switch_player()

        self.print()
        print(f"{self.winner} wins!" if self.winner else "It's a tie!")

    def switch_player(self) -> None:
        self.current_player = self.player1 + self.player2 - self.current_player

    def play_turn(self) -> None:
        print(f"{self.board.player_symbols[self.current_player]}'s turn!")
        (big_x, big_y, small_x, small_y) = self.players[self.current_player].get_turn(self.next_x, self.next_y)

        while not self.board.play_turn(self.current_player, big_x, big_y, small_x, small_y):
            if isinstance(self.players[self.current_player], HumanPlayer):
                print("Invalid move! Try again.")
                (big_x, big_y, small_x, small_y) = self.players[self.current_player].get_turn(self.next_x, self.next_y)
            else:
                (big_x, big_y, small_x, small_y) = RandomPlayer().get_turn(self.next_x, self.next_y)

        if self.board.check_small_win(self.current_player, big_x, big_y):
            print(f"{self.board.player_symbols[self.current_player]} wins small board ({big_x},{big_y})!")

            if self.board.check_big_win(self.current_player):
                self.winner = self.current_player
                print(f"{self.board.player_symbols[self.winner]} wins the game!")

        if not self.test_mode and self.board.check_small_board_valid(small_x, small_y):
            self.next_x = small_x
            self.next_y = small_y
            return

        self.next_x = -1
        self.next_y = -1

    def print(self) -> None:
        self.board.print()