from .game import Game
from ..players.player import Player
from ..players.console_player import ConsolePlayer
from ..players.random_player import RandomPlayer
from ..players.ai_player import AIPlayer
from ..utils import cond_input_or_quit

class ConsoleGame(Game):
    def __init__(self, mode: int, *, test_mode: bool = False):
        super().__init__(mode, test_mode=test_mode)

        opponents: dict[int, Player] = {
            1: ConsolePlayer(),
            2: AIPlayer("agent1"),
            3: RandomPlayer()
        }
        
        self.players: dict[int, Player] = {
            self.player1: ConsolePlayer(),
            self.player2: opponents[mode]
        }

    def play_turn(self) -> tuple[int, int, int, int]:
        print(f"{self.board.player_symbols[self.current_player]}'s turn!")
        return super().play_turn()

    def save(self) -> None:
        choice = cond_input_or_quit(lambda x: x != "" and x.lower()[0] in "yn", 
                                    "Would you like to save the game? (y/n) ", 
                                    "Invalid input!\nWould you like to save the game? (y/n) ")

        if choice == "n":
            return
        
        super().save()

    def play(self) -> None:
        last_turn: tuple[int, int, int, int] | None = None

        while not self.board.is_full() and not self.winner:
            self.render(last_turn)

            try:
                last_turn = self.play_turn()
            except RuntimeError as e:
                print(e)
                self.save()
                exit()
            
            if not self.test_mode:
                self.switch_player()

        self.render(last_turn)
        print(f"{self.board.player_symbols[self.winner]} wins the game!" if self.winner else "It's a tie!")
    
    def invalid_move(self) -> None:
        print("Invalid move! Try again.")

    def render(self, last_turn: tuple[int, int, int, int] | None = None) -> None:
        print(self.board.to_string(last_turn))

    def successful_save(self):
        return print("Game saved successfully!")