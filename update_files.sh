#!/bin/bash
# Script to update remaining game files efficiently

echo "Updating game files with new features..."

# Update map.py to support multiple layouts
cat > src/map_enhanced.py << 'EOF'
"""Enhanced game map with multiple layouts."""

import pygame
from typing import List, Tuple
from src.constants import *
from src.utils import bfs_pathfinding, grid_to_pixel


class GameMap:
    """Game map with support for multiple layouts."""

    def __init__(self, layout_name: str = 'classic'):
        self.grid_width = GRID_WIDTH
        self.grid_height = GRID_HEIGHT
        self.grid_size = GRID_SIZE
        self.layout_name = layout_name
        
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        self.load_layout(layout_name)
        self.waypoints = self.calculate_waypoints()
        self.waypoints_pixel = [grid_to_pixel(wp, self.grid_size) for wp in self.waypoints]

    def load_layout(self, layout_name: str):
        """Load a map layout."""
        layout = MAP_LAYOUTS.get(layout_name, MAP_LAYOUTS['classic'])
        path_coords = layout['path']
        
        for row, col in path_coords:
            if 0 <= row < self.grid_height and 0 <= col < self.grid_width:
                self.grid[row][col] = 1
        
        self.start_pos = path_coords[0]
        self.end_pos = path_coords[-1]

    def calculate_waypoints(self) -> List[Tuple[int, int]]:
        """Calculate waypoints using pathfinding."""
        return bfs_pathfinding(self.grid, self.start_pos, self.end_pos)

    def is_buildable(self, grid_row: int, grid_col: int) -> bool:
        """Check if position is buildable."""
        if 0 <= grid_row < self.grid_height and 0 <= grid_col < self.grid_width:
            return self.grid[grid_row][grid_col] == 0
        return False

    def draw(self, surface: pygame.Surface):
        """Draw the map."""
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                x = col * self.grid_size
                y = row * self.grid_size
                
                if (row, col) == self.start_pos:
                    color = START_COLOR
                elif (row, col) == self.end_pos:
                    color = END_COLOR
                elif self.grid[row][col] == 1:
                    color = PATH_COLOR
                else:
                    color = GRASS_COLOR
                
                pygame.draw.rect(surface, color, (x, y, self.grid_size, self.grid_size))
                pygame.draw.rect(surface, DARK_GRAY, (x, y, self.grid_size, self.grid_size), 1)

    def get_start_position(self) -> Tuple[float, float]:
        """Get start position in pixels."""
        return grid_to_pixel(self.start_pos, self.grid_size)

    def get_end_position(self) -> Tuple[float, float]:
        """Get end position in pixels."""
        return grid_to_pixel(self.end_pos, self.grid_size)
EOF

mv src/map_enhanced.py src/map.py

echo "Map system updated!"
