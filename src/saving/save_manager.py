"""
This module contains functions for saving and loading game state to and from JSON files.
"""

import os
import json
from typing import Any
import aiofiles

SAVES_PATH: str = "saves"

def get_save_file_name() -> str:
    """
    Prompts the user for a save file name.

    Returns:
        str: The save file name.
    """
    name = input("Enter file name: ")

    if not name.endswith(".json"):
        name += ".json"

    return name

async def serialize_to(file_name: str, object: dict[str, Any]) -> None:
    """
    Serializes a dictionary to a JSON file.

    Args:
        file_name (str): The name of the save file.
        object (dict[str, Any]): The dictionary to serialize.
    """
    if not os.path.exists(SAVES_PATH):
        os.mkdir(SAVES_PATH)

    content: str = json.dumps(object)

    if not file_name.endswith(".json"):
        file_name += ".json"

    async with aiofiles.open(os.path.join(SAVES_PATH, file_name), "w") as file:
        await file.write(content)

async def deserialize_from(file_name: str) -> dict[str, Any] | None:
    """
    Deserializes a dictionary from a JSON file.

    Args:
        file_name (str): The name of the save file.

    Returns:
        dict[str, Any] | None: The deserialized dictionary or None if the file does not exist.
    """
    if not file_name.endswith(".json"):
        file_name += ".json"

    path: str = os.path.join(SAVES_PATH, file_name)

    if not os.path.exists(path):
        print("File doesn't exist.")
        return None

    async with aiofiles.open(path, "r") as file:
        content: str = await file.read()

    return json.loads(content)

async def save_json(object: dict[str, Any], file_name: str | None = None) -> None:
    """
    Saves a dictionary to a JSON file.

    Args:
        object (dict[str, Any]): The dictionary to save.
        file_name (str | None, optional): The name of the save file. Defaults to None.
    """
    await serialize_to(get_save_file_name() if file_name is None else file_name, object)

async def load_json() -> dict[str, Any] | None:
    """
    Loads a dictionary from a JSON file.

    Returns:
        dict[str, Any] | None: The loaded dictionary or None if the file does not exist.
    """
    return await deserialize_from(get_save_file_name())
