"""Projectile system for tower attacks."""

import pygame
import math
from typing import Tuple, Optional, List
from src.constants import *
from src.utils import distance, normalize_vector


class Projectile:
    """Base projectile class."""

    def __init__(self, start_pos: Tuple[float, float], target,
                speed: float, damage: int, color: Tuple[int, int, int] = YELLOW):
        """
        Initialize a projectile.

        Args:
            start_pos: Starting position (x, y)
            target: Target enemy object
            speed: Projectile speed
            damage: Damage to deal
            color: Projectile color
        """
        self.x, self.y = start_pos
        self.target = target
        self.speed = speed
        self.damage = damage
        self.color = color
        self.active = True
        self.radius = 4

    def update(self, dt: float) -> bool:
        """
        Update projectile position.

        Returns:
            True if projectile hit target or should be removed
        """
        if not self.active:
            return True

        # Check if target is still alive
        if not self.target or not self.target.alive:
            self.active = False
            return True

        # Get target position
        target_x, target_y = self.target.get_position()

        # Calculate direction
        dx = target_x - self.x
        dy = target_y - self.y
        dist = distance((self.x, self.y), (target_x, target_y))

        # Check if we hit the target
        if dist < self.speed + self.target.size:
            # Hit! Deal damage
            self.target.take_damage(self.damage)
            self.active = False
            return True

        # Move towards target
        if dist > 0:
            move_x = (dx / dist) * self.speed
            move_y = (dy / dist) * self.speed
            self.x += move_x
            self.y += move_y

        return False

    def draw(self, surface: pygame.Surface):
        """Draw the projectile."""
        if self.active:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 1)


class SplashProjectile(Projectile):
    """Projectile that deals splash damage."""

    def __init__(self, start_pos: Tuple[float, float], target,
                speed: float, damage: int, splash_radius: float,
                all_enemies: List, color: Tuple[int, int, int] = PURPLE):
        """Initialize splash projectile."""
        super().__init__(start_pos, target, speed, damage, color)
        self.splash_radius = splash_radius
        self.all_enemies = all_enemies
        self.explosion_radius = 0
        self.exploding = False
        self.explosion_duration = 0.2
        self.explosion_timer = 0

    def update(self, dt: float) -> bool:
        """Update projectile and handle splash damage."""
        if self.exploding:
            self.explosion_timer += dt
            self.explosion_radius = (self.explosion_timer / self.explosion_duration) * self.splash_radius
            if self.explosion_timer >= self.explosion_duration:
                self.active = False
                return True
            return False

        if not self.active:
            return True

        # Check if target is still alive
        if not self.target or not self.target.alive:
            self.active = False
            return True

        # Get target position
        target_x, target_y = self.target.get_position()

        # Calculate direction
        dx = target_x - self.x
        dy = target_y - self.y
        dist = distance((self.x, self.y), (target_x, target_y))

        # Check if we hit the target
        if dist < self.speed + self.target.size:
            # Hit! Deal splash damage
            impact_pos = (self.x, self.y)
            for enemy in self.all_enemies:
                if enemy.alive and distance(impact_pos, enemy.get_position()) <= self.splash_radius:
                    enemy.take_damage(self.damage)

            # Start explosion animation
            self.exploding = True
            return False

        # Move towards target
        if dist > 0:
            move_x = (dx / dist) * self.speed
            move_y = (dy / dist) * self.speed
            self.x += move_x
            self.y += move_y

        return False

    def draw(self, surface: pygame.Surface):
        """Draw the projectile or explosion."""
        if self.exploding:
            # Draw explosion
            if self.explosion_radius > 0:
                pygame.draw.circle(surface, self.color,
                                 (int(self.x), int(self.y)),
                                 int(self.explosion_radius), 2)
        elif self.active:
            # Draw projectile
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


class LaserBeam:
    """Laser beam that deals continuous damage."""

    def __init__(self, start_pos: Tuple[float, float], target,
                damage: int, color: Tuple[int, int, int] = CYAN):
        """Initialize laser beam."""
        self.start_pos = start_pos
        self.target = target
        self.damage = damage
        self.color = color
        self.active = True
        self.width = 3

    def update(self, dt: float) -> bool:
        """
        Update laser beam.

        Returns:
            True if laser should be removed
        """
        if not self.target or not self.target.alive:
            self.active = False
            return True

        # Deal damage over time
        self.target.take_damage(int(self.damage * dt))
        return False

    def draw(self, surface: pygame.Surface):
        """Draw the laser beam."""
        if self.active and self.target and self.target.alive:
            end_pos = self.target.get_position()
            pygame.draw.line(surface, self.color,
                           (int(self.start_pos[0]), int(self.start_pos[1])),
                           (int(end_pos[0]), int(end_pos[1])),
                           self.width)

            # Draw glow effect
            glow_color = tuple(min(255, c + 100) for c in self.color)
            pygame.draw.line(surface, glow_color,
                           (int(self.start_pos[0]), int(self.start_pos[1])),
                           (int(end_pos[0]), int(end_pos[1])),
                           1)
