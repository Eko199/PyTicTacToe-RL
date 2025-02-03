def input_or_quit(prompt: str = "") -> str:
    entered = input(prompt)

    if entered.lower()[0] == "q":
        exit()

    return entered