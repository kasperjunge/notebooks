import itertools


def flatten_list(l: list) -> list:
    return list(itertools.chain.from_iterable(l))
