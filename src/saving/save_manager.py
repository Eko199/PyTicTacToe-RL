import os
import json
from typing import Any

SAVES_PATH: str = "saves"

def get_save_file_name() -> str:
    name = input("Enter file name: ")

    if not name.endswith(".json"):
        name += ".json"

    return os.path.join(SAVES_PATH, name)

def serialize_to(file_name: str, object: dict[str, Any]) -> None:
    if not os.path.exists(SAVES_PATH):
        os.mkdir(SAVES_PATH)

    with open(file_name, "w") as file:
        json.dump(object, file)

def deserialize_from(file_name: str) -> dict[str, Any] | None:
    if not os.path.exists(file_name):
        print("File doesn't exist.")
        return None

    with open(file_name, "r") as file:
        return json.load(file)

def save_json(object: dict[str, Any]) -> None:
    serialize_to(get_save_file_name(), object)

def load_json() -> dict[str, Any] | None:
    return deserialize_from(get_save_file_name())