#test
try:
    import curses
except ImportError:
    curses = None

import UI

def d_menu(cr, items=None, title=None):
    curses.curs_set(0)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) 
    
    current_row = 0
    if items is None:
        items = ['New Game', 'Options (Next Update)', 'Load Save','Delete Save', 'Exit']
    skip = {i for i, it in enumerate(items) if it.startswith("Options")}

    while True:
        cr.clear()

        cr.addstr(1, 2,title or UI.menu() ,curses.color_pair(1) | curses.A_BOLD)
        cr.addstr(2, 2, "Use Up/Down arrows to navigate, Enter to select.")

        h, _ = cr.getmaxyx()
        vis = max(1, h - 5)
        top = max(0, current_row - vis + 1)
        for idx in range(top, min(top + vis, len(items))):
            y = idx - top + 4
            if idx == current_row:
                cr.addstr(y, 4, f"> {items[idx]}", curses.color_pair(2))
            else:
                cr.addstr(y, 4, f"  {items[idx]}")

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
        elif key in [curses.KEY_ENTER, 10, 13]:
            return items[current_row]

def menu(items=None, title=None):
    if curses is not None:
        try:
            return curses.wrapper(d_menu, items, title)
        except curses.error:
            pass
    opts = items or ["New Game", "Load Save", "Delete Save", "Exit"]
    for i, it in enumerate(opts, 1):
        print(i, it)
    while True:
        s = input("> ")
        if s.isdigit() and 1 <= int(s) <= len(opts):
            return opts[int(s) - 1]