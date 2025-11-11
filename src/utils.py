"""Utility functions for the game."""

import math
import pygame
from typing import Tuple, List
from collections import deque


def distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points."""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def normalize_vector(vector: Tuple[float, float]) -> Tuple[float, float]:
    """Normalize a 2D vector."""
    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if magnitude == 0:
        return (0, 0)
    return (vector[0] / magnitude, vector[1] / magnitude)


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation between start and end."""
    return start + (end - start) * t


def draw_health_bar(surface: pygame.Surface, x: int, y: int, width: int, height: int,
                   current: float, maximum: float, border_color: Tuple[int, int, int] = (0, 0, 0),
                   fill_color: Tuple[int, int, int] = (0, 255, 0),
                   background_color: Tuple[int, int, int] = (255, 0, 0)):
    """Draw a health bar."""
    # Background (red)
    pygame.draw.rect(surface, background_color, (x, y, width, height))

    # Current health (green)
    fill_width = int(width * (current / maximum))
    if fill_width > 0:
        pygame.draw.rect(surface, fill_color, (x, y, fill_width, height))

    # Border
    pygame.draw.rect(surface, border_color, (x, y, width, height), 1)


def draw_text(surface: pygame.Surface, text: str, font: pygame.font.Font,
             color: Tuple[int, int, int], x: int, y: int, center: bool = False):
    """Draw text on the surface."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)

    surface.blit(text_surface, text_rect)
    return text_rect


def point_in_rect(point: Tuple[int, int], rect: pygame.Rect) -> bool:
    """Check if a point is inside a rectangle."""
    return rect.collidepoint(point)


def bfs_pathfinding(grid: List[List[int]], start: Tuple[int, int],
                   end: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Find path from start to end using Breadth-First Search.
    Returns list of (row, col) positions.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Queue stores (position, path)
    queue = deque([(start, [start])])
    visited = {start}

    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    while queue:
        (row, col), path = queue.popleft()

        # Check if we reached the end
        if (row, col) == end:
            return path

        # Explore neighbors
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Check bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                # Check if it's a valid path (1 = path, 0 = blocked)
                if grid[new_row][new_col] == 1 and (new_row, new_col) not in visited:
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append(((new_row, new_col), new_path))

    # No path found
    return []


def grid_to_pixel(grid_pos: Tuple[int, int], grid_size: int) -> Tuple[float, float]:
    """Convert grid coordinates to pixel coordinates (center of cell)."""
    return (grid_pos[1] * grid_size + grid_size // 2,
            grid_pos[0] * grid_size + grid_size // 2)


def pixel_to_grid(pixel_pos: Tuple[int, int], grid_size: int) -> Tuple[int, int]:
    """Convert pixel coordinates to grid coordinates."""
    return (pixel_pos[1] // grid_size, pixel_pos[0] // grid_size)
