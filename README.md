# Boxing CLI

### UPDATE 6.3 IS HERE!!!

A terminal-based, turn-based boxing game — Player vs. Computer, fought to a knockout across a Match of Fights. Pick a fighter class, choose your moves each round, and manage stamina, combos, and special tactics (feints, taunts, counters) to take down the AI.

> [!IMPORTANT]
> **The per-version folder layout changes at 7.x.**
> From **version 7.0 onwards, individual releases will no longer be uploaded as folders** under `Releases/`. The code for each 7.x version is published in a new folder named **`Boxing Version 7.x`** — `Boxing Version 7.0`, `Boxing Version 7.1`, and so on — and the `.exe` for every version is still uploaded to the [Releases](../../releases) page as usual. See [Release policy](#release-policy) for details.

## What's New in 6.3

- **A real Settings menu** — four groups (General, Match Rules, Saves, Debug) with twenty options. Values can be toggles, pick-from-a-list choices, or free numbers.
- **Coloured settings values** — ON is green, OFF is red, list values are yellow. The selected row is highlighted with colour instead of a background band, so the colours stay readable.
- **Match Rules** — choose your Match length (best of 1, 3, 5 or 7) and set a Round limit (10, 15 or 20 rounds), with a judges' decision when the limit is reached.
- **Text speed** — Instant, Fast, Normal or Slow. Instant removes every pause between attacks.
- **Display options** — turn colours off entirely, switch the HP / Stamina / Combo Cooldown bars between `■□` and `#-`, and trim the combat log down to results only.
- **Remember your picks** — your last class and last difficulty are offered back to you at the prompt.
- **Debug mode moved into Settings** — no more questions asked at the start of every match.
- **Round Limit decisions** are recorded as their own stat, separately from knockouts.

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
- **Configurable Match structure** — Match → Fight → Round. Each Fight is fought to a KO; the first to enough Fight wins takes the Match. A drawn Fight doesn't end the match undecided — Fights keep going until someone wins.
- **Settings** — twenty options across four groups (see [Settings](#settings)). Settings are saved between sessions.
- **Debug mode** — force specific moves, dump internal round-by-round state, disable stamina costs, seed the RNG for reproducible testing, and force the Computer's class. Games played in debug mode are not saved unless you turn that on.
- **End-of-match stats** — hits, misses, crits, blocks, combos, total damage dealt, and fights won, for both fighters.
- **Main menu** — arrow-key menu with New Game, Settings, Load Save, Delete Save, and Exit. If your terminal doesn't support `curses`, it falls back to a simple numbered text menu automatically.
- **Multiple save slots** — create as many named saves as you like (a-z, 0-9, `_` or `-`, up to 20 characters). Load one to continue, or delete one (with a confirmation prompt). Each save keeps its own stats.
- **Persistent stats** — every completed Match is recorded to your save: lifetime hits, misses, crits, blocks, combos, damage dealt and taken, rounds fought, Fight and Match records, win rate, and win streaks (current and best). Debug matches are never recorded unless you allow it.
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
Go to [Releases](../../releases), download `6.3.exe` from the latest release, and run it. Nothing else needs to be installed.

#### From source (any OS):

```bash
git clone https://github.com/robolivice/Boxing-CLI.git
cd Boxing-CLI/Releases/"Release 6"/"Release 6.3"
```

Windows users should also install the `curses` module for the menu and loading screen:

```bash
pip install -r requirements.txt
```

### Running the game

**Windows exe:** double-click `6.3.exe`. If the window closes before you can read an error, open a terminal in the folder where you saved it and run:

```bash
6.3.exe
```

**From source:** from inside the `Release 6.3` folder (the one that contains the `boxing` folder), run:

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
| From source (`python -m boxing`) | Inside the `Release 6.3` folder (`saves/` and `settings.json`) |
| `.exe` or `pip install .` | Windows: `%APPDATA%\boxing-cli` — other systems: `~/.Boxing-CLI` |
| Custom | Set the `BOXING_HOME` environment variable to any folder |

Each release folder keeps its own saves when run from source. To carry your progress to a new release, copy the `saves/` folder and `settings.json` across, or point `BOXING_HOME` at one shared folder.

## Settings

Open **Settings** from the main menu. The menu is split into four groups. Enter changes the
highlighted option, and on options with more than one value the Left and Right arrows step
through the values straight away.

### General

| Setting | Values | What it does |
|---|---|---|
| Clear Previous Round | ON / OFF | **ON:** the screen is cleared at the start of each new round, so only the current round is shown, and you press Enter after each round to read the results. **OFF:** the full log stays on screen (default). |
| Loading Screen | ON / OFF | **ON:** the animated boxer intro plays at startup. **OFF:** it is skipped. |
| Colors | ON / OFF | **ON:** the game uses colours. **OFF:** plain text only. |
| ASCII Bars | ON / OFF | **ON:** the HP, Stamina and Combo Cooldown bars use `■` and `□`. **OFF:** they use `#` and `-`. The loading screen bar always uses `█` and `░`. |
| Detailed Combat Log | ON / OFF | **ON:** every attack is narrated. **OFF:** only the results are shown. |
| Sound | (Soon) | Reserved for a future release. |
| Text Speed | Instant / Fast / Normal / Slow | Sets how long the game pauses between attacks. Instant removes the pauses completely. |

### Match Rules

| Setting | Values | What it does |
|---|---|---|
| Match Length | Best of 1 / 3 / 5 / 7 | How many Fights make up a Match. |
| Round Limit | No Limit / 10 / 15 / 20 | How many Rounds a Fight can last. When the limit is reached the judges award the Fight to the fighter who dealt more damage, then to whoever has more HP left. A dead heat is a draw. |
| Remember Last Class | ON / OFF | **ON:** the class you picked last time is offered as the default at class selection. |
| Remember Last Difficulty | ON / OFF | **ON:** the difficulty you picked last time is offered as the default. |
| Career Mode | (Soon) | Reserved for a future release. |

### Saves

| Setting | Values | What it does |
|---|---|---|
| Confirm Overwrite | ON / OFF | **ON:** asks before replacing an existing save. |
| Record Debug Matches | ON / OFF | **ON:** matches played in Debug Mode are counted in your stats. |

### Debug

| Setting | Values | What it does |
|---|---|---|
| Debug Mode | ON / OFF | Master switch for every debug option below. |
| Force Player Move | ON / OFF | You type the player's move instead of picking it from the menu. |
| Force AI Move | ON / OFF | You type the Computer's move. |
| Show Internal State | ON / OFF | Prints the internal state at the start of every Round. |
| Disable Stamina Cost | ON / OFF | Moves cost no Stamina. |
| Force AI Class | Random / Berserker / Assassin / Juggernaut / Duelist / Reaper | Fixes the class the Computer uses. |
| RNG Seed | 0 = random, or any number | Seeds the RNG so a match can be repeated exactly. The seed is used for one match only and then resets to random. |

Settings apply to every save and are stored in `settings.json`.

## Repository Layout

```
Boxing-CLI/
├── README.md
├── CHANGELOG.md
└── Releases/
    └── Release 6/
        └── Release 6.3/   (6.3 — the last folder in the old per-version layout)
```

Each release folder is a complete, self-contained copy of the game for that version. Older releases are kept as they were published.

| Release | Notes |
|---|---|
| **6.3** (last in the old layout) | Full settings menu, match rules, text speed, debug in settings |
| 6.2 | Settings menu, loading animation, package restructure, installable |
| 6.1 and earlier | See the [Releases](../../releases) page |

From **7.x onwards** the code for each version is published in a top-level folder named
`Boxing Version 7.x` instead of under `Releases/`. See [Release policy](#release-policy).

### Release policy

**`Release 6.3` is the last folder published in the old per-version layout.**

From **7.x onwards, individual releases will no longer be uploaded as folders** under `Releases/`. Concretely:

- **The code still gets published.** Each 7.x version lives in its own folder named **`Boxing Version 7.x`** — `Boxing Version 7.0`, `Boxing Version 7.1`, and so on — and is kept updated there as the version moves forward.
- **The old layout stops.** There is no `Releases/Release 7/Release 7.0` and nothing like it after that — `Releases/` stops growing after `Release 6.3`.
- **`.exe` files are still published.** Every version, 7.x onwards included, gets a `.exe` on the [Releases](../../releases) page. Downloading and running the executable is how you play.

If a newer version is ever published in a different way, it will be announced on the
[repository page](https://github.com/robolivice/Boxing-CLI).

## Project Structure (Release 6.3)

Inside `Release 6.3/boxing/`:

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
| `ui/colors.py` | ANSI colour table, class colours, and the shared style names used by the menus. |
| `ui/bars.py` | HP, stamina, combo-cooldown and status bars, and the end-of-match stats display. |
| `ui/prompts.py` | The move menu and the class list. |
| `ui/screen.py` | Banners, round/fight headers, screen clearing, and the debug state print. |
| `ui/loadingsc.py` | The animated boxer loading screen. |
| `ui/menu.py` | Arrow-key `curses` menu with a numbered text fallback, and coloured option values. |
| `flow/startup.py` | Class and difficulty selection, including your remembered picks. |
| `flow/session.py` | New Game, Load Save, and Delete Save handling. |
| `flow/match.py` | The Match loop, class pick, and saving results. |
| `flow/fight.py` | A single Fight and each Round inside it, including the Round Limit decision. |
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
- [x] More settings options — twenty of them, across four groups
- [x] Configurable match length and round limit
- [ ] Career/ladder mode (sequential opponents, per-boxer AI, boss fight)
- [ ] Sound
- [ ] Local (hot-seat) multiplayer
- [ ] Online LAN multiplayer

## License

No license specified yet.
