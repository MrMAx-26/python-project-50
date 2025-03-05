def stylish(diff):
    def iter(data, depth=0):
        if not isinstance(data, dict):
            return format_value(data)
        result = []
        for key, val in data.items():
            indent = build_indent(depth)
            if isinstance(val, dict):
                status = val.get('status')
                value = val.get('value')
                formatted_value = iter(value, depth + 1)
                if status == 'added':
                    result.append(f'{indent}+ {key}: {formatted_value}')
                elif status == 'removed':
                    result.append(f'{indent}- {key}: {formatted_value}')
                elif status == 'unchanged':
                    result.append(f'{indent}  {key}: {formatted_value}')
                elif status == 'changed':
                    old_value = iter(val['old_value'], depth + 1)
                    new_value = iter(val['new_value'], depth + 1)
                    result.append(f'{indent}- {key}: {old_value}')
                    result.append(f'{indent}+ {key}: {new_value}')
                elif status == 'nested':
                    result.append(f'{indent}  {key}: {formatted_value}')
                else:
                    formatted_value = iter(val, depth + 1)
                    result.append(f'{indent}  {key}: {formatted_value}')
            else:
                formatted_value = iter(val, depth + 1)
                result.append(f'{indent}  {key}: {formatted_value}')
        return add_braces(format_data(result, depth))
    return iter(diff)


def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return str(value)


def build_indent(depth):
    indent = '    '
    return indent[:-2] + indent * depth


def format_data(data, depth):
    string_data = '\n'.join(data)
    last_indent = build_indent(depth)[:-2]
    return f'{string_data}\n{last_indent}'


def add_braces(formatted_data):
    return f'{{\n{formatted_data}}}'    


