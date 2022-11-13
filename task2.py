# Endpoint 2: Get Depth, Cost, and Time per Drill
# Returns a dictionary with each drill, where the values are the depth, cost, and time of the key (drill name)
def get_depth_cost_and_time_for_asteroid(input_df, input_config):
    bit_stats = {
        "Buzz Drilldrin": [0, 0, 0],  # [depth, cost, time]
        "AstroBit": [0, 0, 0],
        "Apollo": [0, 0, 0],
        "ChallengDriller": [0, 0, 0],
    }
    prev = None
    used_drill_id = set()
    for _, row in input_df.iterrows():
        cost_per_run, cost_per_foot, cost_per_hour = input_config[row["DRILL_BIT_NAME"]]
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


