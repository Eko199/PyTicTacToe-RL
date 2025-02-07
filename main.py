import asyncio
import argparse
from src.main_menu import main_menu

def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="MegaTicTacToe", description="Play a game of Mega Tic Tac Toe!")
    parser.add_argument("--test", 
                        action="store_true", 
                        help="Run the game in test mode. This will allow you to play anywhere on the board and not to switch players.")

    args: argparse.Namespace = parser.parse_args()
    asyncio.run(main_menu(args))
    
if __name__ == "__main__":
    main()