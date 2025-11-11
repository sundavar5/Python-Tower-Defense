"""Tower classes and management."""

import pygame
import math
from typing import Tuple, Optional, List
from src.constants import *
from src.utils import distance, draw_text
from src.projectile import Projectile, SplashProjectile, LaserBeam


class Tower:
    """Base tower class."""

    def __init__(self, tower_type: str, grid_pos: Tuple[int, int], grid_size: int):
        """
        Initialize a tower.

        Args:
            tower_type: Type of tower from TOWER_TYPES
            grid_pos: Grid position (row, col)
            grid_size: Size of grid cells
        """
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
        # Update cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt

        # Find and attack target
        if self.fire_cooldown <= 0:
            # Get target (default to 'first' which is furthest along path)
            self.target = wave_manager.get_targeted_enemy(
                (self.x, self.y), self.range, 'first'
            )

            if self.target:
                self.shoot()
                self.fire_cooldown = 1.0 / self.fire_rate

        # Update projectiles
        for projectile in self.projectiles[:]:
            if projectile.update(dt):
                self.projectiles.remove(projectile)

    def shoot(self):
        """Create and fire a projectile at the target."""
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
        # Draw range circle if selected
        if show_range or self.selected:
            range_surface = pygame.Surface((surface.get_width(), surface.get_height()),
                                          pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (*self.color, 30),
                             (int(self.x), int(self.y)), int(self.range))
            surface.blit(range_surface, (0, 0))
            pygame.draw.circle(surface, self.color,
                             (int(self.x), int(self.y)), int(self.range), 1)

        # Draw tower base (square)
        tower_rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        pygame.draw.rect(surface, self.color, tower_rect)
        pygame.draw.rect(surface, BLACK, tower_rect, 2)

        # Draw tower top (circle)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius // 2)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius // 2, 2)

        # Draw level indicator
        if self.level > 1:
            font = pygame.font.Font(None, 16)
            level_text = f"L{self.level}"
            text_surface = font.render(level_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.x, self.y - self.radius - 8))
            # Draw background
            bg_rect = text_rect.inflate(4, 2)
            pygame.draw.rect(surface, BLACK, bg_rect)
            surface.blit(text_surface, text_rect)

        # Draw target line
        if self.target and self.target.alive:
            pygame.draw.line(surface, self.color,
                           (int(self.x), int(self.y)),
                           (int(self.target.x), int(self.target.y)), 1)

        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(surface)

    def get_upgrade_cost(self) -> int:
        """Calculate cost to upgrade to next level."""
        if self.level >= MAX_UPGRADE_LEVEL:
            return -1  # Max level reached
        return int(self.cost * (UPGRADE_COST_MULTIPLIER ** self.level))

    def upgrade(self) -> bool:
        """
        Upgrade the tower.

        Returns:
            True if upgraded successfully
        """
        if self.level >= MAX_UPGRADE_LEVEL:
            return False

        self.level += 1
        self.total_cost += self.get_upgrade_cost()

        # Improve stats
        self.damage = int(self.damage * 1.5)
        self.range = int(self.range * 1.1)
        self.fire_rate = self.fire_rate * 1.2

        return True

    def get_sell_value(self) -> int:
        """Get the value when selling this tower."""
        return int(self.total_cost * 0.7)

    def get_position(self) -> Tuple[float, float]:
        """Get tower position."""
        return (self.x, self.y)

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """Check if a point is within the tower."""
        return distance(point, (self.x, self.y)) <= self.radius


class SniperTower(Tower):
    """Long range, high damage tower."""

    def __init__(self, grid_pos: Tuple[int, int], grid_size: int):
        super().__init__('sniper', grid_pos, grid_size)


class RapidTower(Tower):
    """Fast firing tower."""

    def __init__(self, grid_pos: Tuple[int, int], grid_size: int):
        super().__init__('rapid', grid_pos, grid_size)


class SplashTower(Tower):
    """Area damage tower."""

    def __init__(self, grid_pos: Tuple[int, int], grid_size: int):
        super().__init__('splash', grid_pos, grid_size)
        self.splash_radius = self.stats['splash_radius']

    def shoot(self):
        """Create and fire a splash projectile at the target."""
        if self.target:
            # Need to pass all enemies for splash damage
            from src.enemy import Enemy
            all_enemies = []
            # We'll pass this from the game update
            projectile = SplashProjectile(
                (self.x, self.y),
                self.target,
                self.projectile_speed,
                self.damage,
                self.splash_radius,
                [],  # Will be filled by game
                self.color
            )
            self.projectiles.append(projectile)


class LaserTower(Tower):
    """Continuous beam tower."""

    def __init__(self, grid_pos: Tuple[int, int], grid_size: int):
        super().__init__('laser', grid_pos, grid_size)
        self.laser_beam: Optional[LaserBeam] = None

    def update(self, dt: float, wave_manager):
        """Update laser tower logic."""
        # Get target
        self.target = wave_manager.get_targeted_enemy(
            (self.x, self.y), self.range, 'first'
        )

        if self.target:
            # Create or update laser beam
            if not self.laser_beam or not self.laser_beam.active:
                self.laser_beam = LaserBeam(
                    (self.x, self.y),
                    self.target,
                    self.damage,
                    self.color
                )
            else:
                # Update existing beam
                self.laser_beam.target = self.target
                self.laser_beam.update(dt)
        else:
            self.laser_beam = None

    def shoot(self):
        """Laser doesn't use traditional shooting."""
        pass

    def draw(self, surface: pygame.Surface, show_range: bool = False):
        """Draw the laser tower and beam."""
        # Draw range
        if show_range or self.selected:
            range_surface = pygame.Surface((surface.get_width(), surface.get_height()),
                                          pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (*self.color, 30),
                             (int(self.x), int(self.y)), int(self.range))
            surface.blit(range_surface, (0, 0))
            pygame.draw.circle(surface, self.color,
                             (int(self.x), int(self.y)), int(self.range), 1)

        # Draw laser beam first (behind tower)
        if self.laser_beam and self.laser_beam.active:
            self.laser_beam.start_pos = (self.x, self.y)
            self.laser_beam.draw(surface)

        # Draw tower
        tower_rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        pygame.draw.rect(surface, self.color, tower_rect)
        pygame.draw.rect(surface, BLACK, tower_rect, 2)

        # Draw glowing center
        pygame.draw.circle(surface, CYAN, (int(self.x), int(self.y)), self.radius // 2)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius // 3)

        # Draw level indicator
        if self.level > 1:
            font = pygame.font.Font(None, 16)
            level_text = f"L{self.level}"
            text_surface = font.render(level_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.x, self.y - self.radius - 8))
            bg_rect = text_rect.inflate(4, 2)
            pygame.draw.rect(surface, BLACK, bg_rect)
            surface.blit(text_surface, text_rect)


# Tower factory
def create_tower(tower_type: str, grid_pos: Tuple[int, int], grid_size: int) -> Tower:
    """Create a tower of the specified type."""
    tower_classes = {
        'basic': Tower,
        'sniper': SniperTower,
        'rapid': RapidTower,
        'splash': SplashTower,
        'laser': LaserTower,
    }

    tower_class = tower_classes.get(tower_type, Tower)
    return tower_class(grid_pos, grid_size)
