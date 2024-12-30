import curses

# Example map function
def generate_map():
    return [
        "LLLLLLLLGGGGGFFFF",
        "FFFFFFFGGGGGGGLLLL",
        "LLLLLLLLGGGGGFFFF",
        "FFFFFFFGGGGGGGLLLL",
    ]

# Example stats function
def get_stats():
    return {
        "Name": "Karl the Conjurer",
        "Location": "The Dungeons of Doom",
        "Strength": 10,
        "Intelligence": 16,
        "Wisdom": 8,
        "Dexterity": 16,
        "Constitution": 14,
        "Charisma": 14,
        "Alignment": "Chaotic Neutral",
        "Dungeon Level": 3,
        "Gold": 80,
        "Hit Points": "9/27",
        "Magic Power": "22/38",
        "Armor Class": 10,
        "Level": 5,
        "Status": "Satiated",
    }

def draw_ui(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    while True:
        # Get current screen dimensions
        height, width = stdscr.getmaxyx()

        # Clear screen and check resizing
        stdscr.clear()
        if curses.is_term_resized(height, width):
            curses.resizeterm(height, width)

        # Dynamic dimensions
        left_width = width // 3
        right_width = width - left_width - 2  # Account for box border
        bottom_height = 3
        map_height = height - bottom_height - 2  # Account for box borders

        # Create subwindows for left panel, map, and stats
        left_panel = stdscr.subwin(map_height + 2, left_width + 1, 0, 0)  # Add border space
        map_panel = stdscr.subwin(map_height + 2, right_width + 1, 0, left_width + 1)
        input_panel = stdscr.subwin(bottom_height, width, height - bottom_height, 0)

        # Add boxes to separate areas
        left_panel.box()
        map_panel.box()
        input_panel.box()

        # Render content in the left panel
        left_panel.addstr(1, 2, "NOTEBOOK FEATURES TBA")

        # Render map in the map panel
        map_title = "Map -- Dynamically Generated"
        map_panel.addstr(1, 2, map_title[:right_width - 2])

        # Example map (dynamic truncation if needed)
        map_data = generate_map()
        for i, line in enumerate(map_data):
            if 2 + i < map_height:
                map_panel.addstr(2 + i, 2, line[:right_width - 2])

        # Render stats in the map panel
        stats = get_stats()
        y_offset = len(map_data) + 3
        for i, (key, value) in enumerate(stats.items()):
            if y_offset + i < map_height:
                stat_line = f"{key}: {value}"
                map_panel.addstr(y_offset + i, 2, stat_line[:right_width - 2])

        # Render input and help bar
        input_panel.addstr(1, 2, "Enter Input Here: ")
        help_text = "h - help | a - abilities | i - inventory | q - save and quit | s - settings"
        stdscr.addstr(height - 1, 1, help_text[:width - 2])

        # Refresh subwindows
        left_panel.refresh()
        map_panel.refresh()
        input_panel.refresh()

        # Handle user input
        key = stdscr.getch()
        if key == ord('q'):  # Exit on 'q'
            break

curses.wrapper(draw_ui)