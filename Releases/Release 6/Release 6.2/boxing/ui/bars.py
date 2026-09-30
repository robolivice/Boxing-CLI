from ..core import data
from .colors import c_name

def d_hp_clr(class_n, c_val):
    hp_mod = data.classes.get(class_n, {}).get("hp", 1.0) 
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
    hp_mod = data.classes.get(class_n, {}).get("hp", 1.0) 
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
        
def stat_bar(plr_class, c_class, plr_stm, plr_hp,comp_stm,comp_hp, s_hp, s_stm, p_combo_cd ,c_combo_cd,end=True,p_feint=False, c_feint=False, p_debuff=False, c_debuff=False):
        if end:
            
            print("="*102)
            print("  \033[36mClass\033[0m  ->  Player:", c_name(plr_class, 49), "Computer:", c_name(c_class))
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