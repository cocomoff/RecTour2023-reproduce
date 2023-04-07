import numpy as np


def dG(lat1, lon1, lat2, lon2, R=6371000):
    """
    Simple version of Harvesine formula
    """
    from math import radians, sin, asin, cos, sqrt

    pi, ri = radians(lat1), radians(lon1)
    pj, rj = radians(lat2), radians(lon2)
    v1 = sin((pi - pj) / 2)
    v2 = sin((ri - rj) / 2)
    d = 2 * R * asin(sqrt(v1**2 + cos(pi) * cos(pj) * v2**2))
    # m -> km
    return d / 1000


def calc_dist_vec(
    longitudes1: np.ndarray,
    latitudes1: np.ndarray,
    longitudes2: np.ndarray,
    latitudes2: np.ndarray,
) -> np.ndarray:
    """
    Calculate the distance (unit: km) between two places on earth, vectorised.

    See
    - The haversine formula, en.wikipedia.org/wiki/Great-circle_distance
    - Mean earth radius, en.wikipedia.org/wiki/Earth_radius#Mean_radius
    """
    # convert degrees to radians
    lng1 = np.radians(longitudes1)
    lat1 = np.radians(latitudes1)
    lng2 = np.radians(longitudes2)
    lat2 = np.radians(latitudes2)
    radius = 6371.0088

    dlng = np.fabs(lng1 - lng2)
    dlat = np.fabs(lat1 - lat2)
    dist = (
        2
        * radius
        * np.arcsin(
            np.sqrt(
                (np.sin(0.5 * dlat)) ** 2
                + np.cos(lat1) * np.cos(lat2) * (np.sin(0.5 * dlng)) ** 2
            )
        )
    )
    return dist


"""
List of city names in Japan.
"""
city_names = [
    "beppu",
    "fukuoka",
    "hiroshima",
    "kanazawa",
    "kumamoto",
    "kyoto",
    "matsumoto",
    "nagasaki",
    "naha",
    "osaka",
    "tokyo",
]
