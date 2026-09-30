import time
from ..core import ai, combat
from .. import ui as UI
from ..storage import settings

def _pad(value):
    if value < 10:
        return 29
    if value < 100:
        return 28
    return 27

def _bars(player, comp, end):
    UI.stat_bar(player.cls, comp.cls, player.stm, player.hp, comp.stm, comp.hp,
                _pad(player.hp), _pad(player.stm), player.combo_cd, comp.combo_cd, end=end,
                p_feint=player.feint["active"], c_feint=comp.feint["active"],
                p_debuff=player.debuff["active"], c_debuff=comp.debuff["active"])

def _plr_move(player, counter_rdy, dbg, opts, tally):
    if dbg and opts["force_player"]:
        return input("DEBUG - Player Move: ").lower().strip()
    move = UI.p_move(player.M, player.S, player.feint["cd"] == 0,
                     player.debuff["cd"] == 0, counter_rdy)
    tally["moves"][move] = tally["moves"].get(move, 0) + 1
    return move

def _comp_move(player, comp, dif, counter_rdy, dbg, opts):
    if dbg and opts["force_ai"]:
        return input("DEBUG - AI move: ").lower().strip()
    return ai.comp_AI(dif, comp.hp, comp.stm, player.hp, player.stm, counter_rdy,
                      comp.last2, player.last2, comp.feint["cd"], comp.debuff["cd"],
                      c_S=comp.S, combo_cd=comp.combo_cd)

def _play_rnd(player, comp, dif, rnd, fight_no , dbg, opts, god, tally):
    if rnd > 1 and settings.get("clear_log"):
        UI.c_sc()
        UI.f_banner(fight_no)
    UI.rnd_banner(rnd)
    time.sleep(0.5)
    _bars(player, comp, True)
    if dbg and opts["show_state"]:
        UI.debug_print(player.feint, comp.feint, player.debuff, comp.debuff,
                       player.counter, comp.counter, player.combo_cd, comp.combo_cd,
                       player.his, comp.his, comp.last2, player.last2)

    player.tick()
    comp.tick(c_last2=True)
    p_ctr, c_ctr = player.counter["rdy"], comp.counter["rdy"]
    p_m = _plr_move(player, p_ctr, dbg, opts, tally)
    c_m = _comp_move(player, comp, dif, c_ctr, dbg, opts)
    player.rem(p_m)
    comp.rem(c_m)
    p_combo = player.combo()
    c_combo = comp.combo()

    p_snap, c_snap = player.stm, comp.stm
    hp_before = comp.hp
    combat.r_turn(player, comp, p_m, c_m, c_snap, True, p_combo, god)
    combat.r_turn(comp, player, c_m, p_m, p_snap, False, c_combo, god)
    tally["max_hit"] = max(tally["max_hit"], hp_before - comp.hp)

    if p_ctr and p_m != "counter":
        player.counter["rdy"] = False
    if c_ctr and c_m != "counter":
        comp.counter["rdy"] = False

    if rnd % 3 == 0:
        player.stm = min(100.0, player.stm + 10.0)
        comp.stm = min(100.0, comp.stm + 10.0)

    time.sleep(0.5)
    _bars(player, comp, False)
    if settings.get("clear_log") and player.hp > 0 and comp.hp > 0:
        input("Press Enter for next round....")

def play_fight(player, comp, dif, mode_c, fight_no, dbg, opts, tally):
    """Returns 'player', 'computer' or 'draw'."""
    god = bool(dbg and opts["god_stamina"])
    if fight_no == 1:
        print("Difficulty: ", mode_c)
        time.sleep(0.5)
    rnd = 1
    while player.hp > 0 and comp.hp > 0:
        _play_rnd(player, comp, dif, rnd, fight_no, dbg, opts, god, tally)
        rnd += 1

    rounds = rnd - 1
    tally["rounds"] += rounds
    if player.hp <= 0 and comp.hp <= 0:
        tally["draws"] += 1
        return "draw"
    if comp.hp <= 0:
        tally["won_rounds"].append(rounds)
        player.stats["f_won"] += 1
        return "player"
    comp.stats["f_won"] += 1
    return "computer"