import math


def get_coords(angle, distance) -> tuple:
    return (distance * math.cos(math.radians(angle)), distance * math.sin(math.radians(angle)))


def calculate_area(data: list) -> float:
    area = 0

    last_point = data[0]
    for i in range(1, len(data)):
        area += _get_area_slice(last_point, data[i])
        last_point = data[i]

    # square cm to square meter
    return area * 0.0001


# SAS area of triangle to approximate area
def _get_area_slice(dist_one, dist_two) -> float:
    # 0.5 degree angle, sin(rad(0.5)) = 0.00872653923
    return 0.5 * dist_one * dist_two * 0.00872653923
