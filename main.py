# main.py

import itertools
import random
import simpy
import matplotlib.pyplot as plt
from rich.console import Console
from typing import List, Generator, Any
from matplotlib import animation
from constants import *
from entities import car, gas_station_control, tank_truck, car_generator
from utils import interpolate_fuel_levels

# Enhanced console output with rich
console = Console()

# Data collection for the plot

# Setup and start the simulation
console.log("Gas Station refuelling")
random.seed(RANDOM_SEED)

env = simpy.Environment()
gas_station = simpy.Resource(env, 2)
# Create multiple station tanks
station_tanks = [
    simpy.Container(env, STATION_TANK_SIZE, init=STATION_TANK_SIZE)
    for _ in range(NUM_DISTRIBUTORS)
]

env.process(gas_station_control(env, station_tanks))
env.process(car_generator(env, gas_station, station_tanks))
env.run(until=SIM_TIME)

# Create a figure for the plot
# Create a figure for the plot


# Function to update the plot
from entities import time_points, fuel_levels, distributor_fuel_levels

# add interpolation to distributor fuel levels. I want changes to be smooth. But there need to be only `time_points` number of points
print(len(time_points))
distributor_fuel_levels = [v[: len(time_points)] for v in distributor_fuel_levels]
print(len(distributor_fuel_levels[0]))
distributor_fuel_levels = interpolate_fuel_levels(time_points, distributor_fuel_levels)
#
# # Create two separate figures and axes for the plots
# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))


def update1(num):
    ax1.clear()
    ax1.plot(
        time_points[:num],
        fuel_levels[:num],
        label=f"Total Fuel Level",
    )
    ax1.set_title(
        f"Total Fuel Level Over Time at Gas Station (up to {time_points[num]} seconds)"
    )
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Total Fuel Level (Liters)")
    ax1.grid(True)
    ax1.legend()


def update2(num):
    ax2.clear()
    ax2.bar(
        range(NUM_DISTRIBUTORS),
        [distributor_fuel_levels[i][num] for i in range(NUM_DISTRIBUTORS)],
        label=[f"Distributor {i+1}" for i in range(NUM_DISTRIBUTORS)],
    )
    ax2.set_xlabel("Distributor")
    ax2.set_ylabel("Fuel Level (Liters)")
    ax2.grid(True)
    ax2.legend()


ani1 = animation.FuncAnimation(
    fig, update1, frames=len(time_points), interval=50, repeat=False
)
ani2 = animation.FuncAnimation(
    fig, update2, frames=len(time_points), interval=50, repeat=False
)
plt.tight_layout()
plt.show()
