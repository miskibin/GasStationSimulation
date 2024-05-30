import itertools
import random
import simpy
from typing import List, Generator, Any

from constants import *
from rich.console import Console

console = Console()
time_points: List[float] = []
fuel_levels: List[float] = []
distributor_fuel_levels: List[List[float]] = [[] for _ in range(NUM_DISTRIBUTORS)]


def car(
    name: str,
    env: simpy.Environment,
    gas_station: simpy.Resource,
    station_tanks: List[simpy.Container],
) -> Generator:
    car_tank_level: int = random.randint(*CAR_TANK_LEVEL)
    console.log(f"{env.now:6.1f} s: {name} arrived at gas station")
    with gas_station.request() as req:
        yield req
        fuel_required: int = CAR_TANK_SIZE - car_tank_level
        station_tank = random.choice(station_tanks)
        yield station_tank.get(fuel_required)
        yield env.timeout(fuel_required / REFUELING_SPEED)
        console.log(
            f"{env.now:6.1f} s: {name} refueled in station {station_tanks.index(station_tank)}"
        )


def gas_station_control(
    env: simpy.Environment,
    station_tanks: List[simpy.Container],
) -> Generator:
    while True:
        for i, station_tank in enumerate(station_tanks):
            if station_tank.level / station_tank.capacity * 100 < THRESHOLD:
                console.log(f"{env.now:6.1f} s: Calling tank truck", style="bold red")
                yield env.process(tank_truck(env, station_tank))
            distributor_fuel_levels[i].append(station_tank.level)
        yield env.timeout(10)
        time_points.append(env.now)
        fuel_levels.append(sum(station_tank.level for station_tank in station_tanks))


def tank_truck(env: simpy.Environment, station_tank: simpy.Container) -> Generator:
    yield env.timeout(TANK_TRUCK_TIME)
    amount: int = station_tank.capacity - station_tank.level
    station_tank.put(amount)
    console.log(
        f"{env.now:6.1f} s: Tank truck arrived and refuelled station with {amount:.1f}L",
        style="bold green",
    )


def car_generator(
    env: simpy.Environment, gas_station: simpy.Resource, station_tank: simpy.Container
) -> Generator:
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(car(f"Car {i}", env, gas_station, station_tank))
