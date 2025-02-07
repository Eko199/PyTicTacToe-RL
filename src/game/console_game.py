from .game import Game
from ..players.player import Player
from ..players.console_player import ConsolePlayer
from ..players.random_player import RandomPlayer
from ..players.ai_player import AIPlayer
from ..agent.choose_agent import choose_agent
from ..utils import cond_input_or_quit

class ConsoleGame(Game):
    def __init__(self, mode: int, *, test_mode: bool = False, is_o: bool = True, auto_save: bool = True, agent_name: str = ""):
        super().__init__(mode, test_mode=test_mode, auto_save=auto_save, agent_name=agent_name)

        opponents: dict[int, Player] = {
            1: ConsolePlayer(),
            2: RandomPlayer(),
            3: AIPlayer(agent_name) if agent_name != "" else RandomPlayer()
        }
        
        self.players: dict[int, Player] = {
            self.player1: ConsolePlayer() if is_o else opponents[mode],
            self.player2: opponents[mode] if is_o else ConsolePlayer()
        }

    async def play_turn(self) -> tuple[int, int, int, int]:
        print(f"{self.board.player_symbols[self.current_player]}'s turn!")
        return await super().play_turn()

    async def save(self, file_name: str | None = None) -> None:
        choice = cond_input_or_quit(lambda x: x != "" and x.lower()[0] in "yn", 
                                    "Would you like to save the game? (y/n) ", 
                                    "Invalid input!\nWould you like to save the game? (y/n) ")

        if choice == "n":
            return
        
        await super().save(file_name)

    async def play(self) -> None:
        last_turn: tuple[int, int, int, int] | None = None

        while not self.board.is_full() and not self.winner:
            self.render(last_turn)

            try:
                last_turn = await self.play_turn()
            except RuntimeError as e:
                print(e)
                await self.save()
                exit()

        self.render(last_turn)
        print(f"{self.board.player_symbols[self.winner]} wins the game!" if self.winner else "It's a tie!")
    
    def invalid_move(self) -> None:
        print("Invalid move! Try again.")

    def render(self, last_turn: tuple[int, int, int, int] | None = None) -> None:
        print(self.board.to_string(last_turn=last_turn, next=self.next))

    def successful_save(self) -> None:
        return print("Game saved successfully!")
    
    @classmethod
    def create_game(cls, *, test_mode: bool = False):
        agent_name: str = ""

        while agent_name == "":
            print("Choose gamemode:")
            print("1. Play hot-seat multiplayer")
            print("2. Play against radomized actions bot")
            print("3. Play against trained AI")

            mode: int = int(cond_input_or_quit(lambda x: x.isdigit() and 1 <= int(x) <= 3, "", "Invalid input. Please try again (1 - 3): "))
            is_o: bool = cond_input_or_quit(lambda x: x.lower() in { "o", "x", "1", "2" }, "Play as O (1st) or X (2nd)? ", "Invalid input! O or X: ") in "o1"

            if mode != 3:
                break

            agent_name: str = choose_agent(not is_o)

        return cls(mode, test_mode=test_mode, is_o=is_o, agent_name=agent_name)