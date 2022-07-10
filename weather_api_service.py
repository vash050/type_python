from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TypeAlias

from coordinates import Coordinates

Celsius: TypeAlias = int


class WeatherType(str, Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


@dataclass(slots=True, frozen=True)
class Weather:
    weather_type = WeatherType
    temperature = Celsius
    sunrise = datetime
    sunset = datetime
    place = str


def get_weather(coordinates: Coordinates) -> Weather:
    """
    Requests weather in OpenWeather API and returns it
    :param coordinates: Coordinates
    :return: Weather
    """
    return Weather(
        temperature=20,
        weather_type=WeatherType.CLEAR,
        sunrise=datetime.fromisoformat("2022-05-04 04:00:00"),
        sunset=datetime.fromisoformat("2022-05-04 20:25:00"),
        city="Moscow"
    )
