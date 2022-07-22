import re
from dataclasses import dataclass
from subprocess import Popen, PIPE
from typing import Literal

import config
from exceptions import CantGetCoordinates


@dataclass(slots=True, frozen=True)
class Coordinates:
    longitude: float
    latitude: float


def get_gps_coordinates() -> Coordinates:
    """
    Return current coordinates from ipinfo.io
    :return: Coordinates
    """

    coordinates = _get_coordinates_from_ipinfo()
    return _round_coordinates(coordinates)


def _get_coordinates_from_ipinfo() -> Coordinates:
    ipinfo_output = _get_ipinfo_output()
    coordinates = _parse_coordinates(ipinfo_output)
    return coordinates


def _get_ipinfo_output() -> bytes:
    process = Popen(["curl", "-s", "ipinfo.io"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    return output


def _parse_coordinates(ipinfo_output: bytes) -> Coordinates:
    try:
        output = ipinfo_output.decode().strip().lower().split("\n")
        latitude, longitude = _parse_coord(output, "loc")
    except UnicodeDecodeError:
        raise CantGetCoordinates
    return Coordinates(
        latitude=latitude,
        longitude=longitude
    )


def _parse_coord(
        output: list[str],
        coord_type: Literal["loc"]) -> tuple:
    for line in output:
        if re.search(f"{coord_type}", line):
            key, value = line.split()
            return _parse_float_coordinate(value.strip(',"').split(','))
    else:
        raise CantGetCoordinates


def _parse_float_coordinate(value: list[str]) -> tuple[float]:
    try:
        return tuple(map(float, value))
    except ValueError:
        raise CantGetCoordinates


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(
        lambda x: round(x, 1),
        [coordinates.latitude, coordinates.longitude]
    ))


if __name__ == "__main__":
    get_gps_coordinates()
