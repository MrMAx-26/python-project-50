def plain(diff):
    def iter(data, path=''):
        result = []
        for key, val in data.items():
            full_path = f'{path}.{key}' if path else key
            if isinstance(val, dict):
                status = val.get('status')
                if status == 'added':
                    result.append(f"Property '{full_path}' "
                        "was added with value: "
                        f"{format_value(val['value'])}"
                    )
                elif status == 'removed':
                    result.append(f"Property '{full_path}' was removed")
                elif status == 'unchanged':
                    continue
                elif status == 'changed':
                    result.append(f"Property '{full_path}' was updated. "
                        f"From {format_value(val['old_value'])} "
                        f"to {format_value(val['new_value'])}"
                    )
                elif status == 'nested':
                    result.append(iter(val['value'], full_path))
                else:
                    result.append(iter(val, full_path))
            else:
                result.append(f"Property '{full_path}' "
                    f"has an unexpected value: {format_value(val)}"
                )
        return "\n".join(result)
    return iter(diff)


def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, str):
        return f"'{value}'"
    return str(value)