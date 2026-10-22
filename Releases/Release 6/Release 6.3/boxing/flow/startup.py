#Setup and Promts
from .. import ui as UI
from ..storage import settings

def class_s(last=None):
    k_map = {"b": "berserker", "a": "assassin", "j": "juggernaut", "d": "duelist", "r": "reaper"}
    while True:
        print("Enter Class Selection")
        UI.class_menu()
        hint = ""
        if last:
            hint = " (last: " + last.capitalize() + ")"
        input_print = UI.color.get("bold")+UI.color.get("yellow")+"B"+UI.color.get("reset")+ "/"+UI.color.get("bold")+UI.color.get("purple")+"A"+UI.color.get("reset")+ "/"+UI.color.get("bold")+UI.color.get("red")+"J"+UI.color.get("reset")+"/"+UI.color.get("bold")+UI.color.get("blue")+"D"+UI.color.get("reset")+"/"+UI.color.get("bold")+UI.color.get("black")+"R"+UI.color.get("reset")+"/"+UI.color.get("bold")+UI.color.get("cyan")+"Q"+UI.color.get("reset")+"(menu)"+hint+": "
        _class = input(input_print).lower().strip()
        if _class == "" and last:
            return last
        if _class == "q":
            return None
        if _class in k_map:
            return k_map[_class]
        print("Please select a Valid Class")
        settings.pause_note(1.2)
        l_p = 8
        for i in range(l_p):
            print("\033[A\r\033[K", end="")
            
def difficulty(last=None):
    c = UI.color
    hint = ""
    if last:
        hint = " (Enter for " + last + ")"
    while True:
        dif = input("Enter Difficulty Level: " + c["bold"] + c["green"] + "Easy (E)" + c["reset"] + " | " + c["bold"] + c["yellow"] + "Medium (M)" + c["reset"] + " | " + c["bold"] + c["red"] + "Hard (H)" + c["reset"] + hint + ": ").lower().strip()
        if dif == "" and last:
            return last, _mode_c(last)
        if dif in ("e", "easy"):
            return "Easy", _mode_c("Easy")
        if dif in ("m", "medium"):
            return "Medium", _mode_c("Medium")
        if dif in ("h", "hard"):
            return "Hard", _mode_c("Hard")
        print("Please select Correct Difficulty")
        settings.pause_note(1.2)
        for i in range(2):
            print("\033[A\r\033[K", end="")

def _mode_c(dif):
    c = UI.color
    if dif == "Easy":
        return c["bold"] + c["green"] + "Easy" + c["reset"]
    if dif == "Medium":
        return c["bold"] + c["yellow"] + "Medium" + c["reset"]
    return c["bold"] + c["red"] + "Hard" + c["reset"]
