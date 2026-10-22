import random
from ..core import data
from ..core.fighter import Fighter
from ..storage import saves, settings
from .. import ui as UI
from . import fight, startup

def _ai_class(dbg, opts):
    if dbg:
        forced = opts.get("ai_class")
        if forced and forced != "random":
            return forced
    return random.choice(list(data.classes))

def _verdict(how):
    c = UI.color
    if how == "decision":
        return c["bold"] + c["cyan"] + "DECISION!" + c["reset"]
    return c["bold"] + c["red"] + "K.O.!" + c["reset"]

def play_mtc(p_class, c_class, dif, mode_c, dbg, opts, best_of=3):
    player = Fighter("Player", p_class)
    comp = Fighter("Computer", c_class)
    need = best_of // 2 + 1
    tally = {"moves": {}, "rounds": 0, "draws": 0, "won_rounds": [], "max_hit": 0.0, "decisions": 0}
    p_won = c_won = 0
    fight_no = 1

    while p_won < need and c_won < need:
        player.reset()
        comp.reset()
        UI.f_banner(fight_no)
        if not dbg:
            if fight_no == 1:
                UI.load_sc("static", 1.0)
            else:
                UI.load_sc("dynamic", 0.5)

        outcome, how = fight.play_fight(player, comp, dif, mode_c, fight_no, dbg, opts, tally)
        if outcome == "draw":
            print("It's a " + UI.color["bold"] + UI.color["yellow"] + "Draw game!" + UI.color["reset"])
        elif outcome == "computer":
            c_won += 1
            print(_verdict(how) + " The Computer wins this Fight.", "(" + str(c_won) + "/" + str(need) + ")")
        else:
            p_won += 1
            print(_verdict(how) + " You win this Fight!", "(" + str(p_won) + "/" + str(need) + ")")
        settings.pause(2)
        print()
        fight_no += 1

    if p_won >= need:
        print(UI.color["bold"] + UI.color["green"] + "Player" + UI.color["reset"] + " won the Match!!",
              UI.color["bold"] + UI.color["green"] + "(" + str(p_won) + "/" + str(need) + ")" + UI.color["reset"])
    else:
        print(UI.color["bold"] + UI.color["red"] + "Computer" + UI.color["reset"] + " won the Match!!",
              UI.color["bold"] + UI.color["red"] + "(" + str(c_won) + "/" + str(need) + ")" + UI.color["reset"])
    return p_won >= need, player, comp, tally

def p_session():
    """Class -> difficulty -> Match -> save, repeated until the player stops."""
    while True:
        dbg = settings.get("debug_mode")
        opts = settings.debug_opts() if dbg else {}
        if dbg and opts["seed"]:
            random.seed(opts["seed"])
            settings.set_val("dbg_seed", 0)

        last_class = settings.get("last_class") if settings.get("remember_class") else None
        last_diff = settings.get("last_diff") if settings.get("remember_diff") else None

        p_class = startup.class_s(last_class)
        if p_class is None:
            return
        settings.set_auto("last_class", p_class)
        c_class = _ai_class(dbg, opts)
        dif, mode_c = startup.difficulty(last_diff)
        settings.set_auto("last_diff", dif)

        best_of = settings.get("match_length")
        won, player, comp, t = play_mtc(p_class, c_class, dif, mode_c, dbg, opts, best_of=best_of)
        if not dbg or settings.get("record_debug"):
            saves.rec_mtc(p_class, c_class, dif, won, player.stats, comp.stats,
                          t["moves"], t["rounds"], t["draws"], t["won_rounds"], t["max_hit"],
                          t["decisions"])
            saves.save()
        UI.m_stats(player.stats, comp.stats)

        if input("Do you wanna play again? " + UI.color["bold"] + UI.color["green"] + "(y/n)" + UI.color["reset"] + ": ").lower() != "y":
            return
