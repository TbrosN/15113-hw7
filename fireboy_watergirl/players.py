from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Controls:
    left: int
    right: int
    jump: int


class Player:
    def __init__(
        self,
        *,
        name: str,
        color: tuple[int, int, int],
        start_pos: tuple[int, int],
        controls: Controls,
    ) -> None:
        self.name = name
        self.color = color
        self.controls = controls

        self.width = 36
        self.height = 52
        self.rect = pygame.Rect(start_pos[0], start_pos[1], self.width, self.height)

        # Store continuous position so movement feels smooth at all frame rates.
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.on_ground = False

        self.move_speed = 290.0
        self.jump_velocity = 560.0
        self.gravity = 1300.0
        self.max_fall_speed = 900.0

    def handle_movement_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        moving_left = keys[self.controls.left]
        moving_right = keys[self.controls.right]

        if moving_left and not moving_right:
            self.vel_x = -self.move_speed
        elif moving_right and not moving_left:
            self.vel_x = self.move_speed
        else:
            self.vel_x = 0.0

    def jump(self) -> None:
        if self.on_ground:
            self.vel_y = -self.jump_velocity
            self.on_ground = False

    def update(self, platforms: list[pygame.Rect], dt: float) -> None:
        self.vel_y = min(self.vel_y + self.gravity * dt, self.max_fall_speed)

        self._move_horizontally(platforms, dt)
        self._move_vertically(platforms, dt)

    def keep_in_bounds(self, bounds: pygame.Rect) -> None:
        if self.rect.left < bounds.left:
            self.rect.left = bounds.left
            self.pos_x = float(self.rect.x)
            self.vel_x = 0.0

        if self.rect.right > bounds.right:
            self.rect.right = bounds.right
            self.pos_x = float(self.rect.x)
            self.vel_x = 0.0

        if self.rect.top < bounds.top:
            self.rect.top = bounds.top
            self.pos_y = float(self.rect.y)
            self.vel_y = 0.0

        if self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom
            self.pos_y = float(self.rect.y)
            self.vel_y = 0.0
            self.on_ground = True

    def _move_horizontally(self, platforms: list[pygame.Rect], dt: float) -> None:
        self.pos_x += self.vel_x * dt
        self.rect.x = round(self.pos_x)

        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue

            if self.vel_x > 0:
                self.rect.right = platform.left
            elif self.vel_x < 0:
                self.rect.left = platform.right
            self.pos_x = float(self.rect.x)
            break

    def _move_vertically(self, platforms: list[pygame.Rect], dt: float) -> None:
        self.pos_y += self.vel_y * dt
        self.rect.y = round(self.pos_y)
        self.on_ground = False

        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue

            if self.vel_y > 0:
                self.rect.bottom = platform.top
                self.on_ground = True
            elif self.vel_y < 0:
                self.rect.top = platform.bottom

            self.vel_y = 0.0
            self.pos_y = float(self.rect.y)
            break

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)


class FireBoy(Player):
    def __init__(self, start_pos: tuple[int, int]) -> None:
        super().__init__(
            name="FireBoy",
            color=(237, 107, 72),
            start_pos=start_pos,
            controls=Controls(
                left=pygame.K_a,
                right=pygame.K_d,
                jump=pygame.K_w,
            ),
        )


class WaterGirl(Player):
    def __init__(self, start_pos: tuple[int, int]) -> None:
        super().__init__(
            name="WaterGirl",
            color=(88, 170, 240),
            start_pos=start_pos,
            controls=Controls(
                left=pygame.K_LEFT,
                right=pygame.K_RIGHT,
                jump=pygame.K_UP,
            ),
        )

