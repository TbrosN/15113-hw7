from __future__ import annotations

import pygame

from fireboy_watergirl.level import Level
from fireboy_watergirl.players import FireBoy, WaterGirl

# pylint: disable=no-member


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen_width = 980
        self.screen_height = 620
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Fireboy & Watergirl MVP")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.running = True

        self.world_bounds = self.screen.get_rect()
        self.levels = Level.sample_levels(self.screen_width, self.screen_height)
        self.level_index = 0
        self._load_level(self.level_index)

    def _load_level(self, level_index: int) -> None:
        self.level_index = level_index % len(self.levels)
        self.level = self.levels[self.level_index]
        self.fireboy = FireBoy(self.level.fire_start)
        self.watergirl = WaterGirl(self.level.water_start)
        self.players = [self.fireboy, self.watergirl]

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()

        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._load_level(self.level_index)
                elif event.key == pygame.K_n:
                    self._load_level(self.level_index + 1)
                elif event.key == pygame.K_p:
                    self._load_level(self.level_index - 1)

    def _update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.handle_movement_input(keys, dt)
            player.update(self.level.platforms, dt)
            player.keep_in_bounds(self.world_bounds)

        if all(player.rect.colliderect(self.level.door) for player in self.players):
            self._load_level(self.level_index + 1)

    def _draw(self) -> None:
        self.level.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)

        controls_text = "FireBoy: A/D move, W jump | WaterGirl: <-/-> move, UP jump"
        level_text = (
            f"{self.level.name} ({self.level_index + 1}/{len(self.levels)})"
            " | N: next level | P: previous | R: reset"
        )
        objective_text = "Objective: both players stand in the green door together"
        controls_surface = self.font.render(controls_text, True, (240, 240, 240))
        level_surface = self.font.render(level_text, True, (240, 240, 240))
        objective_surface = self.font.render(objective_text, True, (190, 238, 170))
        self.screen.blit(controls_surface, (24, 12))
        self.screen.blit(level_surface, (24, 36))
        self.screen.blit(objective_surface, (24, 60))

        pygame.display.flip()

