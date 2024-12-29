import curses, time, json, re, threading, textwrap
import ollama
from player import Player

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.player = Player()
        self.game_content = []
        self.scroll_pos = 0
        self.generation = False
        self.model = ['llama3.2', 'qwen2.5', 'llama3.2-vision:11b'][0]
        self.messages = []
        self.setup_windows()

    def setup_windows(self):
        height, width = self.stdscr.getmaxyx()
        self.stat_win = curses.newwin(3, width, 0, 0)
        self.game_h = height - 6
        self.game_win = curses.newwin(self.game_h, width, 3, 0)
        self.input_win = curses.newwin(3, width, height - 3, 0)
        self.notif_win = curses.newwin(1, width, height - 4, 0)
        self.game_win.scrollok(True)
        self.game_win.idlok(True)
        self.input_win.keypad(True)

    def stats_display(self):
        self.stat_win.clear()
        self.stat_win.box()
        txt = (
            f" Health: {int(self.player.stats.get('Health', 0))} | "
            f"Hunger: {int(self.player.stats.get('Hunger', 0))} | "
            f"Thirst: {int(self.player.stats.get('Thirst', 0))} | "
            f"Gold: {self.player.gold} | "
            f"Press 'i' for Inventory "
        )
        x = (self.stat_win.getmaxyx()[1] - len(txt)) // 2
        self.stat_win.addstr(1, max(x, 1), txt)
        self.stat_win.refresh()

    def notif(self, msg, color=0):
        self.notif_win.clear()
        if color != 0:
            self.notif_win.addstr(0, self.notif_win.getmaxyx()[1] - len(msg) - 2, msg, curses.color_pair(color))
        else:
            self.notif_win.addstr(0, self.notif_win.getmaxyx()[1] - len(msg) - 2, msg)
        self.notif_win.refresh()
        time.sleep(2)
        self.notif_win.clear()
        self.notif_win.refresh()

    def inv_display(self):
        height, width = self.stdscr.getmaxyx()
        inv_win = curses.newwin(height, width, 0, 0)
        inv_win.clear()
        inv_win.box()
        title = "Inventory"
        inv_win.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD | curses.A_UNDERLINE)
        for idx, item in enumerate(self.player.inventory):
            inv_win.addstr(idx + 3, 2, f"- {item}")
        prompt = "Press any key to return"
        inv_win.addstr(height - 2, (width - len(prompt)) // 2, prompt)
        inv_win.refresh()
        inv_win.getch()
        inv_win.clear()
        inv_win.refresh()
        self.stats_display()
        self.refresh_game()

    def refresh_game(self):
        self.game_win.clear()
        start = max(0, self.scroll_pos)
        end = start + self.game_h - 2
        displayed = self.game_content[start:end]
        y = 1
        for line in displayed:
            try:
                self.game_win.addstr(y, 1, line)
            except curses.error:
                pass
            y += 1
        self.game_win.box()
        self.game_win.refresh()

    def adjust_scroll(self):
        total = len(self.game_content)
        self.scroll_pos = max(0, total - (self.game_h - 2))

    def parse_state(self, resp):
        pattern = r'<state>(.*?)</state>'
        match = re.search(pattern, resp, re.DOTALL)
        if match:
            state_json = match.group(1)
            try:
                changes = json.loads(state_json)
                self.player.update_stats(changes.get('stats', {}))
                self.player.update_inventory(changes.get('inventory', {}))
                self.player.update_gold(changes.get('gold', 0))
            except json.JSONDecodeError:
                pass
            resp = re.sub(pattern, '', resp, flags=re.DOTALL).strip()
        return resp

    def handle_input(self):
        input_win = self.input_win
        curses.curs_set(1)
        input_win.clear()
        input_win.border()
        input_win.addstr(1, 2, "> ")
        input_win.refresh()
        user_input = ""
        while True:
            key = input_win.get_wch()
            if key == '\n':
                break
            elif key in ('\x7f', '\b', '\x08'):
                if len(user_input) > 0:
                    user_input = user_input[:-1]
            else:
                user_input += key
            input_win.addstr(1, 4, user_input)
            input_win.refresh()
        curses.curs_set(0)
        return user_input.strip()

    def run(self):
        self.stats_display()
        while True:
            user_input = self.handle_input()
            if user_input.lower() in ["exit", "quit"]:
                break
            elif user_input.lower() == 'i':
                self.inv_display()
            else:
                self.game_content.append(f"> {user_input}")
                self.refresh_game()


def main(stdscr):
    game = Game(stdscr)
    game.run()


if __name__ == "__main__":
    curses.wrapper(main)