import numpy as np


from typing import List, Tuple
import numpy as np


def interpolate_fuel_levels(
    time_points: List[int], distributor_fuel_levels: List[List[float]]
) -> Tuple[List[np.ndarray]]:
    time_points_array = np.array(time_points)
    new_time_points = np.linspace(
        time_points_array.min(), time_points_array.max(), len(time_points)
    )
    interpolated_distributor_fuel_levels = [
        np.interp(new_time_points, time_points_array, distributor_fuel_level)
        for distributor_fuel_level in distributor_fuel_levels
    ]

    return interpolated_distributor_fuel_levels
