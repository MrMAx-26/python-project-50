from gendiff.formatters.json import get_json as json
from gendiff.formatters.plain import plain
from gendiff.formatters.stylish import stylish


def get_formatter(diff, formatter):
    if formatter == 'stylish':
        return stylish(diff)
    elif formatter == 'plain':
        return plain(diff)
    elif formatter == 'json':
        return json(diff)