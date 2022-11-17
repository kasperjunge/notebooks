import pandas as pd
from datasets import load_dataset
from tqdm import tqdm


def download_n_articles_from_url(n: int, url_pattern: str) -> pd.DataFrame:
    """Extract n documents from the the mC4 dataset.
    Args:
        n (int): Number of articles to extract.
        url_pattern (str): Pattern there should be in url to be downloaded.
    Returns:
        pd.DataFrame: Downloaded articles.
    """
    try:
        mc4 = load_dataset("mc4", "da", streaming=True)
        i, docs = 0, []
        with tqdm(total=n) as pbar:
            for doc in mc4["train"].shuffle():
                if url_pattern in doc["url"]:
                    docs.append(doc)
                    i += 1
                    pbar.update(1)
                    if i == n:
                        break
    finally:
        return pd.DataFrame(docs)
