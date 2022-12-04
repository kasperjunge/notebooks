import itertools
import pathlib
from typing import List

import requests
from transformers import BertConfig, BertModel, BertTokenizer


def flatten_list(l: list) -> list:
    return list(itertools.chain.from_iterable(l))


def read_list_from_text_file(path_file: str) -> List[str]:
    with open(path_file, "r") as fp:
        l = fp.readlines()
    l = [x.replace("\n", "") for x in l]
    return l


def write_list_to_text_file(list_to_save, path_file) -> None:
    with open(path_file, "w") as fp:
        for elem in list_to_save:
            fp.write(elem + "\n")

def get_stop_words() -> List[str]:
    """Skud ud til berteltorp 🙏"""
    path = pathlib.Path("./pkg_data/dk_stop_words.txt")
    if path.is_file():
        return read_list_from_text_file(path)
    else:
        url = "https://gist.githubusercontent.com/berteltorp/0cf8a0c7afea7f25ed754f24cfc2467b/raw/305d8e3930cc419e909d49d4b489c9773f75b2d6/stopord.txt"
        return requests.get(url).content.decode().replace("\n", " ").split()

def sort_dict_by_values(dictionary: dict) -> dict:
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}





def init_vanilla_bert_with_pretrained_tokenizer(
        pretrained_model_name_or_path: str,
        kwargs_bert_config: dict = {},
    ) -> tuple[BertModel, BertTokenizer]:
    
    config = BertConfig(**kwargs_bert_config)
    model = BertModel(config)
    tokenizer = BertTokenizer.from_pretrained(pretrained_model_name_or_path)
    return model, tokenizer
