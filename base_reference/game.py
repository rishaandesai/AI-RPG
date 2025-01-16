import curses

class NetHackFramework:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_windows()

    def setup_windows(self):
        height, width = self.stdscr.getmaxyx()

        # Status Bar at the Top
        self.stat_win = curses.newwin(3, width, 0, 0)

        # Main Map/Gameplay Area
        self.map_h = height - 6
        self.map_win = curses.newwin(self.map_h, int(width * 0.7), 3, 0)

        # Sidebar for Stats/Details
        self.sidebar_win = curses.newwin(self.map_h, width - int(width * 0.7), 3, int(width * 0.7))

        # Notification Bar
        self.notif_win = curses.newwin(1, width, height - 4, 0)

        # Input Bar at the Bottom
        self.input_win = curses.newwin(3, width, height - 3, 0)
        self.input_win.keypad(True)

        # Configure windows
        self.map_win.scrollok(True)
        self.map_win.idlok(True)

    def draw_borders(self):
        self.stat_win.clear()
        self.stat_win.border(0)
        self.stat_win.addstr(1, 2, "Status Bar")
        self.stat_win.refresh()

        self.map_win.clear()
        self.map_win.border(0)
        self.map_win.addstr(1, 2, "Map Area")
        self.map_win.refresh()

        self.sidebar_win.clear()
        self.sidebar_win.border(0)
        self.sidebar_win.addstr(1, 2, "Sidebar (Stats/Details)")
        self.sidebar_win.refresh()

        self.notif_win.clear()
        self.notif_win.border(0)
        self.notif_win.addstr(0, 2, "Notification Area")
        self.notif_win.refresh()

        self.input_win.clear()
        self.input_win.border(0)
        self.input_win.addstr(1, 2, "> ")
        self.input_win.refresh()

    def handle_input(self):
        curses.curs_set(1)
        user_input = ""
        while True:
            key = self.input_win.get_wch()
            if key == '\n':
                break
            elif key in ('\x7f', '\b', '\x08'):  # Backspace
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

    def display_notification(self, message):
        self.notif_win.clear()
        self.notif_win.border(0)
        self.notif_win.addstr(0, 2, message)
        self.notif_win.refresh()
        curses.napms(2000)
        self.notif_win.clear()
        self.notif_win.refresh()

    def run(self):
        self.draw_borders()
        while True:
            user_input = self.handle_input()
            if user_input.lower() in ["quit", "exit"]:
                break
            elif user_input:
                self.map_win.addstr(1, 2, f"You entered: {user_input}")
                self.map_win.refresh()
                self.display_notification("Input received!")


def main(stdscr):
    curses.curs_set(0)
    app = NetHackFramework(stdscr)
    app.run()

if __name__ == "__main__":
    curses.wrapper(main)