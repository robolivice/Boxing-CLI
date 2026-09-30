import time
from .colors import color

version = 6

def banner():
    t = "Boxing CLI V"+str(version)
    c_t1 = "="*20 + " " + t + " " + "="*20
    return c_t1

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

def erase_l(n):
    for _ in range(n):
        print("\033[A\r\033[K", end="")

def f_banner(n):
    b, p, r = color["bold"], color["purple"], color["reset"]
    print()
    print("\n" + b + p + "-" * 47 + r, "\033[1m\033[31mFight", str(n) + r, b + p + "-" * 47 + r)

def rnd_banner(n):
    b, p, r = color["bold"], color["purple"], color["reset"]
    print()
    print("\n" + " " * 15 + b + p + "-" * 32 + r, "\033[1m\033[36mRound", str(n) + "\033[0m", b + p + "-" * 32 + r + " " * 15)

def c_sc():
    print("\033[2J\033[H", end="", flush=True)