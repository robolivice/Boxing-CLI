import time
from ..core import data
from .colors import color, c_color

def num(x):
    x = round(x, 2)
    if x == int(x):
        return str(int(x))
    return str(x)

def row(name, dmg, acc, stm, mid):
    return name.ljust(12) + dmg.rjust(8) + acc.rjust(18) + stm.rjust(16) + mid.rjust(15)

def p_move(p_M, p_S, feint_rd = False, taunt_rd = False, counter_a=False):
    lines_printed = 0
    while True:
        m = ["jab", "kick", "uppercut", "block"]
        print("\033[92mMove           Damage            Accuracy         Stamina          ID\033[0m")
        print("\033[94m" + row("Jab", num(p_M["jab"][0]) + "HP", num(p_M["jab"][1]) + "%", num(p_S["jab"]), "1" ))
        print(row("Kick", num(p_M["kick"][0]) + "HP", num(p_M["kick"][1]) + "%", num(p_S["kick"]), "2"))
        print(row("Uppercut", num(p_M["uppercut"][0]) + "HP", num(p_M["uppercut"][1]) + "%", num(p_S["uppercut"]), "3"))
        print("Block".ljust(12) + "Move Dependent".rjust(14) + "Move Dependent".rjust(19) + num(p_S["block"]).rjust(9) + "4".rjust(15) + "\033[0m")
        if feint_rd:
            m.append("feint")
            print("\033[94m" + row("Feint", "0HP", "100%", num(p_S["feint"]), str(len(m))) + "\033[0m")
        if taunt_rd:
            m.append("taunt")
            print("\033[94m" + row("Taunt", "0HP", "100%", num(p_S["taunt"]), str(len(m))) + "\033[0m")
        if counter_a:
            m.append("counter")
            print("\033[91m\033[1m" + row("Counter", num(p_M["counter"][0]) + "HP", num(p_M["counter"][1]) + "%", num(p_S["counter"]), str(len(m))) + "\033[0m")
        print()

        lines_printed = 6
        if feint_rd:
            lines_printed += 1
        if taunt_rd:
            lines_printed += 1
        if counter_a:
            lines_printed += 1
        max_id = len(m)

        try:
            c = int(input("Enter the move ID: ")) - 1
            lines_printed += 1
            
            if 0 <= c < max_id:
                for _ in range(lines_printed):
                    print("\033[A\r\033[K", end="")
                return m[c]
                
        except ValueError:
            lines_printed += 1
            
        for _ in range(lines_printed):
            print("\033[A\r\033[K", end="")
            
        print("Please select correct ID")
        time.sleep(1.2)
        print("\033[A\r\033[K", end="")

def class_menu():
    for key, amp in data.classes.items():
        label = (key.capitalize() + ":").ljust(11)
        print(color["bold"] + color[c_color[key]] + label + color["reset"],
              color["red"] + f"Damage: x{amp['dmg']:.2f}" + color["reset"],
              color["blue"] + f"Accuracy: x{amp['acc']:.2f}" + color["reset"],
              color["yellow"] + f"Stamina Usage: x{amp['stm']:.2f}" + color["reset"],
              color["green"] + f"HP: x{amp['hp']:.2f}" + color["reset"],
              color["purple"] + f"Critical: x{amp['crit']:.2f}" + color["reset"])