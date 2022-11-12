import numpy as np
import pandas as pd
import math


config = {
    "Buzz Drilldrin": [5000, 1.5, 0],
    "AstroBit": [3000, 1, 1500],
    "Apollo": [1000, 4, 2500],
    "ChallengDriller": [10000, 0, 0],
}

# feet, cost, hours
bit_stats = {
    "Buzz Drilldrin": [0, 0, 0],
    "AstroBit": [0, 0, 0],
    "Apollo": [0, 0, 0],
    "ChallengDriller": [0, 0, 0],
}

for i in range(1, 21):
    df = pd.read_csv(
        f"https://raw.githubusercontent.com/ClassicSours/TheInterstellarAsteroidRush/main/Asteroids/Asteroid%20{i}.csv"
    )

    prev = None
    used_drill_id = set()
    for index, row in df.iterrows():
        cost_per_run, cost_per_foot, cost_per_hour = config[row["DRILL_BIT_NAME"]]
        if not math.isnan(row["BIT_DEPTH"]) and not math.isnan(
            row["RATE_OF_PENETRATION"]
        ):
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

print(bit_stats)
cost_efficiencies = {
    "Buzz Drilldrin": 0,
    "AstroBit": 0,
    "Apollo": 0,
    "ChallengDriller": 0,
}
time_efficiencies = {
    "Buzz Drilldrin": 0,
    "AstroBit": 0,
    "Apollo": 0,
    "ChallengDriller": 0,
}
for bit in bit_stats:
    cost_efficiencies[bit] = bit_stats[bit][0] / bit_stats[bit][1]
    time_efficiencies[bit] = bit_stats[bit][0] / bit_stats[bit][2]

print(cost_efficiencies)
print(time_efficiencies)
