import re
from typing import List


class SentenceTokenizer:
    
    def __call__(self, text: str) -> List[str]:
        sentences = text.split(".")
        sentences = [sentence.strip()+"." for sentence in sentences]
        return sentences


class StringCleaner:

    def __call__(self, text: str) -> str:
        text = re.sub(" +", " ", text)
        return text