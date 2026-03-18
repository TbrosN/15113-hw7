from __future__ import annotations

import pygame

from fireboy_watergirl.level import Level
from fireboy_watergirl.players import FireBoy, WaterGirl


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

        self.level = Level.basic_test_level(self.screen_width, self.screen_height)
        self.world_bounds = self.screen.get_rect()
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
                if event.key == self.fireboy.controls.jump:
                    self.fireboy.jump()
                if event.key == self.watergirl.controls.jump:
                    self.watergirl.jump()

    def _update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.handle_movement_input(keys)
            player.update(self.level.platforms, dt)
            player.keep_in_bounds(self.world_bounds)

    def _draw(self) -> None:
        self.level.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)

        controls_text = (
            "FireBoy: A/D move, W jump   |   WaterGirl: <-/-> move, UP jump"
        )
        text_surface = self.font.render(controls_text, True, (240, 240, 240))
        self.screen.blit(text_surface, (24, 16))

        pygame.display.flip()

