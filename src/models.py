from pydantic import BaseModel
from typing import List


class StationModel(BaseModel):
    x: float
    y: float
    capacity: int
    current_fuel: int
    is_refueling_car: bool = False


class TankerModel(BaseModel):
    x: float
    y: float
    capacity: float
    current_load: float
    target_station: str


class RefuelCenterModel(BaseModel):
    x: float
    y: float


class EnvironmentModel(BaseModel):
    stations: List[StationModel]
    tanker: TankerModel
    refuel_center: RefuelCenterModel


class SimulationParameters(BaseModel):
    stations: List[StationModel]
    steps: int
