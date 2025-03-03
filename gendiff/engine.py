from gendiff.formatters.stylish import stylish


def get_diff(file1, file2):
    diff = {}
    keys = sorted(set(file1.keys()).union(set(file2.keys())))

    for key in keys:
        if key not in file1:
            diff[key] = {'status': 'added', 'value': file2[key]}
        elif key not in file2:
            diff[key] = {'status': 'removed', 'value': file1[key]}
        elif isinstance(file1[key], dict) and isinstance(file2[key], dict):
            diff[key] = {'status': 'nested', 
                'value': get_diff(file1[key], file2[key])}
        elif file1[key] == file2[key]:
            diff[key] = {'status': 'unchanged', 'value': file1[key]}
        else:
            diff[key] = {
                'status': 'changed',
                'old_value': file1[key],
                'new_value': file2[key]
            }
    return diff


def get_formatter(diff, formatter):
    if formatter == 'stylish':
        return stylish(diff)