"""
This module contains utility functions for input handling.
"""

import sys
from typing import Callable

def input_or_quit(prompt: str = "") -> str:
    """
    Prompts the user for input and allows them to quit if "q" is entered.

    Args:
        prompt (str, optional): The prompt message. Defaults to "".

    Returns:
        str: The entered input.
    """
    entered = input(prompt)

    if entered != "" and entered.lower()[0] == "q":
        sys.exit()

    return entered

def cond_input_or_quit(condition: Callable[[str], bool],
                       prompt: str = "",
                       error: str = "Invalid input! Please try again: ") -> str:
    """
    Prompts the user for input until it satisfies a condition and allows them to quit.

    Args:
        condition (Callable[[str], bool]): The condition predicate that the input must satisfy.
        prompt (str, optional): The prompt message. Defaults to "".
        error (str, optional): The error message for invalid input. 
                               Defaults to "Invalid input! Please try again: ".

    Returns:
        str: The entered input that satisfies the condition.
    """
    entered: str = input_or_quit(prompt)

    while not condition(entered):
        entered = input_or_quit(error)

    return entered
