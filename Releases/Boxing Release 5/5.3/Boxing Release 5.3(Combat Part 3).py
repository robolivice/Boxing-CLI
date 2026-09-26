#Boxingpy Test build
import time
import os
import random
from collections import deque
import combat #Main combat
import UI     #Main UI
import setup  #Difficulty and AI

if os.name == "nt":
    os.system("")

while True:
    dbg = setup.debug_m()
    DEBUG_OPTS = setup.debug_opts() if dbg else {}
    if dbg and DEBUG_OPTS["seed"] is not None:
        random.seed(DEBUG_OPTS["seed"])

    #Main game
    p_class = setup.class_s()
    if dbg and DEBUG_OPTS["ai_class"]:
        while True:
            c_class = input("Debug - AI Class: ").lower().strip()
            if c_class not in combat.classes:
                print("Error. Not a Valid Class")
                time.sleep(0.5)
                for i in range(2):
                    print("\033[A\r\033[K", end="")
            else:
                break
    else:
        c_class = random.choice(list(combat.classes))

    p_stats={"hits":0, "misses":0,"crits":0, "blocks":0, "combos": 0,"tdmg":0,"f_won": 0}
    c_stats={"hits":0, "misses":0,"crits":0, "blocks":0, "combos": 0,"tdmg":0,"f_won": 0}

    dif, mode_c = setup.difficulty()

    max_mtc = 3
    p_mtc_won, c_mtc_won = 0, 0
    c_mtc = 1
    mtc_to_win = (max_mtc//2) + 1

    while p_mtc_won < mtc_to_win and c_mtc_won < mtc_to_win:
        plr_stm, comp_stm,s_hp, s_stm = 100.0, 100.0, 27, 27

        p_M, p_S = combat.s_class(p_class)
        c_M, c_S = combat.s_class(c_class)
        plr_hp = 100.0 * combat.classes[p_class]["hp"]
        comp_hp = 100.0 * combat.classes[c_class]["hp"]

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
        print()
        print("\n"+UI.color.get("bold")+UI.color.get("purple")+"-"*47+UI.color.get("reset"), "\033[1m\033[31mFight",str(c_mtc)+UI.color.get("reset"), UI.color.get("bold")+ UI.color.get("purple") +"-"*47+UI.color.get("reset"))
        if not dbg:
            if c_mtc == 1:
                UI.load_sc("static", 1.0)
            else:
                UI.load_sc("dynamic", 0.5)

        while plr_hp > 0 and comp_hp > 0:
            if c_mtc == 1 and rnd == 1:
                print("Difficulty: ", mode_c)
                time.sleep(0.5)

            print()
            print("\n"+"               "+UI.color.get("bold")+UI.color.get("purple")+"-"*32+UI.color.get("reset"), "\033[1m\033[36mRound",str(rnd)+"\033[0m",UI.color.get("bold")+UI.color.get("purple")+"-"*32+UI.color.get("reset")+"               ")
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
            
            UI.stat_bar(p_class,c_class,plr_stm,plr_hp,comp_stm,comp_hp,s_hp,s_stm,p_combo_cd,c_combo_cd, end=True, p_feint=p_feint["active"], c_feint = c_feint["active"], p_debuff = p_debuff["active"], c_debuff = c_debuff["active"])

            if dbg and DEBUG_OPTS["show_state"]:
                UI.debug_print(p_feint, c_feint, p_debuff, c_debuff, p_counter, c_counter, p_combo_cd, c_combo_cd, p_his, c_his, AI_his, P_his)

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
            if dbg and DEBUG_OPTS["force_player"]:
                p_m = input("DEBUG - Player Move: ").lower().strip()
            else:
                p_m = UI.p_move(p_M,p_S, p_feint["cd"] == 0, p_debuff["cd"] == 0,p_counter_a)
            if dbg and DEBUG_OPTS["force_ai"]:
                c_move = input("DEBUG - AI move: ").lower().strip()
            else:
                c_move = setup.comp_AI(dif, comp_hp, comp_stm, plr_hp, plr_stm,c_counter_a, AI_his, P_his, c_feint["cd"], c_debuff["cd"], c_S=c_S)
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

            comp_hp, plr_stm, comp_stm = combat.r_turn("Player", "Computer", p_m, c_move, comp_hp, plr_stm, comp_stm, "Player",True,p_stats,c_stats,p_counter,c_counter, p_dmg_b, p_acc_b,p_feint,p_debuff,c_debuff, bypass_stm=(dbg and DEBUG_OPTS["god_stamina"]), atk1_M=p_M, atk1_S=p_S, atk2_S = c_S)
            plr_hp, comp_stm, plr_stm = combat.r_turn("Computer", "Player", c_move, p_m, plr_hp, comp_stm, plr_stm, "Computer",False,c_stats,p_stats,c_counter,p_counter, c_dmg_b, c_acc_b,c_feint,c_debuff,p_debuff, bypass_stm=(dbg and DEBUG_OPTS["god_stamina"]), atk1_M=c_M, atk1_S=c_S, atk2_S = p_S)

            if p_counter_a and p_m != "counter":
                p_counter["rdy"] = False
            if c_counter_a and c_move != "counter":
                c_counter["rdy"] = False

            c += 1
            if c == 3:
                plr_stm = min(100.0, plr_stm + 10.0)
                comp_stm = min(100.0, comp_stm + 10.0)
                c = 0

            time.sleep(0.5)

            UI.stat_bar(p_class, c_class, plr_stm,plr_hp,comp_stm,comp_hp,s_hp,s_stm,p_combo_cd,c_combo_cd, end=False)
            rnd+=1

        #Fight End
        c_mtc += 1
        if plr_hp <= 0 and comp_hp <= 0:
            print("It's a \033[1m\033[33mDraw game!\033[0m")
        elif plr_hp <= 0:
            c_mtc_won += 1
            c_stats["f_won"] += 1
            print("\033[1m\033[31mK.O.!\033[0m The Computer wins this Fight.", "("+str(c_mtc_won)+"/"+ str(mtc_to_win)+")")
        else:
            p_mtc_won += 1
            p_stats["f_won"] += 1
            print("\033[1m\033[31mK.O.!\033[0m You win this Fight!", "("+str(p_mtc_won)+"/"+ str(mtc_to_win)+")")
        time.sleep(2)
        print()
        wonp = "("+str(p_mtc_won)+"/"+ str(mtc_to_win)+")"
        wonc = "("+str(c_mtc_won)+"/"+ str(mtc_to_win)+")"
        if p_mtc_won >= mtc_to_win or c_mtc_won >= mtc_to_win:
            if p_mtc_won >= mtc_to_win:
                print("\033[1m\033[32mPlayer\033[0m won the Match!!",UI.color.get("bold")+UI.color.get("green")+wonp+UI.color.get("reset"))
                break
            else:
                print("\033[1m\033[31mComputer\033[0m won the Match!!",UI.color.get("bold")+UI.color.get("red")+wonc+UI.color.get("reset"))
                break

    #Playing Again
    UI.m_stats(p_stats, c_stats)
    x = input("Do you wanna play again? \033[1m\033[32m(y/n)\033[0m: ").lower()
    if x == "y":
        continue
    else:
        print("\033[1m\033[34mThanks for playing!\033[0m")
        break