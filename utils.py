import os
from config.global_config import (
    FAIL_KEYWORDS
)


def check_fail_keywords(string):
    for keyword in FAIL_KEYWORDS:
        if keyword in string:
            return True
    return False


def get_abs_path(path: str) -> str:
    current_path = os.path.abspath(__file__)
    dir_name, file_name = os.path.split(current_path)
    return os.path.join(dir_name, path)


def convert_to_2d(data, step=10):
    return [data[i:i + step] for i in range(0, len(data), step)]
