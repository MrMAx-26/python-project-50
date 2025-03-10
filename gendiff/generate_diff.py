from gendiff.diff import get_diff
from gendiff.formatters import format
from gendiff.parser import get_file


def generate_diff(file_path1, file_path2, formatter='stylish'):
    file1 = get_file(file_path1)
    file2 = get_file(file_path2)
    diff = get_diff(file1, file2)
    return format(diff, formatter)
