from .player import Player

class HumanPlayer(Player):
    def get_int_or_quit(self, prompt: str) -> int | None:
        entered: str = input(prompt)

        while not entered.isdigit():
            if entered.lower()[0] == "q":
                return None

            print("Invalid input!")
            entered = input(prompt)

        return int(entered)

    def get_turn(self, next_x: int, next_y: int) -> tuple[int, int, int, int] | None:
        if next_x == -1:
            print("You can play anywhere!")
            big_x: int | None = self.get_int_or_quit("Enter big X: ")

            if big_x is None:
                return None

            big_y: int | None = self.get_int_or_quit("Enter big Y: ")

            if big_y is None:
                return None
        else:
            print(f"You must play in the ({next_x}, {next_y}) board!")
            big_x: int | None = next_x
            big_y: int | None = next_y

        small_x: int | None = self.get_int_or_quit("Enter small X: ")

        if small_x is None:
            return None

        small_y: int | None = self.get_int_or_quit("Enter small Y: ")

        if small_y is None:
            return None

        return big_x, big_y, small_x, small_y