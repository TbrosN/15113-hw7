from __future__ import annotations

import pygame


class Level:
    def __init__(
        self,
        platforms: list[pygame.Rect],
        fire_start: tuple[int, int],
        water_start: tuple[int, int],
    ) -> None:
        self.platforms = platforms
        self.fire_start = fire_start
        self.water_start = water_start

        self.background_color = (18, 20, 30)
        self.platform_color = (100, 103, 118)
        self.accent_color = (63, 67, 81)

    @classmethod
    def basic_test_level(cls, screen_width: int, screen_height: int) -> "Level":
        ground_height = 60
        platforms = [
            pygame.Rect(0, screen_height - ground_height, screen_width, ground_height),
        ]

        fire_start = (80, screen_height - ground_height - 52)
        water_start = (160, screen_height - ground_height - 52)

        return cls(platforms, fire_start, water_start)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.background_color)
        for platform in self.platforms:
            pygame.draw.rect(surface, self.platform_color, platform)
            pygame.draw.rect(surface, self.accent_color, platform, width=2)

