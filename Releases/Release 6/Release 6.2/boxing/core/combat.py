#Main combat Mechanics
import random
import time
from .data import M, B, S, C, D

# Manual validation
def calc_acc(m,bonus_acc=0, m_table = None):
    # fallback to 0,0,0
    if m_table is not None:
        tbl = m_table
    else:
        tbl = M
    dmg, acc, _ = tbl.get(m, (0, 0, 0))
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

def stamina(s, s_table = None):
    if s_table is not None:
        tbl = s_table
    else:
        tbl = S
    stm = tbl.get(s)
    return stm

def combo(his):
    return C.get(tuple(his), (0,0))

def AiCombo(his, n_move):
    if len(his) < 2:
        return (0,0)
    return combo(his[-2:] + [n_move])

def fatigue(stm):
    if stm <= 20:
        neg_acc = 20
        neg_dmg = 10
    elif stm <= 40:
        neg_dmg = 0
        neg_acc = 10
    else:
        neg_dmg = 0
        neg_acc = 0
    return neg_dmg, neg_acc

def dmg(s,p, stats=None, bonus_dmg = 0, bonus_acc = 0, m_table = None):
    dmg = calc_acc(s, bonus_acc, m_table)
    if dmg == 0:
        if stats is not None:
            stats["misses"] += 1
        return 0
    if m_table is not None:
        tbl = m_table
    else:
        tbl = M
    __, _, crit_c = tbl.get(s, (0,0,0))
    if stats is not None:
        stats["hits"] += 1
    if random.uniform(0,100) < crit_c:
        if stats is not None:
            stats["crits"] += 1
        print(p,"has landed a \033[31mCRITICAL HIT\033[0m!")
        return dmg*1.5 + bonus_dmg
    return dmg + bonus_dmg

#Main turn
def r_turn(atk, dfn, atk_move, dfn_move, dfn_stm, flag1 = True, bonus = (0,0), bypass_stm = False):
    if flag1:
        print(atk.name, "uses", "\033[33m"+str(atk_move.upper())+"\033[0m", dfn.name, "chose:","\033[34m" +str(dfn_move.upper())+"\033[0m")
    
    stmc = stamina(atk_move, atk.S)
    if stmc is None:
        print("Unknown Move:", atk_move)
        return

    if not bypass_stm and atk.stm < stmc:
        print("Not enough Stamina: Move Failed")
        return

    o_stm = atk.stm
    if not bypass_stm:
        atk.stm -= stmc

    if atk_move in ("block", "feint", "taunt"):
        _utility_move(atk, dfn, atk_move, flag1)
        return

    if atk_move == "counter":
        atk.counter["rdy"] = False

    bonus_dmg, bonus_acc = bonus
    _announce_combo(atk, bonus_dmg, bonus_acc)
    bonus_acc, neg_dmg = _f_and_stats(atk, dfn, atk_move, dfn_move, o_stm, bonus_acc)
    r_dmg = dmg(atk_move, atk.name, atk.stats, bonus_dmg, bonus_acc, atk.M)
    if r_dmg == 0:
        time.sleep(1.0)
        print(atk.name + "'s", "attack \033[1m\033[30mmissed!\033[0m")
        return
    r_dmg *= 1 - neg_dmg / 100.0

    h_bonus = bonus_dmg > 0 or bonus_acc > 0
    f_dmg = _apply_defense(atk, dfn, atk_move, dfn_move, dfn_stm, r_dmg, h_bonus)

    atk.stats["tdmg"] += min(f_dmg, dfn.hp)
    dfn.hp = max(0.0, dfn.hp - f_dmg)
    print(dfn.name, "takes", round(f_dmg, 1), "Damage!")

def _utility_move(atk, dfn, move, announce):
    if move == "block":
        time.sleep(1.0)
        print(atk.name, "Puts up \033[34mGuard\033[0m")
        atk.feint["active"] = False
    elif move == "feint":
        print(atk.name, "Uses \033[30mFeint!\033[0m")
        atk.feint["active"] = True
        atk.feint["cd"] = 3
    elif move == "taunt":
        print(atk.name, "Uses \033[30mTaunt!\033[0m")
        turns = D["taunt"][1]
        if not announce:          # second mover gets +1 (preserved from original)
            turns += 1
        dfn.debuff["active"] = True
        dfn.debuff["turns"] = turns
        atk.debuff["cd"] = D["taunt"][2]


def _announce_combo(atk, bonus_dmg, bonus_acc):
    if (bonus_dmg, bonus_acc) == C[("uppercut", "block", "counter")]:
        print(atk.name, "unleashes a \033[1m\033[31mDEADLY COMBO!!\033[0m")
        atk.stats["combos"] += 1
    elif bonus_dmg > 0 or bonus_acc > 0:
        print(atk.name, "unleashes a \033[1m\033[32mCOMBO!\033[0m")
        atk.stats["combos"] += 1


def _f_and_stats(atk, dfn, move, dfn_move, start_stm, bonus_acc):
    neg_dmg, neg_acc = fatigue(start_stm)
    base_acc = atk.M.get(move, (0, 0, 0))[1]
    bonus_acc -= base_acc * (neg_acc / 100.0)

    if start_stm <= 20:
        print(atk.name, "is \033[31mEXTREMELY TIRED....\033[0m")
    elif start_stm <= 40:
        print(atk.name, "is getting \033[33mtired....\033[0m")

    if atk.feint["active"]:
        if dfn_move in ("block", "counter"):
            print(atk.name, "tricks", dfn.name)
            bonus_acc += 15
        else:
            print("But", dfn.name, "didnt get tricked...")
        atk.feint["active"] = False

    if atk.debuff["active"]:
        bonus_acc -= base_acc * (D["taunt"][0] / 100)
        print(atk.name, "has been \033[30mTaunted!\033[0m")
    return bonus_acc, neg_dmg


def _apply_defense(atk, dfn, move, dfn_move, dfn_stm, r_dmg, has_bonus):
    if move == "counter":
        if not has_bonus:
            print(atk.name, "\033[1m\033[31mCOUNTERED!\033[0m")
        if dfn_move == "block":
            print("Defense Was Rendered \033[31mUSELESS!\033[0m")
        return r_dmg

    if dfn_move == "block" and dfn_stm >= stamina("block", dfn.S):
        f_dmg = block(r_dmg, move)
        if f_dmg < r_dmg:
            print("\033[32mBlocked.\033[0m Reduced the damage")
            dfn.stats["blocks"] += 1
            if dfn.counter["cd"] == 0:
                dfn.counter["rdy"] = True
                dfn.counter["cd"] = 1
            else:
                dfn.counter["cd"] -= 1
        else:
            print("\033[31mBlock Failed.\033[0m Received Full damage")
        return f_dmg

    if dfn_move == "block":
        print("Tried to block but no stamina")
    return r_dmg