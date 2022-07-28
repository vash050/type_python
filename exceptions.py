class CantGetCoordinates(Exception):
    """Program can't get current GPS coordinates"""
    pass


class CantGetWeather(Exception):
    """Program can't get current weather"""
    pass


class DonNotReadToFileTxt(Exception):
    """Program can't read data in file.txt"""
    pass


class DonNotReadToFileJson(Exception):
    """Program can't read data in file.json"""
    pass
