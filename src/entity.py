from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt


class Entity:
    def __init__(self, x, y, name=None):
        self.x = x
        self.y = y
        if not name:
            name = f"Entity at ({x}, {y})"
        self.name = name

    def distance_to(self, other) -> float:
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self):
        return f"{self.name}"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Entity):
            return False
        return self.x == value.x and self.y == value.y
