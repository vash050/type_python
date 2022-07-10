import json
from dataclasses import dataclass
from subprocess import Popen, PIPE

import config
from profiler import profiler
from exceptions import CantGetCoordinates


@dataclass(slots=True, frozen=True)
class Coordinates:
    longitude: float
    latitude: float


@profiler
def get_gps_coordinates() -> Coordinates:
    process = Popen(["curl", "ipinfo.io"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    latitude, longitude = map(float, json.loads(output.decode())['loc'].split(','))
    if config.USE_ROUNDED_COORDS:
        latitude, longitude = map(lambda x: round(x, 1), [latitude, longitude])
    return Coordinates(longitude=longitude, latitude=latitude)


# @profiler
# def get_gps_coordinates_1() -> Coordinates:
#     process = Popen(["curl", "ipinfo.io"], stdout=PIPE)
#     (output, err) = process.communicate()
#     exit_code = process.wait()
#     if err is not None or exit_code != 0:
#         raise CantGetCoordinates
#     loc = json.loads(output.decode())['loc']
#     longitude = loc[0]
#     latitude = loc[1]
#     return Coordinates(longitude=longitude, latitude=latitude)


if __name__ == "__main__":
    print(get_gps_coordinates())
    # get_gps_coordinates_1()
