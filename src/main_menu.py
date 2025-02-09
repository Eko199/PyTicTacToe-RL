"""
This module contains the main menu for the Mega Tic Tac Toe game.
"""

from typing import Any
import argparse
from src.tictactoe.game import Game
from src.tictactoe.console_game import ConsoleGame
from src.saving.save_manager import load_json
from src.agent.training import train_model
from src.utils import cond_input_or_quit

async def main_menu(args: argparse.Namespace):
    """
    Displays the main menu and handles user input.

    Args:
        args (argparse.Namespace): The command-line arguments.
    """
    game: Game | None = None

    while game is None:
        if args.test:
            game = ConsoleGame.create_game(test_mode=args.test)
            continue

        print("Welcome to Mega Tic Tac Toe! At any time you wish to quit, just type 'q'. \
              What would you like to do?")
        print("1. New game")
        print("2. Load game")
        print("3. Train model")

        choice: str = cond_input_or_quit(lambda x: x.isdigit() and 1 <= int(x) <= 3,
                                         "",
                                         "Invalid input. Please try again (1 - 3): ")

        match int(choice):
            case 1:
                game = ConsoleGame.create_game(test_mode=args.test)
            case 2:
                game = await load_game()
            case 3:
                train_menu()
            case _:
                print("An unexpected error occurred. Exiting application.")
                return

        if game is not None:
            await game.play()

async def load_game() -> Game | None:
    """
    Loads a saved game.

    Returns:
        Game | None: The loaded game or None if loading failed.
    """
    try:
        data: dict[str, Any] | None = await load_json()
        return ConsoleGame.load(data) if data is not None else None
    except OSError as e:
        print(e)

    return None

def train_menu() -> None:
    """
    Displays the training menu and handles user input for training a model.
    """
    name: str = input("Enter model name: ")
    steps: int = int(cond_input_or_quit(lambda x: x.isdigit() and int(x) > 0,
                                        "Enter training steps (3M+ recommended): "))

    is_o: bool = cond_input_or_quit(lambda x: x.lower() in { "1", "2", "x", "o" },
                                    "Train as O (1st) or X (2nd)? ") in "1o"

    train_model(name, steps, is_o)
    print("Training completed!")
