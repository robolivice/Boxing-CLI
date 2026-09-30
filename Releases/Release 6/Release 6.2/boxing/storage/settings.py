import json
import os
from .. import paths

path = paths.setting_file

s_opts = [
    {"key": "clear_log", "label": "Clear Previous Round", "default": False, "soon": False},
    {"key": "placeholder_1", "label": "EMPTY", "default": False, "soon": True},
    {"key": "placeholder_2", "label": "EMPTY", "default": False, "soon": True},
    {"key": "placeholder_3", "label": "EMPTY", "default": False, "soon": True},
    {"key": "placeholder_4", "label": "EMPTY", "default": False, "soon": True}
]

values = {}
for o in s_opts:
    values[o["key"]] = o["default"]

def load():
    try:
        with open (path, "r") as f:
            loaded = json.load(f)
    except (OSError, ValueError):
        return
    if isinstance(loaded, dict):
        for k, v in loaded.items():
            if k in values and isinstance(v, bool):
                values[k] = v

def save():
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(values, f, indent=4)
    os.replace(tmp, path)

def get(key):
    return values.get(key, False)

def toggle(key):
    values[key] = not values[key]
    save()