"""Game constants and configuration."""

import pygame

# Window settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Grid settings
GRID_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
DARK_GREEN = (0, 128, 0)
DARK_RED = (139, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Path colors
PATH_COLOR = (101, 67, 33)
GRASS_COLOR = (34, 139, 34)
START_COLOR = (0, 200, 0)
END_COLOR = (200, 0, 0)

# Game settings
STARTING_HEALTH = 20
STARTING_MONEY = 650
BASE_ENEMY_REWARD = 10

# Tower types
TOWER_TYPES = {
    'basic': {
        'name': 'Basic Tower',
        'cost': 100,
        'damage': 10,
        'range': 120,
        'fire_rate': 1.0,  # shots per second
        'color': BLUE,
        'projectile_speed': 8,
        'description': 'Basic tower with balanced stats'
    },
    'sniper': {
        'name': 'Sniper Tower',
        'cost': 200,
        'damage': 50,
        'range': 250,
        'fire_rate': 0.5,
        'color': DARK_GREEN,
        'projectile_speed': 15,
        'description': 'Long range, high damage, slow fire rate'
    },
    'rapid': {
        'name': 'Rapid Tower',
        'cost': 150,
        'damage': 5,
        'range': 100,
        'fire_rate': 3.0,
        'color': ORANGE,
        'projectile_speed': 10,
        'description': 'Fast fire rate, low damage'
    },
    'splash': {
        'name': 'Splash Tower',
        'cost': 250,
        'damage': 15,
        'range': 110,
        'fire_rate': 0.8,
        'color': PURPLE,
        'projectile_speed': 6,
        'splash_radius': 60,
        'description': 'Deals area damage on impact'
    },
    'laser': {
        'name': 'Laser Tower',
        'cost': 300,
        'damage': 8,
        'range': 150,
        'fire_rate': 10.0,  # continuous beam
        'color': CYAN,
        'description': 'Continuous beam damage'
    }
}

# Enemy types
ENEMY_TYPES = {
    'basic': {
        'name': 'Basic Enemy',
        'health': 50,
        'speed': 2.0,
        'reward': 10,
        'color': RED,
        'size': 8
    },
    'fast': {
        'name': 'Fast Enemy',
        'health': 30,
        'speed': 4.0,
        'reward': 15,
        'color': YELLOW,
        'size': 7
    },
    'tank': {
        'name': 'Tank Enemy',
        'health': 200,
        'speed': 1.0,
        'reward': 30,
        'color': DARK_RED,
        'size': 12
    },
    'swarm': {
        'name': 'Swarm Enemy',
        'health': 20,
        'speed': 3.0,
        'reward': 5,
        'color': MAGENTA,
        'size': 6
    },
    'boss': {
        'name': 'Boss Enemy',
        'health': 500,
        'speed': 0.8,
        'reward': 100,
        'color': BLACK,
        'size': 16
    }
}

# Upgrade costs
UPGRADE_COST_MULTIPLIER = 1.5
MAX_UPGRADE_LEVEL = 3

# Wave settings
WAVES = [
    # Wave 1
    {'basic': 10},
    # Wave 2
    {'basic': 15, 'fast': 5},
    # Wave 3
    {'basic': 10, 'fast': 10},
    # Wave 4
    {'basic': 20, 'tank': 2},
    # Wave 5
    {'fast': 15, 'tank': 3},
    # Wave 6
    {'basic': 25, 'fast': 15, 'swarm': 10},
    # Wave 7
    {'tank': 5, 'fast': 20},
    # Wave 8
    {'basic': 30, 'fast': 20, 'tank': 5},
    # Wave 9
    {'swarm': 30, 'tank': 8},
    # Wave 10 - Boss wave
    {'boss': 1, 'basic': 20, 'fast': 20},
    # Wave 11+
    {'basic': 40, 'fast': 30, 'tank': 10, 'swarm': 20},
    {'basic': 50, 'fast': 40, 'tank': 15, 'boss': 1},
    {'swarm': 50, 'tank': 20, 'fast': 30},
    {'basic': 60, 'fast': 50, 'tank': 20, 'boss': 2},
    {'swarm': 80, 'tank': 30, 'boss': 1},
]

# UI settings
UI_PANEL_WIDTH = 400
UI_BUTTON_HEIGHT = 50
UI_PADDING = 10
UI_FONT_SIZE = 20
UI_TITLE_FONT_SIZE = 32
