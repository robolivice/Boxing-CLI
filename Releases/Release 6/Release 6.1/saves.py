#Save Stats
import json
import os
import copy
import re
import sys

version = 1
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
folder = os.path.join(base_dir, "saves")

path = ""
corrupt = False

C = ["berserker", "assassin", "juggernaut", "duelist", "reaper"]
D = ["Easy", "Medium", "Hard"]
M = ["jab", "kick", "uppercut", "block", "counter", "feint", "taunt"]

def record():
    return {"played": 0, "won": 0, "lost": 0}

DEFAULT = {
    "version": version,
    "name": "",
    "l_stats": {
        "hits": 0, "misses": 0, "crits": 0, "blocks": 0, "combos": 0,
        "tdmg": 0.0, "dmg_taken": 0.0, "rounds": 0,
        "fights_played": 0, "fights_won": 0, "fights_lost": 0, "draws": 0,
    },
    "matches": record(),
    "streaks": {"current": 0, "best": 0},
    "by_class": {c: record() for c in C},
    "comp_class": {c: record() for c in C},
    "by_diff": {d: record() for d in D},
    "m_count": {m: 0 for m in M},
    "bests": {
        "max_hit": 0.0,
        "max_dmg_mtc": 0.0,
        "quick_ko": None,
        "long_mtc": 0
    },
    "settings": {"l_class": "", "l_diff": ""},
    "career": {"defeated": [], "pos": 0}
}

data = copy.deepcopy(DEFAULT)

def _merge(base, new):
    for k, v in new.items():
        if k not in base:
            continue
        if isinstance(base[k], dict) and isinstance(v, dict):
            _merge(base[k], v)
        else:
            base[k] = v
    return base


def load():
    global corrupt
    corrupt = False
    try:
        with open(path, "r") as save_f:
            loaded = json.load(save_f)
        if isinstance(loaded, dict):
            _merge(data, loaded)
    except FileNotFoundError:
        pass
    except ValueError:
        corrupt = True
        try:
            os.replace(path, path + ".bak")
        except OSError:
            pass
    except OSError:
        pass
    data["version"] = version
    data["name"] = os.path.splitext(os.path.basename(path))[0]
    return data

def save():
    if not path:
        return
    out = dict(data)
    out["summary"] = {
        "win_rate": round(win_rate(), 1),
        "most_used_class": m_u_class(),
        "most_used_move": m_u_move(),
    }
    tmp = path + ".tmp"
    with open(tmp, "w") as save_f:
        json.dump(out, save_f, indent=4, sort_keys = True)
    os.replace(tmp, path)

def name_s(name):
    data["name"] = name.strip()

def bump(table, key, won):
    rec = data[table].setdefault(key, record())
    rec["played"] += 1
    rec["won" if won else "lost"] += 1

def rec_mtc(plr_class, c_class, dif, won, p_stats, c_stats, moves, rnd, draws, won_rnd, max_hit):
    lt = data["l_stats"]
    for k in ("hits", "misses", "crits", "blocks", "combos"):
        lt[k] += p_stats[k]
    lt["tdmg"] += p_stats["tdmg"]
    lt["dmg_taken"] += c_stats["tdmg"]
    lt["rounds"] += rnd
    lt["fights_won"] += p_stats["f_won"]
    lt["fights_lost"] += c_stats["f_won"]
    lt["draws"] += draws
    lt["fights_played"] += p_stats["f_won"] + c_stats["f_won"] + draws

    m = data["matches"]
    m["played"] += 1
    s = data["streaks"]
    if won:
        m["won"] += 1
        s["current"] += 1
        s["best"] = max(s["best"], s["current"])
    else:
        m["lost"] += 1
        s["current"] = 0

    bump("by_class", plr_class, won)
    bump("comp_class", c_class, won)
    bump("by_diff", dif, won)

    for mv, n in moves.items():
        data["m_count"][mv] = data["m_count"].get(mv, 0) + n

    b = data["bests"]
    b["max_hit"] = max(b["max_hit"], max_hit)
    b["max_dmg_mtc"] = max(b["max_dmg_mtc"], p_stats["tdmg"])
    b["long_mtc"] = max(b["long_mtc"], rnd)
    if won_rnd:
        f = min(won_rnd)
        if b["quick_ko"] is None or f < b["quick_ko"]:
            b["quick_ko"] = f

    data["settings"]["l_class"] = plr_class
    data["settings"]["l_diff"] = dif

def m_u_class():
    played = {c: r["played"] for c, r in data["by_class"].items()}
    best = max(played, key=played.get)
    if played[best] > 0:
        return best

def m_u_move():
    counts = data["m_count"]
    best = max(counts, key=counts.get)
    if counts[best] > 0:
        return best

def win_rate():
    m = data["matches"]
    if m["played"]:
        return (m["won"] / m["played"] * 100)
    else:
        return 0.0

def summary():
    m = data["matches"]
    return [
        "Matches: " + str(m["played"]) + "  Won: " + str(m["won"]) + "  Lost: " + str(m["lost"]),
        "Win rate: " + str(round(win_rate(), 1)) + "%",
        "Streak: " + str(data["streaks"]["current"]) + "  Best: " + str(data["streaks"]["best"]),
        "Most used class: " + str(m_u_class() or "-"),
        "Most used move: " + str(m_u_move() or "-"),  
    ]

def clean(name):
    name = name.strip().lower()
    if not re.fullmatch(r"[a-z0-9_-]{1,20}", name):
        return None
    if name in {"con", "prn", "aux", "nul"} or re.fullmatch(r"(com|lpt)[1-9]", name):
        return None
    return name

def save_path(name):
    return os.path.join(folder, name + ".json")

def exists(name):
    return os.path.isfile(save_path(name))

def list_saves():
    if not os.path.isdir(folder):
        return []
    return sorted(f[:-5] for f in os.listdir(folder) if f.endswith(".json"))

def use(name):
    global path
    os.makedirs(folder, exist_ok=True)
    path = save_path(name)
    data.clear()
    data.update(copy.deepcopy(DEFAULT))
    data["name"] = name

def delete(name):
    try:
        os.remove(save_path(name))
    except OSError:
        pass

def migrate():
    old = os.path.join(os.path.dirname(os.path.abspath(__file__)), "player_stats.json")
    if not os.path.isfile(old):
        return
    name = "player"
    try:
        with open(old, "r") as f:
            n = clean(json.load(f).get("name", ""))
        if n:
            name = n
    except (OSError, ValueError, AttributeError):
        pass
    os.makedirs(folder, exist_ok=True)
    if exists(name):
        name += "_old"
    os.replace(old, save_path(name))