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