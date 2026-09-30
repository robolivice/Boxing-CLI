import random, time
from ..core import data
from ..core.fighter import Fighter
from ..storage import saves
from .. import ui as UI
from . import fight, startup

def _ai_class(dbg, opts):
    if dbg and opts["ai_class"]:
        while True:
            c = input("Debug - AI Class: ").lower().strip()
            if c in data.classes:
                return c
            print("Error. Not a Valid Class")
            time.sleep(0.5)
            UI.erase_l(2)
    return random.choice(list(data.classes))

def play_mtc(p_class, c_class, dif, mode_c, dbg, opts, best_of=3):
    player = Fighter("Player", p_class)
    comp = Fighter("Computer", c_class)
    need = best_of // 2 + 1
    tally = {"moves": {}, "rounds": 0, "draws": 0, "won_rounds": [], "max_hit": 0.0}
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

        outcome = fight.play_fight(player, comp, dif, mode_c, fight_no, dbg, opts, tally)
        if outcome == "draw":
            print("It's a \033[1m\033[33mDraw game!\033[0m")
        elif outcome == "computer":
            c_won += 1
            print("\033[1m\033[31mK.O.!\033[0m The Computer wins this Fight.", f"({c_won}/{need})")
        else:
            p_won += 1
            print("\033[1m\033[31mK.O.!\033[0m You win this Fight!", f"({p_won}/{need})")
        time.sleep(2)
        print()
        fight_no += 1

    if p_won >= need:
        print("\033[1m\033[32mPlayer\033[0m won the Match!!",
              UI.color["bold"] + UI.color["green"] + f"({p_won}/{need})" + UI.color["reset"])
    else:
        print("\033[1m\033[31mComputer\033[0m won the Match!!",
              UI.color["bold"] + UI.color["red"] + f"({c_won}/{need})" + UI.color["reset"])
    return p_won >= need, player, comp, tally

def p_session():
    """Debug prompt -> class -> difficulty -> Match -> save, repeated until the player stops."""
    while True:
        dbg = startup.debug_m()
        opts = startup.debug_opts() if dbg else {}
        if dbg and opts["seed"] is not None:
            random.seed(opts["seed"])

        p_class = startup.class_s()
        if p_class is None:
            return
        c_class = _ai_class(dbg, opts)
        dif, mode_c = startup.difficulty()

        won, player, comp, t = play_mtc(p_class, c_class, dif, mode_c, dbg, opts)
        if not dbg:
            saves.rec_mtc(p_class, c_class, dif, won, player.stats, comp.stats,
                          t["moves"], t["rounds"], t["draws"], t["won_rounds"], t["max_hit"])
            saves.save()
        UI.m_stats(player.stats, comp.stats)

        if input("Do you wanna play again? \033[1m\033[32m(y/n)\033[0m: ").lower() != "y":
            return