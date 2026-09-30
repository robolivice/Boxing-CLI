#Setup and Promts
import time
from .. import ui as UI

def debug_m():
    x = input("Enable Debug Mode? (y/n): ").lower()
    if x == "y":
        return x

def debug_opts():
    opts = {}
    opts["force_player"] = input(" Force Player move manually? (y/n): ").lower() == "y"
    opts["force_ai"] = input(" Force AI move manually? (y/n): ").lower() == "y"
    opts["show_state"] = input(" Show internal state each round? (y/n): ").lower() == "y"
    opts["god_stamina"] = input(" Disable stamina cost? (y/n): ").lower() == "y"
    opts["ai_class"] = input(" Force AI Class? (y/n): ").lower() == "y"
    seed_in = input(" RNG seed (blank for none): ")
    opts["seed"] = int(seed_in) if seed_in.strip().isdigit() else None
    return opts

def class_s():
    k_map = {"b": "berserker", "a": "assassin", "j": "juggernaut", "d": "duelist", "r": "reaper"}
    while True:
        print("Enter Class Selection")
        UI.class_menu()
        input_print = UI.color.get("bold")+UI.color.get("yellow")+"B"+UI.color.get("reset")+ "/"+UI.color.get("bold")+UI.color.get("purple")+"A"+UI.color.get("reset")+ "/"+UI.color.get("bold")+UI.color.get("red")+"J"+UI.color.get("reset")+"/"+UI.color.get("bold")+UI.color.get("blue")+"D"+UI.color.get("reset")+"/"+UI.color.get("bold")+UI.color.get("black")+"R"+UI.color.get("reset")+"/"+UI.color.get("bold")+UI.color.get("cyan")+"Q"+UI.color.get("reset")+"(menu)"+": "
        _class = input(input_print).lower().strip()
        if _class == "q":
            return None
        if _class in k_map:
            return k_map[_class]
        print("Please select a Valid Class")
        time.sleep(1.2)
        l_p = 8
        for i in range(l_p):
            print("\033[A\r\033[K", end="")
            
def difficulty():
    while True:
        dif = input("Enter Difficulty Level: \033[1m\033[32mEasy (E)\033[0m | \033[1m\033[33mMedium (M)\033[0m | \033[1m\033[31mHard (H)\033[0m: ").lower().strip()
        if dif in ("e", "easy"):
            return "Easy", "\033[1m\033[32mEasy\033[0m"
        if dif in ("m", "medium"):
            return "Medium", "\033[1m\033[33mMedium\033[0m"
        if dif in ("h", "hard"):
            return "Hard", "\033[1m\033[31mHard\033[0m"
        print("Please select Correct Difficulty")
        time.sleep(1.2)
        for i in range(2):
            print("\033[A\r\033[K", end="")