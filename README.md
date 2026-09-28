# Boxing CLI

### UPDATE 6 IS HERE!!!

A terminal-based, turn-based boxing game — Player vs. Computer, fought to a knockout across a best-of-3 match. Pick a fighter class, choose your moves each round, and manage stamina, combos, and special tactics (feints, taunts, counters) to take down the AI.

## Features

- **Turn-based combat** — Jab, Kick, and Uppercut, each with its own damage, accuracy, and stamina cost trade-off, plus a Block option with move-dependent mitigation.
- **Five fighter classes** — Berserker, Assassin, Juggernaut, Duelist, and Reaper, each with its own damage / accuracy / stamina / HP / crit multipliers. Pick yours; the computer's is randomized each match.
- **Special moves:**
  - **Feint** — bait the opponent; pays off with a bonus-accuracy follow-up if they Block or Counter in response.
  - **Taunt** — apply an accuracy debuff that lingers over the opponent's next couple of attacks.
  - **Counter** — earned by landing successful blocks; hits hard and can't be blocked, but only lasts for the round it's granted in.
- **Combo system** — specific move sequences (e.g. Jab → Jab → Uppercut) unlock bonus damage and accuracy.
- **Fatigue system** — running low on stamina costs you accuracy and damage.
- **Three difficulty levels** — Easy, Medium, and Hard AI, each with progressively smarter move weighting, combo lookahead, and awareness of your patterns.
- **Best-of-3 Match structure** — Match → Fight → Round. Each Fight is fought to a KO; first to 2 Fight wins takes the Match. A drawn Fight doesn't end the match undecided — Fights keep going until someone wins.
- **Debug mode** — force specific moves, dump internal round-by-round state, disable stamina costs, and seed the RNG for reproducible testing, force Computer's class. Any games with debug mode are not saved.
- **End-of-match stats** — hits, misses, crits, blocks, combos, total damage dealt, and fights won, for both fighters.
- **Main menu** — arrow-key menu with New Game, Load Save, Delete Save, and Exit. If your terminal doesn't support `curses`, it falls back to a simple numbered text menu automatically.
- **Multiple save slots** — create as many named saves as you like (a-z, 0-9, `_` or `-`, up to 20 characters). Load one to continue, or delete one (with a confirmation prompt). Each save keeps its own stats.
- **Persistent stats** — every completed Match is recorded to your save: lifetime hits, misses, crits, blocks, combos, damage dealt and taken, rounds fought, Fight and Match records, win rate, and win streaks (current and best). Debug matches are never recorded.
- **Detailed records** — your save also tracks results per class you play, per class you face, and per difficulty, plus how often you use each move and personal bests (biggest hit, most damage in a Match, quickest KO, longest Match).
- **Save summary** — loading a save shows your Matches played, win rate, streak, and most used class and move before you start.
- **Safe saving** — saves are written atomically so a crash mid-write can't wreck them. A corrupted save is backed up as `.bak` and you're told about it. An older single-file `player_stats.json` is migrated into the new save system automatically.
- **Quit to menu** — press `Q` at class selection to go back to the main menu. Ctrl+C exits the game cleanly.

## Getting Started

### Prerequisites

- Python 3.x
- curses 2.4.2 (For Windows Only)

### Installation

```bash
git clone https://github.com/robolivice/Boxing-CLI.git
cd Boxing-CLI
```

Recommended Installation of ```curses``` module for the Menu for Windows Users for Boxing-CLI Version 6.x and up.

```bash
pip install -r requirements.txt
```

### Running the game

```bash
python "6.1.py"
```

## Project Structure

| File | Responsibility |
|---|---|
| `6.1.py` | Main loop: the menu → save selection → Match/Fight/Round flow, Match/Fight/Round state, debug-mode setup, and class selection. |
| `combat.py` | Core mechanics: move/combo/debuff/class data tables and the per-attack resolver (`r_turn`). |
| `setup.py` | Debug-mode prompts, class and difficulty selection, and the computer AI (`comp_AI`). |
| `UI.py` | Title banner, player move menu, HP/stamina/combo-cooldown bar rendering, status effects, and end-of-match stats display. |
| `menu.py` | Arrow-key `curses` menu used for the main menu and the save picker, with a numbered text fallback when `curses` isn't available. |
| `saves.py` | JSON persistence: one file per save in `saves/`, stats and streak recording, atomic writes, corrupt-save backup, and legacy save migration. |

## How to Play

Each round, you'll be shown a move menu with the damage, accuracy, and stamina cost of each available option (Feint, Taunt, and Counter only appear when they're actually available to you). Enter the corresponding move ID to act. HP, stamina, combo cooldowns, and any active feint/taunt status are shown before every round.

## Fighter Classes

| Class | Damage | Accuracy | Stamina Use | HP | Crit Chance |
|---|---|---|---|---|---|
| Berserker | x1.25 | x0.90 | x1.10 | x1.00 | x1.20 |
| Assassin | x0.90 | x1.20 | x1.00 | x1.00 | x1.30 |
| Juggernaut | x1.00 | x1.00 | x0.75 | x1.20 | x0.80 |
| Duelist | x1.10 | x0.95 | x0.90 | x0.90 | x1.10 |
| Reaper | x1.50 | x0.80 | x1.30 | x0.75 | x1.50 |

## Roadmap

- [x] Best-of-3 Match structure (Match → Fight → Round)
- [x] Persistent stats/streak tracking (across sessions)
- [ ] Options Menu (Settings) and Module Splitting
- [ ] Career/ladder mode (sequential opponents, per-boxer AI, boss fight)
- [ ] Sound
- [ ] Local (hot-seat) multiplayer
- [ ] Online LAN multiplayer

## License

No license specified yet.
