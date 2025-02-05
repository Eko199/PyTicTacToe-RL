from .human_player import HumanPlayer
from ..game.board import Board

class ConsolePlayer(HumanPlayer):
    def get_int_or_quit(self, prompt: str) -> int | None:
        entered: str = input(prompt)

        while not entered.isdigit() or int(entered) < 1 or int(entered) > 3:
            if entered != "" and entered.lower()[0] == "q":
                return None

            print("Invalid input! (1 - 3)")
            entered = input(prompt)

        return int(entered)
    
    def get_coordinates(self, type: str, next: tuple[int, int], board: Board) -> tuple[int, int] | None:
        x: int | None = self.get_int_or_quit(f"Enter {type} X: ")

        if x is None:
            return None

        y: int | None = self.get_int_or_quit(f"Enter {type} Y: ")

        if y is None:
            return None
        
        return x - 1, y - 1
    
    def get_all_coordinates(self, next: tuple[int, int], board: Board) -> tuple[int, int, int, int] | None:
        if next == (-1, -1):
            print("You can play anywhere!")
            big_coord: tuple[int, int] | None = self.get_coordinates("big", next, board)

            if big_coord is None:
                return None
            
            big_x, big_y = big_coord
            
            while board.big_board[big_y, big_x] != Board.EMPTY:
                print(f"Big board ({big_x + 1}, {big_y + 1}) is already taken!")
                big_coord: tuple[int, int] | None = self.get_coordinates("big", next, board)

                if big_coord is None:
                    return None
                
                big_x, big_y = big_coord
        else:
            big_x, big_y = next
            print(f"You must play in the ({big_x + 1}, {big_y + 1}) board!")

        small_coord: tuple[int, int] | None = self.get_coordinates("small", next, board)

        if small_coord is None:
            return None
        
        small_x, small_y = small_coord
        return big_x, big_y, small_x, small_y

    def get_turn(self, next: tuple[int, int], board: Board) -> tuple[int, int, int, int] | None:
        coordinates: tuple[int, int, int, int] | None = self.get_all_coordinates(next, board)

        if coordinates is None:
            return None
        
        big_x, big_y, small_x, small_y = coordinates

        while board.board[big_y, big_x, small_y, small_x] != Board.EMPTY:
            coordinates: tuple[int, int, int, int] | None = self.get_all_coordinates(next, board)

            if coordinates is None:
                return None
            
            big_x, big_y, small_x, small_y = coordinates

        return coordinates