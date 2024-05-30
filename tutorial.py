import itertools
import random
import simpy
import matplotlib.pyplot as plt
from rich.console import Console
from typing import List, Generator, Any

# Enhanced console output with rich
console = Console()

# Data collection for the plot
time_points: List[float] = []
fuel_levels: List[float] = []

RANDOM_SEED: int = 42
STATION_TANK_SIZE: int = 200  # Size of the gas station tank (liters)
THRESHOLD: int = 25  # Station tank minimum level (% of full)
CAR_TANK_SIZE: int = 50  # Size of car fuel tanks (liters)
CAR_TANK_LEVEL: List[int] = [5, 25]  # Min/max levels of car fuel tanks (liters)
REFUELING_SPEED: int = 2  # Rate of refuelling car fuel tank (liters / second)
TANK_TRUCK_TIME: int = 300  # Time it takes tank truck to arrive (seconds)
T_INTER: List[int] = [30, 300]  # Interval between car arrivals [min, max] (seconds)
SIM_TIME: int = 5000  # Simulation time (seconds)


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
    env: simpy.Environment, station_tank: simpy.Container
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


# Setup and start the simulation
console.log("Gas Station refuelling")
random.seed(RANDOM_SEED)

env = simpy.Environment()
gas_station = simpy.Resource(env, 2)
station_tank = simpy.Container(env, STATION_TANK_SIZE, init=STATION_TANK_SIZE)
env.process(gas_station_control(env, station_tank))
env.process(car_generator(env, gas_station, station_tank))

env.run(until=SIM_TIME)

# Plotting the results
plt.figure(figsize=(10, 5))
plt.plot(time_points, fuel_levels, label="Fuel Level")
plt.xlabel("Time (s)")
plt.ylabel("Fuel Level (Liters)")
plt.title("Fuel Level Over Time at Gas Station")
plt.legend()
plt.grid(True)
plt.show()
