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

c_color= {
    "berserker": "yellow", "assassin": "purple", "juggernaut": "red",
    "duelist": "blue", "reaper": "black",
}

def c_name(cls, pad=0):
    text = color["bold"] + color[c_color[cls]] + cls.capitalize() + color["reset"]
    if pad:
        text += " " * (pad - len(cls))
    return text