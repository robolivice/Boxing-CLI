#Main combat Mechanics
import random
import time

# Move data: damage, accuracy, crit chance
M = {"jab": (5, 100, 10),"kick": (15, 65, 5),"uppercut": (25, 40, 3),"counter":(40,85,0)}
# Block rates: success chance and mitigation percentage
B = {"jab": (90, 60.0),"kick": (75, 33.3),"uppercut": (50, 30.0), "counter": (0, 0)}
# Stamina Values
S = {"jab": 0, "kick": 10, "uppercut": 20, "block": 15, "counter": 30}
# Combos: Extra damage then extra accuracy
C = {("jab", "jab", "uppercut"): (15, 20),
     ("jab","kick","uppercut"): (25, 35),
     ("uppercut","block","counter"):(40, 100)
     }

# Manual validation
def calc_acc(m,bonus_acc=0):
    # fallback to 0,0,0
    dmg, acc, _ = M.get(m, (0, 0, 0))
    acc = max(0, min(100, acc + bonus_acc))
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

def combo(his):
    return C.get(tuple(his), (0,0))

def AiCombo(his, n_move):
    if len(his) < 2:
        return (0,0)
    return combo(his[-2:] + [n_move])

def dmg(s,p, stats=None, bonus_dmg = 0, bonus_acc = 0):
    dmg = calc_acc(s, bonus_acc)
    if dmg == 0:
        if stats is not None:
            stats["misses"] += 1
        return 0
    __, _, crit_c = M.get(s, (0,0,0))
    if stats is not None:
        stats["hits"] += 1
    if random.uniform(0,100) < crit_c:
        if stats is not None:
            stats["crits"] += 1
        print(p,"has landed a \033[31mCRITICAL HIT\033[0m!")
        return dmg*1.5 + bonus_dmg
    return dmg + bonus_dmg
#Main turn
def r_turn(atk1_n, atk2_n, atk1_move, atk2_move, atk2_hp, atk1_stm, atk2_stm,p,flag1, atk_stats=None, def_stats=None, atk_c = None, def_c = None, bonus_dmg=0, bonus_acc=0):
    stmc = stamina(atk1_move)

    if atk1_stm < stmc:
        print("Not enough Stamina: Move Failed")
        return atk2_hp, atk1_stm, atk2_stm

    atk1_stm -= stmc
    if flag1 == True:
        print(atk1_n, "uses", "\033[33m"+str(atk1_move.upper())+"\033[0m", atk2_n, "chose:","\033[34m" +str(atk2_move.upper())+"\033[0m")

    if atk1_move == "block":
        time.sleep(1.0)
        print(atk1_n, "Puts up \033[34mGuard\033[0m")
        return atk2_hp,atk1_stm,atk2_stm
    
    if atk1_move == "counter" and atk_c is not None:
        atk_c["rdy"] = False

    d_combo = C[("uppercut", "block", "counter")]
    if (bonus_dmg, bonus_acc) == d_combo:
        print(atk1_n, "unleashes a \033[1m\033[31mDEADLY COMBO!!\033[0m")
        if atk_stats is not None:
            atk_stats["combos"] += 1
    elif bonus_dmg > 0 or bonus_acc > 0:
        print(atk1_n, "unleashes a \033[1m\033[32mCOMBO!\033[0m")
        if atk_stats is not None:
            atk_stats["combos"] += 1

    r_dmg = dmg(atk1_move,p,atk_stats,bonus_dmg,bonus_acc)
    if r_dmg == 0:
        time.sleep(1.0)
        print(atk1_n+"'s","attack \033[1m\033[30mmissed!\033[0m")
        return atk2_hp, atk1_stm, atk2_stm
    if atk1_move == "counter":
        if not (bonus_dmg > 0 or bonus_acc > 0):
            print(atk1_n, "\033[1m\033[31mCOUNTERED!\033[0m")
        if atk2_move == "block":
            print("Defense Was Rendered \033[31mUSELESS!\033[0m")
        f_dmg = r_dmg
    elif atk2_move == "block" and atk2_stm >= stamina("block"):
        f_dmg = block(r_dmg,atk1_move)
        if f_dmg < r_dmg:
            print("\033[32mBlocked.\033[0m Reduced the damage")
            if def_stats is not None:
                def_stats["blocks"] += 1
            if def_c is not None:
                if def_c["cd"] == 0:
                    def_c["rdy"] = True
                    def_c["cd"] = 1
                else:
                    def_c["cd"] -= 1
        else:
            print("\033[31mBlock Failed.\033[0m Received Full damage")
    else:
        if atk2_move == "block":
            print("Tried to block but no stamina")
        f_dmg = r_dmg

    if atk_stats is not None:
        atk_stats["tdmg"] += f_dmg

    print(atk2_n, "takes", round(f_dmg, 1),"Damage!")
    return max(0.0, atk2_hp - f_dmg),atk1_stm,atk2_stm