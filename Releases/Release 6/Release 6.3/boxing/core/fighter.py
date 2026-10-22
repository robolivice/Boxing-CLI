from collections import deque
from . import data, combat

#Class Selection
def s_class(class_k):
    amp = data.classes.get(class_k)
    if amp is None:
        return dict(data.M), dict(data.S)
    new_M = {}
    for mv, (d,a,c) in data.M.items():
        new_d = d*amp["dmg"]
        new_a = a*amp["acc"]
        new_c = c*amp["crit"]
        new_M[mv] = (new_d, new_a, new_c)
    new_S = {}
    for mv, cost in data.S.items():
        new_S[mv] = cost*amp["stm"]

    return new_M, new_S


class Fighter:
    def __init__(self, name, cls):
        self.name = name
        self.cls = cls
        self.M, self.S = s_class(cls)
        self.max_hp = 100.0*data.classes[cls]["hp"]
        self.stats = {
            "hits": 0,
            "misses": 0,
            "crits":0,
            "blocks": 0,
            "combos": 0,
            "tdmg": 0,
            "f_won": 0
        }
        self.reset()

    def reset(self):
        self.hp = self.max_hp
        self.stm = 100.0
        self.counter = {"cd": 0, "rdy": False}
        self.feint = {"active": False, "cd": 0}
        self.debuff = {"active": False, "cd": 0, "turns": 0}
        self.his = deque(maxlen =3)
        self.last2 = []
        self.combo_cd = 0

    def tick(self, c_last2 = False):
        if self.combo_cd > 0:
            self.combo_cd -= 1
            self.his.clear()
            if c_last2:
                self.last2.clear()
        if self.feint["cd"] > 0:
            self.feint["cd"] -= 1
        if self.debuff["cd"] > 0:
            self.debuff["cd"] -= 1
        if self.debuff["turns"] > 0:
            self.debuff["turns"] -= 1
            if self.debuff["turns"] == 0:
                self.debuff["active"] = False

    def rem(self,move):
        self.his.append(move)
        self.last2.append(move)
        self.last2 = self.last2[-2:]

    def combo(self):
        dmg_b, acc_b = combat.combo(self.his)
        if (dmg_b, acc_b) != (0, 0):
            if self.combo_cd >0:
                dmg_b, acc_b = 0, 0
            else:
                self.combo_cd = 3
            self.his.clear()
        return dmg_b, acc_b