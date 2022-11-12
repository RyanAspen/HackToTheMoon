import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# normalize
def normalize(df, cat):
    normalized_df = df
    for col in df.columns:
        if col not in cat:
            normalized_df[col] = (df[col]-df[col].mean())/df[col].std()
    return normalized_df

# remove outliers and anomaly
def remove_outliers(df, cat):
    new_df = df
    const = 15.0
    for col in new_df.columns:
        if col not in cat:
            Q1 = new_df[col].quantile(0.25)
            Q3 = new_df[col].quantile(0.75)
            IQR = (Q3 - Q1)    #IQR is interquartile range. 

            # filter = (normalized_df[col] >= Q1 - 1.5 * IQR) & (normalized_df[col] <= Q3 + 1.5 *IQR)
            new_df = new_df[new_df[col] >= Q1 - const * IQR]
            new_df = new_df[new_df[col] <= Q3 + const * IQR]
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