#Main Ui mechanics
import time
import combat

color = {
    "reset":      "\033[0m",
    "bold":       "\033[1m",
    "black":      "\033[30m",
    "red":        "\033[31m",
    "green":      "\033[32m",
    "yellow":     "\033[33m",
    "blue":       "\033[34m",
    "purple":     "\033[35m",
    "cyan":       "\033[36m",
    "white":      "\033[37m",
    "black_b":    "\033[90m",
    "red_b":      "\033[91m",
    "green_b":    "\033[92m",
    "yellow_b":   "\033[93m",
    "blue_b":     "\033[94m",
    "purple_b":   "\033[95m",
    "cyan_b":     "\033[96m",
    "white_b":    "\033[97m", 
    "f_black":    "\033[40m",
    "f_red":      "\033[41m",
    "f_green":    "\033[42m",
    "f_yellow":   "\033[43m",
    "f_blue":     "\033[44m",
    "f_purple":   "\033[45m",
    "f_cyan":     "\033[46m",
    "f_white":    "\033[47m",
    "f_black_b":  "\033[100m",
    "f_red_b":    "\033[101m",
    "f_green_b":  "\033[102m",
    "f_yellow_b": "\033[103m",
    "f_blue_b":   "\033[104m",
    "f_purple_b": "\033[105m",
    "f_cyan_b":   "\033[106m",
    "f_white_b":  "\033[107m",
}

def load_sc(mode, dur):
    if mode == "static":
        print("Loading.")
        time.sleep(dur)
        print("\033[A\r\033[K", end="")
        print("Loading..")
        time.sleep(dur)
        print("\033[A\r\033[K", end="")
        print("Loading...")
        time.sleep(dur)
        print("\033[A\r\033[K", end="")
    if mode == "dynamic":
        print("Loading.")
        time.sleep(dur)
        print("\033[A\r\033[K", end="")
        print("Loading..")
        time.sleep(dur)
        print("\033[A\r\033[K", end="")
        print("Loading...")
        time.sleep(dur+0.5)
        print("\033[A\r\033[K", end="")

def debug_print(p_feint, c_feint, p_debuff, c_debuff, p_counter, c_counter, p_combo_cd, c_combo_cd, p_his, c_his, AI_his, P_his):
    print("\033[90m---- DEBUG STATE ----")
    print("p_feint:", p_feint, "c_feint:", c_feint)
    print("p_debuff:", p_debuff, "c_debuff:", c_debuff)
    print("p_counter:", p_counter, "c_counter:", c_counter)
    print("p_combo_cd:", p_combo_cd, "c_combo_cd:", c_combo_cd)
    print("p_his:", list(p_his), "c_his:", list(c_his))
    print("AI_his:", AI_his, "P_his:", P_his)
    print("---------------------\033[0m")

def class_menu():
            
    print(color.get("bold")+color.get("yellow")+"Berserker: "+color.get("reset"), color.get("red")+"Damage: x1.25"+color.get("reset"), color.get("blue")+"Accuracy: x0.90"+color.get("reset"), color.get("yellow")+"Stamina Usage: x1.10"+color.get("reset"), color.get("green")+"HP: x1.00"+color.get("reset"), color.get("purple")+"Critical: x1.20"+color.get("reset"))
    print(color.get("bold")+color.get("purple")+"Assassin:  "+color.get("reset"), color.get("red")+"Damage: x0.90"+color.get("reset"), color.get("blue")+"Accuracy: x1.20"+color.get("reset"), color.get("yellow")+"Stamina Usage: x1.00"+color.get("reset"), color.get("green")+"HP: x1.00"+color.get("reset"), color.get("purple")+"Critical: x1.30"+color.get("reset"))
    print(color.get("bold")+color.get("red")   +"Juggernaut:"+color.get("reset"), color.get("red")+"Damage: x1.00"+color.get("reset"), color.get("blue")+"Accuracy: x1.00"+color.get("reset"), color.get("yellow")+"Stamina Usage: x0.75"+color.get("reset"), color.get("green")+"HP: x1.20"+color.get("reset"), color.get("purple")+"Critical: x0.80"+color.get("reset"))
    print(color.get("bold")+color.get("blue")  +"Duelist:   "+color.get("reset"), color.get("red")+"Damage: x1.10"+color.get("reset"), color.get("blue")+"Accuracy: x0.95"+color.get("reset"), color.get("yellow")+"Stamina Usage: x0.90"+color.get("reset"), color.get("green")+"HP: x0.90"+color.get("reset"), color.get("purple")+"Critical: x1.10"+color.get("reset"))
    print(color.get("bold")+color.get("black") +"Reaper:    "+color.get("reset"), color.get("red")+"Damage: x1.50"+color.get("reset"), color.get("blue")+"Accuracy: x0.80"+color.get("reset"), color.get("yellow")+"Stamina Usage: x1.30"+color.get("reset"), color.get("green")+"HP: x0.75"+color.get("reset"), color.get("purple")+"Critical: x1.50"+color.get("reset"))

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

def d_hp_clr(class_n, c_val):
    hp_mod = combat.classes.get(class_n, {}).get("hp", 1.0) 
    max_val = 100*hp_mod
    c_val = max(0.0, min(c_val, max_val))
    t_b = 15
    f_b = int((c_val/max_val)*t_b)
    if f_b >= 10:
        cde = "\033[32m"
    elif f_b >= 5:
        cde = "\033[33m"
    else:
        cde = "\033[31m"
    return cde

def hp_bars(class_n, c_val,c_code):
    hp_mod = combat.classes.get(class_n, {}).get("hp", 1.0) 
    max_val = 100*hp_mod
    c_val = max(0.0, min(c_val, max_val))
    total_b = 15
    filled_b = int((c_val/max_val)*total_b)
    empty_b = 15 - filled_b
    bar = c_code + ("■"*filled_b) + "\033[0m" + ("□"*empty_b)
    return bar

def stm_bar(c_val,c_code):
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
        p_line = " Player   -->   Hits: " + str(p_stats["hits"]).ljust(sp) + " Misses: " + str(p_stats["misses"]).ljust(sp) + " Crits: " + str(p_stats["crits"]).ljust(sp) + " Blocks: " + str(p_stats["blocks"]).ljust(sp) + " Combos: " + str(p_stats["combos"]).ljust(sp) +" Total Damage Dealt: " + str(round(float(p_stats["tdmg"]),1)).ljust(sp) +" Fights Won: " + str(p_stats["f_won"])
        c_line = "Computer  -->   Hits: " + str(c_stats["hits"]).ljust(sp) + " Misses: " + str(c_stats["misses"]).ljust(sp) + " Crits: " + str(c_stats["crits"]).ljust(sp) + " Blocks: " + str(c_stats["blocks"]).ljust(sp) + " Combos: " + str(c_stats["combos"]).ljust(sp) +" Total Damage Dealt: " + str(round(float(c_stats["tdmg"]),1)).ljust(sp) +" Fights Won: " + str(c_stats["f_won"])
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

def class_color(plr_class):
    if plr_class == "berserker":
        spc = 49 - len("berserker")
        c_cde = "\033[1m\033[33m"+"Berserker"+"\033[0m"+" "*spc
    elif plr_class == "assassin":
        spc = 49 - len("assassin")
        c_cde = "\033[1m\033[35m"+"Assassin"+"\033[0m"+" "*spc
    elif plr_class == "juggernaut":
        spc = 49 - len("juggernaut")
        c_cde = "\033[1m\033[31m"+"Juggernaut"+"\033[0m"+" "*spc
    elif plr_class == "duelist":
        spc = 49 - len("duelist")
        c_cde = "\033[1m\033[34m"+"Duelist"+"\033[0m"+" "*spc
    elif plr_class == "reaper":
        spc = 49 - len("reaper")
        c_cde = "\033[1m\033[30m"+"Reaper"+"\033[0m"+" "*spc
    return c_cde

def c_class_color(c_class):
    if c_class == "berserker":
        comp_cde = "\033[1m\033[33m"+"Berserker"+"\033[0m"
    elif c_class == "assassin":
        comp_cde = "\033[1m\033[35m"+"Assassin"+"\033[0m"
    elif c_class == "juggernaut":
        comp_cde = "\033[1m\033[31m"+"Juggernaut"+"\033[0m"
    elif c_class == "duelist":
        comp_cde = "\033[1m\033[34m"+"Duelist"+"\033[0m"
    elif c_class == "reaper":
        comp_cde = "\033[1m\033[30m"+"Reaper"+"\033[0m"
    return comp_cde

def stat_bar(plr_class, c_class, plr_stm, plr_hp,comp_stm,comp_hp, s_hp, s_stm, p_combo_cd ,c_combo_cd,end=True,p_feint=False, c_feint=False, p_debuff=False, c_debuff=False):
        if end:
            
            print("="*102)
            print("  \033[36mClass\033[0m  ->  Player:", class_color(plr_class), "Computer:", c_class_color(c_class))
            print("    \033[32mHP\033[0m   ->  Player:", hp_bars(plr_class, plr_hp, d_hp_clr(plr_class, plr_hp)),d_hp_clr(plr_class, plr_hp)+str(round(plr_hp,1))+"\033[0m"," "*s_hp, "Computer:", hp_bars(c_class, comp_hp, d_hp_clr(c_class, comp_hp)),d_hp_clr(c_class, comp_hp)+str(round(comp_hp,1))+"\033[0m")
            print(" \033[33mStamina\033[0m ->  Player:", stm_bar(plr_stm, "\033[33m"),"\033[33m"+str(round(plr_stm,1))+"\033[0m"," "*s_stm, "Computer:", stm_bar(comp_stm, "\033[33m"),"\033[33m"+str(round(comp_stm,1))+"\033[0m")
            print("\033[35mCombo Cd\033[0m ->  Player:", c_bar(p_combo_cd), " "*45 ,"Computer:", c_bar(c_combo_cd))
            if deb_bar_c(p_feint, c_feint, p_debuff, c_debuff):
                p_status, c_status = deb_bar(p_feint, c_feint, p_debuff, c_debuff)
                print(" \033[36mStatus\033[0m  ->  Player:", p_status, "Computer:", c_status)
            print("="*102)
            print()
        else:
            print("   \033[32mRemaining HP\033[0m   -> Player:", hp_bars(plr_class, plr_hp, d_hp_clr(plr_class, plr_hp)),d_hp_clr(plr_class, plr_hp)+str(round(plr_hp,1))+"\033[0m"," "*s_hp, "Computer:", hp_bars(c_class, comp_hp, d_hp_clr(c_class, comp_hp)),d_hp_clr(c_class, comp_hp)+str(round(comp_hp,1))+"\033[0m")
            print("\033[33mRemaining Stamina\033[0m -> Player:", stm_bar(plr_stm, "\033[33m"),"\033[33m"+str(round(plr_stm,1))+"\033[0m"," "*s_stm, "Computer:", stm_bar(comp_stm, "\033[33m"),"\033[33m"+str(round(comp_stm,1))+"\033[0m")