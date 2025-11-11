"""Enhanced tower system with all special abilities implemented."""

import pygame
import math
from typing import Tuple, Optional, List
from src.constants import *
from src.utils import distance, draw_text
from src.projectile import Projectile, SplashProjectile, LaserBeam


class StatusProjectile(Projectile):
    """Projectile that applies status effects."""

    def __init__(self, start_pos: Tuple[float, float], target,
                speed: float, damage: int, color: Tuple[int, int, int],
                status_type: str, status_duration: float, status_value: float):
        super().__init__(start_pos, target, speed, damage, color)
        self.status_type = status_type
        self.status_duration = status_duration
        self.status_value = status_value

    def update(self, dt: float) -> bool:
        """Update and apply status effect on hit."""
        if not self.active:
            return True

        if not self.target or not self.target.alive:
            self.active = False
            return True

        target_x, target_y = self.target.get_position()
        dx = target_x - self.x
        dy = target_y - self.y
        dist = distance((self.x, self.y), (target_x, target_y))

        if dist < self.speed + self.target.size:
            # Hit! Deal damage and apply status effect
            self.target.take_damage(self.damage)
            self.target.apply_status_effect(self.status_type, self.status_duration, self.status_value)
            self.active = False
            return True

        if dist > 0:
            move_x = (dx / dist) * self.speed
            move_y = (dy / dist) * self.speed
            self.x += move_x
            self.y += move_y

        return False


class ElectricProjectile(Projectile):
    """Projectile that chains to multiple enemies."""

    def __init__(self, start_pos: Tuple[float, float], target,
                speed: float, damage: int, color: Tuple[int, int, int],
                chain_count: int, chain_reduction: float, all_enemies: List):
        super().__init__(start_pos, target, speed, damage, color)
        self.chain_count = chain_count
        self.chain_reduction = chain_reduction
        self.all_enemies = all_enemies
        self.chained_enemies = []
        self.chain_lines = []  # For visual effect

    def update(self, dt: float) -> bool:
        """Update with chain lightning logic."""
        if not self.active:
            return True

        if not self.target or not self.target.alive:
            self.active = False
            return True

        target_x, target_y = self.target.get_position()
        dx = target_x - self.x
        dy = target_y - self.y
        dist = distance((self.x, self.y), (target_x, target_y))

        if dist < self.speed + self.target.size:
            # Hit! Apply damage and chain
            self.target.take_damage(self.damage)
            self.chained_enemies.append(self.target)
            
            # Chain to nearby enemies
            current_pos = (target_x, target_y)
            current_damage = self.damage
            
            for _ in range(self.chain_count - 1):
                # Find nearest unchained enemy
                nearest = None
                nearest_dist = float('inf')
                
                for enemy in self.all_enemies:
                    if enemy.alive and enemy not in self.chained_enemies:
                        d = distance(current_pos, enemy.get_position())
                        if d < 150 and d < nearest_dist:  # Max chain distance
                            nearest = enemy
                            nearest_dist = d
                
                if nearest:
                    # Apply reduced damage
                    current_damage = int(current_damage * self.chain_reduction)
                    nearest.take_damage(current_damage)
                    self.chained_enemies.append(nearest)
                    self.chain_lines.append((current_pos, nearest.get_position()))
                    current_pos = nearest.get_position()
                else:
                    break
            
            self.active = False
            return True

        if dist > 0:
            move_x = (dx / dist) * self.speed
            move_y = (dy / dist) * self.speed
            self.x += move_x
            self.y += move_y

        return False

    def draw(self, surface: pygame.Surface):
        """Draw projectile and chain lightning."""
        super().draw(surface)
        
        # Draw chain lightning lines
        for start, end in self.chain_lines:
            pygame.draw.line(surface, ELECTRIC_BLUE,
                           (int(start[0]), int(start[1])),
                           (int(end[0]), int(end[1])), 2)


class Tower:
    """Enhanced base tower class."""

    def __init__(self, tower_type: str, grid_pos: Tuple[int, int], grid_size: int):
        self.type = tower_type
        self.stats = TOWER_TYPES[tower_type].copy()

        # Position
        self.grid_pos = grid_pos
        self.grid_size = grid_size
        self.x = grid_pos[1] * grid_size + grid_size // 2
        self.y = grid_pos[0] * grid_size + grid_size // 2

        # Stats
        self.damage = self.stats['damage']
        self.range = self.stats['range']
        self.fire_rate = self.stats['fire_rate']
        self.color = self.stats['color']
        self.projectile_speed = self.stats.get('projectile_speed', 8)
        self.cost = self.stats['cost']

        # Upgrade system
        self.level = 1
        self.total_cost = self.cost

        # Shooting
        self.target: Optional[object] = None
        self.fire_cooldown = 0
        self.projectiles: List = []

        # Visual
        self.radius = grid_size // 3
        self.selected = False

        # Stats tracking
        self.kills = 0
        self.damage_dealt = 0

    def update(self, dt: float, wave_manager):
        """Update tower logic."""
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt

        if self.fire_cooldown <= 0:
            self.target = wave_manager.get_targeted_enemy(
                (self.x, self.y), self.range, 'first'
            )

            if self.target:
                self.shoot()
                self.fire_cooldown = 1.0 / self.fire_rate

        for projectile in self.projectiles[:]:
            if projectile.update(dt):
                self.projectiles.remove(projectile)

    def shoot(self):
        """Create and fire a projectile."""
        if self.target:
            projectile = Projectile(
                (self.x, self.y),
                self.target,
                self.projectile_speed,
                self.damage,
                self.color
            )
            self.projectiles.append(projectile)

    def draw(self, surface: pygame.Surface, show_range: bool = False):
        """Draw the tower."""
        if show_range or self.selected:
            range_surface = pygame.Surface((surface.get_width(), surface.get_height()),
                                          pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (*self.color, 30),
                             (int(self.x), int(self.y)), int(self.range))
            surface.blit(range_surface, (0, 0))
            pygame.draw.circle(surface, self.color,
                             (int(self.x), int(self.y)), int(self.range), 1)

        tower_rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        pygame.draw.rect(surface, self.color, tower_rect)
        pygame.draw.rect(surface, BLACK, tower_rect, 2)

        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius // 2)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius // 2, 2)

        if self.level > 1:
            font = pygame.font.Font(None, 16)
            level_text = f"L{self.level}"
            text_surface = font.render(level_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.x, self.y - self.radius - 8))
            bg_rect = text_rect.inflate(4, 2)
            pygame.draw.rect(surface, BLACK, bg_rect)
            surface.blit(text_surface, text_rect)

        if self.target and self.target.alive:
            pygame.draw.line(surface, self.color,
                           (int(self.x), int(self.y)),
                           (int(self.target.x), int(self.target.y)), 1)

        for projectile in self.projectiles:
            projectile.draw(surface)

    def get_upgrade_cost(self) -> int:
        if self.level >= MAX_UPGRADE_LEVEL:
            return -1
        return int(self.cost * (UPGRADE_COST_MULTIPLIER ** self.level))

    def upgrade(self) -> bool:
        if self.level >= MAX_UPGRADE_LEVEL:
            return False

        self.level += 1
        self.total_cost += self.get_upgrade_cost()
        self.damage = int(self.damage * 1.5)
        self.range = int(self.range * 1.1)
        self.fire_rate = self.fire_rate * 1.2
        return True

    def get_sell_value(self) -> int:
        return int(self.total_cost * 0.7)

    def get_position(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def contains_point(self, point: Tuple[int, int]) -> bool:
        return distance(point, (self.x, self.y)) <= self.radius


class IceTower(Tower):
    """Tower that slows enemies."""

    def __init__(self, grid_pos: Tuple[int, int], grid_size: int):
        super().__init__('ice', grid_pos, grid_size)
        self.slow_duration = self.stats['slow_duration']
        self.slow_amount = self.stats['slow_amount']

    def shoot(self):
        if self.target:
            projectile = StatusProjectile(
                (self.x, self.y),
                self.target,
                self.projectile_speed,
                self.damage,
                self.color,
                'slow',
                self.slow_duration,
                self.slow_amount
            )
            self.projectiles.append(projectile)


class PoisonTower(Tower):
    """Tower that poisons enemies."""

    def __init__(self, grid_pos: Tuple[int, int], grid_size: int):
        super().__init__('poison', grid_pos, grid_size)
        self.poison_damage = self.stats['poison_damage']
        self.poison_duration = self.stats['poison_duration']

    def shoot(self):
        if self.target:
            projectile = StatusProjectile(
                (self.x, self.y),
                self.target,
                self.projectile_speed,
                self.damage,
                self.color,
                'poison',
                self.poison_duration,
                self.poison_damage
            )
            self.projectiles.append(projectile)


class FlameTower(Tower):
    """Tower that burns enemies."""

    def __init__(self, grid_pos: Tuple[int, int], grid_size: int):
        super().__init__('flame', grid_pos, grid_size)
        self.burn_damage = self.stats['burn_damage']
        self.burn_duration = self.stats['burn_duration']

    def shoot(self):
        if self.target:
            projectile = StatusProjectile(
                (self.x, self.y),
                self.target,
                self.projectile_speed,
                self.damage,
                self.color,
                'burn',
                self.burn_duration,
                self.burn_damage
            )
            self.projectiles.append(projectile)


class ElectricTower(Tower):
    """Tower with chain lightning."""

    def __init__(self, grid_pos: Tuple[int, int], grid_size: int):
        super().__init__('electric', grid_pos, grid_size)
        self.chain_count = self.stats['chain_count']
        self.chain_reduction = self.stats['chain_damage_reduction']
        self.projectile_speed = 15  # Fast projectile

    def update(self, dt: float, wave_manager):
        """Update with enemy list access."""
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt

        if self.fire_cooldown <= 0:
            self.target = wave_manager.get_targeted_enemy(
                (self.x, self.y), self.range, 'first'
            )

            if self.target:
                self.shoot(wave_manager.enemies)
                self.fire_cooldown = 1.0 / self.fire_rate

        for projectile in self.projectiles[:]:
            if projectile.update(dt):
                self.projectiles.remove(projectile)

    def shoot(self, all_enemies):
        if self.target:
            projectile = ElectricProjectile(
                (self.x, self.y),
                self.target,
                self.projectile_speed,
                self.damage,
                self.color,
                self.chain_count,
                self.chain_reduction,
                all_enemies
            )
            self.projectiles.append(projectile)


class ArtilleryTower(Tower):
    """Massive splash damage tower."""

    def __init__(self, grid_pos: Tuple[int, int], grid_size: int):
        super().__init__('artillery', grid_pos, grid_size)
        self.splash_radius = self.stats['splash_radius']

    def update(self, dt: float, wave_manager):
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt

        if self.fire_cooldown <= 0:
            self.target = wave_manager.get_targeted_enemy(
                (self.x, self.y), self.range, 'first'
            )

            if self.target:
                self.shoot(wave_manager.enemies)
                self.fire_cooldown = 1.0 / self.fire_rate

        for projectile in self.projectiles[:]:
            if projectile.update(dt):
                self.projectiles.remove(projectile)

    def shoot(self, all_enemies):
        if self.target:
            projectile = SplashProjectile(
                (self.x, self.y),
                self.target,
                self.projectile_speed,
                self.damage,
                self.splash_radius,
                all_enemies,
                self.color
            )
            self.projectiles.append(projectile)


class SupportTower(Tower):
    """Tower that buffs nearby towers."""

    def __init__(self, grid_pos: Tuple[int, int], grid_size: int):
        super().__init__('support', grid_pos, grid_size)
        self.buff_range = self.stats['buff_range']
        self.damage_buff = self.stats['damage_buff']

    def update(self, dt: float, wave_manager):
        """Support towers don't attack."""
        pass

    def shoot(self):
        """Support towers don't shoot."""
        pass

    def draw(self, surface: pygame.Surface, show_range: bool = False):
        """Draw support tower with buff aura."""
        if show_range or self.selected:
            range_surface = pygame.Surface((surface.get_width(), surface.get_height()),
                                          pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (*GOLD, 30),
                             (int(self.x), int(self.y)), int(self.buff_range))
            surface.blit(range_surface, (0, 0))
            pygame.draw.circle(surface, GOLD,
                             (int(self.x), int(self.y)), int(self.buff_range), 1)

        # Draw support tower as star shape
        star_points = []
        for i in range(5):
            angle = (i * 144 - 90) * math.pi / 180
            x = self.x + self.radius * math.cos(angle)
            y = self.y + self.radius * math.sin(angle)
            star_points.append((x, y))

        pygame.draw.polygon(surface, GOLD, star_points)
        pygame.draw.polygon(surface, BLACK, star_points, 2)

        if self.level > 1:
            font = pygame.font.Font(None, 16)
            level_text = f"L{self.level}"
            text_surface = font.render(level_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.x, self.y - self.radius - 8))
            bg_rect = text_rect.inflate(4, 2)
            pygame.draw.rect(surface, BLACK, bg_rect)
            surface.blit(text_surface, text_rect)


class SniperTower(Tower):
    def __init__(self, grid_pos, grid_size):
        super().__init__('sniper', grid_pos, grid_size)


class RapidTower(Tower):
    def __init__(self, grid_pos, grid_size):
        super().__init__('rapid', grid_pos, grid_size)


class SplashTower(Tower):
    def __init__(self, grid_pos, grid_size):
        super().__init__('splash', grid_pos, grid_size)
        self.splash_radius = self.stats['splash_radius']

    def update(self, dt: float, wave_manager):
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt

        if self.fire_cooldown <= 0:
            self.target = wave_manager.get_targeted_enemy(
                (self.x, self.y), self.range, 'first'
            )

            if self.target:
                self.shoot(wave_manager.enemies)
                self.fire_cooldown = 1.0 / self.fire_rate

        for projectile in self.projectiles[:]:
            if projectile.update(dt):
                self.projectiles.remove(projectile)

    def shoot(self, all_enemies):
        if self.target:
            projectile = SplashProjectile(
                (self.x, self.y),
                self.target,
                self.projectile_speed,
                self.damage,
                self.splash_radius,
                all_enemies,
                self.color
            )
            self.projectiles.append(projectile)


class LaserTower(Tower):
    def __init__(self, grid_pos, grid_size):
        super().__init__('laser', grid_pos, grid_size)
        self.laser_beam: Optional[LaserBeam] = None

    def update(self, dt: float, wave_manager):
        self.target = wave_manager.get_targeted_enemy(
            (self.x, self.y), self.range, 'first'
        )

        if self.target:
            if not self.laser_beam or not self.laser_beam.active:
                self.laser_beam = LaserBeam(
                    (self.x, self.y),
                    self.target,
                    self.damage,
                    self.color
                )
            else:
                self.laser_beam.target = self.target
                self.laser_beam.update(dt)
        else:
            self.laser_beam = None

    def shoot(self):
        pass

    def draw(self, surface: pygame.Surface, show_range: bool = False):
        if show_range or self.selected:
            range_surface = pygame.Surface((surface.get_width(), surface.get_height()),
                                          pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (*self.color, 30),
                             (int(self.x), int(self.y)), int(self.range))
            surface.blit(range_surface, (0, 0))
            pygame.draw.circle(surface, self.color,
                             (int(self.x), int(self.y)), int(self.range), 1)

        if self.laser_beam and self.laser_beam.active:
            self.laser_beam.start_pos = (self.x, self.y)
            self.laser_beam.draw(surface)

        tower_rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        pygame.draw.rect(surface, self.color, tower_rect)
        pygame.draw.rect(surface, BLACK, tower_rect, 2)

        pygame.draw.circle(surface, CYAN, (int(self.x), int(self.y)), self.radius // 2)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius // 3)

        if self.level > 1:
            font = pygame.font.Font(None, 16)
            level_text = f"L{self.level}"
            text_surface = font.render(level_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.x, self.y - self.radius - 8))
            bg_rect = text_rect.inflate(4, 2)
            pygame.draw.rect(surface, BLACK, bg_rect)
            surface.blit(text_surface, text_rect)


def create_tower(tower_type: str, grid_pos: Tuple[int, int], grid_size: int) -> Tower:
    """Create a tower of the specified type."""
    tower_classes = {
        'basic': Tower,
        'sniper': SniperTower,
        'rapid': RapidTower,
        'splash': SplashTower,
        'laser': LaserTower,
        'ice': IceTower,
        'poison': PoisonTower,
        'electric': ElectricTower,
        'artillery': ArtilleryTower,
        'support': SupportTower,
        'flame': FlameTower,
    }

    tower_class = tower_classes.get(tower_type, Tower)
    return tower_class(grid_pos, grid_size)
