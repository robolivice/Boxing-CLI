
# Move data: damage, accuracy, crit chance
M = {"jab": (5, 100, 10),"kick": (15, 65, 5),"uppercut": (25, 40, 3),"counter":(40,85,0),"feint": (0, 100, 0),"taunt": (0,100,0)}
# Block rates: success chance and mitigation percentage
B = {"jab": (90, 60.0),"kick": (75, 33.3),"uppercut": (50, 30.0), "counter": (0, 0)}
# Stamina Values
S = {"jab": 0, "kick": 10, "uppercut": 20, "block": 15, "counter": 30, "feint": 10, "taunt": 10}
# Combos: Extra damage then extra accuracy
C = {("jab", "jab", "uppercut"): (15, 20),
     ("jab","kick","uppercut"): (25, 35),
     ("uppercut","block","counter"):(40, 100)
     }
#Debuffs: Percentage acc reduction, Duration (in rounds), cd
D = {"taunt": (15, 2, 5)}
#Classes (all numbers in multipliers)
classes = {
    "berserker":  {"dmg": 1.25, "acc": 0.90, "stm": 1.10, "hp": 1.00, "crit": 1.20},
    "assassin":   {"dmg": 0.90, "acc": 1.20, "stm": 1.00, "hp": 1.00, "crit": 1.30},
    "juggernaut": {"dmg": 1.00, "acc": 1.00, "stm": 0.75, "hp": 1.20, "crit": 0.80},
    "duelist":    {"dmg": 1.10, "acc": 0.95, "stm": 0.90, "hp": 0.90, "crit": 1.10},
    "reaper":     {"dmg": 1.50, "acc": 0.80, "stm": 1.30, "hp": 0.75, "crit": 1.50}
}
