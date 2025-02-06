import os
import json
import aiofiles
from typing import Any

SAVES_PATH: str = "saves"

def get_save_file_name() -> str:
    name = input("Enter file name: ")

    if not name.endswith(".json"):
        name += ".json"

    return name

async def serialize_to(file_name: str, object: dict[str, Any]) -> None:
    if not os.path.exists(SAVES_PATH):
        os.mkdir(SAVES_PATH)

    content: str = json.dumps(object)

    if not file_name.endswith(".json"):
        file_name += ".json"


    async with aiofiles.open(os.path.join(SAVES_PATH, file_name), "w") as file:
        await file.write(content)

async def deserialize_from(file_name: str) -> dict[str, Any] | None:
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
    await serialize_to(get_save_file_name() if file_name is None else file_name, object)

async def load_json() -> dict[str, Any] | None:
    return await deserialize_from(get_save_file_name())