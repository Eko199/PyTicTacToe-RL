import os
from .training import MODELS_PATH

def get_agents() -> list[str]:
    return [f[:-4] for f in os.listdir(MODELS_PATH) if f.endswith(".zip")]

def choose_agent(agent_o: bool) -> str | None:
    pass