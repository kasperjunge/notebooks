import pathlib


class Config:
    PATH_DATA = pathlib.Path(__file__).parents[2].joinpath("data")
