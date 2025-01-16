from typing import Optional

def print_colored(text, text_color=None, bg_color=None):
    def hex_to_ansi(hex_color, is_background=False):
        if not hex_color:
            return ""
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        return f"\033[{48 if is_background else 38};2;{r};{g};{b}m"

    text_color_code = hex_to_ansi(text_color)
    background_color_code = hex_to_ansi(bg_color, is_background=True)
    reset_code = "\033[0m"

    return f"{background_color_code}{text_color_code}{text}{reset_code}"

map_legend = [
    {"symbol": "p", "biome": "Plains", "text_color": "#2AC42E", "background_color": None},
    {"symbol": "h", "biome": "Hills", "text_color": "#2ED332", "background_color": None},
    {"symbol": "v", "biome": "Valley", "text_color": "#31E134", "background_color": None},
    {"symbol": "f", "biome": "Light Forest", "text_color": "#27A828", "background_color": None},
    {"symbol": "F", "biome": "Dense Forest", "text_color": "#27AA29", "background_color": None},
    {"symbol": "J", "biome": "Jungle", "text_color": "#25A024", "background_color": None},
    {"symbol": "y", "biome": "Swamp", "text_color": "#DAD91B", "background_color": None},
    {"symbol": "Y", "biome": "Field", "text_color": "#FBFA1E", "background_color": None},
    {"symbol": "b", "biome": "Beach", "text_color": "#F7F61F", "background_color": None},
    {"symbol": "d", "biome": "Desert", "text_color": "#CBCA1B", "background_color": None},
    {"symbol": "c", "biome": "Canyon", "text_color": "#4C4C4C", "background_color": None},
    {"symbol": "C", "biome": "Chasm", "text_color": "#4C4C4C", "background_color": None},
    {"symbol": "s", "biome": "Snow", "text_color": "#FFFFFF", "background_color": None},
    {"symbol": "r", "biome": "River", "text_color": "#010080", "background_color": None},
    {"symbol": "l", "biome": "Lake", "text_color": "#010081", "background_color": None},
    {"symbol": "w", "biome": "Waterfall", "text_color": "#010080", "background_color": None},
    {"symbol": "R", "biome": "Reef", "text_color": "#E251D9", "background_color": None},
    {"symbol": "L", "biome": "Lava", "text_color": "#E43332", "background_color": None},
    {"symbol": "^", "biome": "Mountain", "text_color": "#8D8D20", "background_color": None},
    {"symbol": "^", "biome": "Snowy Mountain", "text_color": "#FFFFFF", "background_color": None},
    {"symbol": "~", "biome": "Shallow Ocean", "text_color": "#FFFFFF", "background_color": "#027D7E"},
    {"symbol": "~", "biome": "Deep Ocean", "text_color": "#FFFFFF", "background_color": "#01007C"},
    {"symbol": "/-\\|", "biome": "Roads", "text_color": "#7F7E1C", "background_color": None},
    {"symbol": "/-\\|", "biome": "Walls", "text_color": "#525252", "background_color": None},
    {"symbol": "/-\\|", "biome": "Cliffs", "text_color": "#525252", "background_color": None},
    {"symbol": "/-\\|", "biome": "Bridges", "text_color": "#525252", "background_color": None},
    {"symbol": "?", "biome": "Point of Interest", "text_color": "#FFFFFF", "background_color": None},
    {"symbol": "#", "biome": "Entrance", "text_color": "#FFFFFF", "background_color": None},
    {"symbol": "!", "biome": "Tower", "text_color": "#FFFFFF", "background_color": None},
    {"symbol": "%", "biome": "Keep", "text_color": "#FFFFFF", "background_color": None},
    {"symbol": "%", "biome": "Fortress", "text_color": "#FFFFFF", "background_color": None},
    {"symbol": "=", "biome": "Cityscape", "text_color": "#05A5A6", "background_color": None},
]

def biome(biome: str, rotation_angle: Optional[float] = 0) -> None:
    """
    Prints the symbol of a biome in its corresponding color. For Roads, Walls, Cliffs, or Bridges,
    the symbol adjusts based on the rotation_angle provided.

    Args:
        biome (str): The name of the biome to look up. 
        \n
        Biomes: Plains, Hills, Valley, Light Forest, Dense Forest, Jungle, Swamp, Field, Beach, Desert, Canyon, Chasm, Snow, River, Lake, Waterfall, Reef, Lava, Mountain, Snowy Mountain, Shallow Ocean, Deep Ocean, Roads, Walls, Cliffs, Bridges, Point of Interest, Entrance, Tower, Keep, Fortress, Cityscape
        \n\n
        rotation_angle (optional float): The rotation angle in degrees (used only for Roads, Walls, Cliffs, Bridges).
                                          Rounds to the nearest multiple of 45°.

    Returns:
        None: Prints the symbol with the appropriate color or an error message if the biome is not found.
    """
    # Define rotation symbols
    rotation_symbols = {0: "|", 45: "/", 90: "-", 135: "\\", 180: "|"}
    
    # Find the biome in map_legend
    biome_data = next((item for item in map_legend if item["biome"].lower() == biome.lower()), None)

    if not biome_data:
        raise ValueError(f"Biome '{biome}' not found in the map legend.")

    # Handle rotation angle for Roads, Walls, Cliffs, Bridges
    symbol = biome_data["symbol"]
    if biome.lower() in ["roads", "walls", "cliffs", "bridges"]:
        normalized_angle = round(rotation_angle / 45) * 45 % 180  # Normalize to 0°, 45°, 90°, 135°, or 180°
        symbol = rotation_symbols.get(normalized_angle, "|")

    # Print the symbol with its color
    text_color = biome_data["text_color"]
    background_color = biome_data["background_color"]

    return print_colored(symbol, text_color, background_color)



if __name__ == "__main__":
    for i in range(100):
        for i in range(360):
            # print(biome("Roads"), end="")
            print(biome("Deep Ocean"), end="")
        print()
    