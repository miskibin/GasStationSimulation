# constants.py

RANDOM_SEED: int = 42
STATION_TANK_SIZE: int = 200  # Size of the gas station tank (liters)
THRESHOLD: int = 25  # Station tank minimum level (% of full)
CAR_TANK_SIZE: int = 50  # Size of car fuel tanks (liters)
CAR_TANK_LEVEL: list[int] = [5, 25]  # Min/max levels of car fuel tanks (liters)
REFUELING_SPEED: int = 2  # Rate of refuelling car fuel tank (liters / second)
TANK_TRUCK_TIME: int = 300  # Time it takes tank truck to arrive (seconds)
T_INTER: list[int] = [10, 200]  # Interval between car arrivals [min, max] (seconds)
SIM_TIME: int = 11000  # Simulation time (seconds)
NUM_DISTRIBUTORS = 4
