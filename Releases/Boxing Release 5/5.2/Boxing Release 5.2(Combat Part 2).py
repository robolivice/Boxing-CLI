#Boxingpy Test build
import time
import os
from collections import deque
import combat #Main combat
import UI     #Main UI
import setup  #Difficulty and AI

if os.name == "nt":
    os.system("")

while True:
    #Main game
    plr_hp, comp_hp, plr_stm, comp_stm,s_hp, s_stm = 100.0, 100.0, 100.0, 100.0,27, 27

    p_stats={"hits":0, "misses":0,"crits":0, "blocks":0, "combos": 0,"tdmg":0}
    c_stats={"hits":0, "misses":0,"crits":0, "blocks":0, "combos": 0,"tdmg":0}
    p_counter = {"cd": 0, "rdy": False}
    c_counter = {"cd": 0, "rdy": False}
    p_feint = {"active": False, "cd": 0}
    c_feint = {"active": False, "cd": 0}
    p_debuff = {"active": False, "cd": 0, "turns": 0}
    c_debuff = {"active": False, "cd": 0, "turns": 0}

    p_his = deque(maxlen=3)
    c_his = deque(maxlen=3)
    p_combo_cd = 0
    c_combo_cd = 0
    AI_his = []
    P_his = []

    c = 0
    rnd = 1
    dif = setup.difficulty()

    while plr_hp > 0 and comp_hp > 0:
        if rnd == 1:
            print("Difficulty: ", dif)
            time.sleep(0.5)

        print()
        print("\n-------- Round",rnd,"-------- ")
        time.sleep(0.5)

        if plr_hp < 10:
            s_hp = 29
        elif plr_hp < 100:
            s_hp = 28
        else: 
            s_hp = 27

        if plr_stm < 10:
            s_stm = 29
        elif plr_stm < 100:
            s_stm = 28
        else:
            s_stm = 27   
        
        UI.stat_bar(plr_stm,plr_hp,comp_stm,comp_hp,s_hp,s_stm,p_combo_cd,c_combo_cd, end=True, p_feint=p_feint["active"], c_feint = c_feint["active"], p_debuff = p_debuff["active"], c_debuff = c_debuff["active"])

        if p_combo_cd > 0:
            p_combo_cd -= 1
            p_his.clear()
        if c_combo_cd > 0:
            c_combo_cd -= 1
            c_his.clear()
        if p_feint["cd"] > 0:
            p_feint["cd"] -= 1
        if c_feint["cd"] > 0:
            c_feint["cd"] -= 1
        if p_debuff["cd"] > 0:
            p_debuff["cd"] -= 1
        if c_debuff["cd"] > 0:
            c_debuff["cd"] -= 1
        if p_debuff["turns"] > 0:
            p_debuff["turns"] -= 1
            if p_debuff["turns"] == 0:
                p_debuff["active"] = False
        if c_debuff["turns"] > 0:
            c_debuff["turns"] -= 1
            if c_debuff["turns"] == 0:
                c_debuff["active"] = False

        p_counter_a = p_counter["rdy"]
        c_counter_a = c_counter["rdy"]

        p_m = UI.p_move(p_feint["cd"] == 0, p_debuff["cd"] == 0,p_counter_a)
        c_move = setup.comp_AI(dif, comp_hp, comp_stm, plr_hp, plr_stm,c_counter_a, AI_his, P_his, c_feint["cd"], c_debuff["cd"])
        p_his.append(p_m)
        c_his.append(c_move)

        P_his.append(p_m)
        AI_his.append(c_move)
        P_his = P_his[-2:]
        AI_his = AI_his[-2:]

        p_dmg_b, p_acc_b = combat.combo(p_his)
        c_dmg_b, c_acc_b = combat.combo(c_his)

        if (p_dmg_b, p_acc_b) != (0,0):
            if p_combo_cd > 0:
                p_dmg_b , p_acc_b = (0,0)
            else:
                p_combo_cd = 3
            p_his.clear()

        if (c_dmg_b, c_acc_b) != (0,0):
            if c_combo_cd > 0:
                c_dmg_b , c_acc_b = (0,0)
            else:
                c_combo_cd = 3
            c_his.clear()

        comp_hp, plr_stm, comp_stm = combat.r_turn("Player", "Computer", p_m, c_move, comp_hp, plr_stm, comp_stm, "Player",True,p_stats,c_stats,p_counter,c_counter, p_dmg_b, p_acc_b,p_feint,p_debuff,c_debuff)
        plr_hp, comp_stm, plr_stm = combat.r_turn("Computer", "Player", c_move, p_m, plr_hp, comp_stm, plr_stm, "Computer",False,c_stats,p_stats,c_counter,p_counter, c_dmg_b, c_acc_b,c_feint,c_debuff,p_debuff)

        c += 1
        if c == 3:
            plr_stm = min(100.0, plr_stm + 10.0)
            comp_stm = min(100.0, comp_stm + 10.0)
            c = 0

        time.sleep(0.5)

        UI.stat_bar(plr_stm,plr_hp,comp_stm,comp_hp,s_hp,s_stm,p_combo_cd,c_combo_cd, end=False)
        rnd+=1

    #end
    if plr_hp <= 0 and comp_hp <= 0:
        print("It's a \033[1m\033[33mDraw game!\033[0m")
        flag = True
    elif plr_hp <= 0:
        print("\033[1m\033[31mK.O.!\033[0m The Computer wins.")
        flag = True
    else:
        print("\033[1m\033[31mK.O.!\033[0m You win!")
        flag = True
    #Playing Again
    if flag == True:
        UI.m_stats(p_stats, c_stats)
        x = input("Do you wanna play again? \033[1m\033[32m(y/n)\033[0m]: ").lower()
        if x == "y":
            continue
        else:
            print("\033[1m\033[34mThanks for playing!\033[0m")
            break