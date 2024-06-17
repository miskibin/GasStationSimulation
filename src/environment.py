from loguru import logger
from entity import Entity
from tank_station import Station
from vehicle import Tanker, Vehicle
from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from models import EnvironmentModel, RefuelCenterModel, StationModel, TankerModel


class Environment:
    def __init__(self):
        self.stations: list[Station] = []
        self.tanker = Tanker(3, 3, 1000)
        self.refuel_center = Entity(0, 0, "Refuel Center")
        self.fig, self.ax = plt.subplots()

    def register_station(self, tank_station):
        self.stations.append(tank_station)
        tank_station.environment = self

    def notify(self, station):
        if self.tanker.target_station is None and not self.tanker.needs_refuel():
            self.tanker.target_station = station
            print(f"Tanker set to move to station at ({station.x}, {station.y}).")
        else:
            print(f"Tanker is currently busy and cannot respond to new requests.")

    def update(self):
        if self.tanker.needs_refuel():
            logger.info("Tanker needs refuel.")
            self.tanker.target_station = self.refuel_center
        if self.tanker.target_station:
            self.tanker.move_to(self.tanker.target_station)
            self.tanker.deliver_fuel(self.tanker.target_station)
        for station in self.stations:
            station.process_queue()
            station.request_fuel()

    def animate(self, i):
        self.ax.clear()
        G = nx.Graph()
        positions = {
            self.refuel_center.name: (self.refuel_center.x, self.refuel_center.y)
        }

        for station in self.stations:
            node_label = (
                f"Station ({station.x}, {station.y})\nFuel: {station.current_fuel}L"
            )
            G.add_node(node_label, pos=(station.x, station.y))
            positions[node_label] = (station.x, station.y)
        G.add_node("Refuel Center", pos=(self.refuel_center.x, self.refuel_center.y))

        tanker_label = f"Tanker\nFuel: {self.tanker.current_load}L"
        G.add_node(tanker_label, pos=(self.tanker.x, self.tanker.y))
        positions[tanker_label] = (self.tanker.x, self.tanker.y)

        nx.draw(
            G,
            pos=positions,
            ax=self.ax,
            with_labels=True,
            node_color="skyblue",
            node_size=700,
        )
        plt.title(f"Step {i}")
        self.update()

    def run_simulation(self, steps: int):
        ani = FuncAnimation(
            self.fig, self.animate, frames=steps, repeat=False, interval=50
        )
        plt.show()

    def state_as_model(self) -> EnvironmentModel:
        return EnvironmentModel(
            stations=[
                StationModel(
                    x=station.x,
                    y=station.y,
                    capacity=station.capacity,
                    current_fuel=station.current_fuel,
                    is_refueling_car=station.is_refueling_car,
                    loss=station.loss,
                )
                for station in self.stations
            ],
            tanker=TankerModel(
                x=self.tanker.x,
                y=self.tanker.y,
                capacity=self.tanker.capacity,
                current_load=self.tanker.current_load,
                target_station=(
                    self.tanker.target_station.name
                    if self.tanker.target_station
                    else ""
                ),
            ),
            refuel_center=RefuelCenterModel(
                x=self.refuel_center.x,
                y=self.refuel_center.y,
            ),
        )


if __name__ == "__main__":
    env = Environment()
    env.register_station(Station(10, 10, 500, 15))
    env.register_station(Station(-10, -10, 400, 24))
    env.register_station(Station(20, -20, 600, 17))

    # Add vehicles
    for station in env.stations:
        station.vehicles.extend(
            [Vehicle(33) for _ in range(120)]
        )  # Add 5 vehicles needing 50 liters each to each station
    print(env.state_as_model())
    # env.run_simulation(20)
