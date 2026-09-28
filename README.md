# Boxing CLI

### BIG UPDATE COMING SOON!!!

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
- **Debug mode** — force specific moves, dump internal round-by-round state, disable stamina costs, and seed the RNG for reproducible testing.
- **End-of-match stats** — hits, misses, crits, blocks, combos, total damage dealt, and fights won, for both fighters.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

```bash
git clone https://github.com/robolivice/Boxing-CLI.git
cd Boxing-CLI
```

No external dependencies — everything runs on the standard library.

### Running the game

```bash
python "Boxing Release 5.3(Combat Part 3).py"
```

## Project Structure

| File | Responsibility |
|---|---|
| `Boxing Release 5.3(Combat Part 3).py` | Main loop — owns Match/Fight/Round state, debug-mode setup, and class selection. |
| `combat.py` | Core mechanics — move/combo/debuff/class data tables and the per-attack resolver (`r_turn`). |
| `setup.py` | Debug-mode prompts, class and difficulty selection, and the computer AI (`comp_AI`). |
| `UI.py` | Player move menu, HP/stamina/combo-cooldown bar rendering, status effects, and end-of-match stats display. |

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
- [ ] Persistent stats/streak tracking (across sessions)
- [ ] Career/ladder mode (sequential opponents, per-boxer AI, boss fight)
- [ ] Sound
- [ ] Local (hot-seat) multiplayer
- [ ] Online LAN multiplayer

## License

No license specified yet.
