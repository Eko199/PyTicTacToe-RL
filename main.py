import argparse
from src.game import Game

def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="MegaTicTacToe", description="Play a game of Mega Tic Tac Toe!")
    parser.add_argument("--test", action="store_true", help="Run the game in test mode. This will allow you to play anywhere on the board and to take no turns.")

    args: argparse.Namespace = parser.parse_args()

    game: Game = Game(test_mode=args.test)
    game.print()

if __name__ == "__main__":
    main()