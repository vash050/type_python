import json
import ssl
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from json import JSONDecodeError
from typing import TypeAlias, Literal
from urllib.error import URLError

import config
from coordinates import Coordinates
from exceptions import CantGetWeather

Celsius: TypeAlias = int


class WeatherType(str, Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


@dataclass
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    place: str


def get_weather(coordinates: Coordinates) -> Weather:
    """
    Requests weather in OpenWeather API and returns it
    :param coordinates: Coordinates
    :return: Weather
    """
    response_from_openweather = _get_weather_from_openweather(
        longitude=coordinates.longitude,
        latitude=coordinates.latitude
    )

    weather = _parse_response_from_openweather(response_from_openweather)
    return weather


def _get_weather_from_openweather(longitude: float, latitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise CantGetWeather


def _parse_response_from_openweather(response_from_site: str) -> Weather:
    try:
        openweather_dict = json.loads(response_from_site)
    except JSONDecodeError:
        raise CantGetWeather
    return Weather(
        temperature=_parse_temperature(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, "sunrise"),
        sunset=_parse_sun_time(openweather_dict, "sunset"),
        place=_parse_city(openweather_dict)
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict["main"]["temp"])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise CantGetWeather
    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise CantGetWeather


def _parse_sun_time(
        openweather_dict: dict,
        time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
    return datetime.fromtimestamp(openweather_dict["sys"][time])


def _parse_city(openweather_dict: dict) -> str:
    return openweather_dict["name"]


if __name__ == "__main__":
    print(get_weather(Coordinates(longitude=64.6, latitude=30.6)))
