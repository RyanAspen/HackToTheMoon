import pandas as pd

config = {
    "Buzz Drilldrin": [5000, 1.5, 0],
    "AstroBit": [3000, 1, 1500],
    "Apollo": [1000, 4, 2500],
    "ChallengDriller": [10000, 0, 0],
}

for i in range(1, 21):
    df = pd.read_csv(
        f"https://raw.githubusercontent.com/ClassicSours/TheInterstellarAsteroidRush/main/Asteroids/Asteroid%20{i}.csv"
    )

    def get_time_and_cost(df):
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

        return df

    handled = get_time_and_cost(df)
    print(f'csv1 time is {handled["TIME"].sum()}, cost is {handled["COST"].sum()}')
