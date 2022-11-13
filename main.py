from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from helper_functions import *
from data_aggr import *
from predict import advise

from functools import cache

config = {
    "Buzz Drilldrin": [5000, 1.5, 0],
    "AstroBit": [3000, 1, 1500],
    "Apollo": [1000, 4, 2500],
    "ChallengDriller": [10000, 0, 0],
}
cat = ['DRILL_BIT_ID', 'DRILL_BIT_NAME', 'TIMESTAMP']
file_dir = "https://raw.githubusercontent.com/ClassicSours/TheInterstellarAsteroidRush/main/Asteroids/Asteroid%20"

data = load_data(file_dir, 20)
normalized_data = [0]*len(data)
for d in range(len(data)):
    data[d] = data_precessing(data[d], cat, config, 15.0)
    normalized_data[d] = data[d].copy()
    normalize(normalized_data[d], cat)

origins = [
    "https://ryanaspen.github.io",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200",
    "http://localhost:4000",
    "http://temochacksasteroids.tech",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def default():
    return {"Hello": "World"}


@app.get("/count")
async def count():
    return len(data)


@cache
def get_cost_and_time(asteroid_id=0):
    total_cost, total_time = get_cost_and_time_for_asteroid(data[int(asteroid_id) - 1], config)
    return {asteroid_id: {"total_cost": total_cost, "total_time": total_time}}


@app.get("/get_cost_and_time")
async def get_cost_and_time_api(asteroid_id=0):
    return get_cost_and_time(asteroid_id)


@cache
def get_cost_and_time_all():
    total_cost_all = []
    total_time_all = []

    for i in data:
        total_cost, total_time = get_cost_and_time_for_asteroid(i, config)
        total_cost_all.append(total_cost)
        total_time_all.append(total_time)
    return {i + 1: {"total_cost": total_cost_all[i], "total_time": total_time_all[i]} for i in range(len(data))}


@app.get("/get_cost_and_time_all")
async def get_cost_and_time_all_api():
    return get_cost_and_time_all()


@cache
def get_efficiencies(asteroid_id=0):
    bit_stats = get_depth_cost_and_time_for_asteroid(data[int(asteroid_id) - 1], config)
    return {asteroid_id: {"bit_stats": bit_stats}}


@app.get("/get_efficiencies")
async def get_efficiencies_api(asteroid_id=0):
    return get_efficiencies(asteroid_id)


@cache
def get_efficiencies_all():
    bit_stats_all = []

    for i in data:
        bit_stats = get_depth_cost_and_time_for_asteroid(i, config)
        bit_stats_all.append(bit_stats)
    return {i + 1: {"bit_stats": bit_stats_all[i]} for i in range(len(bit_stats_all))}


@app.get("/get_efficiencies_all")
async def get_efficiencies_all_api():
    return get_efficiencies_all()


@app.get("/get_column")
async def get_column(asteroid_id=0, column_name="TIMESTAMP"):
    return {asteroid_id: {column_name: list(data[int(asteroid_id)-1][column_name])}}


@app.get("/column_names")
async def get_column_names():
    return {"column_names": list(data[0].columns)}


@app.get("/get_advise")
async def get_advise(hook_load=111.1, differential_pressure=111.1,
                     weight_on_bit=111.1, drill_bit_name="AstroBit"):
    dict = {"HOOK_LOAD": float(hook_load), "DIFFERENTIAL_PRESSURE": float(differential_pressure),
            "WEIGHT_ON_BIT": float(weight_on_bit), "DRILL_BIT_NAME": drill_bit_name}
    ser = pd.Series(data=dict)
    return {"advise": advise(ser)}




