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

def comp_AI(mode, c_hp, c_stm, plr_hp, plr_stm, counter_a=False, his=None):
    if counter_a and c_stm >= 30:
        return "counter"
    
    if mode == "Easy":
        Ai = random.choice(["jab", "kick", "uppercut", "block"])

    elif mode == "Medium":
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

        Ai = random.choices(["jab", "kick", "uppercut", "block"], weights=w)[0]

    elif mode == "Hard":
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

        Ai = random.choices(["jab", "kick", "uppercut", "block"], weights = w)[0]

        for prob_m in ["jab", "kick", "uppercut", "block", "counter"]:
            if c_stm > combat.S[prob_m]:
                combo = combat.AiCombo(his, prob_m)
                if combo != (0,0):
                    Ai = prob_m
                    break
        else:
            Ai = random.choices(["jab", "kick", "uppercut", "block"], weights = w)[0]
    return Ai
