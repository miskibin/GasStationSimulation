from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
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
import math

app = FastAPI()

current_dir = Path(__file__).parent

app.mount("/static", StaticFiles(directory=current_dir / "static"), name="static")
templates = Jinja2Templates(directory=current_dir / "templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


ENVIRONMENT = Environment()
ENVIRONMENT.register_station(Station(10, 10, 800, 15))
ENVIRONMENT.register_station(Station(-10, -10, 700, 24))
ENVIRONMENT.register_station(Station(20, -20, 900, 17))

# Add vehicles
for station in ENVIRONMENT.stations:
    station.vehicles.extend([Vehicle(33) for _ in range(1020)])


@app.get("/step", response_model=EnvironmentModel)
def step_simulation():
    ENVIRONMENT.update()
    return ENVIRONMENT.state_as_model()


@app.get("/set_tanker_destination/{destination}")
def set_tanker_destination(destination):
    x, y = destination.split(",")
    # it is always existing station
    station = None
    for s in ENVIRONMENT.stations:
        if math.isclose(s.x, float(x), rel_tol=1e-5) and math.isclose(
            s.y, float(y), rel_tol=1e-5
        ):
            station = s
            logger.warning(f"Station found: {station}")
            break
    ENVIRONMENT.tanker.target_station = station
    return {"message": "Destination set"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
