from typing import Any
import argparse
from .game.game import Game
from .game.console_game import ConsoleGame
from .saving.save_manager import load_json
from .utils import cond_input_or_quit

async def main_menu(args: argparse.Namespace):
    game: Game | None = None

    while game is None:
        if args.test:
            game = ConsoleGame.create_game(test_mode=args.test)
            continue

        print("Welcome to Mega Tic Tac Toe! At any time you wish to quit, just type 'q'. What would you like to do?")
        print("1. New game")
        print("2. Load game")

        choice: str = cond_input_or_quit(lambda x: x.isdigit() and 1 <= int(x) <= 2, "", "Invalid input. Please try again (1 - 2): ")

        match int(choice):
            case 1:
                game = ConsoleGame.create_game(test_mode=args.test)
            case 2:
                game = await load_game()
            case _:
                print("An unexpected error occurred. Exiting application.")
                return
            
        if game is not None:
            await game.play()

async def load_game() -> Game | None:
    try:
        data: dict[str, Any] | None = await load_json()
        return ConsoleGame.load(data) if data is not None else None
    except OSError as e:
        print(e)
        
    return None
    