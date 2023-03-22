from serial_monitor import SerialController, Signal
from map_walls import WallMapper
from utils import calculate_area
import numpy as np

OUTLIER_THRESHOLD = 3
MAX_DIST = 400


class Controller:
    def __init__(self) -> None:
        self.serial_controller = SerialController()
        self.normalized_data = []

    def get_room_data(self) -> None:
        print("Gathering Room Data...")
        print(" -> Turning Counterclockwise...")
        counter_clockwise_data = self.serial_controller.get_room_data(Signal.COUNTER_CLOCKWISE)
        print(f"   -> {len(counter_clockwise_data)} Points Measured")

        print(" -> Turning Clockwise...")
        clockwise_data = self.serial_controller.get_room_data(Signal.CLOCKWISE)
        print(f"   -> {len(clockwise_data)} Points Measured")

        self._normalize_scan_data(clockwise=clockwise_data, counter_clockwise_data=counter_clockwise_data)

    def _normalize_scan_data(self, clockwise, counter_clockwise_data) -> None:
        counter_clockwise_data.reverse()
        reversed_counter_clockwise = counter_clockwise_data

        if len(clockwise) != len(reversed_counter_clockwise):
            raise Exception("Mismatched Scan Length")

        print("\nNormalizing Outliers In Scanned Data...")
        for i in range(len(clockwise)):
            if clockwise[i] > MAX_DIST:
                clockwise[i] = MAX_DIST
            if reversed_counter_clockwise[i] > MAX_DIST:
                reversed_counter_clockwise[i] = MAX_DIST

        normalized_clockwise = np.zeros_like(clockwise, dtype=np.float64)
        for i in range(len(clockwise)):
            if i == 0 or i == len(clockwise) - 1:  # skip first and last elements
                normalized_clockwise[i] = clockwise[i]
            else:
                adjacent_values = [clockwise[i - 1], clockwise[i + 1]]
                mean = np.mean(adjacent_values)
                std = np.std(adjacent_values)
                if abs(clockwise[i] - mean) > OUTLIER_THRESHOLD * std:
                    normalized_clockwise[i] = mean  # replace outlier with mean of adjacent values
                else:
                    normalized_clockwise[i] = clockwise[i]

        normalized_counter_clockwise = np.zeros_like(reversed_counter_clockwise, dtype=np.float64)
        for i in range(len(reversed_counter_clockwise)):
            if i == 0 or i == len(reversed_counter_clockwise) - 1:  # skip first and last elements
                normalized_counter_clockwise[i] = reversed_counter_clockwise[i]
            else:
                adjacent_values = [reversed_counter_clockwise[i - 1], reversed_counter_clockwise[i + 1]]
                mean = np.mean(adjacent_values)
                std = np.std(adjacent_values)
                if abs(reversed_counter_clockwise[i] - mean) > OUTLIER_THRESHOLD * std:
                    normalized_counter_clockwise[i] = mean  # replace outlier with mean of adjacent values
                else:
                    normalized_counter_clockwise[i] = reversed_counter_clockwise[i]

        for i in range(len(normalized_clockwise)):
            self.normalized_data.append((normalized_clockwise[i] + normalized_counter_clockwise[i]) / 2)

    def create_wall_map(self) -> None:
        print("Creating Wall Map Image...")
        wall_mapper = WallMapper()
        wall_mapper.process_data(self.normalized_data, "./scan_result.png")

    def calculate_approx_area(self) -> None:
        print("Calculating Approximate Area...")
        print(f"Approximate Area: {calculate_area(self.normalized_data)} m^2")


controller = Controller()
controller.get_room_data()
controller.create_wall_map()
controller.calculate_approx_area()
