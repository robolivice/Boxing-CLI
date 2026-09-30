import time
from ..storage import saves
from ..ui import menu
from .. import ui as UI

def _flash(msg, secs=1.2, l = 2):
    print(msg)
    time.sleep(secs)
    UI.erase_l(l)

def _new_save_name():
    while True:
        raw = input("Save name (a-z, 0-9, _ or -, max 20; blank to cancel): ")
        if raw.strip() == "":
            return None
        name = saves.clean(raw)
        if name is None:
            _flash("Invalid name.", 0.8)
            continue
        if saves.exists(name):
            if input("That save exists. Overwrite? (y/n): ").lower() != "y":
                return None
            saves.delete(name)
        return name

def new_game():
    name = _new_save_name()
    if name is None:
        return False
    saves.use(name)
    saves.save()
    return True

def load_game():
    names = saves.list_saves()
    if not names:
        _flash("No saves found. Start a New Game first.", l=1)
        return False
    pick = menu.menu(names + ["Back"], "Select Save")
    if pick == "Back":
        return False
    saves.use(pick)
    saves.load()
    if saves.corrupt:
        print("Save was corrupted, backed up as .bak. Starting fresh.")
        time.sleep(1.5)
    return True

def delete_game():
    names = saves.list_saves()
    if not names:
        _flash("No saves found. Start a New Game first.",l=1)
        return False
    pick = menu.menu(names + ["Back"], "Delete Save")
    if pick == "Back":
        return False
    if input("Delete '" + pick + "' permanently? (y/n): ").lower() != "y":
        return False
    saves.delete(pick)
    print("Save", UI.color["bold"] + UI.color["red"] + "Deleted" + UI.color["reset"], "Successfully")
    time.sleep(1.2)
    UI.erase_l(2)
    if saves.path == saves.save_path(pick):
        saves.path = ""
    return False