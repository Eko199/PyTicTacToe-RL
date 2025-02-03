from .player import Player

class HumanPlayer(Player):
    def get_int_or_quit(self, prompt: str) -> int:
        entered: str = input(prompt)

        while not entered.isdigit():
            if entered.lower()[0] == "q":
                exit()

            print("Invalid input!")
            entered = input(prompt)

        return int(entered)

    def get_turn(self, next_x: int, next_y: int) -> tuple[int, int, int, int]:
        if next_x == -1:
            print("You can play anywhere!")
            big_x: int = self.get_int_or_quit("Enter big X: ")
            big_y: int = self.get_int_or_quit("Enter big Y: ")
        else:
            print(f"You must play in the ({next_x}, {next_y}) board!")
            big_x: int = next_x
            big_y: int = next_y

        small_x: int = self.get_int_or_quit("Enter small X: ")
        small_y: int = self.get_int_or_quit("Enter small Y: ")

        return big_x, big_y, small_x, small_y