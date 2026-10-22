from ..ui import menu
from .. import ui as UI
from ..storage import settings

def _state(key):
    o = settings.OPT_BY_KEY.get(key)
    t = o["type"]
    if t == settings.TYPE_BOOL:
        return "ON" if settings.get(key) else "OFF"
    if t == settings.TYPE_CYCLE:
        return settings.label_of(key)
    if t == settings.TYPE_INT:
        v = settings.get(key)
        return "Random" if not v else str(v)
    return ""

def _style(o):
    t = o["type"]
    if t == settings.TYPE_BOOL:
        return "ok" if settings.get(o["key"]) else "bad"
    if t == settings.TYPE_CYCLE:
        return "val"
    if t == settings.TYPE_INT:
        return "val"
    return None

def _grp_rows():
    rows = []
    for g in settings.GROUPS:
        rows.append((g["label"], g["key"], [(g["label"], None)]))
    rows.append(("Back", None, [("Back", None)]))
    return rows

def _opt_rows(group):
    rows = []
    for o in group["opts"]:
        if o.get("soon"):
            lbl = o["label"] + "(Soon)"
            rows.append((lbl, None, [(lbl, "dim")]))
        else:
            v = _state(o["key"])
            rows.append((o["label"] + ": " + v, o["key"],
                         [(o["label"] + ": ", None), (v, _style(o))]))
    rows.append(("Back", None, [("Back", None)]))
    return rows

def _labels(rows):
    return [r[0] for r in rows]

def _items(rows):
    return [r[2] for r in rows]

def _int_edit(key):
    o = settings.OPT_BY_KEY.get(key)
    while True:
        raw = input(o["label"] + " (0 = random, blank to cancel): ").strip()
        if raw == "":
            return
        if raw.isdigit():
            settings.set_val(key, int(raw))
            return
        print("Please enter a valid number.")

def _step(group, row, direction):
    rows = _opt_rows(group)
    if not (0 <= row < len(rows)):
        return False
    key = rows[row][1]
    if key is None:
        return False
    o = settings.OPT_BY_KEY.get(key)
    if o["type"] != settings.TYPE_CYCLE:
        return False
    settings.cycle(key, direction)
    return True

def _run_grp(group):
    idx = 0
    while True:
        arrow = []
        def on_step(row, direction, g=group, a=arrow):
            if _step(g, row, direction):
                a.append(True)
        pick = menu.menu(None, group["label"], start=idx,
                         items_fn=lambda g=group: _items(_opt_rows(g)),
                         on_step=on_step)
        rows = _opt_rows(group)
        labels = _labels(rows)
        if pick not in labels:
            continue
        idx = labels.index(pick)
        key = rows[idx][1]
        if key is None:
            return
        o = settings.OPT_BY_KEY.get(key)
        if o["type"] == settings.TYPE_BOOL:
            settings.toggle(key)
            if key == "colors":
                UI.set_colors(settings.get("colors"))
        elif o["type"] == settings.TYPE_CYCLE:
            if not arrow:
                settings.cycle(key, 1)
        elif o["type"] == settings.TYPE_INT:
            _int_edit(key)

def run():
    idx = 0
    while True:
        pick = menu.menu(None, "Settings", start=idx,
                         items_fn=lambda: _items(_grp_rows()))
        rows = _grp_rows()
        labels = _labels(rows)
        if pick not in labels:
            continue
        idx = labels.index(pick)
        key = rows[idx][1]
        if key is None:
            return False
        _run_grp(settings.GROUP_BY_KEY[key])
