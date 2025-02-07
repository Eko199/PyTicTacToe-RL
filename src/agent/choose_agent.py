import os
from .training import MODELS_PATH
from ..utils import cond_input_or_quit

def get_agents(prefix: str = "") -> list[str]:
    return [f[:-4] for f in os.listdir(MODELS_PATH) if f.endswith(".zip") and f.startswith(prefix)]

def choose_agent(agent_o: bool) -> str:
    prefix: str = "o_" if agent_o else "x_"
    agents: list[str] = get_agents(prefix)

    if len(agents) == 0:
        input("There are no trained agents currently! Press any key to go back. ")
        return ""

    print("0. Back")

    for i, name in enumerate(agents):
        print(f"{i+1}. {name[2:]}")

    choice: int = int(cond_input_or_quit(lambda x: x.isdigit() and 0 <= int(x) <= len(agents), "", f"Invalid input! (0 - {len(agents)})"))
    return agents[choice - 1] if choice != 0 else ""