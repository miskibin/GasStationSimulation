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

# Enhanced console output with rich
console = Console()

# Data collection for the plot
time_points: List[float] = []
fuel_levels: List[float] = []

# Setup and start the simulation
console.log("Gas Station refuelling")
random.seed(RANDOM_SEED)

env = simpy.Environment()
gas_station = simpy.Resource(env, 2)
station_tank = simpy.Container(env, STATION_TANK_SIZE, init=STATION_TANK_SIZE)
env.process(gas_station_control(env, station_tank, time_points, fuel_levels))
env.process(car_generator(env, gas_station, station_tank))

env.run(until=SIM_TIME)

# Create a figure for the plot
# Create a figure for the plot
fig, ax = plt.subplots(figsize=(10, 5))


# Function to update the plot
def update(num):
    ax.clear()
    ax.plot(
        time_points[:num],
        fuel_levels[:num],
        label=f"Fuel Level ",
    )

    # Set the title and labels
    ax.set_title(
        f"Fuel Level Over Time at Gas Station (up to {time_points[num]} seconds)"
    )
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Fuel Level (Liters)")

    # Enable the grid
    ax.grid(True)

    ax.legend()


# Create an animation with a faster frame rate (e.g., 50 ms between frames)
ani = animation.FuncAnimation(
    fig, update, frames=len(time_points), interval=50, repeat=False
)

# Show the plot
plt.show()
