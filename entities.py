import itertools
import random
import simpy
from typing import List, Generator, Any

from constants import *
from rich.console import Console

console = Console()


def car(
    name: str,
    env: simpy.Environment,
    gas_station: simpy.Resource,
    station_tank: simpy.Container,
) -> Generator:
    car_tank_level: int = random.randint(*CAR_TANK_LEVEL)
    console.log(f"{env.now:6.1f} s: {name} arrived at gas station")
    with gas_station.request() as req:
        yield req
        fuel_required: int = CAR_TANK_SIZE - car_tank_level
        yield station_tank.get(fuel_required)
        yield env.timeout(fuel_required / REFUELING_SPEED)
        console.log(f"{env.now:6.1f} s: {name} refueled with {fuel_required:.1f}L")


def gas_station_control(
    env: simpy.Environment,
    station_tank: simpy.Container,
    time_points: List[float],
    fuel_levels: List[float],
) -> Generator:
    while True:
        if station_tank.level / station_tank.capacity * 100 < THRESHOLD:
            console.log(f"{env.now:6.1f} s: Calling tank truck", style="bold red")
            yield env.process(tank_truck(env, station_tank))
        yield env.timeout(10)
        # Collect data for the plot
        time_points.append(env.now)
        fuel_levels.append(station_tank.level)


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
