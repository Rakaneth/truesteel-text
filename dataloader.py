import json

def load_data(filename: str) -> dict:
    with open(f"data/{filename}") as f:
        return json.load(f)

GAME_DATA = load_data("chardata.json")