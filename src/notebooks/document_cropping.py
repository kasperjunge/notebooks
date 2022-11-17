import math
import random

import pandas as pd
from nltk import sent_tokenize
from tqdm import tqdm

from .utils import flatten_list

tqdm.pandas()

## TODO: docstrings
## TODO: make constrastive generation possible without discriminator column
## TODO: is n_triplets arg nessecary?


def generate_contrastive_doc_crop_dataset(
    df: pd.DataFrame,
    crop_size: int,
    n_triplets: int = None,
) -> pd.DataFrame:
    """Generate a contrastive dataset using the self-supervised "document cropping" technique.
    Args:
        df (pd.DataFrame):
            Dataframe contatining text data. The dataframe is expected to have:
            - "text" column (str)
            - "doc_id" column (str)
            - "discriminator" column (str)
        crop_size (int):
            Number of sentences in each text crop.
        n_triplets (int):
            Number of document triplets to form.
    Returns:
        pd.DataFrame: Contrastive document cropped dataset.
    """
    df_crop = crop_documents(df=df, crop_size=crop_size)
    df_triplets = generate_triplets(df_crop=df_crop, n_triplets=n_triplets)
    return df_triplets


def crop_documents(
    df: pd.DataFrame,
    crop_size: int,
) -> pd.DataFrame:

    print("Cropping documents".upper())

    # crop articles
    print("sentence tokenize..")
    df["sentences"] = df["text"].progress_apply(lambda x: sent_tokenize(x, language="danish"))
    df["n_sentences"] = df["sentences"].apply(len)
    df = df.explode("sentences")

    def crop(sentences: pd.Series, crop_size: int) -> pd.Series:
        n_sentences = len(sentences)
        n_crops = math.ceil(n_sentences / crop_size)
        remainder = n_sentences % crop_size

        # make crop layout
        if remainder > 0:
            layout = (n_crops - 1) * ["crop_size"]
            layout = layout + ["remainder"]
        else:
            layout = n_crops * ["crop_size"]
        random.shuffle(layout)

        # generate crop ids
        crop_ids = []
        for idx, crop in enumerate(layout):
            if crop == "crop_size":
                crop_ids.append([idx] * crop_size)
            else:
                crop_ids.append([idx] * remainder)
        crop_ids = flatten_list(crop_ids)

        return crop_ids

    print("make crop layout..")
    df["doc_crop_id"] = (
        df.groupby("doc_id")["sentences"].progress_transform(lambda x: crop(x, crop_size=crop_size)).astype(str)
    )
    print("join crop sentences..")
    df["crop"] = df.groupby(["doc_id", "doc_crop_id"])["sentences"].progress_transform(lambda x: " ".join(x).strip())
    df_crop = df.drop_duplicates(subset=["doc_id", "crop", "url", "timestamp"])
    df_crop = df_crop.reset_index(drop=True)
    df_crop["crop_id"] = df_crop.index.astype(str)
    df_crop = df_crop[["crop_id", "doc_id", "crop", "url", "timestamp", "discriminator"]]
    return df_crop


def generate_triplets(df_crop: pd.DataFrame, n_triplets: int = None):

    print("Generate triplets".upper())

    if n_triplets is None:
        n_triplets = round(df_crop.shape[0] / 3)

    # generate triplets
    df_crop["triplet_id"] = np.nan
    df_crop["triplet_type"] = np.nan

    print("sampling triplets..")
    triplets = []
    for triplet_id in tqdm(range(n_triplets)):

        try:

            c = df_crop.loc[df_crop["triplet_id"].isna()].sample(1)

            p = df_crop.loc[
                (df_crop["triplet_id"].isna())
                & (df_crop["doc_id"] == c["doc_id"].iloc[0])
                & (df_crop["crop_id"] != c["crop_id"].iloc[0])
            ].sample(1)

            n = df_crop.loc[
                (df_crop["triplet_id"].isna())
                & (df_crop["doc_id"] != c["doc_id"].iloc[0])
                & (df_crop["discriminator"] != c["discriminator"].iloc[0])
            ].sample(1)

            c["triplet_type"] = "candidate"
            p["triplet_type"] = "positive"
            n["triplet_type"] = "negative"

            c["triplet_id"] = triplet_id
            p["triplet_id"] = triplet_id
            n["triplet_id"] = triplet_id

            triplet = pd.concat([c, p, n])

            triplets.append(triplet)
        except:
            pass

    df_triplets = pd.concat(triplets)
    df_triplets["triplet_id"] = df_triplets["triplet_id"].astype(str)
    return df_triplets
