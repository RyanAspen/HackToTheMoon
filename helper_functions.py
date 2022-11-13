import pandas as pd


def load_data(file_dir, number):
    data = [
        pd.read_csv(
            f"{file_dir}{i}.csv"
        )
        for i in range(1, number + 1)
    ]
    return data

