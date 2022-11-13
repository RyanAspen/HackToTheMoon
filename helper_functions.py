from data_manipulation import *


def load_data(file_dir, number):
    data = [
        pd.read_csv(
            f"{file_dir}{i}.csv"
        )
        for i in range(1, number + 1)
    ]
    return data


def data_precessing(input_df, input_cat, input_config, const=1.5):
    input_df = input_df.dropna(axis=0).copy()
    remove_outliers(input_df, input_cat, const)
    compute_cost_and_time_for_asteroid(input_df, input_config)
    compute_timestamp(input_df)
    return input_df


