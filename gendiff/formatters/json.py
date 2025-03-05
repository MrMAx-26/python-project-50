from json import dumps


def get_json(diff):
    return dumps(diff, indent=4)