import curses

def draw_interface(stdscr):
    try:
        curses.curs_set(0)  # Disable cursor
        stdscr.clear()

        # Screen dimensions
        height, width = stdscr.getmaxyx()

        # Check for minimum terminal size
        if height < 24 or width < 80:
            stdscr.addstr(0, 0, "Terminal too small. Resize and try again.")
            stdscr.refresh()
            stdscr.getch()
            return

        # Panel dimensions
        top_panel_height = int(height * 0.6)  # Top panels take 60% of the height
        bottom_panel_height = height - top_panel_height
        panel_width = width // 3

        # Create windows for each panel
        notebook_win = curses.newwin(top_panel_height, panel_width, 0, 0)
        story_win = curses.newwin(top_panel_height, panel_width, 0, panel_width)
        map_win = curses.newwin(top_panel_height, panel_width, 0, 2 * panel_width)
        keymap_win = curses.newwin(bottom_panel_height, panel_width, top_panel_height, 0)
        input_win = curses.newwin(bottom_panel_height, panel_width, top_panel_height, panel_width)
        stats_win = curses.newwin(bottom_panel_height, panel_width, top_panel_height, 2 * panel_width)

        # Draw boxes around each panel
        notebook_win.box()
        story_win.box()
        map_win.box()
        keymap_win.box()
        input_win.box()
        stats_win.box()

        # Add content to the notebook panel
        notebook_win.addstr(2, 2, "NOTEBOOK FEATURES TBA")
        notebook_win.addstr(4, 2, "Leave blank for now")
        notebook_win.refresh()

        # Add content to the story panel
        for i in range(3, top_panel_height - 2):
            story_win.addstr(i, 2, "Bla Bla Previous Story here")
        story_win.refresh()

        # Add content to the map panel
        map_section = [
            "LLLLLLLLGGGGFFFFFFFFGGGGGGLL",
            "LLLLLLLLGGGGFFFFFFFFGGGGGGLL",
            "OOOOOOOOOOFFFFFFFFFOOOOOOOOO",
            "OOOOOOOOOOFFFFFFFFFOOOOOOOOO",
            "LLLLLLLLGGGGFFFFFFFFFOOOOOOO",
            "FFFFFFFFFRRGGGLLLLLLGGGGGFFF",
            "FFFFFFFFFRRGGGLLLLLLGGGGGFFF",
            "FFFFFFFFFRRGGGLLLLLLGGGGGFFF",
            "FFFFFFFFFRRGGGLLLLLLGGGGGFFF",
        ]
        for idx, line in enumerate(map_section):
            if idx + 2 < top_panel_height - 1:
                map_win.addstr(2 + idx, 2, line)
        map_win.refresh()

        # Add content to the keymap panel
        keymap_win.addstr(2, 2, "h - help")
        keymap_win.addstr(3, 2, "a - abilities")
        keymap_win.addstr(4, 2, "i - inventory")
        keymap_win.addstr(5, 2, "q - save and quit")
        keymap_win.refresh()

        # Add content to the input panel
        input_win.addstr(2, 2, "Enter Input Here")
        input_win.refresh()

        # Add content to the stats panel
        stats = [
            "Karl the Conjurer",
            "The Dungeons of Doom",
            "Strength: 10",
            "Intelligence: 16",
            "Wisdom: 8",
            "Dexterity: 16",
            "Constitution: 14",
            "Charisma: 14",
            "Alignment: Chaotic Neutral",
            "Dungeon Level: 3",
            "Gold: 80",
            "Hit Points: 9/27",
            "Magic Power: 22/38",
            "Armor Class: 10",
            "Level: 5",
            "Satiated",
        ]
        for idx, stat in enumerate(stats):
            if idx + 2 < bottom_panel_height - 1:
                stats_win.addstr(2 + idx, 2, stat)
        stats_win.refresh()

        # Wait for user input before exiting
        stdscr.getch()
    except curses.error as e:
        # Log the error to a file for debugging
        with open("curses_error.log", "w") as log_file:
            log_file.write(str(e))
        raise

curses.wrapper(draw_interface)