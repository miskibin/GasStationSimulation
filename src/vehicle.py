from entity import Entity
import numpy as np
from loguru import logger


class Tanker(Entity):
    def __init__(self, x, y, capacity):
        super().__init__(x, y, "Tanker")
        self.logger = logger
        self.capacity = capacity
        self.current_load = 2000  # Initial load at full capacity for simplicity
        self.target_station = None
        self.cost_per_move = 2

    def load_fuel(self, amount):
        self.current_load += amount
        print(
            f"Tanker loaded with {amount} liters of fuel, total now {self.current_load}."
        )

    def needs_refuel(self):
        return self.current_load < self.capacity * 0.2

    def deliver_fuel(self, tank_station):

        if self.distance_to(tank_station) < 1:
            if tank_station.x == 0 and tank_station.y == 0:
                self.current_load = 2000
                logger.info("Refueled at the center.")
                self.target_station = None
                return
            fuel_to_give = min(
                tank_station.capacity - tank_station.current_fuel, self.current_load
            )
            tank_station.add_fuel(fuel_to_give)
            self.current_load -= fuel_to_give
            self.target_station = None
            print(
                f"Delivered {fuel_to_give} liters to station at ({tank_station.x}, {tank_station.y})."
            )

    def move_to(self, destination):
        if destination:
            step_size = 1
            dx, dy = destination.x - self.x, destination.y - self.y
            distance = np.sqrt(dx**2 + dy**2)
            if distance > 0:
                self.current_load -= self.cost_per_move
                self.x += step_size * dx / distance
                self.y += step_size * dy / distance
            self.logger.info(f"Moved to ({self.x:.2f}, {self.y:.2f})")


class Vehicle:
    def __init__(self, fuel_need):
        self.fuel_need = fuel_need

    def refuel(self, amount):
        self.fuel_need -= amount
        print(f"Vehicle now needs {self.fuel_need} liters.")
