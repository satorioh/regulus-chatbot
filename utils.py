from config.global_config import (
    FAIL_KEYWORDS
)


def check_fail_keywords(string):
    for keyword in FAIL_KEYWORDS:
        if keyword in string:
            return True
    return False
