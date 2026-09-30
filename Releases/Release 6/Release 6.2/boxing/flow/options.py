from ..ui import menu
from ..storage import settings

def _items():
    items = []
    for o in settings.s_opts:
        if o["soon"]:
            items.append(o["label"] + "(Soon)")
        else:
            if settings.get(o["key"]):
                state = "ON"
            else:
                state = "OFF"
            items.append(o["label"] + ": " + state)
    return items + ["Back"]

def run():
    idx = 0
    while True:
        items = _items()
        pick = menu.menu(items, "Options", start = idx)
        if pick == "Back":
            return False
        idx = items.index(pick)
        settings.toggle(settings.s_opts[idx]["key"])
        