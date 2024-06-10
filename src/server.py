from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from environment import Environment
from tank_station import Station
from vehicle import Tanker, Vehicle
from models import (
    EnvironmentModel,
    StationModel,
    TankerModel,
    RefuelCenterModel,
    SimulationParameters,
)
from pathlib import Path

app = FastAPI()

current_dir = Path(__file__).parent

app.mount("/static", StaticFiles(directory=current_dir / "static"), name="static")
templates = Jinja2Templates(directory=current_dir / "templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


ENVIRONMENT = Environment()
ENVIRONMENT.register_station(Station(10, 10, 500, 15))
ENVIRONMENT.register_station(Station(-10, -10, 400, 24))
ENVIRONMENT.register_station(Station(20, -20, 600, 17))

# Add vehicles
for station in ENVIRONMENT.stations:
    station.vehicles.extend([Vehicle(33) for _ in range(120)])


@app.get("/step", response_model=EnvironmentModel)
def step_simulation():
    ENVIRONMENT.update()
    return ENVIRONMENT.state_as_model()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
