def get_gold() -> int:
    """
    Get the user's current gold amount. Returns an integer.
    """
    pass

def get_health() -> int:
    """
    Get the user's current health. Returns an integer.
    """
    pass

def get_inventory() -> list:
    """
    Get the user's inventory. Returns a list of dictionaries. Each dictionary contains the item's name, type, damage (if applicable), bonus (if applicable), and other information
    """
    pass

def get_location() -> tuple:
    """
    Get the user's current location. Returns a tuple of integers. The first integer is the x-coordinate (horizontal position on the map) and the second integer is the y-coordinate (vertical position on the map). The third integer is the z-coordinate (depth). If z >= 0, the user is on the surface. If z < 0, the user is underground. The surface is at z = 0.
    """
    pass

def get_map() -> list:
    """
    Get the current map. Returns a 2d list array representing the map. The following are each type of tile:
    M - Mountains; Color - White
    F - Forest; Color - Green
    f - Fields; Color - Light Green
    d - Desert; Color - Yellow
    g - Grass; Color - Green
    s - Sand; Color - Red
    w - Shallow Water; Color - Blue
    W - Deep Water; Color - Blue
    """
    pass