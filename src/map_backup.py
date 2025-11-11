"""Game map and pathfinding system."""

import pygame
from typing import List, Tuple
from src.constants import *
from src.utils import bfs_pathfinding, grid_to_pixel


class GameMap:
    """Represents the game map with pathfinding."""

    def __init__(self):
        """Initialize the game map."""
        self.grid_width = GRID_WIDTH
        self.grid_height = GRID_HEIGHT
        self.grid_size = GRID_SIZE

        # Create the grid (0 = grass/buildable, 1 = path)
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        # Define path coordinates
        self.create_path()

        # Find waypoints for enemies to follow
        self.waypoints = self.calculate_waypoints()
        self.waypoints_pixel = [grid_to_pixel(wp, self.grid_size) for wp in self.waypoints]

    def create_path(self):
        """Create a winding path from start to end."""
        # Define a specific path pattern
        # Start at top-left, wind through the map, end at bottom-right

        path_coords = [
            # Start from left side
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
            # Turn down
            (8, 6), (9, 6), (10, 6),
            # Turn right
            (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12),
            # Turn up
            (9, 12), (8, 12), (7, 12), (6, 12), (5, 12), (4, 12), (3, 12),
            # Turn right
            (3, 13), (3, 14), (3, 15), (3, 16), (3, 17),
            # Turn down
            (4, 17), (5, 17), (6, 17), (7, 17), (8, 17), (9, 17),
            (10, 17), (11, 17), (12, 17), (13, 17), (14, 17),
            # End point
        ]

        # Mark path cells
        for row, col in path_coords:
            if 0 <= row < self.grid_height and 0 <= col < self.grid_width:
                self.grid[row][col] = 1

        # Set start and end positions
        self.start_pos = path_coords[0]
        self.end_pos = path_coords[-1]

    def calculate_waypoints(self) -> List[Tuple[int, int]]:
        """Calculate waypoints along the path using pathfinding."""
        return bfs_pathfinding(self.grid, self.start_pos, self.end_pos)

    def is_buildable(self, grid_row: int, grid_col: int) -> bool:
        """Check if a grid cell is buildable (not on path)."""
        if 0 <= grid_row < self.grid_height and 0 <= grid_col < self.grid_width:
            return self.grid[grid_row][grid_col] == 0
        return False

    def draw(self, surface: pygame.Surface):
        """Draw the map."""
        # Draw grass and path
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                x = col * self.grid_size
                y = row * self.grid_size

                # Determine color
                if (row, col) == self.start_pos:
                    color = START_COLOR
                elif (row, col) == self.end_pos:
                    color = END_COLOR
                elif self.grid[row][col] == 1:
                    color = PATH_COLOR
                else:
                    color = GRASS_COLOR

                # Draw cell
                pygame.draw.rect(surface, color, (x, y, self.grid_size, self.grid_size))

                # Draw grid lines
                pygame.draw.rect(surface, DARK_GRAY, (x, y, self.grid_size, self.grid_size), 1)

    def get_start_position(self) -> Tuple[float, float]:
        """Get the starting position in pixel coordinates."""
        return grid_to_pixel(self.start_pos, self.grid_size)

    def get_end_position(self) -> Tuple[float, float]:
        """Get the ending position in pixel coordinates."""
        return grid_to_pixel(self.end_pos, self.grid_size)
