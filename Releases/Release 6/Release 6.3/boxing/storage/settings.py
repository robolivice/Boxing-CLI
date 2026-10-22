import json
import os
import time
from .. import paths

path = paths.setting_file

TYPE_BOOL = "bool"
TYPE_CYCLE = "cycle"
TYPE_INT = "int"

GROUPS = [
    {
        "key": "general",
        "label": "General",
        "opts": [
            {"key": "clear_log", "label": "Clear Previous Round", "default": False, "type": TYPE_BOOL},
            {"key": "show_loading", "label": "Loading Screen", "default": True, "type": TYPE_BOOL},
            {"key": "colors", "label": "Colors", "default": True, "type": TYPE_BOOL},
            {"key": "ascii_bars", "label": "ASCII Bars", "default": False, "type": TYPE_BOOL},
            {"key": "combat_log", "label": "Detailed Combat Log", "default": True, "type": TYPE_BOOL},
            {"key": "sound", "label": "Sound", "default": False, "type": TYPE_BOOL, "soon": True},
            {"key": "text_speed", "label": "Text Speed", "default": 1.0, "type": TYPE_CYCLE,
             "choices": [(0.0, "Instant"), (0.5, "Fast"), (1.0, "Normal"), (1.5, "Slow")]},
        ],
    },
    {
        "key": "match_rules",
        "label": "Match Rules",
        "opts": [
            {"key": "match_length", "label": "Match Length", "default": 3, "type": TYPE_CYCLE,
             "choices": [(1, "Best of 1"), (3, "Best of 3"), (5, "Best of 5"), (7, "Best of 7")]},
            {"key": "round_limit", "label": "Round Limit", "default": 0, "type": TYPE_CYCLE,
             "choices": [(0, "No Limit"), (10, "10 Rounds"), (15, "15 Rounds"), (20, "20 Rounds")]},
            {"key": "remember_class", "label": "Remember Last Class", "default": True, "type": TYPE_BOOL},
            {"key": "remember_diff", "label": "Remember Last Difficulty", "default": True, "type": TYPE_BOOL},
            {"key": "career_mode", "label": "Career Mode", "default": False, "type": TYPE_BOOL, "soon": True},
        ],
    },
    {
        "key": "saves",
        "label": "Saves",
        "opts": [
            {"key": "confirm_overwrite", "label": "Confirm Overwrite", "default": True, "type": TYPE_BOOL},
            {"key": "record_debug", "label": "Record Debug Matches", "default": False, "type": TYPE_BOOL},
        ],
    },
    {
        "key": "debug",
        "label": "Debug",
        "opts": [
            {"key": "debug_mode", "label": "Debug Mode", "default": False, "type": TYPE_BOOL},
            {"key": "dbg_force_player", "label": "Force Player Move", "default": False, "type": TYPE_BOOL},
            {"key": "dbg_force_ai", "label": "Force AI Move", "default": False, "type": TYPE_BOOL},
            {"key": "dbg_show_state", "label": "Show Internal State", "default": False, "type": TYPE_BOOL},
            {"key": "dbg_god_stamina", "label": "Disable Stamina Cost", "default": False, "type": TYPE_BOOL},
            {"key": "dbg_ai_class", "label": "Force AI Class", "default": "random", "type": TYPE_CYCLE,
             "choices": [("random", "Random"), ("berserker", "Berserker"), ("assassin", "Assassin"),
                         ("juggernaut", "Juggernaut"), ("duelist", "Duelist"), ("reaper", "Reaper")]},
            {"key": "dbg_seed", "label": "RNG Seed", "default": 0, "type": TYPE_INT},
        ],
    },
]

AUTO = {"last_class": "", "last_diff": ""}

def _all_opts():
    out = []
    for g in GROUPS:
        out.extend(g["opts"])
    return out

OPTS = _all_opts()
OPT_BY_KEY = {}
for o in OPTS:
    OPT_BY_KEY[o["key"]] = o

GROUP_BY_KEY = {}
for g in GROUPS:
    GROUP_BY_KEY[g["key"]] = g

values = {}
for o in OPTS:
    values[o["key"]] = o["default"]
for k, v in AUTO.items():
    values[k] = v

def _ok(o, v):
    t = o["type"]
    if t == TYPE_BOOL:
        return isinstance(v, bool)
    if t == TYPE_INT:
        return isinstance(v, int) and not isinstance(v, bool)
    if t == TYPE_CYCLE:
        for c in o["choices"]:
            if v == c[0] and type(v) is type(c[0]):
                return True
        return False
    return False

def load():
    try:
        with open (path, "r") as f:
            loaded = json.load(f)
    except (OSError, ValueError):
        return
    if not isinstance(loaded, dict):
        return
    for k, v in loaded.items():
        if k in OPT_BY_KEY:
            if _ok(OPT_BY_KEY[k], v):
                values[k] = v
        elif k in AUTO:
            if isinstance(v, str):
                values[k] = v

def save():
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(values, f, indent=4)
    os.replace(tmp, path)

def get(key):
    return values.get(key)

def set_val(key, val):
    o = OPT_BY_KEY.get(key)
    if o is not None and not _ok(o, val):
        return
    values[key] = val
    save()

def toggle(key):
    o = OPT_BY_KEY.get(key)
    if o is None or o["type"] != TYPE_BOOL:
        return
    values[key] = not values[key]
    save()

def cycle(key, step=1):
    o = OPT_BY_KEY.get(key)
    if o is None or o["type"] != TYPE_CYCLE:
        return
    choices = o["choices"]
    vals = [c[0] for c in choices]
    cur = values.get(key)
    i = 0
    for n, v in enumerate(vals):
        if v == cur and type(v) is type(cur):
            i = n
            break
    i = (i + step) % len(vals)
    values[key] = vals[i]
    save()

def label_of(key):
    o = OPT_BY_KEY.get(key)
    if o is None:
        return ""
    if o["type"] == TYPE_CYCLE:
        for v, lab in o["choices"]:
            if v == values.get(key):
                return lab
    return str(values.get(key))

def set_auto(key, val):
    if key in AUTO:
        values[key] = val
        save()

def pause(secs):
    d = secs * values.get("text_speed", 1.0)
    if d > 0:
        time.sleep(d)

def pause_note(secs):
    d = max(secs * values.get("text_speed", 1.0), 0.8)
    time.sleep(d)

def debug_opts():
    return {
        "force_player": get("dbg_force_player"),
        "force_ai": get("dbg_force_ai"),
        "show_state": get("dbg_show_state"),
        "god_stamina": get("dbg_god_stamina"),
        "ai_class": get("dbg_ai_class"),
        "seed": get("dbg_seed"),
    }
