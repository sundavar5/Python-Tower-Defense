"""Enemy classes and wave management."""

import pygame
import random
from typing import List, Tuple
from src.constants import *
from src.utils import distance, draw_health_bar


class Enemy:
    """Base enemy class."""

    def __init__(self, enemy_type: str, waypoints: List[Tuple[float, float]], wave_number: int = 1):
        """
        Initialize an enemy.

        Args:
            enemy_type: Type of enemy from ENEMY_TYPES
            waypoints: List of waypoint positions to follow
            wave_number: Current wave number for scaling
        """
        self.type = enemy_type
        self.stats = ENEMY_TYPES[enemy_type].copy()

        # Scale health and reward based on wave number
        wave_multiplier = 1 + (wave_number - 1) * 0.15
        self.max_health = int(self.stats['health'] * wave_multiplier)
        self.health = self.max_health
        self.speed = self.stats['speed']
        self.reward = int(self.stats['reward'] * (1 + (wave_number - 1) * 0.1))
        self.color = self.stats['color']
        self.size = self.stats['size']

        # Movement
        self.waypoints = waypoints
        self.waypoint_index = 0
        self.x, self.y = waypoints[0] if waypoints else (0, 0)
        self.distance_traveled = 0

        # Status
        self.alive = True
        self.reached_end = False

    def update(self, dt: float):
        """Update enemy position."""
        if not self.alive or self.reached_end:
            return

        if self.waypoint_index >= len(self.waypoints):
            self.reached_end = True
            return

        # Get target waypoint
        target_x, target_y = self.waypoints[self.waypoint_index]

        # Calculate direction
        dx = target_x - self.x
        dy = target_y - self.y
        dist = distance((self.x, self.y), (target_x, target_y))

        # Move towards waypoint
        if dist < self.speed:
            # Reached waypoint, move to next
            self.x = target_x
            self.y = target_y
            self.waypoint_index += 1
            self.distance_traveled += dist
        else:
            # Move towards waypoint
            move_x = (dx / dist) * self.speed
            move_y = (dy / dist) * self.speed
            self.x += move_x
            self.y += move_y
            self.distance_traveled += self.speed

    def take_damage(self, damage: int) -> bool:
        """
        Apply damage to enemy.

        Returns:
            True if enemy died, False otherwise
        """
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False

    def draw(self, surface: pygame.Surface):
        """Draw the enemy."""
        if not self.alive:
            return

        # Draw enemy circle
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

        # Draw outline
        outline_color = WHITE if self.type == 'boss' else BLACK
        pygame.draw.circle(surface, outline_color, (int(self.x), int(self.y)), self.size, 2)

        # Draw health bar
        health_bar_width = self.size * 2
        health_bar_height = 4
        health_bar_x = int(self.x - health_bar_width / 2)
        health_bar_y = int(self.y - self.size - 8)

        draw_health_bar(surface, health_bar_x, health_bar_y,
                       health_bar_width, health_bar_height,
                       self.health, self.max_health)

    def get_position(self) -> Tuple[float, float]:
        """Get current position."""
        return (self.x, self.y)

    def get_progress(self) -> float:
        """Get progress along path (0 to 1)."""
        if not self.waypoints:
            return 0
        # Calculate total path length
        total_length = sum(distance(self.waypoints[i], self.waypoints[i + 1])
                          for i in range(len(self.waypoints) - 1))
        if total_length == 0:
            return 0
        return min(1.0, self.distance_traveled / total_length)


class WaveManager:
    """Manages enemy waves."""

    def __init__(self, waypoints: List[Tuple[float, float]]):
        """Initialize wave manager."""
        self.waypoints = waypoints
        self.current_wave = 0
        self.enemies: List[Enemy] = []
        self.enemies_to_spawn: List[Tuple[str, float]] = []  # (enemy_type, spawn_time)
        self.wave_active = False
        self.wave_spawn_timer = 0
        self.time_between_enemies = 0.5  # seconds between each enemy spawn

    def start_wave(self):
        """Start the next wave."""
        if self.wave_active:
            return

        self.current_wave += 1
        self.wave_active = True
        self.wave_spawn_timer = 0

        # Get wave composition
        wave_index = min(self.current_wave - 1, len(WAVES) - 1)
        wave_data = WAVES[wave_index]

        # Create spawn queue
        self.enemies_to_spawn = []
        spawn_time = 0

        for enemy_type, count in wave_data.items():
            for _ in range(count):
                self.enemies_to_spawn.append((enemy_type, spawn_time))
                spawn_time += self.time_between_enemies

        # Shuffle to mix enemy types
        random.shuffle(self.enemies_to_spawn)

        # Reassign spawn times after shuffle
        for i, (enemy_type, _) in enumerate(self.enemies_to_spawn):
            self.enemies_to_spawn[i] = (enemy_type, i * self.time_between_enemies)

    def update(self, dt: float) -> Tuple[int, int]:
        """
        Update wave and spawn enemies.

        Returns:
            (enemies_killed, enemies_reached_end)
        """
        enemies_killed = 0
        enemies_reached_end = 0

        # Update spawn timer
        if self.wave_active and self.enemies_to_spawn:
            self.wave_spawn_timer += dt

            # Spawn enemies
            while self.enemies_to_spawn and self.wave_spawn_timer >= self.enemies_to_spawn[0][1]:
                enemy_type, _ = self.enemies_to_spawn.pop(0)
                enemy = Enemy(enemy_type, self.waypoints, self.current_wave)
                self.enemies.append(enemy)

        # Update all enemies
        for enemy in self.enemies[:]:
            enemy.update(dt)

            # Check if enemy died
            if not enemy.alive:
                self.enemies.remove(enemy)
                enemies_killed += 1

            # Check if enemy reached end
            elif enemy.reached_end:
                self.enemies.remove(enemy)
                enemies_reached_end += 1

        # Check if wave is complete
        if self.wave_active and not self.enemies_to_spawn and not self.enemies:
            self.wave_active = False

        return enemies_killed, enemies_reached_end

    def draw(self, surface: pygame.Surface):
        """Draw all enemies."""
        for enemy in self.enemies:
            enemy.draw(surface)

    def is_wave_complete(self) -> bool:
        """Check if current wave is complete."""
        return not self.wave_active

    def get_enemies_in_range(self, position: Tuple[float, float], range_distance: float) -> List[Enemy]:
        """Get all enemies within range of a position."""
        enemies_in_range = []
        for enemy in self.enemies:
            if enemy.alive and not enemy.reached_end:
                if distance(position, enemy.get_position()) <= range_distance:
                    enemies_in_range.append(enemy)
        return enemies_in_range

    def get_furthest_enemy_in_range(self, position: Tuple[float, float],
                                    range_distance: float) -> Enemy:
        """Get the enemy that has traveled furthest along the path within range."""
        enemies_in_range = self.get_enemies_in_range(position, range_distance)
        if not enemies_in_range:
            return None

        # Return enemy with highest progress
        return max(enemies_in_range, key=lambda e: e.get_progress())
