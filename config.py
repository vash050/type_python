from env import OPENWEATHER_API

USE_ROUNDED_COORDS = True
OPENWEATHER_API = OPENWEATHER_API
OPENWEATHER_URL = (
        "https://api.openweathermap.org/data/2.5/weather?"
        "lat={latitude}&lon={longitude}&"
        "appid=" + OPENWEATHER_API + "&lang=ru&"
        "units=metric"
)
