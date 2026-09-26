#Main Ui mechanics
import time

def p_move(feint_rd = False, taunt_rd = False, counter_a=False):
    lines_printed = 0
    while True:
        m = ["jab", "kick", "uppercut", "block"]
        print("\033[92mMove            Damage           Accuracy         Stamina          ID\033[0m")
        print("\033[94mJab              5HP              100%               0              1")
        print("Kick            15HP               65%              10              2")
        print("Uppercut        25HP               40%              20              3")
        print("Block       Move Dependent     Move Dependent       15              4\033[0m")
        if feint_rd:
            m.append("feint")
            print("\033[94mFeint            0HP              100%              10             ",str(len(m))+"\033[0m")
        if taunt_rd:
            m.append("taunt")
            print("\033[94mTaunt            0HP              100%              10             ",str(len(m))+"\033[0m")
        if counter_a:
            m.append("counter")
            print("\033[91m\033[1mCounter         40HP               85%              30             ",str(len(m))+"\033[0m")
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

def d_hp_clr(c_val):
    c_val = max(0.0, min(c_val, 100.0))
    t_b = 15
    f_b = int((c_val/100)*t_b)
    if f_b >= 10:
        cde = "\033[32m"
    elif f_b >= 5:
        cde = "\033[33m"
    else:
        cde = "\033[31m"
    return cde

def s_bars(c_val,c_code):
    c_val = max(0.0, min(c_val, 100.0))
    total_b = 15
    filled_b = int((c_val/100)*total_b)
    empty_b = 15 - filled_b
    bar = c_code + ("■"*filled_b) + "\033[0m" + ("□"*empty_b)
    return bar

def c_bar(c_cd):
    c_cd_e = 3 - c_cd
    bar = "\033[35m" + ("■"*c_cd) + ("□"*c_cd_e) + "\033[0m"
    return bar

def deb_bar_c(p_feint=False, c_feint=False, p_debuff=False, c_debuff=False):
    deb_bar = False
    if p_feint == True or c_feint == True or p_debuff == True or c_debuff == True:
        deb_bar = True
    return deb_bar

def deb_bar(p_feint=False, c_feint=False, p_debuff=False, c_debuff=False):
    def UI(feint, debuff):
        if feint and debuff:
            return "\033[32mFEINT\033[0m \033[31mTAUNTED\033[0m" + " "*36
        elif feint:
            return "\033[32mFEINT\033[0m" + " "*44
        elif debuff:
            return "\033[31mTAUNTED\033[0m" + " "*42
        else:
            return "-" + " "*48
    return UI(p_feint, p_debuff), UI(c_feint, c_debuff)

    # Future Plans
    """ 
    p_text = UI(p_feint, p_debuff)
    c_text = UI(c_feint, c_debuff)

    pad_w = 20
    p_pad = p_text.ljust(pad_w)
    c_pad = c_text.ljust(pad_w)

    if p_feint:
        p_colour = "\033[32m"
    elif p_debuff:
        p_colour = "\033[31m"
    else:
        p_colour = "\033[0m"
    if c_feint:
        c_colour = "\033[32m"
    elif c_debuff:
        c_colour = "\033[31m"
    else:
        c_colour = "\033[0m"

    p_status = p_colour + p_pad + "\033[0m"
    c_status = c_colour + c_pad + "\033[0m"

    return p_status, c_status"""
    #-------------------------------------------------------------------------

def m_stats(p_stats, c_stats):
        
        sp = 8
        p_line = " Player   -->   Hits: " + str(p_stats["hits"]).ljust(sp) + " Misses: " + str(p_stats["misses"]).ljust(sp) + " Crits: " + str(p_stats["crits"]).ljust(sp) + " Blocks: " + str(p_stats["blocks"]).ljust(sp) + " Combos: " + str(p_stats["combos"]).ljust(sp) +" Total Damage Dealt: " + str(round(float(p_stats["tdmg"]),1))
        c_line = "Computer  -->   Hits: " + str(c_stats["hits"]).ljust(sp) + " Misses: " + str(c_stats["misses"]).ljust(sp) + " Crits: " + str(c_stats["crits"]).ljust(sp) + " Blocks: " + str(c_stats["blocks"]).ljust(sp) + " Combos: " + str(c_stats["combos"]).ljust(sp) +" Total Damage Dealt: " + str(round(float(c_stats["tdmg"]),1))
        title = "Match Stats"
        wid = max(len(p_line),len(c_line))
        rem = wid - len(title) - 2
        l = rem//2
        r = rem - l

        print()
        print("="*l, "\033[32m"+title+"\033[0m", "="*r)
        print(p_line)
        print(c_line)
        print("="*wid)
        print()

def stat_bar(plr_stm, plr_hp,comp_stm,comp_hp, s_hp, s_stm, p_combo_cd ,c_combo_cd,end=True,p_feint=False, c_feint=False, p_debuff=False, c_debuff=False):
        if end:
            
            print("="*102)
            print("    \033[32mHP\033[0m   ->  Player:", s_bars(plr_hp, d_hp_clr(plr_hp)),d_hp_clr(plr_hp)+str(round(plr_hp,1))+"\033[0m"," "*s_hp, "Computer:", s_bars(comp_hp, d_hp_clr(comp_hp)),d_hp_clr(comp_hp)+str(round(comp_hp,1))+"\033[0m")
            print(" \033[33mStamina\033[0m ->  Player:", s_bars(plr_stm, "\033[33m"),"\033[33m"+str(round(plr_stm,1))+"\033[0m"," "*s_stm, "Computer:", s_bars(comp_stm, "\033[33m"),"\033[33m"+str(round(comp_stm,1))+"\033[0m")
            print("\033[35mCombo Cd\033[0m ->  Player:", c_bar(p_combo_cd), " "*45 ,"Computer:", c_bar(c_combo_cd))
            if deb_bar_c(p_feint, c_feint, p_debuff, c_debuff):
                p_status, c_status = deb_bar(p_feint, c_feint, p_debuff, c_debuff)
                print(" \033[36mStatus\033[0m  ->  Player:", p_status, "Computer:", c_status)
            print("="*102)
            print()
        else:
            print("   \033[32mRemaining HP\033[0m   -> Player:", s_bars(plr_hp, d_hp_clr(plr_hp)),d_hp_clr(plr_hp)+str(round(plr_hp,1))+"\033[0m"," "*s_hp, "Computer:", s_bars(comp_hp, d_hp_clr(comp_hp)),d_hp_clr(comp_hp)+str(round(comp_hp,1))+"\033[0m")
            print("\033[33mRemaining Stamina\033[0m -> Player:", s_bars(plr_stm, "\033[33m"),"\033[33m"+str(round(plr_stm,1))+"\033[0m"," "*s_stm, "Computer:", s_bars(comp_stm, "\033[33m"),"\033[33m"+str(round(comp_stm,1))+"\033[0m")