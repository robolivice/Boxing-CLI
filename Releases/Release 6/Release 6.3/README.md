# Boxing CLI — Release 6.3

A terminal-based, turn-based boxing game. Player vs. Computer, fought to a knockout across a
Match of Fights. Pick a fighter class, choose your moves each round, and manage stamina,
combos, and special tactics (feints, taunts, counters) to beat the AI.

This release is all about the **Settings menu** — it is now a full, typed, grouped menu with
twenty options across four categories.

## What's New in 6.3

- **A real Settings menu** — four groups (General, Match Rules, Saves, Debug) with twenty
  options. Values can be booleans, pick-from-a-list, or free numbers.
- **Coloured settings values** — ON is green, OFF is red, and pick-from-a-list values are
  yellow. The selected row is highlighted with colour instead of a background band, so the
  colours stay readable.
- **Match Rules** — pick your Match length (best of 1, 3, 5 or 7) and set a Round limit
  (10, 15 or 20 rounds) with a judges' decision when the limit is reached.
- **Text speed** — Instant, Fast, Normal or Slow. Instant removes every pause between attacks.
- **Display options** — turn colours off entirely, switch the HP / Stamina / Combo Cooldown
  bars between `■□` and `#-`, and trim the combat log down to results only.
- **Remember your picks** — your last class and last difficulty are offered back to you.
- **Debug mode moved into Settings** — no more questions at the start of every match.
- **Round Limit decisions** are recorded as their own stat, separately from knockouts.

## Run from source

From this folder:

```bash
python -m boxing
```

or:

```bash
python run_boxing.py
```

On Windows, install the optional curses support first:

```bash
pip install -r requirements.txt
```

## Install as a command

```bash
pip install .
boxing
```

> [!IMPORTANT]
> **`Release 6.3` is the last folder in the old per-version layout.** From **7.x onwards, individual releases will no longer be uploaded as folders** under `Releases/` — the code for each version is published in a new folder named **`Boxing Version 7.x`** instead. **`.exe` files are still uploaded** to the [Releases](../../releases) page for every version, so running the executable is how you play.

## Data location

| How you run it | Saves and settings |
|---|---|
| `python -m boxing` / `python run_boxing.py` | This folder (`saves/` and `settings.json`) |
| Built exe or `pip install .` | Windows: `%APPDATA%\Boxing-CLI`; macOS / Linux: `~/.Boxing-CLI` |
| Custom | Set `BOXING_HOME` to any folder |

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

## How to Play

Each round, you'll be shown a move menu with the damage, accuracy, and stamina cost of each
available option (Feint, Taunt, and Counter only appear when they're actually available to
you). Enter the corresponding move ID to act. HP, stamina, combo cooldowns, and any active
feint/taunt status are shown before every round.

## Fighter Classes

| Class | Damage | Accuracy | Stamina Use | HP | Crit Chance |
|---|---|---|---|---|---|
| Berserker | x1.25 | x0.90 | x1.10 | x1.00 | x1.20 |
| Assassin | x0.90 | x1.20 | x1.00 | x1.00 | x1.30 |
| Juggernaut | x1.00 | x1.00 | x0.75 | x1.20 | x0.80 |
| Duelist | x1.10 | x0.95 | x0.90 | x0.90 | x1.10 |
| Reaper | x1.50 | x0.80 | x1.30 | x0.75 | x1.50 |

## Project structure

```
Release 6.3/
├── README.md
├── pyproject.toml
├── requirements.txt
├── run_boxing.py         Entry script used to build the exe
├── 6.3.spec              PyInstaller build config
├── icon.ico
├── boxing/
│   ├── __main__.py       python -m boxing
│   ├── main.py
│   ├── paths.py
│   ├── assets/boxer.txt
│   ├── core/             data.py, combat.py, fighter.py, ai.py
│   ├── ui/               colors.py, bars.py, prompts.py, screen.py, loadingsc.py, menu.py
│   ├── flow/             startup.py, session.py, match.py, fight.py, options.py
│   └── storage/          saves.py, settings.py
├── saves/                Created/used when running from source
└── settings.json         Created/used when running from source
```

## Build the exe

```bash
pip install pyinstaller windows-curses
pyinstaller "6.3.spec"
```

The executable is written to `dist/6.3.exe`.

## License

No license specified yet.
