from fastapi import FastAPI, File, UploadFile, HTTPException
from helper_functions import *
from data_aggr import *

config = {
    "Buzz Drilldrin": [5000, 1.5, 0],
    "AstroBit": [3000, 1, 1500],
    "Apollo": [1000, 4, 2500],
    "ChallengDriller": [10000, 0, 0],
}
cat = ['DRILL_BIT_ID', 'DRILL_BIT_NAME', 'TIMESTAMP']
file_dir = "https://raw.githubusercontent.com/ClassicSours/TheInterstellarAsteroidRush/main/Asteroids/Asteroid%20"

data = load_data(file_dir, 2)
normalized_data = [0]*len(data)
for d in range(len(data)):
    data[d] = data_precessing(data[d], cat, config, 15.0)
    normalized_data[d] = data[d].copy()
    normalize(normalized_data[d], cat)


app = FastAPI()


@app.get("/")
async def default():
    return {"Hello": "World"}


@app.get("/count")
async def count():
    return len(data)


@app.get("/get_cost_and_time")
async def get_cost_and_time(asteroid_id):
    total_cost, total_time = get_cost_and_time_for_asteroid(data[int(asteroid_id)-1], config)
    return {asteroid_id: {"total_cost": total_cost, "total_time": total_time}}


@app.get("/get_cost_and_time_all")
async def get_cost_and_time_all():
    total_cost_all = []
    total_time_all = []

    for i in data:
        total_cost, total_time = get_cost_and_time_for_asteroid(i, config)
        total_cost_all.append(total_cost)
        total_time_all.append(total_time)
    return {i+1: {"total_cost": total_cost_all[i], "total_time": total_time_all[i]} for i in range(len(data))}


@app.get("/get_efficiencies")
async def get_efficiencies(asteroid_id):
    bit_stats = get_depth_cost_and_time_for_asteroid(data[int(asteroid_id)-1], config)
    return {asteroid_id: {"bit_stats": bit_stats}}


@app.get("/get_efficiencies_all")
async def get_efficiencies_all():
    bit_stats_all = []

    for i in data:
        bit_stats = get_depth_cost_and_time_for_asteroid(i, config)
        bit_stats_all.append(bit_stats)
    return {i+1: {"bit_stats": bit_stats_all[i]} for i in range(len(bit_stats_all))}

























