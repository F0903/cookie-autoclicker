import sys


def is_debug() -> bool:
    return getattr(sys, "gettrace", None)
