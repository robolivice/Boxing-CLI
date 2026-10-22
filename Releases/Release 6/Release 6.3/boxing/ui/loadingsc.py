import math
import threading
import time
try:
    import curses
except ImportError:
    curses = None
from .. import paths
from .screen import version


DENSE_CHARS = set("#%@")

REGIONS = {
    "skin": (216, 3),
    "glove": (196, 1),
    "shorts": (39, 6),
}
REGION_ORDER = list(REGIONS)


def pair_id(region, dense):
    return 10 + REGION_ORDER.index(region) * 2 + (1 if dense else 0)


GLOVE_PAIRS = {pair_id("glove", False), pair_id("glove", True)}


def pick_pair(char, row, total_rows, is_glove):
    if is_glove:
        region = "glove"
    elif row >= total_rows * 0.75:
        region = "shorts"
    else:
        region = "skin"
    return pair_id(region, char in DENSE_CHARS)

def hand_boxes(art):
    h, w = len(art), len(art[0])
    return {
        "L": (int(h * 0.35), int(h * 0.70), 0, int(w * 0.30)),
        "R": (int(h * 0.35), int(h * 0.70), int(w * 0.70), w),
    }


def split_layers(art, boxes):
    body = [list(line) for line in art]
    hands = {}
    for name, (r0, r1, c0, c1) in boxes.items():
        hands[name] = (r0, c0, [art[r][c0:c1] for r in range(r0, r1)])
        for r in range(r0, r1):
            for c in range(c0, c1):
                body[r][c] = " "
    return ["".join(row) for row in body], hands

def load_art(name="boxer.txt"):
    with open(paths.asset(name), encoding="utf-8") as f:
        lines = f.read().split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    w = max(len(l) for l in lines)
    return [l.ljust(w) for l in lines]

def place(layers, dx, dy, lean, hand_off=None, pad_x=14, pad_y=1):
    body, hands = layers
    h, w = len(body), len(body[0])
    cw, chh = w + pad_x * 2, h + pad_y * 2
    chars = [[" "] * cw for _ in range(chh)]
    pairs = [[0] * cw for _ in range(chh)]

    def draw(rows, r_start, c_start, ox, oy, is_glove):
        for i, line in enumerate(rows):
            r = r_start + i
            row_lean = round(lean * (1 - r / (h - 1)))
            y = r + pad_y + dy + oy
            if not 0 <= y < chh:
                continue
            for j, char in enumerate(line):
                if char == " ":
                    continue
                x = c_start + j + pad_x + dx + row_lean + ox
                if 0 <= x < cw:
                    chars[y][x] = char
                    pairs[y][x] = pick_pair(char, r, h, is_glove)

    draw(body, 0, 0, 0, 0, False)
    hand_off = hand_off or {}
    for name, (r0, c0, rows) in hands.items():
        ox, oy = hand_off.get(name, (0, 0))
        draw(rows, r0, c0, ox, oy, True)

    return [list(zip(chars[y], pairs[y])) for y in range(chh)]


def build_animation(art):
    layers = split_layers(art, hand_boxes(art))

    weave = []
    for i in range(16):
        t = i / 16 * 2 * math.pi
        s = math.sin(2 * t + 0.5)
        hand_off = {
            "L": (round(1.5 * s), round(s)),
            "R": (round(-1.5 * s), round(-s)),
        }
        weave.append(
            place(
                layers,
                dx=round(3 * math.sin(t)),
                dy=round(math.sin(2 * t)),
                lean=round(4 * math.sin(t)),
                hand_off=hand_off,
            )
        )

    keys = [
        (0, 0, 0, (0, 0), (0, 0)),
        (-1, 0, -1, (-1, 0), (0, 0)),
        (-2, 1, -2, (-2, 0), (-1, 0)),
        (-2, 1, -3, (-2, 0), (-1, 0)),
        (2, 0, 3, (2, 0), (-1, 0)),
        (4, 0, 5, (4, 0), (-1, 0)),
        (5, 0, 6, (5, 0), (-1, 0)),
        (5, 0, 6, (5, 0), (-1, 0)),
        (4, 0, 4, (3, 0), (-1, 0)),
        (2, 0, 2, (1, 0), (0, 0)),
        (1, 0, 1, (0, 0), (0, 0)),
        (0, 0, 0, (0, 0), (0, 0)),
    ]
    punch = [
        place(layers, dx, dy, lean, {"R": r, "L": l})
        for dx, dy, lean, r, l in keys
    ]

    return weave + punch + weave + punch

class StableAsciiLoader:

    def __init__(self, animation):
        self.animation = animation
        self.progress = 0
        self.status_message = "Preparing system modules..."
        self.is_running = True

    def render_frame(self, stdscr, frame_index):
        height, width = stdscr.getmaxyx()
        center_x = width // 2
        max_safe_y = height - 2
        max_safe_x = width - 1

        frame = self.animation[frame_index]
        art_top = 2
        frame_w = len(frame[0])
        art_left = max(0, center_x - frame_w // 2)

        for y, row in enumerate(frame):
            plot_y = art_top + y
            if plot_y > max_safe_y:
                break
            x = 0
            while x < frame_w:
                if row[x][0] == " ":
                    x += 1
                    continue
                
                start, pair = x, row[x][1]
                while x < frame_w and row[x][0] != " " and row[x][1] == pair:
                    x += 1
                plot_x = art_left + start
                if plot_x >= max_safe_x:
                    break
                run = "".join(c for c, _ in row[start:x])[: max_safe_x - plot_x]
                attr = curses.color_pair(pair)
                if pair in GLOVE_PAIRS:
                    attr |= curses.A_BOLD
                try:
                    stdscr.addstr(plot_y, plot_x, run, attr)
                except curses.error:
                    pass

        art_bottom = art_top + len(frame)
        title_text = "BOXING CLI V"+str(version)
        if width < len(title_text) + 4:
            title_text = "LOADING..."
        title_y = 0
        title_x = max(0, center_x - len(title_text) // 2)
        try:
            stdscr.addstr(title_y, title_x, title_text, curses.color_pair(2) | curses.A_BOLD)
        except curses.error:
            pass

        max_element_width = max(10, width - 6)
        bar_width = min(34, max_element_width)
        filled_width = int((self.progress / 100) * bar_width)

        bar = "█" * filled_width + "░" * (bar_width - filled_width)
        progress_text = f" {self.progress}% Loading... "
        status = f" Status: {self.status_message} "[:max_element_width]

        bar_y = min(max_safe_y, art_bottom + 1)
        text_y = min(max_safe_y, art_bottom + 2)
        status_y = min(max_safe_y, art_bottom + 3)

        bar_x = max(0, center_x - len(bar) // 2)
        text_x = max(0, center_x - len(progress_text) // 2)
        status_x = max(0, center_x - len(status) // 2)

        try:
            if bar_x + len(bar) <= max_safe_x:
                stdscr.addstr(bar_y, bar_x, "█" * filled_width, curses.color_pair(2) | curses.A_BOLD)
                stdscr.addstr(bar_y, bar_x + filled_width, "░" * (bar_width - filled_width), curses.color_pair(2) | curses.A_DIM)
            if text_y != bar_y and text_x + len(progress_text) <= max_safe_x:
                stdscr.addstr(text_y, text_x, progress_text)
            if (
                status_y not in (text_y, bar_y)
                and status_x + len(status) <= max_safe_x
            ):
                stdscr.addstr(status_y, status_x, status, curses.color_pair(2))
        except curses.error:
            pass

    def run_ui(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)

        if curses.has_colors():
          curses.start_color()
          curses.use_default_colors()
          hi = curses.COLORS >= 256
          curses.init_pair(1, curses.COLOR_GREEN, -1)
          curses.init_pair(2, curses.COLOR_CYAN, -1)
          curses.init_pair(3, curses.COLOR_RED, -1)
          for name in REGION_ORDER:
              color = REGIONS[name][0] if hi else REGIONS[name][1]
              curses.init_pair(pair_id(name, False), color, -1)
              curses.init_pair(
                  pair_id(name, True), 16 if hi else curses.COLOR_BLACK, color
              )

        frame_index = 0
        while self.is_running and self.progress <= 100:
            stdscr.erase()
            self.render_frame(stdscr, frame_index)
            stdscr.refresh()

            frame_index = (frame_index + 1) % len(self.animation)
            time.sleep(0.06)

            try:
                if stdscr.getch() == ord("q"):
                    self.is_running = False
                    break
            except Exception:
                pass

        stdscr.clear()
        stdscr.refresh()


def background_workload(loader):
    steps = [
        (25, "Testing Data Structures..."),
        (50, "Injecting application execution frames..."),
        (75, "Compiling native modules and packages..."),
        (100, "Initialization successful! Finishing..."),
    ]

    for target_pct, message in steps:
        loader.status_message = message
        while loader.progress < target_pct:
            if not loader.is_running:
                return
            time.sleep(0.08)
            loader.progress += 1

    time.sleep(0.8)
    loader.is_running = False

def loadsc():
    if curses is None:
        return
    try:
        ani_art = build_animation(load_art("boxer.txt"))
    except OSError:
        return

    loader_system = StableAsciiLoader(ani_art)
    worker_thread = threading.Thread(
        target=background_workload, args=(loader_system,), daemon=True
    )
    worker_thread.start()

    try:
        curses.wrapper(loader_system.run_ui)
    except curses.error:
        pass
    finally:
        loader_system.is_running = False
    worker_thread.join()
