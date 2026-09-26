#Setup and AI
import random
import time
import combat

def difficulty():
    while True:
        try:
            dif = input("Enter Difficulty Level: Easy (E) | Medium (M) | Hard (H): ").lower()
            if dif == "e" or dif == "easy":
                mode = "Easy"
            elif dif == "m" or dif == "medium":
                mode = "Medium"
            elif dif == "h" or dif == "hard":
                mode = "Hard"
            return mode
        except:
            print("Please select Correct Difficulty")
            time.sleep(1.2)
            for i in range(2):
                print("\033[A\r\033[K", end="")

def comp_AI(mode, c_hp, c_stm, plr_hp, plr_stm, counter_a=False, his=None, p_his = None, feint_cd = 0, taunt_cd = 0):
    if counter_a and c_stm >= 30:
        return "counter"

    feint_a = False
    if feint_cd == 0 and c_stm >= combat.S["feint"]:
        feint_a = True
    taunt_a = False
    if taunt_cd == 0 and c_stm >= combat.S["taunt"]:
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
        if c_stm <= 20.0:
            w = [20, 15, 2, 3]
        if plr_stm < 15:
            if c_stm >= 25:
                w = [5, 10, 20, 2]
            elif c_stm < 25 and c_stm > 20:
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
        Ai = random.choices(c_m, weights=w)[0]

    elif mode == "Hard":
        c_h = ["jab", "kick", "uppercut", "block"]
        w= [10, 10, 10, 10]
        if plr_hp <= 25:
            if c_stm >= 25:
                w = [3, 10, 20, 2]
            elif c_stm < 25 and c_stm >=10:
                w = [20, 10, 3, 2]
            else:
                w = [1, 0, 0, 0]

        if c_hp <= 25:
            if c_stm >= 15:
                w = [5, 2, 1, 20]
            elif c_stm < 15 and c_stm >= 10:
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

        Ai = random.choices(c_h, weights = w)[0]

        c_prob_m = ["jab", "kick", "uppercut", "block", "counter"]
        if feint_a:
            c_prob_m.append("feint")
        if taunt_a:
            c_prob_m.append("taunt")

        for prob_m in c_prob_m:
            if c_stm > combat.S[prob_m]:
                combo = combat.AiCombo(his, prob_m)
                if combo != (0,0):
                    Ai = prob_m
                    break
        else:
            Ai = random.choices(c_h, weights = w)[0]
    return Ai
