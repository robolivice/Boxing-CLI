# Changelog

All notable changes to **Boxing CLI** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [6.3] - 2026-10-22

The settings release: the Options menu grows from one toggle and four empty slots into a full, typed, grouped Settings menu, and a new Match Rules group lets you pick the shape of the match itself. Gameplay aside from the optional Round Limit is unchanged from 6.2.

### Added

- **Grouped Settings menu** — four groups (**General**, **Match Rules**, **Saves**, **Debug**) holding twenty options, opened from the main menu.
- **Three settings value types** — booleans (toggle with Enter), pick-from-a-list choices (Enter advances, Left and Right arrows step through them live), and free numbers (Enter opens an input box).
- **Match Rules group:**
  - **Match Length** — best of 1, 3, 5, or 7 Fights.
  - **Round Limit** — no limit, 10, 15, or 20 Rounds per Fight. When the limit is hit, the judges award the Fight to whoever dealt more damage, then to whoever has more HP left; a dead heat is a draw.
  - **Remember Last Class** and **Remember Last Difficulty** — your last picks are offered back to you at the prompt, and pressing Enter accepts them.
- **General group:**
  - **Loading Screen** — skip the animated boxer intro.
  - **Colors** — switch the whole game to plain text.
  - **ASCII Bars** — switch the HP, Stamina, and Combo Cooldown bars between `■`/`□` and `#`/`-`.
  - **Detailed Combat Log** — keep only the results and drop the tactical chatter.
  - **Text Speed** — Instant, Fast, Normal, or Slow. Instant removes every pause between attacks; messages you need to read keep a floor so they never flash past.
- **Saves group:**
  - **Confirm Overwrite** — skip the "That save exists. Overwrite?" prompt.
  - **Record Debug Matches** — count debug matches in your stats.
- **Debug group** — Debug Mode, Force Player Move, Force AI Move, Show Internal State, Disable Stamina Cost, Force AI Class, and RNG Seed.
- **Coloured settings values** — ON is green, OFF is red, and list values are yellow. The highlighted row uses colour and bold rather than a background band, so the value colours stay readable.
- **Coloured text-menu fallback** — the numbered menu uses the same colour scheme when `curses` isn't available.
- **Round Limit decisions** are recorded as their own stat, separately from knockouts, and shown in the save summary.
- **Release-specific README** for 6.3.

### Changed

- **Debug mode moved out of the session prompt and into Settings.** It used to ask seven questions at the start of every single match. Now it is one master switch plus a group of options, and it applies from the first match.
- **The RNG seed is one-shot.** It is used for exactly one match and then resets to random, so a fixed seed can never make every future match identical.
- **The settings store is typed.** `settings.json` now holds booleans, numbers, and strings, each validated on load. Older settings files still load: unknown keys are ignored and missing ones fall back to their defaults.
- **The Match length is configurable** instead of hardcoded to best-of-3.
- **The menu renderer understands styled items.** A menu item can be a plain string or a list of coloured segments, and the same style names resolve to curses colour pairs in the arrow-key menu and to ANSI codes in the text fallback.
- **Combat pacing goes through a single helper**, so Text Speed scales every pause in one place.

### Fixed

- The loading screen is now skipped when the Loading Screen setting is off, and it no longer fails if the animation can't run.
- The menu no longer drops to the numbered fallback on a monochrome terminal — it keeps the arrow keys and highlights the row with reverse video instead.
- The settings file is read before the loading screen starts, so the first thing you see already honours your settings.
- Settings now apply the moment you change them, without needing a restart.

### Upgrade notes

- **Your saves carry over untouched.** The save format did not change; the only addition is a `decisions` counter, which starts at zero on older saves.
- **Your settings carry over too.** A 6.2 `settings.json` keeps its `clear_log` value, the four old placeholder slots are dropped, and the new options start at their defaults.
- If you run from source, each release folder keeps its own `saves/` and `settings.json`. Copy them across, or point `BOXING_HOME` at one shared folder.

### Release policy

**`Release 6.3` is the last folder published in the old per-version layout.** From 7.x onwards,
individual releases will no longer be uploaded as folders under `Releases/` — there is no
`Releases/Release 7/Release 7.0` and nothing like it after that. The code for each 7.x version is
instead published in its own folder named `Boxing Version 7.x` (`Boxing Version 7.0`,
`Boxing Version 7.1`, and so on), kept updated in place as the version moves forward. `.exe` files
are still uploaded to the [Releases](../../releases) page for every version, 7.x onwards included,
so downloading and running the executable is how you play.

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

[6.3]: ../../releases
[6.2]: ../../releases
[6.1]: ../../releases
