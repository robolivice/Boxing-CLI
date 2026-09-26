#Setup and AI
import random
import time
import combat
import UI

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
    seed_in = input(" RNG seed (blank for none): ")
    opts["seed"] = int(seed_in) if seed_in.strip().isdigit() else None
    return opts

def class_s():
    k_map = {"b": "berserker", "a": "assassin", "j": "juggernaut", "d": "duelist", "r": "reaper"}
    while True:
        print("Enter Class Selection")
        UI.class_menu()
        input_print = UI.color.get("bold")+UI.color.get("yellow")+"B"+UI.color.get("reset")+ "/"+UI.color.get("bold")+UI.color.get("purple")+"A"+UI.color.get("reset")+ "/"+UI.color.get("bold")+UI.color.get("red")+"J"+UI.color.get("reset")+"/"+UI.color.get("bold")+UI.color.get("blue")+"D"+UI.color.get("reset")+"/"+UI.color.get("bold")+UI.color.get("black")+"R"+UI.color.get("reset")+": "
        _class = input(input_print).lower().strip()

        if _class in k_map:
            return k_map[_class]
        print("Please select a Valid Class")
        time.sleep(1.2)
        l_p = 8
        for i in range(l_p):
            print("\033[A\r\033[K", end="")
            
def difficulty():
    while True:
        try:
            dif = input("Enter Difficulty Level: \033[1m\033[32mEasy (E)\033[0m | \033[1m\033[33mMedium (M)\033[0m | \033[1m\033[31mHard (H)\033[0m: ").lower()
            if dif == "e" or dif == "easy":
                display = ("\033[1m\033[32mEasy\033[0m")
                mode = "Easy"
            elif dif == "m" or dif == "medium":
                display =("\033[1m\033[33mMedium\033[0m")
                mode = "Medium"
            elif dif == "h" or dif == "hard":
                display =("\033[1m\033[31mHard\033[0m")
                mode = "Hard"
            return mode, display
        except:
            print("Please select Correct Difficulty")
            time.sleep(1.2)
            for i in range(2):
                print("\033[A\r\033[K", end="")

def comp_AI(mode, c_hp, c_stm, plr_hp, plr_stm, counter_a=False, his=None, p_his = None, feint_cd = 0, taunt_cd = 0, c_S = None):
    if c_S is not None:
        s_tbl = c_S
    else:
        s_tbl = combat.S

    up = s_tbl["uppercut"]
    kick = s_tbl["kick"]
    blk = s_tbl["block"]

    if counter_a and c_stm >= s_tbl["counter"]:
        return "counter"

    feint_a = False
    if feint_cd == 0 and c_stm >= s_tbl["feint"]:
        feint_a = True
    taunt_a = False
    if taunt_cd == 0 and c_stm >= s_tbl["taunt"]:
        taunt_a = True
    
    if mode == "Easy":
        c_e = ["jab", "kick", "uppercut", "block"]
        if feint_a:
            c_e.append("feint")
        if taunt_a:
            c_e.append("taunt")
        Ai = random.choice(c_e)

    elif mode == "Medium":
        c_m = ["jab", "kick", "uppercut", "block"]
        w = [10, 10, 10, 10]
        if c_stm <= up:
            w = [20, 15, 2, 3]
        if plr_stm < blk:
            if c_stm >= up+5:
                w = [5, 10, 20, 2]
            elif c_stm < up+5 and c_stm > up:
                w = [20, 10, 5, 2]
            else:
                w = [20, 15, 2, 3]
        if feint_a:
            c_m.append("feint")
            if plr_stm >= 40:
                w.append(10)
            else:
                w.append(5)
        if taunt_a:
            c_m.append("taunt")
            if c_hp >= plr_hp:
                w.append(10)
            else:
                w.append(5)

        c_m2 = []
        w2 = []
        for i in range(len(c_m)):
            if c_stm >= s_tbl[c_m[i]]:
                c_m2.append(c_m[i])
                w2.append(w[i])
        Ai = random.choices(c_m2, weights=w2)[0]

    elif mode == "Hard":
        c_h = ["jab", "kick", "uppercut", "block"]
        w= [10, 10, 10, 10]
        if plr_hp <= 25:
            if c_stm >= up+5:
                w = [3, 10, 20, 2]
            elif c_stm < up+5 and c_stm >=kick:
                w = [20, 10, 3, 2]
            else:
                w = [1, 0, 0, 0]

        if c_hp <= 25:
            if c_stm >= blk:
                w = [5, 2, 1, 20]
            elif c_stm < blk and c_stm >= kick:
                w = [80, 20, 3, 4]
            else:
                w = [1, 0, 0, 0]
        r_d = False
        if feint_a:
            c_h.append("feint")
            if p_his is not None and len(p_his) > 0 and p_his[-1] in ("block", "counter"):
                r_d = True
            if r_d == True:
                w.append(15)
            else: 
                w.append(5)     

        if taunt_a:
            c_h.append("taunt")
            if plr_stm > 40:
                w.append(15)
            else:
                w.append(2)

        c_h2 = []
        w2 = []
        for i in range(len(c_h)):
            if c_stm >= s_tbl[c_h[i]]:
                c_h2.append(c_h[i])
                w2.append(w[i])
        Ai = random.choices(c_h2, weights=w2)[0]

        c_prob_m = ["jab", "kick", "uppercut", "block"]
        if counter_a:
            c_prob_m.append("counter")
        if feint_a:
            c_prob_m.append("feint")
        if taunt_a:
            c_prob_m.append("taunt")

        for prob_m in c_prob_m:
            if c_stm > s_tbl[prob_m]:
                combo = combat.AiCombo(his, prob_m)
                if combo != (0,0):
                    Ai = prob_m
                    break
    return Ai
