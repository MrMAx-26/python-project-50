from gendiff.formatters.json import get_json as json
from gendiff.formatters.plain import format_plain
from gendiff.formatters.stylish import format_stylish


def format(diff, formatter):
    if formatter == 'stylish':
        return format_stylish(diff)
    elif formatter == 'plain':
        return format_plain(diff)
    elif formatter == 'json':
        return json(diff)