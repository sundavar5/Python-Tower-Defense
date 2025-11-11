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
LIME = (0, 255, 0)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)
DARK_PURPLE = (75, 0, 130)
NEON_GREEN = (57, 255, 20)
ELECTRIC_BLUE = (125, 249, 255)

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
        'fire_rate': 1.0,
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
        'fire_rate': 10.0,
        'color': CYAN,
        'description': 'Continuous beam damage'
    },
    'ice': {
        'name': 'Ice Tower',
        'cost': 225,
        'damage': 8,
        'range': 130,
        'fire_rate': 1.2,
        'color': LIGHT_BLUE,
        'projectile_speed': 9,
        'slow_duration': 2.0,
        'slow_amount': 0.5,
        'description': 'Slows enemies by 50%'
    },
    'poison': {
        'name': 'Poison Tower',
        'cost': 275,
        'damage': 5,
        'range': 120,
        'fire_rate': 0.7,
        'color': NEON_GREEN,
        'projectile_speed': 7,
        'poison_damage': 3,
        'poison_duration': 5.0,
        'description': 'Deals 3 damage per second for 5s'
    },
    'electric': {
        'name': 'Electric Tower',
        'cost': 350,
        'damage': 20,
        'range': 140,
        'fire_rate': 1.5,
        'color': ELECTRIC_BLUE,
        'chain_count': 3,
        'chain_damage_reduction': 0.7,
        'description': 'Chains to 3 enemies, -30% dmg per jump'
    },
    'artillery': {
        'name': 'Artillery Tower',
        'cost': 400,
        'damage': 80,
        'range': 200,
        'fire_rate': 0.3,
        'color': MAROON,
        'projectile_speed': 10,
        'splash_radius': 80,
        'description': 'Massive damage and splash radius'
    },
    'support': {
        'name': 'Support Tower',
        'cost': 180,
        'damage': 0,
        'range': 160,
        'fire_rate': 0,
        'color': GOLD,
        'buff_range': 160,
        'damage_buff': 1.25,
        'description': 'Increases nearby tower damage by 25%'
    },
    'flame': {
        'name': 'Flame Tower',
        'cost': 280,
        'damage': 12,
        'range': 100,
        'fire_rate': 2.0,
        'color': ORANGE,
        'burn_damage': 4,
        'burn_duration': 3.0,
        'description': 'Burns enemies for 4 damage/sec'
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
    },
    'armored': {
        'name': 'Armored Enemy',
        'health': 120,
        'speed': 1.5,
        'reward': 25,
        'color': SILVER,
        'size': 10,
        'armor': 0.5,  # 50% damage reduction
        'description': 'Takes 50% reduced damage'
    },
    'healer': {
        'name': 'Healer Enemy',
        'health': 80,
        'speed': 1.8,
        'reward': 35,
        'color': PINK,
        'size': 9,
        'heal_range': 80,
        'heal_amount': 2,
        'heal_rate': 1.0,
        'description': 'Heals nearby enemies'
    },
    'speedy': {
        'name': 'Speedy Enemy',
        'health': 40,
        'speed': 5.0,
        'reward': 20,
        'color': LIME,
        'size': 7,
        'description': 'Very fast, hard to hit'
    },
    'regenerating': {
        'name': 'Regenerating Enemy',
        'health': 100,
        'speed': 2.0,
        'reward': 28,
        'color': TEAL,
        'size': 9,
        'regen_rate': 1.5,
        'description': 'Regenerates 1.5 HP per second'
    },
    'flying': {
        'name': 'Flying Enemy',
        'health': 60,
        'speed': 3.5,
        'reward': 22,
        'color': LIGHT_BLUE,
        'size': 8,
        'flying': True,
        'description': 'Can only be hit by certain towers'
    },
    'ghost': {
        'name': 'Ghost Enemy',
        'health': 70,
        'speed': 2.5,
        'reward': 30,
        'color': (200, 200, 255),
        'size': 9,
        'immune_to_slow': True,
        'description': 'Immune to slow effects'
    },
    'shielded': {
        'name': 'Shielded Enemy',
        'health': 90,
        'speed': 1.8,
        'reward': 32,
        'color': NAVY,
        'size': 10,
        'shield': 50,
        'description': 'Has 50 HP shield that regenerates'
    },
    'mega_boss': {
        'name': 'Mega Boss',
        'health': 2000,
        'speed': 0.6,
        'reward': 500,
        'color': (50, 0, 50),
        'size': 20,
        'armor': 0.3,
        'description': 'Massive health and 30% damage reduction'
    }
}

# Upgrade costs
UPGRADE_COST_MULTIPLIER = 1.5
MAX_UPGRADE_LEVEL = 3

# Wave settings
WAVES = [
    # Wave 1-5: Early game
    {'basic': 10},
    {'basic': 15, 'fast': 5},
    {'basic': 10, 'fast': 10},
    {'basic': 20, 'tank': 2},
    {'fast': 15, 'tank': 3, 'swarm': 5},
    # Wave 6-10: Mid game
    {'basic': 25, 'fast': 15, 'swarm': 10, 'armored': 2},
    {'tank': 5, 'fast': 20, 'healer': 1},
    {'basic': 30, 'fast': 20, 'tank': 5, 'speedy': 8},
    {'swarm': 30, 'tank': 8, 'regenerating': 3},
    {'boss': 1, 'basic': 20, 'fast': 20, 'armored': 5},
    # Wave 11-15: Late game
    {'basic': 40, 'fast': 30, 'tank': 10, 'swarm': 20, 'flying': 10},
    {'healer': 3, 'tank': 15, 'armored': 8, 'regenerating': 5},
    {'swarm': 50, 'speedy': 20, 'fast': 30, 'ghost': 5},
    {'tank': 20, 'armored': 15, 'shielded': 10, 'boss': 1},
    {'basic': 50, 'fast': 40, 'tank': 20, 'flying': 15, 'healer': 3},
    # Wave 16-20: Expert
    {'swarm': 60, 'speedy': 30, 'ghost': 10, 'regenerating': 10},
    {'tank': 25, 'armored': 20, 'shielded': 15, 'boss': 2},
    {'flying': 30, 'fast': 50, 'speedy': 25, 'healer': 5},
    {'basic': 80, 'tank': 30, 'armored': 25, 'regenerating': 15},
    {'mega_boss': 1, 'boss': 2, 'healer': 5, 'armored': 20},
    # Wave 21-25: Ultimate challenge
    {'swarm': 100, 'speedy': 50, 'flying': 40, 'ghost': 20},
    {'tank': 40, 'armored': 35, 'shielded': 25, 'regenerating': 20},
    {'boss': 3, 'mega_boss': 1, 'healer': 8, 'armored': 30},
    {'fast': 80, 'speedy': 60, 'flying': 50, 'ghost': 30},
    {'mega_boss': 2, 'boss': 4, 'armored': 40, 'shielded': 30},
]

# Targeting modes
TARGET_MODES = ['first', 'last', 'closest', 'strongest', 'weakest']

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {
        'name': 'Easy',
        'health_multiplier': 1.5,
        'money_multiplier': 1.5,
        'enemy_health_multiplier': 0.7,
        'enemy_speed_multiplier': 0.8,
        'description': 'Relaxed gameplay for beginners'
    },
    'normal': {
        'name': 'Normal',
        'health_multiplier': 1.0,
        'money_multiplier': 1.0,
        'enemy_health_multiplier': 1.0,
        'enemy_speed_multiplier': 1.0,
        'description': 'Balanced experience'
    },
    'hard': {
        'name': 'Hard',
        'health_multiplier': 0.7,
        'money_multiplier': 0.8,
        'enemy_health_multiplier': 1.3,
        'enemy_speed_multiplier': 1.2,
        'description': 'Challenging gameplay'
    },
    'extreme': {
        'name': 'Extreme',
        'health_multiplier': 0.5,
        'money_multiplier': 0.6,
        'enemy_health_multiplier': 1.6,
        'enemy_speed_multiplier': 1.4,
        'description': 'For veterans only!'
    }
}

# Special abilities
SPECIAL_ABILITIES = {
    'airstrike': {
        'name': 'Air Strike',
        'cost': 150,
        'cooldown': 45.0,
        'damage': 100,
        'radius': 120,
        'description': 'Call an air strike dealing massive area damage'
    },
    'freeze_all': {
        'name': 'Freeze All',
        'cost': 120,
        'cooldown': 60.0,
        'duration': 3.0,
        'description': 'Freeze all enemies for 3 seconds'
    },
    'cash_boost': {
        'name': 'Cash Boost',
        'cost': 100,
        'cooldown': 90.0,
        'duration': 10.0,
        'multiplier': 2.0,
        'description': 'Double money earned for 10 seconds'
    },
    'damage_boost': {
        'name': 'Damage Boost',
        'cost': 80,
        'cooldown': 50.0,
        'duration': 8.0,
        'multiplier': 2.5,
        'description': 'Increase all tower damage by 150% for 8 seconds'
    },
    'health_restore': {
        'name': 'Health Restore',
        'cost': 200,
        'cooldown': 120.0,
        'restore_amount': 10,
        'description': 'Restore 10 health'
    }
}

# Achievements
ACHIEVEMENTS = {
    'first_blood': {
        'name': 'First Blood',
        'description': 'Defeat your first enemy',
        'condition': 'kills',
        'threshold': 1
    },
    'tower_master': {
        'name': 'Tower Master',
        'description': 'Build 10 towers',
        'condition': 'towers_built',
        'threshold': 10
    },
    'wave_survivor': {
        'name': 'Wave Survivor',
        'description': 'Complete 10 waves',
        'condition': 'waves',
        'threshold': 10
    },
    'sharpshooter': {
        'name': 'Sharpshooter',
        'description': 'Defeat 100 enemies',
        'condition': 'kills',
        'threshold': 100
    },
    'fortress_builder': {
        'name': 'Fortress Builder',
        'description': 'Build 25 towers',
        'condition': 'towers_built',
        'threshold': 25
    },
    'veteran': {
        'name': 'Veteran',
        'description': 'Complete 20 waves',
        'condition': 'waves',
        'threshold': 20
    },
    'exterminator': {
        'name': 'Exterminator',
        'description': 'Defeat 500 enemies',
        'condition': 'kills',
        'threshold': 500
    },
    'boss_slayer': {
        'name': 'Boss Slayer',
        'description': 'Defeat 5 boss enemies',
        'condition': 'boss_kills',
        'threshold': 5
    },
    'mega_money': {
        'name': 'Mega Money',
        'description': 'Earn $10,000 total',
        'condition': 'money_earned',
        'threshold': 10000
    },
    'perfect_defense': {
        'name': 'Perfect Defense',
        'description': 'Complete a wave without losing health',
        'condition': 'perfect_wave',
        'threshold': 1
    },
    'upgrade_enthusiast': {
        'name': 'Upgrade Enthusiast',
        'description': 'Upgrade towers 20 times',
        'condition': 'upgrades',
        'threshold': 20
    },
    'the_survivor': {
        'name': 'The Survivor',
        'description': 'Reach wave 25',
        'condition': 'waves',
        'threshold': 25
    }
}

# Map layouts
MAP_LAYOUTS = {
    'classic': {
        'name': 'Classic',
        'path': [
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
            (8, 6), (9, 6), (10, 6),
            (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12),
            (9, 12), (8, 12), (7, 12), (6, 12), (5, 12), (4, 12), (3, 12),
            (3, 13), (3, 14), (3, 15), (3, 16), (3, 17),
            (4, 17), (5, 17), (6, 17), (7, 17), (8, 17), (9, 17),
            (10, 17), (11, 17), (12, 17), (13, 17), (14, 17),
        ],
        'difficulty': 'normal'
    },
    'spiral': {
        'name': 'Spiral',
        'path': [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
            (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
            (6, 7), (5, 7), (4, 7), (3, 7), (2, 7),
            (2, 8), (2, 9), (2, 10), (2, 11), (2, 12),
            (3, 12), (4, 12), (5, 12), (6, 12), (7, 12),
            (7, 13), (7, 14), (7, 15), (7, 16), (7, 17), (7, 18), (7, 19),
        ],
        'difficulty': 'easy'
    },
    'zigzag': {
        'name': 'Zigzag',
        'path': [
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
            (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4),
            (8, 5), (8, 6), (8, 7), (8, 8),
            (7, 8), (6, 8), (5, 8), (4, 8), (3, 8),
            (3, 9), (3, 10), (3, 11), (3, 12),
            (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12),
            (9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (9, 18), (9, 19),
        ],
        'difficulty': 'normal'
    },
    'cross': {
        'name': 'Cross',
        'path': [
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
            (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7),
        ],
        'difficulty': 'hard'
    },
    'maze': {
        'name': 'Maze',
        'path': [
            (1, 0), (2, 0), (3, 0),
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
            (4, 5), (5, 5), (6, 5), (7, 5), (8, 5),
            (8, 6), (8, 7), (8, 8), (8, 9),
            (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9), (1, 9),
            (1, 10), (1, 11), (1, 12), (1, 13),
            (2, 13), (3, 13), (4, 13), (5, 13), (6, 13), (7, 13), (8, 13),
            (8, 14), (8, 15), (8, 16), (8, 17), (8, 18), (8, 19),
        ],
        'difficulty': 'hard'
    },
    'double': {
        'name': 'Double Path',
        'path': [
            (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
            (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14),
            (11, 0), (11, 1), (11, 2), (11, 3), (11, 4), (11, 5), (11, 6),
            (11, 7), (11, 8), (11, 9), (11, 10), (11, 11), (11, 12), (11, 13), (11, 14),
        ],
        'difficulty': 'extreme'
    }
}

# Particle effects settings
PARTICLE_LIFETIME = 1.0
MAX_PARTICLES = 500

# UI settings
UI_PANEL_WIDTH = 400
UI_BUTTON_HEIGHT = 50
UI_PADDING = 10
UI_FONT_SIZE = 20
UI_TITLE_FONT_SIZE = 32

# Sound settings (for future implementation)
ENABLE_SOUND = False
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7
