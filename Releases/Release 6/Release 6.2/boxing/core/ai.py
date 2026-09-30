import random
from . import data, combat

BASE = ["jab", "kick", "uppercut", "block"]

def comp_AI(mode, c_hp, c_stm, plr_hp, plr_stm, counter_a=False, his=None, p_his=None,
            feint_cd=0, taunt_cd=0, c_S=None, combo_cd=0):
    if c_S is not None:
        s_tbl = c_S 
    else:
        s_tbl = data.S

    if counter_a and c_stm >= s_tbl["counter"]:
        return "counter"
    
    feint_a = False
    if feint_cd == 0 and c_stm >= s_tbl["feint"]:
        feint_a = True

    taunt_a = False
    if taunt_cd == 0 and c_stm >= s_tbl["taunt"]:
        taunt_a = True

    if mode == "Easy":
        return _easy(feint_a, taunt_a)
    if mode == "Medium":
        return _medium(c_hp, c_stm, plr_hp, plr_stm, s_tbl, feint_a, taunt_a)
    return _hard(c_hp, c_stm, plr_hp, plr_stm, s_tbl, feint_a, taunt_a, counter_a, his, p_his, combo_cd)


def _pick(moves, weights, c_stm, s_tbl):
    ok = [(m, w) for m, w in zip(moves, weights) if c_stm >= s_tbl[m]]
    return random.choices([m for m, _ in ok], weights=[w for _, w in ok])[0]


def _easy(feint_a, taunt_a):
    moves = list(BASE)
    if feint_a:
        moves.append("feint")
    if taunt_a:
        moves.append("taunt")
    return random.choice(moves)


def _medium(c_hp, c_stm, plr_hp, plr_stm, s_tbl, feint_a, taunt_a):
    up, blk = s_tbl["uppercut"], s_tbl["block"]
    w = [10, 10, 10, 10]
    if c_stm <= up:
        w = [20, 15, 2, 3]
    if plr_stm < blk:
        if c_stm >= up + 5:
            w = [5, 10, 20, 2]
        elif c_stm > up:
            w = [20, 10, 5, 2]
        else:
            w = [20, 15, 2, 3]
    moves = list(BASE)
    if feint_a:
        moves.append("feint")
        w.append(10 if plr_stm >= 40 else 5)
    if taunt_a:
        moves.append("taunt")
        w.append(10 if c_hp >= plr_hp else 5)
    return _pick(moves, w, c_stm, s_tbl)


def _hard(c_hp, c_stm, plr_hp, plr_stm, s_tbl, feint_a, taunt_a, counter_a, his, p_his, combo_cd):
    up, kick, blk = s_tbl["uppercut"], s_tbl["kick"], s_tbl["block"]
    w = [10, 10, 10, 10]
    if plr_hp <= 25:
        if c_stm >= up + 5:
            w = [3, 10, 20, 2]
        elif c_stm >= kick:
            w = [20, 10, 3, 2]
        else:
            w = [1, 0, 0, 0]
    if c_hp <= 25:
        if c_stm >= blk:
            w = [5, 2, 1, 20]
        elif c_stm >= kick:
            w = [80, 20, 3, 4]
        else:
            w = [1, 0, 0, 0]

    moves = list(BASE)
    if feint_a:
        moves.append("feint")
        read = p_his is not None and len(p_his) > 0 and p_his[-1] in ("block", "counter")
        w.append(15 if read else 5)
    if taunt_a:
        moves.append("taunt")
        w.append(15 if plr_stm > 40 else 2)
    choice = _pick(moves, w, c_stm, s_tbl)

    if combo_cd == 0:
        candidates = list(BASE)
        if counter_a:
            candidates.append("counter")
        if feint_a:
            candidates.append("feint")
        if taunt_a:
            candidates.append("taunt")
        for m in candidates:
            if c_stm >= s_tbl[m] and combat.AiCombo(his, m) != (0, 0):
                return m
    return choice
