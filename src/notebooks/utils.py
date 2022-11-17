import itertools
import pathlib
from typing import List, Union

import requests


def flatten_list(l: list) -> list:
    return list(itertools.chain.from_iterable(l))


def read_list_from_txt(path: Union[str, pathlib.PosixPath]) -> List[str]:
    with open(path, "r") as fp:
        l = fp.readlines()
    l = [x.replace("\n", "") for x in l]
    return l


def get_stop_words() -> List[str]:
    """Skud ud til berteltorp 🙏"""
    path = pathlib.Path("./pkg_data/dk_stop_words.txt")
    if path.is_file():
        return read_list_from_txt(path)
    else:
        url = "https://gist.githubusercontent.com/berteltorp/0cf8a0c7afea7f25ed754f24cfc2467b/raw/305d8e3930cc419e909d49d4b489c9773f75b2d6/stopord.txt"
        return requests.get(url).content.decode().replace("\n", " ").split()
