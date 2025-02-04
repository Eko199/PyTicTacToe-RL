from typing import Callable

def input_or_quit(prompt: str = "") -> str:
    entered = input(prompt)

    if entered != "" and entered.lower()[0] == "q":
        exit()

    return entered

def cond_input_or_quit(condition: Callable[[str], bool], prompt: str = "",  error: str = "Invalid input! Please try again: "):
    entered: str = input_or_quit(prompt)

    while not condition(entered):
        entered = input_or_quit(error)

    return entered