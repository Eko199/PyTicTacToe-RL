import argparse
from src.game import Game
from src.players.player import Player
from src.players.human_player import HumanPlayer
from src.players.random_player import RandomPlayer

def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="MegaTicTacToe", description="Play a game of Mega Tic Tac Toe!")
    parser.add_argument("--test", 
                        action="store_true", 
                        help="Run the game in test mode. This will allow you to play anywhere on the board and to take no turns.")

    args: argparse.Namespace = parser.parse_args()

    print("Welcome to Mega Tic Tac Toe! At any time you wish to quit, just type 'q'. What would you like to play?")
    print("1. Play hot-seat multiplayer")
    print("2. Play against radomized actions bot")
    print("3. Play against trained AI")

    choice: str = input()

    while not choice.isdigit() or int(choice) < 1 or int(choice) > 3:
        if choice.lower()[0] == "q":
            exit()

        choice = input("Invalid input. Please try again (1-3): ")

    opponents: dict[int, Player] = {
        1: HumanPlayer(),
        2: RandomPlayer(),
        3: RandomPlayer()
    }

    game: Game = Game(opponents[int(choice)], test_mode=args.test)
    game.play()

if __name__ == "__main__":
    main()