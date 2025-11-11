"""Enhanced enemy classes with special abilities and wave management."""

import pygame
import random
from typing import List, Tuple, Optional
from src.constants import *
from src.utils import distance, draw_health_bar


class StatusEffect:
    """Represents a status effect on an enemy."""

    def __init__(self, effect_type: str, duration: float, value: float = 0):
        self.type = effect_type  # 'slow', 'poison', 'burn', 'freeze'
        self.duration = duration
        self.value = value
        self.time = 0

    def update(self, dt: float) -> bool:
        """Update effect, returns True if expired."""
        self.time += dt
        return self.time >= self.duration


class Enemy:
    """Enhanced enemy base class with status effects."""

    def __init__(self, enemy_type: str, waypoints: List[Tuple[float, float]],
                wave_number: int = 1, difficulty_mult: dict = None):
        self.type = enemy_type
        self.stats = ENEMY_TYPES[enemy_type].copy()

        # Apply difficulty multipliers
        if difficulty_mult is None:
            difficulty_mult = {'health': 1.0, 'speed': 1.0}

        # Scale based on wave and difficulty
        wave_mult = 1 + (wave_number - 1) * 0.15
        self.max_health = int(self.stats['health'] * wave_mult * difficulty_mult['health'])
        self.health = self.max_health
        self.base_speed = self.stats['speed'] * difficulty_mult['speed']
        self.speed = self.base_speed
        self.reward = int(self.stats['reward'] * (1 + (wave_number - 1) * 0.1))
        self.color = self.stats['color']
        self.size = self.stats['size']

        # Special attributes
        self.armor = self.stats.get('armor', 0)
        self.flying = self.stats.get('flying', False)
        self.immune_to_slow = self.stats.get('immune_to_slow', False)
        self.regen_rate = self.stats.get('regen_rate', 0)
        self.heal_range = self.stats.get('heal_range', 0)
        self.heal_amount = self.stats.get('heal_amount', 0)
        self.heal_rate = self.stats.get('heal_rate', 0)
        self.heal_cooldown = 0

        # Shield system
        self.max_shield = self.stats.get('shield', 0)
        self.shield = self.max_shield
        self.shield_regen_rate = 5.0 if self.max_shield > 0 else 0

        # Movement
        self.waypoints = waypoints
        self.waypoint_index = 0
        self.x, self.y = waypoints[0] if waypoints else (0, 0)
        self.distance_traveled = 0

        # Status
        self.alive = True
        self.reached_end = False
        self.status_effects: List[StatusEffect] = []
        self.frozen = False

    def update(self, dt: float, all_enemies: List['Enemy'] = None):
        """Update enemy with status effects and special abilities."""
        if not self.alive or self.reached_end:
            return

        # Update status effects
        self._update_status_effects(dt)

        # Regeneration
        if self.regen_rate > 0 and self.health < self.max_health:
            self.health = min(self.max_health, self.health + self.regen_rate * dt)

        # Shield regeneration
        if self.shield < self.max_shield:
            self.shield = min(self.max_shield, self.shield + self.shield_regen_rate * dt)

        # Healing ability (for healer enemies)
        if self.heal_range > 0 and all_enemies:
            self._heal_nearby_enemies(dt, all_enemies)

        # Don't move if frozen
        if self.frozen:
            return

        # Movement
        if self.waypoint_index >= len(self.waypoints):
            self.reached_end = True
            return

        target_x, target_y = self.waypoints[self.waypoint_index]
        dx = target_x - self.x
        dy = target_y - self.y
        dist = distance((self.x, self.y), (target_x, target_y))

        if dist < self.speed:
            self.x = target_x
            self.y = target_y
            self.waypoint_index += 1
            self.distance_traveled += dist
        else:
            move_x = (dx / dist) * self.speed
            move_y = (dy / dist) * self.speed
            self.x += move_x
            self.y += move_y
            self.distance_traveled += self.speed

    def _update_status_effects(self, dt: float):
        """Update all status effects."""
        self.speed = self.base_speed
        self.frozen = False

        for effect in self.status_effects[:]:
            if effect.update(dt):
                self.status_effects.remove(effect)
                continue

            if effect.type == 'slow' and not self.immune_to_slow:
                self.speed *= (1 - effect.value)
            elif effect.type == 'poison':
                self.health -= effect.value * dt
            elif effect.type == 'burn':
                self.health -= effect.value * dt
            elif effect.type == 'freeze':
                self.frozen = True
                self.speed = 0

        if self.health <= 0:
            self.alive = False

    def _heal_nearby_enemies(self, dt: float, all_enemies: List['Enemy']):
        """Heal nearby enemies (healer ability)."""
        self.heal_cooldown -= dt
        if self.heal_cooldown > 0:
            return

        self.heal_cooldown = 1.0 / self.heal_rate

        for enemy in all_enemies:
            if enemy == self or not enemy.alive:
                continue

            if distance((self.x, self.y), (enemy.x, enemy.y)) <= self.heal_range:
                if enemy.health < enemy.max_health:
                    enemy.health = min(enemy.max_health, enemy.health + self.heal_amount)

    def apply_status_effect(self, effect_type: str, duration: float, value: float = 0):
        """Apply a status effect to the enemy."""
        # Remove existing effect of same type
        self.status_effects = [e for e in self.status_effects if e.type != effect_type]

        # Add new effect
        effect = StatusEffect(effect_type, duration, value)
        self.status_effects.append(effect)

    def take_damage(self, damage: int) -> bool:
        """Apply damage with armor and shield calculation."""
        # Apply to shield first
        if self.shield > 0:
            shield_damage = min(self.shield, damage)
            self.shield -= shield_damage
            damage -= shield_damage

            if damage <= 0:
                return False

        # Apply armor reduction
        actual_damage = damage * (1 - self.armor)

        self.health -= actual_damage

        if self.health <= 0:
            self.alive = False
            return True

        return False

    def draw(self, surface: pygame.Surface):
        """Draw enemy with status effect indicators."""
        if not self.alive:
            return

        # Draw enemy circle
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

        # Draw outline based on type
        outline_color = WHITE if self.type in ['boss', 'mega_boss'] else BLACK
        pygame.draw.circle(surface, outline_color, (int(self.x), int(self.y)), self.size, 2)

        # Draw shield indicator
        if self.shield > 0:
            shield_ring_radius = self.size + 3
            pygame.draw.circle(surface, LIGHT_BLUE, (int(self.x), int(self.y)),
                             shield_ring_radius, 2)

        # Draw armor indicator
        if self.armor > 0:
            armor_size = self.size // 2
            armor_rect = pygame.Rect(self.x - armor_size // 2, self.y - self.size - 2,
                                    armor_size, armor_size)
            pygame.draw.rect(surface, SILVER, armor_rect)

        # Draw status effect icons
        icon_y = int(self.y - self.size - 15)
        icon_x = int(self.x - 10)

        for effect in self.status_effects:
            if effect.type == 'slow':
                color = LIGHT_BLUE
            elif effect.type == 'poison':
                color = NEON_GREEN
            elif effect.type == 'burn':
                color = ORANGE
            elif effect.type == 'freeze':
                color = CYAN
            else:
                continue

            pygame.draw.circle(surface, color, (icon_x, icon_y), 3)
            icon_x += 7

        # Draw health bar
        health_bar_width = self.size * 2
        health_bar_height = 4
        health_bar_x = int(self.x - health_bar_width / 2)
        health_bar_y = int(self.y - self.size - 8)

        draw_health_bar(surface, health_bar_x, health_bar_y,
                       health_bar_width, health_bar_height,
                       self.health, self.max_health)

        # Draw shield bar if present
        if self.max_shield > 0:
            shield_bar_y = health_bar_y - 5
            draw_health_bar(surface, health_bar_x, shield_bar_y,
                           health_bar_width, health_bar_height,
                           self.shield, self.max_shield,
                           fill_color=LIGHT_BLUE)

    def get_position(self) -> Tuple[float, float]:
        """Get current position."""
        return (self.x, self.y)

    def get_progress(self) -> float:
        """Get progress along path (0 to 1)."""
        if not self.waypoints:
            return 0
        total_length = sum(distance(self.waypoints[i], self.waypoints[i + 1])
                          for i in range(len(self.waypoints) - 1))
        if total_length == 0:
            return 0
        return min(1.0, self.distance_traveled / total_length)

    def is_boss(self) -> bool:
        """Check if this is a boss enemy."""
        return self.type in ['boss', 'mega_boss']


class WaveManager:
    """Enhanced wave manager with difficulty support."""

    def __init__(self, waypoints: List[Tuple[float, float]],
                difficulty_mult: dict = None):
        self.waypoints = waypoints
        self.difficulty_mult = difficulty_mult or {'health': 1.0, 'speed': 1.0}
        self.current_wave = 0
        self.enemies: List[Enemy] = []
        self.enemies_to_spawn: List[Tuple[str, float]] = []
        self.wave_active = False
        self.wave_spawn_timer = 0
        self.time_between_enemies = 0.5

    def start_wave(self):
        """Start the next wave."""
        if self.wave_active:
            return

        self.current_wave += 1
        self.wave_active = True
        self.wave_spawn_timer = 0

        wave_index = min(self.current_wave - 1, len(WAVES) - 1)
        wave_data = WAVES[wave_index]

        self.enemies_to_spawn = []
        spawn_time = 0

        for enemy_type, count in wave_data.items():
            for _ in range(count):
                self.enemies_to_spawn.append((enemy_type, spawn_time))
                spawn_time += self.time_between_enemies

        random.shuffle(self.enemies_to_spawn)

        for i, (enemy_type, _) in enumerate(self.enemies_to_spawn):
            self.enemies_to_spawn[i] = (enemy_type, i * self.time_between_enemies)

    def update(self, dt: float) -> Tuple[int, int, int]:
        """
        Update wave and spawn enemies.

        Returns:
            (enemies_killed, enemies_reached_end, boss_kills)
        """
        enemies_killed = 0
        enemies_reached_end = 0
        boss_kills = 0

        if self.wave_active and self.enemies_to_spawn:
            self.wave_spawn_timer += dt

            while self.enemies_to_spawn and self.wave_spawn_timer >= self.enemies_to_spawn[0][1]:
                enemy_type, _ = self.enemies_to_spawn.pop(0)
                enemy = Enemy(enemy_type, self.waypoints,
                            self.current_wave, self.difficulty_mult)
                self.enemies.append(enemy)

        for enemy in self.enemies[:]:
            enemy.update(dt, self.enemies)

            if not enemy.alive:
                self.enemies.remove(enemy)
                enemies_killed += 1
                if enemy.is_boss():
                    boss_kills += 1
            elif enemy.reached_end:
                self.enemies.remove(enemy)
                enemies_reached_end += 1

        if self.wave_active and not self.enemies_to_spawn and not self.enemies:
            self.wave_active = False

        return enemies_killed, enemies_reached_end, boss_kills

    def draw(self, surface: pygame.Surface):
        """Draw all enemies."""
        for enemy in self.enemies:
            enemy.draw(surface)

    def is_wave_complete(self) -> bool:
        """Check if current wave is complete."""
        return not self.wave_active

    def get_enemies_in_range(self, position: Tuple[float, float],
                            range_distance: float) -> List[Enemy]:
        """Get all enemies within range."""
        return [e for e in self.enemies
                if e.alive and not e.reached_end
                and distance(position, e.get_position()) <= range_distance]

    def get_targeted_enemy(self, position: Tuple[float, float],
                          range_distance: float, mode: str = 'first') -> Optional[Enemy]:
        """Get enemy based on targeting mode."""
        enemies = self.get_enemies_in_range(position, range_distance)
        if not enemies:
            return None

        if mode == 'first':
            return max(enemies, key=lambda e: e.get_progress())
        elif mode == 'last':
            return min(enemies, key=lambda e: e.get_progress())
        elif mode == 'closest':
            return min(enemies, key=lambda e: distance(position, e.get_position()))
        elif mode == 'strongest':
            return max(enemies, key=lambda e: e.health)
        elif mode == 'weakest':
            return min(enemies, key=lambda e: e.health)
        else:
            return enemies[0]

    def apply_freeze_to_all(self, duration: float):
        """Freeze all enemies."""
        for enemy in self.enemies:
            if enemy.alive:
                enemy.apply_status_effect('freeze', duration)

    def damage_in_radius(self, position: Tuple[float, float],
                        radius: float, damage: int) -> int:
        """Apply damage to all enemies in radius, return count hit."""
        count = 0
        for enemy in self.enemies:
            if enemy.alive and distance(position, enemy.get_position()) <= radius:
                enemy.take_damage(damage)
                count += 1
        return count
