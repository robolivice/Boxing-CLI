# Changelog

All notable changes to **Boxing CLI** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [6.2] - 2026-09-29

The restructure release: a Settings menu, an animated loading screen, and the whole game rebuilt as an installable Python package. Gameplay and the save file format are unchanged from 6.1.

### Added

- **Settings menu** on the main menu (`New Game`, `Settings`, `Load Save`, `Delete Save`, `Exit`). Options are toggled with Enter and saved immediately to `settings.json`. Settings apply to every save.
- **Clear Previous Round** setting (default: off). When on, the screen is cleared at the start of each round after the first, showing only the current fight and round, and you press Enter after each round to read the results.
- **Four reserved settings slots**, shown greyed out as `(Soon)` and skipped by menu navigation.
- **Animated boxer loading screen** at startup, built with `curses`. Press `Q` to skip it.
- **Three ways to run the game:** the `6.2.exe` on Windows, `python -m boxing` from source, or a `boxing` command via `pip install .`.
- **Packaging files:** `pyproject.toml`, `requirements.txt` (`windows-curses` on Windows only), `run_boxing.py`, and a PyInstaller spec (`6.2.spec`) with a custom `icon.ico`.
- **`BOXING_HOME` environment variable** to store saves and settings in any folder you choose.
- **Release-specific README** for 6.2.

### Changed

- **Code structure:** the flat 6.1 script files were reorganised into a `boxing` package.
  - `core` — data tables, combat resolver, `Fighter` class, AI
  - `ui` — colours, bars, prompts, screen helpers, `curses` menu, loading animation
  - `flow` — startup prompts, save sessions, Match loop, Fight/Round loop, Settings menu
  - `storage` — saves and settings persistence
- **Data location** is now resolved by a new `paths` module:
  - From source: inside the release folder, as before.
  - `.exe` or `pip install .`: Windows `%APPDATA%\Boxing-CLI`, macOS / Linux `~/.Boxing-CLI`.
  - `BOXING_HOME`, if set, overrides both.
- The 6.1 menu placeholder `Options (Next Update)` is now a working **Settings** entry.
- The `Fighter` class now holds HP, stamina, cooldowns, and move history, replacing the many loose variables in the old main script.
- The Match, Fight, and Round logic is split into separate functions instead of one long nested loop.

### Fixed

- Ctrl+C now exits cleanly at the difficulty prompt.
- Startup no longer fails if the loading animation can't run (no `curses`, missing art file, or a `curses` error). The game simply skips it.

### Upgrade notes

- **Saves did not change format, but the default exe location did.** 6.1 stored `saves/` next to the script or exe; 6.2 exe and `pip install .` use the per-user folder above. Copy your 6.1 `saves/` folder into the new location, or set `BOXING_HOME`. The legacy `player_stats.json` migration still works.
- If you run from source, each release folder keeps its own `saves/` and `settings.json`.

## [6.1]

The last release in the original flat-file layout (`6.1.py`, `UI.py`, `combat.py`, `setup.py`, `saves.py`, `menu.py`).

### Features

- Best-of-3 Match structure (Match → Fight → Round). Drawn Fights are replayed until someone wins.
- Five fighter classes: Berserker, Assassin, Juggernaut, Duelist, Reaper.
- Moves: Jab, Kick, Uppercut, Block, plus Feint, Taunt, and Counter.
- Combo system and fatigue system.
- Easy, Medium, and Hard AI.
- Debug mode: force moves, print round state, disable stamina costs, seed the RNG, force the computer's class. Debug matches are not saved.
- End-of-match stats for both fighters.
- Arrow-key `curses` main menu with a numbered fallback. `Options` was shown as a disabled "Next Update" placeholder.
- Multiple named save slots with New, Load, and Delete (with confirmation).
- Persistent stats and streaks recorded after every completed Match, plus per-class, per-difficulty, and per-move records and personal bests.
- Save summary shown on load.
- Atomic save writes, corrupt-save backup as `.bak`, and automatic migration of the old `player_stats.json`.
- `Q` at class selection returns to the main menu. Ctrl+C exits with a "Thanks For Playing!!" message.

---

Releases before 6.1 are not documented in this file.

[6.2]: ../../releases
[6.1]: ../../releases
