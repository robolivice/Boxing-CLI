#Boxing.py Test build
import random
import time

# Move data: damage, accuracy, crit chance
M = {"jab": (5, 100, 10),"kick": (15, 65, 5),"uppercut": (25, 40, 3)}
# Block rates: success chance and mitigation percentage
B = {"jab": (90, 60.0),"kick": (75, 33.3),"uppercut": (50, 30.0)}
# Stamina Values
S = {"jab": 0, "kick": 10, "uppercut": 20, "block": 15}
# Manual validation
def calc_acc(m):
    # fallback to 0,0,0
    dmg, acc, _ = M.get(m, (0, 0, 0))
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

def dmg(s,p):
    dmg = calc_acc(s)
    if dmg == 0:
        return 0
    __, _, crit_c = M.get(s, (0,0,0))
    if random.uniform(0,100) < crit_c:
        print(p,"has landed a Critical Hit!")
        return dmg*1.5
    return dmg

def p_move():
    while True:
        m = ["jab", "kick", "uppercut", "block"]
        print("Move            Damage           Accuracy         Stamina          ID")
        print("Jab              5HP              100%               0              1")
        print("Kick            15HP               65%              10              2")
        print("Uppercut        25HP               40%              20              3")
        print("Block       Move Dependent     Move Dependent       15              4")

        try:
            c = int(input("Enter the move ID: ")) - 1
            if 0 <= c < len(m):
                return m[c]
        except ValueError:
            pass
        print("Please select correct ID")
#Main turn
def r_turn(atk1_n, atk2_n, atk1_move, atk2_move, atk2_hp, atk1_stm, atk2_stm,p,flag1):
    stmc = stamina(atk1_move)

    if atk1_stm < stmc:
        print("Not enough Stamina: Move Failed")
        return atk2_hp, atk1_stm, atk2_stm

    atk1_stm -= stmc
    if flag1 == True:
        print(atk1_n, "uses", atk1_move.upper(), atk2_n, "chose:", atk2_move.upper())

    if atk1_move == "block":
        time.sleep(1.0)
        print(atk1_n, "Puts up Guard")
        return atk2_hp,atk1_stm,atk2_stm
    r_dmg = dmg(atk1_move,p)
    if r_dmg == 0:
        time.sleep(1.0)
        print(atk1_n+"'s","attack missed!")
        return atk2_hp, atk1_stm, atk2_stm

    if atk2_move == "block" and atk2_stm >= stamina("block"):
        f_dmg = block(r_dmg,atk1_move)
        if f_dmg < r_dmg:
            print("Blocked. Reduced the damage")
    else:
        if atk2_move == "block":
            print("Tried to block but no stamina")
        f_dmg = r_dmg

    print(atk2_n, "takes", round(f_dmg, 1),"Damage!")
    return max(0.0, atk2_hp - f_dmg),atk1_stm,atk2_stm

while True:
    #Main game
    plr_hp, comp_hp, plr_stm, comp_stm = 100.0, 100.0, 100.0, 100.0
    c = 0
    rnd = 1
    while plr_hp > 0 and comp_hp > 0:
        print("\n-------- Round",rnd,"-------- ")
        time.sleep(0.5)

        p_m = p_move()
        c_move = random.choice(["jab", "kick", "uppercut", "block"])

        comp_hp, plr_stm, comp_stm = r_turn("Player", "Computer", p_m, c_move, comp_hp, plr_stm, comp_stm, "Player",True)
        plr_hp, comp_stm, plr_stm = r_turn("Computer", "Player", c_move, p_m, plr_hp, comp_stm, plr_stm, "Computer",False)

        c += 1
        if c == 3:
            plr_stm = min(100.0, plr_stm + 10.0)
            comp_stm = min(100.0, comp_stm + 10.0)
            c = 0

        print("Remaining HP -> Player:", round(plr_hp,1), "| Computer:", round(comp_hp,1))
        print("Remaining Stamina -> Player:", round(plr_stm,1), "| Computer:", round(comp_stm,1))

        rnd+=1
        time.sleep(2.5)

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
