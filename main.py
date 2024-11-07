import locale
import ollama, curses, time, json, re, random, textwrap, threading
from parser import parse
import sys
sys.stdout.reconfigure(encoding='utf-8')

model = ['llama3.2', 'qwen2.5'][0]

stats = {
    'Health': 100.0,
    'Hunger': 50.0,
    'Thirst': 75.0,
    'Strength': 10.0,
    'Dexterity': 10.0,
    'Constitution': 10.0,
    'Intelligence': 10.0,
    'Wisdom': 10.0,
    'Charisma': 10.0,
    'Passive Perception': 10.0,
    'Hit Points': 50.0,
    'Death': 100.0
}

inv = [
    'Short sword',
    'Leather tunic',
    'Wooden shield',
    "Backpack with 2 days' worth of rations",
    'Empty waterskin',
    '10 gold pieces'
]

gold = 10
msgs = []

def sys_msg():
    with open('/Users/rishaandesai/Downloads/AI Dungeon/instructions.txt', 'r') as f:
        instructions = f.read()
    return {'role': 'user', 'content': instructions}

# Initialize msgs with sys_msg only once
msgs = [sys_msg()]

def main(stdscr):
    global generation
    locale.setlocale(locale.LC_ALL, '')
    generation = False
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    height, width = stdscr.getmaxyx()
    stat_win = curses.newwin(3, width, 0, 0)
    game_h = height - 6
    game_win = curses.newwin(game_h, width, 3, 0)
    input_win = curses.newwin(3, width, height - 3, 0)
    notif_win = curses.newwin(1, width, height - 4, 0)
    game_win.scrollok(True)
    game_win.idlok(True)
    input_win.keypad(True)
    game_content = []
    scroll_pos = 0

    def stats_display():
        stat_win.clear()
        stat_win.box()
        txt = (
            f" Health: {int(stats.get('Health', 0))} | "
            f"Hunger: {int(stats.get('Hunger', 0))} | "
            f"Thirst: {int(stats.get('Thirst', 0))} | "
            f"Gold: {gold} | "
            f"Press 'i' for Inventory "
        )
        x = (width - len(txt)) // 2
        stat_win.addstr(1, max(x, 1), txt)
        stat_win.refresh()

    def inv_display():
        inv_win = curses.newwin(height, width, 0, 0)
        inv_win.clear()
        inv_win.box()
        title = "Inventory"
        inv_win.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD | curses.A_UNDERLINE)
        for idx, item in enumerate(inv):
            inv_win.addstr(idx + 3, 2, f"- {item}")
        prompt = "Press any key to return"
        inv_win.addstr(height - 2, (width - len(prompt)) // 2, prompt)
        inv_win.refresh()
        inv_win.getch()
        inv_win.clear()
        inv_win.refresh()
        stats_display()
        refresh_game()

    def notif(msg, color=0):
        notif_win.clear()
        if color != 0:
            notif_win.addstr(0, width - len(msg) - 2, msg, curses.color_pair(color))
        else:
            notif_win.addstr(0, width - len(msg) - 2, msg)
        notif_win.refresh()
        time.sleep(2)
        notif_win.clear()
        notif_win.refresh()

    def apply_state(changes):
        global gold
        stat_changes = changes.get('stats', {})
        for s, c in stat_changes.items():
            if s in stats:
                try:
                    stats[s] += float(c)
                except ValueError:
                    pass
        inv_changes = changes.get('inventory', {})
        if inv_changes:
            if isinstance(inv_changes, dict):
                for item in inv_changes.get('add', []):
                    if item not in inv:
                        inv.append(item)
                        notif(f"+ {item}", 1)
                for item in inv_changes.get('remove', []):
                    if item in inv:
                        inv.remove(item)
                        notif(f"- {item}", 2)
        gold_change = changes.get('gold', 0)
        if isinstance(gold_change, (int, float)):
            gold += int(gold_change)
        stats_display()

    def parse_state(resp):
        pattern = r'<state>(.*?)</state>'
        match = re.search(pattern, resp, re.DOTALL)
        if match:
            state_json = match.group(1)
            try:
                changes = json.loads(state_json)
                apply_state(changes)
            except json.JSONDecodeError:
                pass
            resp = re.sub(pattern, '', resp, flags=re.DOTALL).strip()
        return resp

    def handle_dice(narrative):
        while True:
            pattern = r'<dice_roll type="(\d+)d(\d+)">(.*?)</dice_roll>'
            match = re.search(pattern, narrative, re.DOTALL)
            if match:
                num, sides, reason = int(match.group(1)), int(match.group(2)), match.group(3).strip()
                rolls = [random.randint(1, sides) for _ in range(num)]
                total = sum(rolls)
                notif(f"{reason}: {rolls} Total: {total}")
                dice_result = f"<dice_result>{total}</dice_result>"
                msgs.append({'role': 'user', 'content': dice_result})
                narrative = get_resp()
                msgs.pop()
            else:
                break
        return narrative

    def refresh_game():
        game_win.clear()
        start = max(0, scroll_pos)
        end = start + game_h - 2
        displayed = game_content[start:end]
        y = 1
        for line in displayed:
            try:
                game_win.addstr(y, 1, line)
            except curses.error:
                pass
            y += 1
        game_win.box()
        game_win.refresh()

    def show_text(text):
        lines = textwrap.wrap(text, width=width - 2)
        for line in lines:
            game_content.append(line)
            adjust_scroll()
            refresh_game()
            time.sleep(0.02)

    def adjust_scroll():
        nonlocal scroll_pos
        total = len(game_content)
        scroll_pos = max(0, total - (game_h - 2))

    def loading():
        frames = ["", ".", "..", "...", "..", "."]
        idx = 0
        while generation:
            input_win.clear()
            input_win.border()
            load_txt = f"Generating response{frames[idx]}"
            input_win.addstr(1, 2, load_txt)
            input_win.refresh()
            idx = (idx + 1) % len(frames)
            time.sleep(0.3)

    def send_msg(user_input):
        global generation
        generation = True
        load_thread = threading.Thread(target=loading)
        load_thread.start()
        prompt = f'Player Input: {user_input}'
        msgs.append({'role': 'user', 'content': prompt})
        if user_input.strip():
            game_content.append("")
            game_content.append(f"> {user_input}")
            game_content.append("")
            adjust_scroll()
            refresh_game()
        input_win.clear()
        input_win.border()
        input_win.refresh()
        narrative = get_resp()
        generation = False
        load_thread.join()
        narrative = parse_state(narrative)
        narrative = handle_dice(narrative)
        show_text(narrative)
        msgs.pop()

    def get_resp():
        stream = ollama.chat(model=model, messages=msgs, stream=True)
        response = ""
        for chunk in stream:
            part = chunk['message']['content']
            response += part
        return response

    def initial():
        global generation
        generation = True
        load_thread = threading.Thread(target=loading)
        load_thread.start()
        narrative = get_resp()
        generation = False
        load_thread.join()
        narrative = parse_state(narrative)
        narrative = handle_dice(narrative)
        show_text(narrative)

    def setup():
        stats_display()
        initial()

    def loop():
        nonlocal scroll_pos
        while True:
            stats_display()
            input_win.clear()
            input_win.border()
            input_win.addstr(1, 2, "> ")
            input_win.refresh()
            curses.curs_set(1)
            user_input = ""
            start_x = 4
            while True:
                try:
                    key = input_win.get_wch()
                except curses.error:
                    continue
                if isinstance(key, str):
                    if key == '\n':
                        break
                    elif key in ('\x7f', '\b', '\x08'):
                        if len(user_input) > 0:
                            user_input = user_input[:-1]
                            input_win.addstr(1, start_x + len(user_input), ' ')
                            input_win.move(1, start_x + len(user_input))
                            input_win.refresh()
                    else:
                        user_input += key
                        try:
                            input_win.addstr(1, start_x + len(user_input) - 1, key)
                        except curses.error:
                            pass
                        input_win.refresh()
                elif key == curses.KEY_BACKSPACE:
                    if len(user_input) > 0:
                        user_input = user_input[:-1]
                        input_win.addstr(1, start_x + len(user_input), ' ')
                        input_win.move(1, start_x + len(user_input))
                        input_win.refresh()
                elif key == curses.KEY_UP:
                    up()
                elif key == curses.KEY_DOWN:
                    down()
                elif key == curses.KEY_RESIZE:
                    height, width = stdscr.getmaxyx()
                    stat_win.resize(3, width)
                    game_h = height - 6
                    game_win.resize(game_h, width)
                    input_win.resize(3, width)
                    input_win.mvwin(height - 3, 0)
                    notif_win.mvwin(height - 4, 0)
                    refresh_game()
                    stats_display()
                    input_win.refresh()
                else:
                    pass
            curses.curs_set(0)
            input_win.clear()
            input_win.border()
            input_win.refresh()
            if user_input.lower() in ["exit", "quit"]:
                break
            elif user_input.lower() == 'i':
                inv_display()
            else:
                send_msg(user_input)

    def up():
        if not generation:
            nonlocal scroll_pos
            if scroll_pos > 0:
                scroll_pos -= 1
                refresh_game()

    def down():
        if not generation:
            nonlocal scroll_pos
            if scroll_pos < len(game_content) - (game_h - 2):
                scroll_pos += 1
                refresh_game()

    def run_game():
        setup()
        loop()

    run_game()
    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)