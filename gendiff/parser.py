import json
import yaml


def is_json(file) -> bool:
    return str(file).endswith('.json')


def is_yaml(file) -> bool:
    return str(file).endswith('.yml')


def reading_and_parsing(file) -> dict:
    data = {}
    if is_json(file):
        data = json.load(open(file))
    if is_yaml(file):
        data = yaml.load(open(file), Loader=yaml.SafeLoader)
    return data