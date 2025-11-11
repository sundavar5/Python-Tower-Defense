# Tower Defense Game

A fully-fledged tower defense game built with Python and Pygame featuring multiple tower types, enemy waves, strategic gameplay, and a polished user interface.

## Features

### 🎮 Gameplay
- **Wave-based Combat**: Face increasingly difficult waves of enemies
- **Strategic Tower Placement**: Plan your defense on a grid-based map
- **Resource Management**: Earn money from defeating enemies to build and upgrade towers
- **Progressive Difficulty**: 15+ waves with scaling enemy stats

### 🗼 Tower Types

1. **Basic Tower** ($100)
   - Balanced stats for general-purpose defense
   - Damage: 10 | Range: 120 | Fire Rate: 1.0/s

2. **Sniper Tower** ($200)
   - Long-range, high-damage specialist
   - Damage: 50 | Range: 250 | Fire Rate: 0.5/s

3. **Rapid Tower** ($150)
   - Fast-firing tower with lower damage
   - Damage: 5 | Range: 100 | Fire Rate: 3.0/s

4. **Splash Tower** ($250)
   - Deals area-of-effect damage on impact
   - Damage: 15 | Range: 110 | Splash Radius: 60

5. **Laser Tower** ($300)
   - Continuous beam that deals constant damage
   - Damage: 8/s | Range: 150

### 👾 Enemy Types

- **Basic Enemy**: Standard health and speed
- **Fast Enemy**: Quick but fragile
- **Tank Enemy**: Slow but extremely durable
- **Swarm Enemy**: Low health, appears in large numbers
- **Boss Enemy**: Massive health pool, appears in boss waves

### ✨ Game Features

- **Tower Upgrades**: Upgrade towers up to level 3 for increased damage, range, and fire rate
- **Sell Towers**: Reclaim 70% of your investment if you need to reposition
- **Smart Targeting**: Towers automatically target enemies furthest along the path
- **Visual Effects**: Projectiles, explosions, laser beams, and health bars
- **Intuitive UI**: Clean interface with tower stats and game information
- **Restart Functionality**: Quickly restart after game over

## Installation

### Requirements
- Python 3.7 or higher
- Pygame 2.5.0 or higher

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Python-Tower-Defense
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

### Starting the Game

Run the game with:
```bash
python main.py
```

### Controls

| Action | Control |
|--------|---------|
| Place/Select Tower | Left Click |
| Cancel/Deselect | Right Click or ESC |
| Start Wave | Space or Start Wave Button |
| Upgrade Tower | Click Upgrade Button (when tower selected) |
| Sell Tower | Click Sell Button (when tower selected) |

### Gameplay Guide

1. **Starting Out**
   - You begin with 20 health and $650
   - Place towers on the green grass areas (not on the brown path)
   - Click a tower type from the shop, then click on the map to place it

2. **Managing Waves**
   - Click "Start Wave" or press Space to begin a wave
   - Enemies follow the path from green (start) to red (end)
   - Defeat enemies before they reach the end to prevent losing health

3. **Earning Money**
   - Defeating enemies rewards you with money
   - Use money to build more towers or upgrade existing ones
   - Each enemy type has different reward values

4. **Strategy Tips**
   - Place towers at corners where enemies slow down
   - Mix tower types for balanced defense
   - Upgrade high-value towers rather than building many weak ones
   - Use Splash Towers for clustered enemies
   - Save money for tough waves (every 5th wave has bosses)

5. **Upgrading**
   - Select a tower by clicking on it
   - Click the "Upgrade" button (up to 3 levels)
   - Each level increases damage (×1.5), range (×1.1), and fire rate (×1.2)

6. **Victory Conditions**
   - Survive as many waves as possible
   - Game ends when health reaches 0
   - Your score is based on money earned from defeating enemies

## Game Structure

```
Python-Tower-Defense/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── README.md           # This file
└── src/
    ├── __init__.py     # Package init
    ├── constants.py    # Game configuration
    ├── game.py         # Main game loop and state
    ├── map.py          # Map and pathfinding
    ├── enemy.py        # Enemy classes and wave manager
    ├── tower.py        # Tower classes
    ├── projectile.py   # Projectile and laser systems
    ├── ui.py           # UI components
    └── utils.py        # Utility functions
```

## Customization

### Modifying Game Constants

Edit `src/constants.py` to customize:
- Tower stats (damage, range, cost, fire rate)
- Enemy stats (health, speed, rewards)
- Wave compositions
- Starting resources
- Grid size and window dimensions

### Adding New Waves

Add new wave configurations to the `WAVES` list in `src/constants.py`:

```python
WAVES = [
    {'basic': 10, 'fast': 5},  # Wave 1
    {'tank': 3, 'swarm': 20},  # Wave 2
    # Add more...
]
```

### Creating Custom Tower Types

1. Define tower stats in `TOWER_TYPES` in `src/constants.py`
2. Create a tower class in `src/tower.py` (if special behavior needed)
3. Add to the tower factory in `src/tower.py`

## Technical Details

### Architecture

- **Game Loop**: Fixed timestep at 60 FPS
- **Pathfinding**: BFS algorithm for enemy path calculation
- **Targeting**: Priority system targeting enemies furthest along path
- **Rendering**: Pygame-based 2D graphics with layered rendering

### Performance

- Optimized for 60 FPS with 50+ enemies and 20+ towers
- Efficient collision detection using distance calculations
- Minimal object creation during gameplay

## Troubleshooting

### Game won't start
- Ensure Python 3.7+ is installed: `python --version`
- Install Pygame: `pip install pygame`

### Performance issues
- Close other applications
- Reduce number of enemies per wave in `src/constants.py`

### Display issues
- Check your screen resolution supports 1200x800
- Modify `WINDOW_WIDTH` and `WINDOW_HEIGHT` in `src/constants.py`

## Credits

Built with:
- Python 3
- Pygame 2.5.0

## License

See LICENSE file for details.

## Future Enhancements

Potential features for future versions:
- Multiple map layouts
- More tower types (freeze, poison, electric)
- Enemy special abilities
- Achievement system
- Sound effects and music
- Save/load game state
- Difficulty levels
- Multiplayer co-op mode

---

Enjoy defending your territory! 🎮🗼
