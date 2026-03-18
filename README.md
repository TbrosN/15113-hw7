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

## Structure

- `fireboy_watergirl/main.py` – entry point and game loop
- `fireboy_watergirl/game.py` – `Game` class (window, clock, level/players)
- `fireboy_watergirl/players.py` – `FireBoy` and `WaterGirl` (stubs)
- `fireboy_watergirl/level.py` – `Level` (platforms, hazards; stub with ground)

Controls and full gameplay are left for you to implement.
