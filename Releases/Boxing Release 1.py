import random
import time

# Move data: damage, accuracy, stamina req
M = {"jab": (5, 100),"kick": (15, 65),"uppercut": (25, 40)}
# Block rates: success chance and mitigation percentage
B = {"jab": (90, 60.0),"kick": (75, 33.3),"uppercut": (50, 30.0)}
# Stamina Values
S = {"jab": (0), "kick": (10), "uppercut": (20), "block": (15)}
# Manual validation
def calc_dmg(m):
    # fallback to 0,0
    dmg, acc = M.get(m, (0, 0))
    if random.uniform(0, 100) < acc:
        return dmg
    else:
        return 0

def block(r_dmg, a_move):
    chance, red = B.get(a_move, (0, 0))
    if random.uniform(0, 100) < chance:
        return r_dmg * (1 - red / 100.0)
    return r_dmg

def stamina(s):
    stm = S.get(s)
    return stm

def p_move():
    while True:
        m = ["jab", "kick", "uppercut", "block"]
        print("Move            Damage           Accuracy         Stamina          ID")
        print("Jab              5HP              100%               0              1")
        print("Kick            15HP               65%              10              2")
        print("Uppercut        25HP               40%              20              3")
        print("Block        Block % damage        90%              15              4")

        try:
            c = int(input("Enter the move ID: ")) - 1
            if 0 <= c < len(m):
                return m[c]
        except ValueError:
            pass
        print("Please select correct ID")
#Main turn
def r_turn(atk_n, def_n, atk_move, def_move, def_hp, atk_stm, def_stm):
    stmc = stamina(atk_move)
    if atk_stm < stmc:
        print("Not enough Stamina: Move Failed")
        return def_hp, atk_stm, def_stm

    atk_stm -= stmc
    print(atk_n, "uses", atk_move.upper(), "Defender chose:", def_move.upper())

    if atk_move == "block":
        print(atk_n, "Puts up Guard")
        return def_hp,atk_stm,def_stm
    r_dmg = calc_dmg(atk_move)
    if r_dmg == 0:
        print("The attack missed!")
        return def_hp, atk_stm, def_stm

    if def_move == "block" and def_stm >= stamina("block"):
        f_dmg = block(r_dmg,atk_move)
        def_stm -= stamina("block")
        if f_dmg < r_dmg:
            print("Blocked. Reduced the damage")
    else:
        if def_move == "block":
            print("Tried to block but no stamina")
        f_dmg = r_dmg

    print(def_n, "takes", round(f_dmg, 1),"Damage!")
    return max(0.0, def_hp - f_dmg),atk_stm,def_stm

while True:
    #Main game
    plr_hp, comp_hp, plr_stm, comp_stm = 100.0, 100.0, 100.0, 100.0
    c = 0
    while plr_hp > 0 and comp_hp > 0:
        print("\n--- Selecting Player Turn -------- ")
        time.sleep(1.0)
        
        first = random.choice(["plr", "comp"])
        p_m = p_move()
        c_move = random.choice(["jab", "kick", "uppercut", "block"])
        
        if first == "plr":
            comp_hp,plr_stm,comp_stm = r_turn("Player", "Computer", p_m, c_move, comp_hp, plr_stm, comp_stm)
        else:
            plr_hp,comp_stm, plr_stm = r_turn("Computer", "Player", c_move, p_m, plr_hp,comp_stm, plr_stm)

        c += 1
        if c == 3:
            plr_stm = min(100.0, plr_stm + 10.0)
            comp_stm = min(100.0, comp_stm + 10.0)
            c = 0

        print("Remaining HP -> Player:", round(plr_hp,1), "| Computer:", round(comp_hp,1))
        print("Remaining Stamina -> Player:", round(plr_stm,1), "| Computer:", round(comp_stm,1))

    #end
    if plr_hp <= 0 and comp_hp <= 0:
        print("It's a Draw game!")
        flag = True
    elif plr_hp <= 0:
        print("K.O.! The Computer wins.")
        flag = True
    else:
        print("K.O.! You win!")
        flag = True
    #Playing Again
    if flag == True:
        x = input("Do you wanna play again? (y/n): ").lower()
        if x == "y":
            continue
        else:
            print("Thanks for playing!")
            break