config = {
    "Buzz Drilldrin": [5000, 1.5, 0],
    "AstroBit": [3000, 1, 1500],
    "Apollo": [1000, 4, 2500],
    "ChallengDriller": [10000, 0, 0],
}

# Endpoint 1: Get Cost and Time per Asteroid
# Returns total cost and total time for a particular asteroid
def get_cost_and_time_for_asteroid(df):
    # compute the time

    prev = None
    for index, row in df.iterrows():
        if prev is not None:
            depth = row["BIT_DEPTH"] - prev["BIT_DEPTH"]
            df.at[index, "STEP_DEPTH"] = depth
            try:
                df.at[index, "TIME"] = depth / (
                    (row["RATE_OF_PENETRATION"] + prev["RATE_OF_PENETRATION"]) / 2
                )
                if prev["DRILL_BIT_ID"] != row["DRILL_BIT_ID"]:
                    df.at[index, "TIME"] += 30 / 3600 * 2 * (row["BIT_DEPTH"] / 100)
            except:
                df.at[index, "TIME"] = 0

        else:
            df.at[index, "TIME"] = 0
            df.at[index, "STEP_DEPTH"] = 0

        prev = row

    # compute cost

    prev = None
    used_drill_id = set()
    for index, row in df.iterrows():
        cost_per_run, cost_per_foot, cost_per_hour = config[row["DRILL_BIT_NAME"]]

        df.at[index, "COST"] = (
            row["STEP_DEPTH"] * cost_per_foot + row["TIME"] * cost_per_hour
        )
        if row["DRILL_BIT_ID"] not in used_drill_id:
            used_drill_id.add(row["DRILL_BIT_ID"])
            df.at[index, "COST"] += cost_per_run

        prev = row

    # Extract costs and times
    total_cost = df["COST"].sum()
    total_time = df["TIME"].sum()

    return total_cost, total_time


# Endpoint 2: Get Depth, Cost, and Time per Drill
# Returns a dictionary with each drill, where the values are the depth, cost, and time of the key (drill name)
def get_depth_cost_and_time_for_asteroid(df):
    bit_stats = {
        "Buzz Drilldrin": [0, 0, 0],
        "AstroBit": [0, 0, 0],
        "Apollo": [0, 0, 0],
        "ChallengDriller": [0, 0, 0],
    }
    prev = None
    used_drill_id = set()
    for _, row in df.iterrows():
        cost_per_run, cost_per_foot, cost_per_hour = config[row["DRILL_BIT_NAME"]]
        if prev is not None:
            depth = row["BIT_DEPTH"] - prev["BIT_DEPTH"]
            bit_stats[row["DRILL_BIT_NAME"]][0] += depth
            if (row["RATE_OF_PENETRATION"] + prev["RATE_OF_PENETRATION"]) != 0:
                time = depth / (
                    (row["RATE_OF_PENETRATION"] + prev["RATE_OF_PENETRATION"]) / 2
                )
            else:
                time = 0
            bit_stats[row["DRILL_BIT_NAME"]][2] += time
            bit_stats[row["DRILL_BIT_NAME"]][1] += (
                depth * cost_per_foot + time * cost_per_hour
            )
            if row["DRILL_BIT_ID"] not in used_drill_id:
                used_drill_id.add(row["DRILL_BIT_ID"])
                bit_stats[row["DRILL_BIT_NAME"]][1] += cost_per_run

        prev = row
    return bit_stats
