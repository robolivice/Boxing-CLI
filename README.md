# Boxing CLI

### UPDATE 6.2 IS HERE!!!

A terminal-based, turn-based boxing game — Player vs. Computer, fought to a knockout across a best-of-3 match. Pick a fighter class, choose your moves each round, and manage stamina, combos, and special tactics (feints, taunts, counters) to take down the AI.

## What's New in 6.2

- **Settings menu** — a new Settings entry on the main menu. The first option, **Clear Previous Round**, wipes the screen at the start of each round so only the current round is shown. Four more slots are reserved for future settings.
- **Animated loading screen** — a boxer ASCII animation plays at startup (skipped automatically if your terminal doesn't support `curses`).
- **Rebuilt code structure** — the game is now a proper Python package split into `core`, `ui`, `flow`, and `storage` modules, so it's easier to read, maintain, and extend.
- **Run it your way** — play the `.exe` on Windows, run it from source with `python -m boxing`, or install it as a `boxing` command with `pip install .`.
- **Fixes** — Ctrl+C now exits cleanly at the difficulty prompt, and startup no longer fails if the loading animation can't run.

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
- **Settings** — toggle **Clear Previous Round** to keep the screen uncluttered (see [Settings](#settings)). Settings are saved between sessions.
- **Debug mode** — force specific moves, dump internal round-by-round state, disable stamina costs, seed the RNG for reproducible testing, and force the Computer's class. Games played in debug mode are not saved.
- **End-of-match stats** — hits, misses, crits, blocks, combos, total damage dealt, and fights won, for both fighters.
- **Main menu** — arrow-key menu with New Game, Settings, Load Save, Delete Save, and Exit. If your terminal doesn't support `curses`, it falls back to a simple numbered text menu automatically.
- **Multiple save slots** — create as many named saves as you like (a-z, 0-9, `_` or `-`, up to 20 characters). Load one to continue, or delete one (with a confirmation prompt). Each save keeps its own stats.
- **Persistent stats** — every completed Match is recorded to your save: lifetime hits, misses, crits, blocks, combos, damage dealt and taken, rounds fought, Fight and Match records, win rate, and win streaks (current and best). Debug matches are never recorded.
- **Detailed records** — your save also tracks results per class you play, per class you face, and per difficulty, plus how often you use each move and personal bests (biggest hit, most damage in a Match, quickest KO, longest Match).
- **Save summary** — loading a save shows your Matches played, win rate, streak, and most used class and move before you start.
- **Safe saving** — saves are written atomically so a crash mid-write can't wreck them. A corrupted save is backed up as `.bak` and you're told about it. An older single-file `player_stats.json` is migrated into the new save system automatically.
- **Quit to menu** — press `Q` at class selection to go back to the main menu. Ctrl+C exits the game cleanly.

## Getting Started

### Prerequisites

- Python 3.9 or newer (only needed to run from source)
- `windows-curses` (Windows only, only needed to run from source; it's included in `requirements.txt`)

### Installation

#### Windows (easiest):
Go to [Releases](../../releases), download `6.2.exe` from the latest release, and run it. Nothing else needs to be installed.

#### From source (any OS):

```bash
git clone https://github.com/robolivice/Boxing-CLI.git
cd Boxing-CLI/Releases/"Release 6"/"Release 6.2"
```

Windows users should also install the `curses` module for the menu and loading screen:

```bash
pip install -r requirements.txt
```

### Running the game

**Windows exe:** double-click `6.2.exe`. If the window closes before you can read an error, open a terminal in the folder where you saved it and run:

```bash
6.2.exe
```

**From source:** from inside the `Release 6.2` folder (the one that contains the `boxing` folder), run:

```bash
python -m boxing
```

**As an installed command (optional):** from the same folder, run `pip install .`, then start the game from anywhere with:

```bash
boxing
```

### Where your data is stored

| How you run it | Saves and settings location |
|---|---|
| From source (`python -m boxing`) | Inside the `Release 6.2` folder (`saves/` and `settings.json`) |
| `.exe` or `pip install .` | Windows: `%APPDATA%\boxing-cli` — other systems: `~/.Boxing-CLI` |
| Custom | Set the `BOXING_HOME` environment variable to any folder |

Each release folder keeps its own saves when run from source. To carry your progress to a new release, copy the `saves/` folder and `settings.json` across, or point `BOXING_HOME` at one shared folder.

## Settings

Open **Settings** from the main menu and press Enter on an option to toggle it.

| Setting | What it does |
|---|---|
| Clear Previous Round | **ON:** the screen is cleared at the start of each new round, so only the current round is shown. After each round you'll be asked to press Enter, giving you time to read the results first. **OFF:** the full log stays on screen (default). |
| Empty slots (x4) | Reserved for future settings. |

Settings apply to every save and are stored in `settings.json`.

## Repository Layout

```
Boxing-CLI/
├── README.md
├── CHANGELOG.md
└── Releases/
    └── Release 6/
        └── Release 6.2/   (current release: the full, runnable project)
```

Each release folder is a complete, self-contained copy of the game for that version. Older releases are kept as they were published.

| Release | Notes |
|---|---|
| **6.2** (latest) | Settings menu, loading animation, package restructure, installable |
| 6.1 and earlier | See the [Releases](../../releases) page |

## Project Structure (Release 6.2)

Inside `Release 6.2/boxing/`:

| File | Responsibility |
|---|---|
| `__main__.py` | Lets you start the game with `python -m boxing`. |
| `main.py` | Entry point: loading screen, main menu, save selection, then hands off to a game session. |
| `paths.py` | Works out where assets and save data live (source, installed, or exe). |
| `assets/boxer.txt` | ASCII art used by the loading animation. |
| `core/data.py` | Move, combo, debuff, and fighter-class data tables. |
| `core/combat.py` | Per-attack resolver (`r_turn`) and its helpers: fatigue, feints, taunts, blocks, counters. |
| `core/fighter.py` | The `Fighter` class: HP, stamina, cooldowns, and move history for the player and the computer. |
| `core/ai.py` | The computer AI (`comp_AI`) with Easy, Medium, and Hard behaviour. |
| `ui/colors.py` | ANSI colour table and class colours. |
| `ui/bars.py` | HP, stamina, combo-cooldown and status bars, and the end-of-match stats display. |
| `ui/prompts.py` | The move menu and the class list. |
| `ui/screen.py` | Banners, round/fight headers, screen clearing, and the debug state print. |
| `ui/loadingsc.py` | The animated boxer loading screen. |
| `ui/menu.py` | Arrow-key `curses` menu with a numbered text fallback. |
| `flow/startup.py` | Debug-mode prompts and class and difficulty selection. |
| `flow/session.py` | New Game, Load Save, and Delete Save handling. |
| `flow/match.py` | The Match loop (best-of-3), class pick, and saving results. |
| `flow/fight.py` | A single Fight and each Round inside it. |
| `flow/options.py` | The Settings menu. |
| `storage/saves.py` | JSON persistence: one file per save, stats and streak recording, atomic writes, corrupt-save backup, legacy migration. |
| `storage/settings.py` | Loading and saving the Settings options. |

## How to Play

Each round, you'll be shown a move menu with the damage, accuracy, and stamina cost of each available option (Feint, Taunt, and Counter only appear when they're actually available to you). [ASCII Loading Screen is Skipable with q key] .Enter the corresponding move ID to act. HP, stamina, combo cooldowns, and any active feint/taunt status are shown before every round. 

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
- [x] Options Menu (Settings) — first option added, more slots reserved
- [x] Module splitting and packaging
- [ ] More settings options
- [ ] Career/ladder mode (sequential opponents, per-boxer AI, boss fight)
- [ ] Sound
- [ ] Local (hot-seat) multiplayer
- [ ] Online LAN multiplayer

## License

No license specified yet.