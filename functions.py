import aiofiles
import json

async def read_json_file(filename: str) -> dict:
    try:
        async with aiofiles.open(filename, 'r', encoding='utf-8') as file:
            content = await file.read()
            data = json.loads(content)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"File '{filename}' is not a valid JSON file.")


