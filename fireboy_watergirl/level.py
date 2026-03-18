from __future__ import annotations

import pygame


PLAYER_WIDTH = 36
PLAYER_HEIGHT = 52


class Level:
    """This class is used to create levels for the game, and contains
    code to generate some sample levels."""
    def __init__(
        self,
        platforms: list[pygame.Rect],
        fire_start: tuple[int, int],
        water_start: tuple[int, int],
        door: pygame.Rect,
        *,
        name: str,
    ) -> None:
        self.platforms = platforms
        self.fire_start = fire_start
        self.water_start = water_start
        self.door = door
        self.name = name

        self.background_color = (18, 20, 30)
        self.platform_color = (100, 103, 118)
        self.accent_color = (63, 67, 81)
        self.door_color = (170, 210, 115)
        self.door_border_color = (214, 242, 168)

    @classmethod
    def sample_levels(cls, screen_width: int, screen_height: int) -> list["Level"]:
        tile_size = 20
        cols = screen_width // tile_size
        rows = screen_height // tile_size

        level_specs = [
            ("Level 1 - Stair Steps", cls._build_stair_steps_grid(cols, rows)),
            ("Level 2 - Twin Towers", cls._build_twin_towers_grid(cols, rows)),
        ]

        return [
            cls.from_grid(grid=grid, tile_size=tile_size, name=name)
            for name, grid in level_specs
        ]

    @classmethod
    def from_grid(
        cls,
        *,
        grid: list[str],
        tile_size: int,
        name: str,
    ) -> "Level":
        if not grid:
            msg = "Level grid cannot be empty."
            raise ValueError(msg)

        width = len(grid[0])
        if width == 0:
            msg = "Level grid rows cannot be empty."
            raise ValueError(msg)
        if any(len(row) != width for row in grid):
            msg = "All level grid rows must have the same width."
            raise ValueError(msg)

        fire_markers: list[tuple[int, int]] = []
        water_markers: list[tuple[int, int]] = []
        door_markers: list[tuple[int, int]] = []
        platforms: list[pygame.Rect] = []

        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                x = col_idx * tile_size
                y = row_idx * tile_size
                if cell == "#":
                    platforms.append(pygame.Rect(x, y, tile_size, tile_size))
                elif cell == "F":
                    fire_markers.append((col_idx, row_idx))
                elif cell == "W":
                    water_markers.append((col_idx, row_idx))
                elif cell == "D":
                    door_markers.append((col_idx, row_idx))
                elif cell == ".":
                    continue
                else:
                    msg = f"Unsupported level cell {cell!r} in level {name!r}."
                    raise ValueError(msg)

        if (
            len(fire_markers) != 1
            or len(water_markers) != 1
            or len(door_markers) != 1
        ):
            msg = f"Level {name!r} must include exactly one F, one W, and one D."
            raise ValueError(msg)

        fire_start = cls._spawn_from_marker(fire_markers[0], tile_size)
        water_start = cls._spawn_from_marker(water_markers[0], tile_size)
        door = cls._door_from_marker(door_markers[0], tile_size)
        return cls(
            platforms=platforms,
            fire_start=fire_start,
            water_start=water_start,
            door=door,
            name=name,
        )

    @staticmethod
    def _spawn_from_marker(marker: tuple[int, int], tile_size: int) -> tuple[int, int]:
        col_idx, row_idx = marker
        x = col_idx * tile_size + (tile_size - PLAYER_WIDTH) // 2
        y = (row_idx + 1) * tile_size - PLAYER_HEIGHT
        return (x, y)

    @staticmethod
    def _door_from_marker(marker: tuple[int, int], tile_size: int) -> pygame.Rect:
        col_idx, row_idx = marker
        x = col_idx * tile_size
        y = row_idx * tile_size
        return pygame.Rect(x, y, tile_size, tile_size * 2)

    @staticmethod
    def _blank_grid(cols: int, rows: int) -> list[list[str]]:
        return [["." for _ in range(cols)] for _ in range(rows)]

    @staticmethod
    def _fill_rect(
        grid: list[list[str]],
        *,
        left: int,
        top: int,
        width: int,
        height: int,
        char: str,
    ) -> None:
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        for row_idx in range(top, top + height):
            if not (0 <= row_idx < rows):
                continue
            for col_idx in range(left, left + width):
                if 0 <= col_idx < cols:
                    grid[row_idx][col_idx] = char

    @classmethod
    def _build_stair_steps_grid(cls, cols: int, rows: int) -> list[str]:
        grid = cls._blank_grid(cols, rows)
        cls._fill_rect(grid, left=0, top=rows - 2, width=cols, height=2, char="#")

        stair_specs = [
            (6, rows - 6, 7, 1),
            (16, rows - 9, 7, 1),
            (27, rows - 12, 7, 1),
            (38, rows - 15, 7, 1),
        ]
        for left, top, width, height in stair_specs:
            cls._fill_rect(
                grid,
                left=left,
                top=top,
                width=width,
                height=height,
                char="#",
            )

        grid[rows - 3][2] = "F"
        grid[rows - 3][6] = "W"
        grid[rows - 4][cols - 4] = "D"
        return ["".join(row) for row in grid]

    @classmethod
    def _build_twin_towers_grid(cls, cols: int, rows: int) -> list[str]:
        grid = cls._blank_grid(cols, rows)
        cls._fill_rect(grid, left=0, top=rows - 2, width=cols, height=2, char="#")

        # Two tall tower structures with cross-bridges.
        cls._fill_rect(grid, left=10, top=rows - 12, width=3, height=10, char="#")
        cls._fill_rect(grid, left=36, top=rows - 14, width=3, height=12, char="#")
        cls._fill_rect(grid, left=13, top=rows - 12, width=10, height=1, char="#")
        cls._fill_rect(grid, left=24, top=rows - 16, width=11, height=1, char="#")
        cls._fill_rect(grid, left=30, top=rows - 8, width=8, height=1, char="#")
        cls._fill_rect(grid, left=5, top=rows - 7, width=7, height=1, char="#")

        grid[rows - 3][3] = "F"
        grid[rows - 3][8] = "W"
        grid[rows - 4][cols - 5] = "D"
        return ["".join(row) for row in grid]

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.background_color)
        for platform in self.platforms:
            pygame.draw.rect(surface, self.platform_color, platform)
            pygame.draw.rect(surface, self.accent_color, platform, width=2)
        pygame.draw.rect(surface, self.door_color, self.door)
        pygame.draw.rect(surface, self.door_border_color, self.door, width=3)

