import json


def reading_and_parsing(file) -> dict:
    data = json.load(open(file))
    return data