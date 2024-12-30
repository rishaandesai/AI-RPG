import curses


class NetHackFramework:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def setup_windows(self):
        self.height, self.width = self.stdscr.getmaxyx()

        # Status bar at the top
        self.stat_win = curses.newwin(3, self.width, 0, 0)

        # Main map/gameplay area
        self.map_h = self.height - 6
        self.map_w = int(self.width * 0.7)
        self.map_win = curses.newwin(self.map_h, self.map_w, 3, 0)

        # Sidebar for stats/details
        self.sidebar_w = self.width - self.map_w
        self.sidebar_win = curses.newwin(self.map_h, self.sidebar_w, 3, self.map_w)

        # Input bar at the bottom
        self.input_win = curses.newwin(3, self.width, self.height - 3, 0)
        self.input_win.keypad(True)

        # Enable scrolling for the map window
        self.map_win.scrollok(True)
        self.map_win.idlok(True)

    def draw_borders(self):
        # Draw borders for all windows
        self.stat_win.clear()
        self.stat_win.border(0)
        self.stat_win.addstr(1, 2, " Status Bar ")
        self.stat_win.refresh()

        self.map_win.clear()
        self.map_win.border(0)
        self.map_win.addstr(1, 2, " Map Area ")
        self.map_win.refresh()

        self.sidebar_win.clear()
        self.sidebar_win.border(0)
        self.sidebar_win.addstr(1, 2, " Sidebar (Stats/Details) ")
        self.sidebar_win.refresh()

        self.input_win.clear()
        self.input_win.border(0)
        self.input_win.addstr(1, 2, "> ")
        self.input_win.refresh()

    def handle_input(self):
        curses.curs_set(1)
        user_input = ""
        while True:
            key = self.input_win.get_wch()
            if key == "\n":  # Enter key to submit input
                break
            elif key in ("\x7f", "\b", "\x08"):  # Backspace
                if len(user_input) > 0:
                    user_input = user_input[:-1]
            else:
                user_input += key
            self.input_win.clear()
            self.input_win.border(0)
            self.input_win.addstr(1, 2, f"> {user_input}")
            self.input_win.refresh()
        curses.curs_set(0)
        return user_input.strip()

    def adjust_layout(self):
        # Adjust the layout dynamically
        self.setup_windows()
        self.draw_borders()

    def run(self):
        self.setup_windows()
        self.draw_borders()
        while True:
            self.height, self.width = self.stdscr.getmaxyx()
            if (
                self.height != self.stdscr.getmaxyx()[0]
                or self.width != self.stdscr.getmaxyx()[1]
            ):
                self.adjust_layout()

            user_input = self.handle_input()
            if user_input.lower() in ["quit", "exit"]:
                break
            elif user_input:
                # Example: Update the map area with the input for demonstration
                self.map_win.addstr(2, 2, f"You entered: {user_input}")
                self.map_win.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()
    app = NetHackFramework(stdscr)
    app.run()


if __name__ == "__main__":
    curses.wrapper(main)