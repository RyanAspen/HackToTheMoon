import pandas as pd


def normalize(input_df, input_cat):
    # normalize
    input_cat = set(input_cat)
    normalized_df = input_df
    for col in input_df.columns:
        if col not in input_cat:
            normalized_df[col] = (input_df[col] - input_df[col].mean()) / input_df[col].std()
    return normalized_df


# remove outliers and anomaly
def remove_outliers(input_df, input_cat, const):
    new_df = input_df
    input_cat = set(input_cat)
    const = const
    for col in new_df.columns:
        if col not in input_cat:
            q1 = new_df[col].quantile(0.25)
            q3 = new_df[col].quantile(0.75)
            iqr = (q3 - q1)  # iqr is interquartile range.

            # filter = (normalized_df[col] >= q1 - 1.5 * iqr) & (normalized_df[col] <= q3 + 1.5 *iqr)
            new_df = new_df[new_df[col] >= q1 - const * iqr]
            new_df = new_df[new_df[col] <= q3 + const * iqr]
            new_df = new_df[new_df[col] != 0]
    return new_df


if __name__ == "__main__":
    cat = {'DRILL_BIT_ID', 'DRILL_BIT_NAME'}
    df = pd.concat(
        [
            pd.read_csv(
                f"https://raw.githubusercontent.com/ClassicSours/TheInterstellarAsteroidRush/main/Asteroids/Asteroid%20{i}.csv"
            )
            for i in range(1, 2)
        ]
    )
    df1 = normalize(df, cat)
    df2 = remove_outliers(df1, cat)

# without_cat = df2.loc[:, ~df2.columns.isin(['DRILL_BIT_ID', 'DRILL_BIT_NAME'])]
# plt.figure(figsize=(20, 6), dpi=80)
# sns.boxplot(data=without_cat)
