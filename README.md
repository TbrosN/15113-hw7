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
- `fireboy_watergirl/level.py` - rectangle platform test level

## Controls

- FireBoy: `A` / `D` to move, `W` to jump
- WaterGirl: Left / Right arrows to move, Up arrow to jump
