import pandas as pd

from notebooks.mc4 import download_n_articles_from_url

df = download_n_articles_from_url(n=100000000, url_pattern="nyheder.tv2.dk")
df.to_csv("./data/news3.csv", index=False)
