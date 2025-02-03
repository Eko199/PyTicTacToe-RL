from typing import Any
import argparse
from .game import Game
from .saving.save_manager import load_json
from .utils import input_or_quit

def main_menu(args: argparse.Namespace):
    game: Game | None = None

    while game is None:
        print("Welcome to Mega Tic Tac Toe! At any time you wish to quit, just type 'q'. What would you like to do?")
        print("1. New game")
        print("2. Load game")

        choice: str = input_or_quit()

        while not choice.isdigit() or int(choice) < 1 or int(choice) > 2:
            choice = input_or_quit("Invalid input. Please try again (1-2): ")

        match int(choice):
            case 1:
                game = new_game(args)
            case 2:
                game = load_game()
            case _:
                print("An unexpected error occurred. Exiting application.")
                return
            
        if game is not None:
            game.play()


def new_game(args: argparse.Namespace) -> Game:
    print("1. Play hot-seat multiplayer")
    print("2. Play against radomized actions bot")
    print("3. Play against trained AI")

    choice: str = input_or_quit()

    while not choice.isdigit() or int(choice) < 1 or int(choice) > 3:
        choice = input_or_quit("Invalid input. Please try again (1-3): ")

    return Game(int(choice), test_mode=args.test)

def load_game() -> Game | None:
    try:
        data: dict[str, Any] | None = load_json()
        return Game.load(data) if data is not None else None
    except OSError as e:
        print(e)
        
    return None
    