import os, sys

from . import ui as UI
from .ui import menu
from .ui.loadingsc import loadsc
from .storage import saves, settings
from .flow import session, match, options

if os.name == "nt":
    os.system("")

def _bye():
    return UI.color["bold"] + UI.color["blue"] + "Thanks For Playing!!" + UI.color["reset"]

def _quit(exc_type, exc, tb):
    if exc_type is KeyboardInterrupt:
        print("\n" + _bye())
    else:
        sys.__excepthook__(exc_type, exc, tb)
sys.excepthook = _quit

ACTIONS = {
    "New Game": session.new_game,
    "Settings": options.run,
    "Load Save": session.load_game,
    "Delete Save": session.delete_game,
}

def main():
    settings.load()
    UI.set_colors(settings.get("colors"))
    try:
        if settings.get("show_loading"):
            loadsc()
    except Exception:
        pass
    saves.migrate()
    while True:
        choice = menu.menu()
        if choice == "Exit":
            print(_bye())
            sys.exit()
        action = ACTIONS.get(choice)
        if action is None or not action():
            continue
        for line in saves.summary():
            print(line)
            settings.pause(0.3)
        match.p_session()
