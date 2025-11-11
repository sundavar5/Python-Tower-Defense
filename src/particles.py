"""Particle effects system for visual feedback."""

import pygame
import random
import math
from typing import Tuple, List
from src.constants import *


class Particle:
    """Single particle for visual effects."""

    def __init__(self, x: float, y: float, color: Tuple[int, int, int],
                velocity: Tuple[float, float] = None, lifetime: float = 1.0,
                size: int = 3, fade: bool = True):
        """Initialize a particle."""
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.fade = fade

        if velocity:
            self.vx, self.vy = velocity
        else:
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(20, 80)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed

        self.gravity = 100  # pixels per second^2
        self.alive = True

    def update(self, dt: float):
        """Update particle position and lifetime."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, surface: pygame.Surface):
        """Draw the particle."""
        if not self.alive:
            return

        # Calculate alpha based on lifetime if fading
        if self.fade:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            color = (*self.color, alpha)
        else:
            color = (*self.color, 255)

        # Calculate current size
        size_factor = self.lifetime / self.max_lifetime if self.fade else 1.0
        current_size = max(1, int(self.size * size_factor))

        # Draw particle
        try:
            particle_surface = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, (current_size, current_size), current_size)
            surface.blit(particle_surface, (int(self.x - current_size), int(self.y - current_size)))
        except:
            pass  # Silently fail if particle is off screen


class ParticleSystem:
    """Manages all particle effects."""

    def __init__(self):
        """Initialize particle system."""
        self.particles: List[Particle] = []

    def update(self, dt: float):
        """Update all particles."""
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.alive:
                self.particles.remove(particle)

        # Limit max particles
        if len(self.particles) > MAX_PARTICLES:
            self.particles = self.particles[-MAX_PARTICLES:]

    def draw(self, surface: pygame.Surface):
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(surface)

    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int],
                        count: int = 20, size: int = 4):
        """Create an explosion effect."""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 150)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            particle = Particle(x, y, color, velocity=velocity,
                              lifetime=random.uniform(0.3, 0.8), size=size)
            self.particles.append(particle)

    def create_impact(self, x: float, y: float, color: Tuple[int, int, int],
                     direction: Tuple[float, float] = (0, -1), count: int = 10):
        """Create impact effect (sparks in a direction)."""
        for _ in range(count):
            angle = math.atan2(direction[1], direction[0]) + random.uniform(-0.5, 0.5)
            speed = random.uniform(100, 200)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            particle = Particle(x, y, color, velocity=velocity,
                              lifetime=random.uniform(0.2, 0.5), size=3)
            self.particles.append(particle)

    def create_heal_effect(self, x: float, y: float, count: int = 15):
        """Create healing effect (green particles rising up)."""
        for _ in range(count):
            offset_x = random.uniform(-20, 20)
            offset_y = random.uniform(-20, 20)
            velocity = (random.uniform(-20, 20), random.uniform(-100, -50))

            particle = Particle(x + offset_x, y + offset_y, NEON_GREEN,
                              velocity=velocity, lifetime=random.uniform(0.5, 1.0),
                              size=4, fade=True)
            particle.gravity = -30  # Negative gravity to rise
            self.particles.append(particle)

    def create_freeze_effect(self, x: float, y: float, count: int = 12):
        """Create freeze effect (ice blue particles)."""
        for _ in range(count):
            offset_x = random.uniform(-15, 15)
            offset_y = random.uniform(-15, 15)
            velocity = (random.uniform(-30, 30), random.uniform(-30, 30))

            particle = Particle(x + offset_x, y + offset_y, LIGHT_BLUE,
                              velocity=velocity, lifetime=random.uniform(0.4, 0.8),
                              size=3, fade=True)
            particle.gravity = 0  # No gravity for freeze
            self.particles.append(particle)

    def create_poison_cloud(self, x: float, y: float, count: int = 15):
        """Create poison cloud effect."""
        for _ in range(count):
            offset_x = random.uniform(-25, 25)
            offset_y = random.uniform(-25, 25)
            velocity = (random.uniform(-20, 20), random.uniform(-40, -10))

            particle = Particle(x + offset_x, y + offset_y, NEON_GREEN,
                              velocity=velocity, lifetime=random.uniform(0.6, 1.2),
                              size=5, fade=True)
            particle.gravity = -10
            self.particles.append(particle)

    def create_electric_spark(self, x: float, y: float, count: int = 8):
        """Create electric spark effect."""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(80, 150)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            color = ELECTRIC_BLUE if random.random() > 0.5 else WHITE
            particle = Particle(x, y, color, velocity=velocity,
                              lifetime=random.uniform(0.1, 0.3), size=2)
            particle.gravity = 0
            self.particles.append(particle)

    def create_fire_burst(self, x: float, y: float, count: int = 10):
        """Create fire burst effect."""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(40, 100)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            color = ORANGE if random.random() > 0.5 else RED
            particle = Particle(x, y, color, velocity=velocity,
                              lifetime=random.uniform(0.3, 0.7), size=4)
            self.particles.append(particle)

    def create_money_effect(self, x: float, y: float, count: int = 8):
        """Create money collection effect."""
        for _ in range(count):
            velocity = (random.uniform(-50, 50), random.uniform(-100, -50))

            particle = Particle(x, y, GOLD, velocity=velocity,
                              lifetime=random.uniform(0.3, 0.6), size=3)
            self.particles.append(particle)

    def create_trail(self, x: float, y: float, color: Tuple[int, int, int],
                    count: int = 3):
        """Create a trail effect (for projectiles)."""
        for _ in range(count):
            offset_x = random.uniform(-3, 3)
            offset_y = random.uniform(-3, 3)

            particle = Particle(x + offset_x, y + offset_y, color,
                              velocity=(0, 0), lifetime=0.2, size=2)
            particle.gravity = 0
            self.particles.append(particle)

    def create_airstrike_explosion(self, x: float, y: float):
        """Create massive explosion for airstrike."""
        # Large orange/red explosion
        for _ in range(50):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(100, 300)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            color = random.choice([RED, ORANGE, YELLOW])
            particle = Particle(x, y, color, velocity=velocity,
                              lifetime=random.uniform(0.5, 1.5), size=6)
            self.particles.append(particle)

        # Smoke particles
        for _ in range(30):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(20, 80)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            particle = Particle(x, y, DARK_GRAY, velocity=velocity,
                              lifetime=random.uniform(0.8, 1.5), size=8)
            particle.gravity = -20
            self.particles.append(particle)

    def clear(self):
        """Clear all particles."""
        self.particles.clear()
