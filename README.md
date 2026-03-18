# Fire Boy & Water Girl

A cooperative puzzle platformer clone built with Pygame.

## Setup

Uses [uv](https://docs.astral.sh/uv/) as the package manager. Install uv if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

From the project root:

```bash
uv sync
```

## Run

```bash
uv run fireboy-watergirl
```

Or:

```bash
uv run python -m fireboy_watergirl.main
```

## MVP Structure

- `fireboy_watergirl/main.py` - entry point (`run`)
- `fireboy_watergirl/game.py` - game loop, input, update, render
- `fireboy_watergirl/players.py` - player physics (walk/jump + collisions)
- `fireboy_watergirl/level.py` - generated grid-based levels (`#`, `F`, `W`, `D`, `L`, `U`, `G`)

## Controls

- FireBoy: `A` / `D` to move, `W` to jump
- WaterGirl: Left / Right arrows to move, Up arrow to jump
- Level controls: `N` next level, `P` previous level, `R` reset current level
- Goal: both players must overlap the green door at the same time to clear the level
- Pools: `L` (fire pool; safe for FireBoy), `U` (water pool; safe for WaterGirl), `G` (green pool; unsafe for both)
