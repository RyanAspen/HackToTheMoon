import pandas as pd


def compute_cost_and_time_for_asteroid(input_df, input_config):
    # Get Cost and Time per Asteroid
    # Returns total cost and total time for a particular asteroid

    # compute time
    prev = None
    for index, row in input_df.iterrows():
        if prev is not None:
            depth = row["BIT_DEPTH"] - prev["BIT_DEPTH"]
            input_df.at[index, "STEP_DEPTH"] = depth
            try:
                input_df.at[index, "TIME"] = depth / (
                        (row["RATE_OF_PENETRATION"] + prev["RATE_OF_PENETRATION"]) / 2
                )
                if prev["DRILL_BIT_ID"] != row["DRILL_BIT_ID"]:
                    input_df.at[index, "TIME"] += 30 / 3600 * 2 * (row["BIT_DEPTH"] / 100)
            except:
                input_df.at[index, "TIME"] = 0
        else:
            input_df.at[index, "TIME"] = 0
            input_df.at[index, "STEP_DEPTH"] = 0
        prev = row

    # compute cost
    prev = None
    used_drill_id = set()
    for index, row in input_df.iterrows():
        cost_per_run, cost_per_foot, cost_per_hour = input_config[row["DRILL_BIT_NAME"]]

        input_df.at[index, "COST"] = (
                row["STEP_DEPTH"] * cost_per_foot + row["TIME"] * cost_per_hour
        )
        if row["DRILL_BIT_ID"] not in used_drill_id:
            used_drill_id.add(row["DRILL_BIT_ID"])
            input_df.at[index, "COST"] += cost_per_run
        prev = row


def compute_timestamp(input_df):
    timestamp = 0
    for index, row in input_df.iterrows():
        timestamp += row["TIME"]
        input_df.loc[index, "TIMESTAMP"] = timestamp


def normalize(input_df, input_cat):
    # normalize
    input_cat = set(input_cat)
    normalized_df = input_df
    for col in input_df.columns:
        if col not in input_cat:
            normalized_df[col] = (input_df[col] - input_df[col].mean()) / input_df[col].std()


# remove outliers and anomaly
def remove_outliers(input_df, input_cat, const):
    input_cat = set(input_cat)
    const = const
    for col in input_df.columns:
        if col not in input_cat:
            q1 = input_df[col].quantile(0.25)
            q3 = input_df[col].quantile(0.75)
            iqr = (q3 - q1)  # iqr is interquartile range.

            # filter = (normalized_df[col] >= q1 - 1.5 * iqr) & (normalized_df[col] <= q3 + 1.5 *iqr)
            input_df = input_df[input_df[col] >= q1 - const * iqr]
            input_df = input_df[input_df[col] <= q3 + const * iqr]
            input_df = input_df[input_df[col] != 0]
    return input_df



