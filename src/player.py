class Player:
    def get_int_or_quit(self, prompt: str) -> int:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input (must be an integer)! Quitting game.")
            exit()

    def get_turn(self, next_x: int, next_y: int) -> tuple[int, int, int, int]:
        if next_x == -1:
            print("You can play anywhere!")
            bigX: int = self.get_int_or_quit("Enter big X: ")
            bigY: int = self.get_int_or_quit("Enter big Y: ")
        else:
            print(f"You must play in the ({next_x}, {next_y}) board!")
            bigX: int = next_x
            bigY: int = next_y

        smallX: int = self.get_int_or_quit("Enter small X: ")
        smallY: int = self.get_int_or_quit("Enter small Y: ")

        return bigX, bigY, smallX, smallY