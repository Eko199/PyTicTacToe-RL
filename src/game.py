from typing import Any
import numpy as np
from .board import Board
from .players.human_player import HumanPlayer, Player
from .players.random_player import RandomPlayer
from .saving.save_manager import save_json

class Game:
    def __init__(self, mode: int, *, test_mode: bool = False):
        self.test_mode: bool = test_mode
        self.player1: int = 1
        self.player2: int = 2

        self.board: Board = Board()
        self.next_x: int = -1
        self.next_y: int = -1

        opponents: dict[int, Player] = {
            1: HumanPlayer(),
            2: RandomPlayer(),
            3: RandomPlayer()
        }

        self.mode = mode
        self.players: dict[int, Player] = {
            self.player1: HumanPlayer(),
            self.player2: opponents[mode]
        }

        self.current_player: int = self.player1
        self.winner: int | None = None

    def play(self) -> None:
        last_turn: tuple[int, int, int, int] | None = None

        while not self.board.is_full() and not self.winner:
            self.print(last_turn)
            last_turn = self.play_turn()
            
            if not self.test_mode:
                self.switch_player()

        self.print(last_turn)
        print(f"{self.winner} wins!" if self.winner else "It's a tie!")

    def switch_player(self) -> None:
        self.current_player = self.player1 + self.player2 - self.current_player

    def play_turn(self) -> tuple[int, int, int, int]:
        print(f"{self.board.player_symbols[self.current_player]}'s turn!")
        turn: tuple[int, int, int, int] | None = self.players[self.current_player].get_turn(self.next_x, self.next_y)

        if turn is None:
            self.save()
            exit()
        
        big_x, big_y, small_x, small_y = turn

        while not self.board.play_turn(self.current_player, big_x, big_y, small_x, small_y):
            if isinstance(self.players[self.current_player], HumanPlayer):
                print("Invalid move! Try again.")
                turn = self.players[self.current_player].get_turn(self.next_x, self.next_y)

                if turn is None:
                    self.save()
                    exit()
                
                big_x, big_y, small_x, small_y = turn
            else:
                big_x, big_y, small_x, small_y = RandomPlayer().get_turn(self.next_x, self.next_y)

        if self.board.check_small_win(self.current_player, big_x, big_y):
            print(f"{self.board.player_symbols[self.current_player]} wins small board ({big_x},{big_y})!")

            if self.board.check_big_win(self.current_player):
                self.winner = self.current_player
                print(f"{self.board.player_symbols[self.winner]} wins the game!")

        if not self.test_mode and self.board.check_small_board_valid(small_x, small_y):
            self.next_x = small_x
            self.next_y = small_y
            return big_x, big_y, small_x, small_y

        self.next_x = -1
        self.next_y = -1

        return big_x, big_y, small_x, small_y

    def print(self, last_turn: tuple[int, int, int, int] | None = None) -> None:
        self.board.print(last_turn)

    def save(self) -> None:
        choice = input("Would you like to save the game? (y/n) ").lower()[0]

        while choice not in { "y", "n" }:
            print("Invalid input!")
            choice = input("Would you like to save the game? (y/n) ").lower()[0]

        if choice == "n":
            return
        
        data: dict[str, Any] = {
            "board": self.board.board.tolist(), 
            "big_board": self.board.big_board.tolist(), 
            "current_player": self.current_player,
            "next": (self.next_x, self.next_y),
            "mode": self.mode
        }
        
        try:
            save_json(data)
            print("Game saved successfully!")
        except OSError as e:
            print(e)

    @classmethod
    def load(cls, data: dict[str, Any]):
        game = cls(data["mode"])
        game.board.board = np.array(data["board"])
        game.board.big_board = np.array(data["big_board"])
        game.current_player = data["current_player"]
        game.next_x, game.next_y = data["next"]

        return game