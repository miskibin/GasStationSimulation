import numpy as np
from entity import Entity
from loguru import logger


class Station(Entity):
    def __init__(self, x, y, capacity, fueling_speed=3):
        super().__init__(x, y, name=f"TankStation at {x} : {y}")
        self.fueling_speed = fueling_speed
        self.capacity = capacity
        self.current_fuel = capacity
        self.fuel_alert_level = capacity / 5
        self.vehicles = []
        self.environment = (
            None  # This will be set when the station is registered with the environment
        )

    def request_fuel(self):
        if self.current_fuel < self.fuel_alert_level:
            self.environment.notify(self)

    def add_fuel(self, amount):
        self.current_fuel = min(self.capacity, self.current_fuel + amount)
        print(
            f"TankStation at ({self.x}, {self.y}) refueled: current fuel {self.current_fuel} liters"
        )

    def process_queue(self):
        if np.random.rand() < 0.2:
            return
        if self.vehicles and self.current_fuel > 0:
            vehicle = self.vehicles[0]  # Check the first vehicle without removing it
            required_fuel = min(
                vehicle.fuel_need, self.current_fuel, self.fueling_speed
            )
            vehicle.refuel(required_fuel)
            self.current_fuel -= required_fuel

            if vehicle.fuel_need <= 0:  # Vehicle is fully refueled
                self.vehicles.pop(0)  # Remove vehicle from queue