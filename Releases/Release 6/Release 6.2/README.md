# Boxing CLI — Release 6.2

A terminal-based, turn-based boxing game. Player vs. Computer, fought to a knockout across a best-of-3 match. Pick a fighter class, choose your moves each round, and manage stamina, combos, and special tactics (feints, taunts, counters) to beat the AI.

> This is the README for **Release 6.2** only. For the project overview and roadmap, see the [main README](../../../README.md). For the full version history, see the [CHANGELOG](../../../CHANGELOG.md).

## What's New in 6.2

- **Settings menu** — a new **Settings** entry on the main menu. The first option, **Clear Previous Round**, wipes the screen at the start of each round so only the current round is shown. Four more slots are reserved for future settings.
- **Animated loading screen** — a boxer ASCII animation plays at startup. Press `Q` to skip it. It is skipped automatically if your terminal doesn't support `curses`.
- **Rebuilt code structure** — the game is now a proper Python package (`boxing/`) split into `core`, `ui`, `flow`, and `storage` modules.
- **Run it your way** — play the `.exe` on Windows, run from source with `python -m boxing`, or install a `boxing` command with `pip install .`.
- **Fixes** — Ctrl+C exits cleanly at the difficulty prompt, and startup no longer fails if the loading animation can't run.

> **Upgrading from 6.1?** Gameplay and the save format are unchanged, but save **locations** moved. See [Moving your saves from 6.1](#moving-your-saves-from-61).

## Requirements

- **Windows exe:** nothing. Just download and run.
- **From source:** Python 3.9 or newer.
- **Windows, from source:** the `windows-curses` package (listed in `requirements.txt`) for the arrow-key menu and loading screen.

## Installation and Running

### Windows exe (easiest)

1. Go to [Releases](../../../../../releases) and download `6.2.exe`.
2. Double-click it.

If the window closes before you can read an error, open a terminal in the folder containing the file and run:

```bash
6.2.exe
```

### From source (any OS)

```bash
git clone https://github.com/robolivice/Boxing-CLI.git
cd Boxing-CLI/Releases/"Release 6"/"Release 6.2"
```

On Windows, install the curses module first:

```bash
pip install -r requirements.txt
```

Then, from inside the `Release 6.2` folder (the one that contains the `boxing` folder), run:

```bash
python -m boxing
```

### As an installed command (optional)

From the same folder:

```bash
pip install .
boxing
```

The `boxing` command then works from any directory.

## Where Your Data Is Stored

| How you run it | Saves and settings location |
|---|---|
| From source (`python -m boxing`) | Inside the `Release 6.2` folder (`saves/` and `settings.json`) |
| `.exe` or `pip install .` | Windows: `%APPDATA%\Boxing-CLI` — macOS / Linux: `~/.Boxing-CLI` |
| Custom | Set the `BOXING_HOME` environment variable to any folder |

`BOXING_HOME` always wins if it is set.

### Moving your saves from 6.1

6.1 kept saves in a `saves/` folder next to the script or exe, so a fresh 6.2 install won't see them automatically. Save files are identical between the two releases, so just copy them over:

1. Copy the `saves/` folder from your 6.1 folder into the location for how you run 6.2 (table above).
2. Copy `settings.json` too, if you have one (6.1 didn't use it, so you usually won't).

Alternatively, point `BOXING_HOME` at one shared folder and use it for every release. An older single-file `player_stats.json` is still migrated into the save system automatically.

## Settings

Choose **Settings** on the main menu and press Enter on an option to toggle it. Changes are saved immediately to `settings.json` and apply to every save.

| Setting | What it does |
|---|---|
| Clear Previous Round | **ON:** the screen is cleared at the start of each new round, and you press Enter after each round to read the results first. **OFF:** the full log stays on screen (default). |
| EMPTY (x4) | Reserved for future settings. Shown as `(Soon)` and can't be selected. |

## Controls

| Where | Keys |
|---|---|
| Main menu, Settings, save lists | Up / Down to move, Enter to select. Without `curses`, type the option's number instead. |
| Loading screen | `Q` to skip |
| Class selection | `B` Berserker, `A` Assassin, `J` Juggernaut, `D` Duelist, `R` Reaper, `Q` back to the main menu |
| Difficulty | `E` / `M` / `H` (or type the full word) |
| During a round | Enter the move ID shown in the move menu |
| Anywhere | `Ctrl+C` exits cleanly |

## How to Play

Each round you see a move menu listing the damage, accuracy, and stamina cost of every available option. Feint, Taunt, and Counter only appear when they're available to you. HP, stamina, combo cooldowns, and any active feint or taunt are shown before every round.

- **Jab / Kick / Uppercut** — each trades damage, accuracy, and stamina differently.
- **Block** — reduces incoming damage, with mitigation that depends on the move being blocked.
- **Counter** — earned by landing successful blocks; hits hard, can't be blocked, and is only available for the round right after it's granted.
- **Feint** — bait the opponent; you get a bonus-accuracy follow-up if they Block or Counter.
- **Taunt** — applies an accuracy debuff for the opponent's next couple of attacks.
- **Combos** — specific sequences (for example Jab → Jab → Uppercut) unlock bonus damage and accuracy.
- **Fatigue** — low stamina costs you accuracy and damage.

**Match structure:** Match → Fight → Round. Each Fight runs to a KO, and the first to win 2 Fights takes the Match. A drawn Fight doesn't count for either side; Fights continue until someone wins.

### Fighter classes

| Class | Damage | Accuracy | Stamina Use | HP | Crit Chance |
|---|---|---|---|---|---|
| Berserker | x1.25 | x0.90 | x1.10 | x1.00 | x1.20 |
| Assassin | x0.90 | x1.20 | x1.00 | x1.00 | x1.30 |
| Juggernaut | x1.00 | x1.00 | x0.75 | x1.20 | x0.80 |
| Duelist | x1.10 | x0.95 | x0.90 | x0.90 | x1.10 |
| Reaper | x1.50 | x0.80 | x1.30 | x0.75 | x1.50 |

The computer's class is random each match. Difficulty (Easy, Medium, Hard) controls how smart the AI's move choices are.

## Saves, Stats, and Debug Mode

- **Multiple named saves** (a-z, 0-9, `_` or `-`, up to 20 characters), each with its own stats. Loading a save shows a summary before you start.
- **Persistent stats** are recorded after every completed Match: hits, misses, crits, blocks, combos, damage dealt and taken, Fight and Match records, win rate, streaks, per-class and per-difficulty results, move usage, and personal bests.
- **Safe saving:** files are written atomically. A corrupted save is backed up as `.bak` and you're told about it.
- **Debug mode** (prompted at the start of every match): force player or AI moves, print internal state each round, disable stamina costs, seed the RNG, and force the computer's class. **Debug matches are never saved or recorded.**

## Project Structure

```
Release 6.2/
├── README.md
├── pyproject.toml        Packaging metadata (pip install .)
├── requirements.txt      windows-curses (Windows only)
├── run_boxing.py         Entry script used to build the exe
├── 6.2.spec              PyInstaller build config
├── icon.ico
├── boxing/
│   ├── __main__.py       python -m boxing
│   ├── main.py           Loading screen, main menu, session hand-off
│   ├── paths.py          Where assets and save data live
│   ├── assets/boxer.txt  ASCII art for the loading animation
│   ├── core/             data.py, combat.py, fighter.py, ai.py
│   ├── ui/               colors.py, bars.py, prompts.py, screen.py, loadingsc.py, menu.py
│   ├── flow/             startup.py, session.py, match.py, fight.py, options.py
│   └── storage/          saves.py, settings.py
└── dist/6.2.exe          Built executable
```

| Package | Responsibility |
|---|---|
| `core` | Move, combo, debuff and class data; the per-attack resolver; the `Fighter` class; the Easy/Medium/Hard AI. |
| `ui` | ANSI colours, HP/stamina/status bars, end-of-match stats, move menu, banners, the `curses` menu and loading animation. |
| `flow` | Class and difficulty selection, New/Load/Delete Save handling, the Match loop, a single Fight and its Rounds, the Settings menu. |
| `storage` | JSON persistence for saves (atomic writes, corrupt-save backup, legacy migration) and for settings. |

## Building the Exe

```bash
pip install pyinstaller windows-curses
pyinstaller 6.2.spec
```

The executable is written to `dist/6.2.exe`. The spec bundles `boxing/assets` and uses `icon.ico`.

## Troubleshooting

| Problem | Fix |
|---|---|
| Menu shows numbers instead of arrow-key navigation | Your terminal has no `curses` support. On Windows run `pip install windows-curses` (source only); otherwise type the number and press Enter. |
| No loading animation | Expected without `curses`, or if you pressed `Q`. The game continues normally. |
| Colours or bars look garbled | Use a terminal with ANSI colour support, such as Windows Terminal. |
| My 6.1 saves are missing | Saves moved locations. See [Moving your saves from 6.1](#moving-your-saves-from-61). |
| Exe window closes instantly on an error | Launch it from a terminal (`6.2.exe`) to read the message. |

## License

No license specified yet.
