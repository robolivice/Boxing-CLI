#test
try:
    import curses
except ImportError:
    curses = None

from .screen import banner
from .colors import s_name
from ..storage import settings

C_TITLE = 1
C_HL = 2
C_WARN = 3
C_OK = 4
C_BAD = 5
C_VAL = 6

STYLES = {
    "ok": C_OK,
    "bad": C_BAD,
    "val": C_VAL,
}

def _plain(item):
    if isinstance(item, str):
        return item
    return "".join(t for t, _ in item)

def _segs(item):
    if isinstance(item, str):
        return [(item, None)]
    return item

def _ansi(item):
    segs = _segs(item)
    if len(segs) == 1 and segs[0][1] is None:
        return segs[0][0]
    return "".join(s_name(style, text) for text, style in segs)

def _init_pairs():
    try:
        curses.start_color()
    except curses.error:
        return False
    if not curses.has_colors():
        return False
    curses.init_pair(C_TITLE, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(C_HL, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(C_WARN, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(C_OK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(C_BAD, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(C_VAL, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    return True

def _attr(style, hl, col):
    if not col:
        if hl:
            return curses.A_REVERSE
        if style == "dim":
            return curses.A_DIM
        return curses.A_NORMAL
    if style is None:
        if hl:
            return curses.color_pair(C_HL) | curses.A_BOLD
        return curses.A_NORMAL
    if style == "dim":
        return curses.A_DIM
    if style in STYLES:
        a = curses.color_pair(STYLES[style])
        if hl:
            a |= curses.A_BOLD
        return a
    return curses.A_NORMAL

def _put(cr, y, x, text, attr):
    if text == "":
        return
    try:
        cr.addstr(y, x, text, attr)
    except curses.error:
        pass

def d_menu(cr, items=None, title=None, start=0, items_fn=None, on_step=None):
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    col = False
    if settings.get("colors"):
        col = _init_pairs()

    if items is None and items_fn is None:
        items = ['New Game', 'Settings', 'Load Save','Delete Save', 'Exit']

    current_row = 0
    first = True

    while True:
        if items_fn is not None:
            items = items_fn()
        if not items:
            items = ['New Game', 'Settings', 'Load Save','Delete Save', 'Exit']

        skip = set()
        for i, it in enumerate(items):
            if _plain(it).endswith("(Soon)"):
                skip.add(i)
        if not (0 <= current_row < len(items)) or current_row in skip:
            current_row = 0
            while current_row in skip and current_row < len(items):
                current_row += 1
        if first:
            if 0 <= start < len(items) and start not in skip:
                current_row = start
            first = False

        cr.clear()

        _put(cr, 1, 2, title or banner(), _attr(None, False, col) | curses.A_BOLD | (curses.color_pair(C_TITLE) if col else 0))
        _put(cr, 2, 2, "Use Up/Down arrows to navigate, Enter to select.", _attr(None, False, col))

        h, _ = cr.getmaxyx()
        vis = max(1, h - 5)
        top = max(0, current_row - vis + 1)
        for idx in range(top, min(top + vis, len(items))):
            y = idx - top + 4
            hl = (idx == current_row)
            x = 4
            _put(cr, y, x, "> " if hl else "  ", _attr(None, hl, col))
            x += 2
            for text, style in _segs(items[idx]):
                _put(cr, y, x, text, _attr(style, hl, col))
                x += len(text)

        cr.refresh()

        key = cr.getch()
        if key == curses.KEY_UP:
            r = current_row - 1
            while r in skip:
                r -= 1
            if r >= 0:
                current_row = r
        elif key == curses.KEY_DOWN:
            r = current_row + 1
            while r in skip:
                r += 1
            if r < len(items):
                current_row = r
        elif key in (curses.KEY_LEFT, curses.KEY_RIGHT):
            if on_step is not None:
                on_step(current_row, -1 if key == curses.KEY_LEFT else 1)
        elif key in [curses.KEY_ENTER, 10, 13]:
            return _plain(items[current_row])

def menu(items=None, title=None, start =0, items_fn=None, on_step=None):
    if curses is not None:
        try:
            return curses.wrapper(d_menu, items, title, start, items_fn, on_step)
        except Exception:
            pass
    opts = items
    if opts is None and items_fn is None:
        opts = ["New Game", "Settings" ,"Load Save", "Delete Save", "Exit"]
    while True:
        if items_fn is not None:
            opts = items_fn()
        for i, it in enumerate(opts, 1):
            print(i, _ansi(it))
        s = input("> ")
        if s.isdigit() and 1 <= int(s) <= len(opts) and not _plain(opts[int(s) - 1]).endswith("(Soon)"):
            return _plain(opts[int(s) - 1])
