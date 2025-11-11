# Tower Defense Game - MASSIVELY ENHANCED EDITION

A comprehensively featured tower defense game built with Python and Pygame. This game includes **11 tower types**, **13 enemy types**, **25 waves**, **6 map layouts**, **4 difficulty levels**, **special abilities**, **achievements**, and much more!

## 🎮 **MAJOR FEATURES**

### **Content Overview**
- ✅ **11 Unique Tower Types** with special abilities
- ✅ **13 Enemy Types** with unique behaviors and abilities
- ✅ **25 Progressive Waves** with increasing difficulty
- ✅ **6 Different Map Layouts** to master
- ✅ **4 Difficulty Levels** (Easy, Normal, Hard, Extreme)
- ✅ **5 Special Abilities** for strategic gameplay
- ✅ **12 Achievements** to unlock
- ✅ **Particle Effects System** for visual feedback
- ✅ **Statistics Tracking** for all your accomplishments
- ✅ **Save/Load System** to persist progress
- ✅ **Tower Targeting Modes** (First, Last, Closest, Strongest, Weakest)
- ✅ **Status Effect System** (Slow, Poison, Burn, Freeze)

## 🗼 **TOWER TYPES** (11 Total)

### Basic Towers
1. **Basic Tower** ($100)
   - Balanced stats for general defense
   - Damage: 10 | Range: 120 | Fire Rate: 1.0/s

2. **Rapid Tower** ($150)
   - Fast firing, lower damage
   - Damage: 5 | Range: 100 | Fire Rate: 3.0/s

3. **Sniper Tower** ($200)
   - Long range, high single-target damage
   - Damage: 50 | Range: 250 | Fire Rate: 0.5/s

### Area Effect Towers
4. **Splash Tower** ($250)
   - Deals area-of-effect damage on impact
   - Damage: 15 | Range: 110 | Splash: 60

5. **Artillery Tower** ($400)
   - Massive damage and huge splash radius
   - Damage: 80 | Range: 200 | Splash: 80

### Status Effect Towers
6. **Ice Tower** ($225)
   - Slows enemies by 50% for 2 seconds
   - Damage: 8 | Range: 130 | Fire Rate: 1.2/s

7. **Poison Tower** ($275)
   - Deals 3 damage/second for 5 seconds
   - Damage: 5 | Range: 120 | Fire Rate: 0.7/s

8. **Flame Tower** ($280)
   - Burns enemies for 4 damage/second for 3 seconds
   - Damage: 12 | Range: 100 | Fire Rate: 2.0/s

### Special Towers
9. **Laser Tower** ($300)
   - Continuous beam that deals constant damage
   - Damage: 8/s | Range: 150

10. **Electric Tower** ($350)
    - Chains to 3 enemies with -30% damage per jump
    - Damage: 20 | Range: 140 | Chains: 3

11. **Support Tower** ($180)
    - Increases nearby tower damage by 25%
    - Range: 160 | Buff: +25% damage

## 👾 **ENEMY TYPES** (13 Total)

### Standard Enemies
1. **Basic Enemy** - Standard health and speed
2. **Fast Enemy** - Quick but fragile
3. **Swarm Enemy** - Low health, appears in large numbers
4. **Tank Enemy** - Slow but extremely durable
5. **Speedy Enemy** - Very fast, hard to hit

### Special Ability Enemies
6. **Armored Enemy** - Takes 50% reduced damage from all sources
7. **Healer Enemy** - Heals nearby enemies over time
8. **Regenerating Enemy** - Regenerates 1.5 HP per second
9. **Shielded Enemy** - Has 50 HP regenerating shield
10. **Ghost Enemy** - Immune to slow effects

### Advanced Enemies
11. **Flying Enemy** - Can only be hit by certain towers
12. **Boss Enemy** - Massive health pool
13. **Mega Boss** - 2000 HP with 30% damage reduction

## 🗺️ **MAP LAYOUTS** (6 Total)

1. **Classic** - Traditional winding path (Normal difficulty)
2. **Spiral** - Spiral pattern with long path (Easy difficulty)
3. **Zigzag** - Back-and-forth pattern (Normal difficulty)
4. **Cross** - Short, direct path (Hard difficulty)
5. **Maze** - Complex maze-like path (Hard difficulty)
6. **Double Path** - Two separate paths! (Extreme difficulty)

## 🎯 **DIFFICULTY LEVELS**

| Difficulty | Your Health | Your Money | Enemy Health | Enemy Speed |
|------------|-------------|------------|--------------|-------------|
| **Easy**     | 150%        | 150%       | 70%          | 80%         |
| **Normal**   | 100%        | 100%       | 100%         | 100%        |
| **Hard**     | 70%         | 80%        | 130%         | 120%        |
| **Extreme**  | 50%         | 60%        | 160%         | 140%        |

## ⚡ **SPECIAL ABILITIES**

1. **Air Strike** ($150, 45s cooldown)
   - Call an air strike dealing 100 damage in large radius

2. **Freeze All** ($120, 60s cooldown)
   - Freeze all enemies for 3 seconds

3. **Cash Boost** ($100, 90s cooldown)
   - Double money earned for 10 seconds

4. **Damage Boost** ($80, 50s cooldown)
   - Increase all tower damage by 150% for 8 seconds

5. **Health Restore** ($200, 120s cooldown)
   - Restore 10 health

## 🏆 **ACHIEVEMENTS** (12 Total)

- **First Blood** - Defeat your first enemy
- **Sharpshooter** - Defeat 100 enemies
- **Exterminator** - Defeat 500 enemies
- **Boss Slayer** - Defeat 5 boss enemies
- **Tower Master** - Build 10 towers
- **Fortress Builder** - Build 25 towers
- **Upgrade Enthusiast** - Upgrade towers 20 times
- **Wave Survivor** - Complete 10 waves
- **Veteran** - Complete 20 waves
- **The Survivor** - Reach wave 25
- **Mega Money** - Earn $10,000 total
- **Perfect Defense** - Complete a wave without losing health

## 📊 **STATISTICS TRACKING**

The game tracks comprehensive statistics:
- Total kills and boss kills
- Towers built, sold, and upgraded
- Waves completed and perfect waves
- Money earned and spent
- Damage dealt and lives lost
- Highest wave reached and score
- Total playtime

## 🎨 **VISUAL EFFECTS**

### Particle System
- Explosion effects for enemy deaths
- Impact sparks for projectile hits
- Healing effects (green rising particles)
- Freeze effects (ice blue particles)
- Poison clouds (green mist)
- Electric sparks (blue lightning)
- Fire bursts (orange/red flames)
- Money collection effects (gold particles)
- Airstrike massive explosions

### Status Effect Indicators
- Colored dots above enemies show active effects
- Shield rings around shielded enemies
- Armor indicators on armored enemies
- Health and shield bars
- Visual effects for burns, poison, slow, freeze

## 🎮 **INSTALLATION & SETUP**

### Requirements
- Python 3.7 or higher
- Pygame 2.5.0 or higher

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Python-Tower-Defense

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## 🕹️ **CONTROLS**

| Action | Control |
|--------|---------|
| Place/Select Tower | Left Click |
| Cancel/Deselect | Right Click or ESC |
| Start Wave | Space or Button |
| Upgrade Tower | Click Upgrade (tower selected) |
| Sell Tower | Click Sell (tower selected) |
| Use Ability | Click ability button |

## 📖 **HOW TO PLAY**

### Getting Started
1. You start with 20 health and $650 (varies by difficulty)
2. Purchase towers from the shop on the right
3. Place towers on grass (not on the brown path)
4. Start waves to spawn enemies
5. Earn money by defeating enemies
6. Upgrade towers or build more defenses

### Advanced Strategy

#### Tower Placement
- **Corners** - Place high-damage towers where enemies slow down
- **Chokepoints** - Use splash towers where enemies cluster
- **Support Towers** - Place near groups of other towers for damage buff
- **Ice Towers** - Place early in path to slow enemies for longer

#### Enemy Counters
- **Armored** → High damage towers (Sniper, Artillery)
- **Fast/Speedy** → Area effect or rapid fire towers
- **Healers** → Kill first! Focus fire with snipers
- **Regenerating** → Burst damage towers
- **Shielded** → Sustained damage (Laser, Rapid)
- **Bosses** → Everything! All hands on deck!

#### Tower Synergies
- Support + Any tower = +25% damage
- Ice + High damage = More time to deal damage
- Poison + Burn = Multiple damage over time effects
- Electric + Swarms = Chain lightning massacres

### Special Ability Usage
- **Save Air Strikes** for boss waves or emergencies
- **Freeze All** when overwhelmed by fast enemies
- **Cash Boost** during high-reward waves
- **Damage Boost** for boss waves
- **Health Restore** as last resort

## 🏗️ **PROJECT STRUCTURE**

```
Python-Tower-Defense/
├── main.py                 # Game entry point
├── requirements.txt        # Dependencies
├── README.md              # This file
├── test_imports.py        # Import verification
└── src/
    ├── __init__.py        # Package init
    ├── constants.py       # Game configuration (11 towers, 13 enemies, etc.)
    ├── utils.py           # Utility functions
    ├── map.py             # Map system with 6 layouts
    ├── enemy.py           # Enhanced enemy system with status effects
    ├── tower.py           # Tower classes
    ├── projectile.py      # Projectile and laser systems
    ├── particles.py       # Particle effects system (NEW!)
    ├── statistics.py      # Stats and achievements (NEW!)
    ├── abilities.py       # Special abilities system (NEW!)
    ├── ui.py              # UI components
    ├── game.py            # Main game loop
    └── *_backup.py        # Backup files
```

## 🔧 **CUSTOMIZATION**

### Adding New Content

#### Custom Tower
Edit `src/constants.py` and add to `TOWER_TYPES`:
```python
'my_tower': {
    'name': 'My Tower',
    'cost': 150,
    'damage': 20,
    'range': 140,
    'fire_rate': 1.5,
    'color': (255, 100, 0),
    'projectile_speed': 12,
    'description': 'My custom tower'
}
```

#### Custom Enemy
Add to `ENEMY_TYPES` in `src/constants.py`:
```python
'my_enemy': {
    'name': 'My Enemy',
    'health': 100,
    'speed': 2.5,
    'reward': 20,
    'color': (100, 255, 100),
    'size': 10,
    'armor': 0.25,  # Optional special attributes
    'regen_rate': 1.0
}
```

#### Custom Wave
Add to `WAVES` list:
```python
{'basic': 50, 'tank': 10, 'my_enemy': 20}
```

#### Custom Map Layout
Add to `MAP_LAYOUTS`:
```python
'my_map': {
    'name': 'My Map',
    'path': [
        (0, 0), (1, 0), (2, 0), ...  # List of (row, col) positions
    ],
    'difficulty': 'normal'
}
```

## 🎓 **ADVANCED FEATURES**

### Status Effects System
Enemies can be affected by:
- **Slow** - Reduces movement speed
- **Poison** - Deals damage over time
- **Burn** - Fire damage over time
- **Freeze** - Stops movement completely

### Tower Targeting Modes
*(Framework implemented, full UI integration pending)*
- **First** - Target enemy furthest along path
- **Last** - Target enemy closest to start
- **Closest** - Target nearest enemy
- **Strongest** - Target enemy with most HP
- **Weakest** - Target enemy with least HP

### Save System
Progress automatically saved including:
- All-time statistics
- Unlocked achievements
- High scores and records

Location: `towerdefense_save.json`

## 🐛 **TROUBLESHOOTING**

### Import Errors
```bash
# Verify all imports
python test_imports.py
```

### Performance Issues
- Reduce particles in `src/constants.py` (`MAX_PARTICLES`)
- Lower wave enemy counts
- Close other applications

### Display Issues
- Adjust `WINDOW_WIDTH` and `WINDOW_HEIGHT` in `src/constants.py`
- Ensure screen resolution supports 1200x800

## 📈 **GAME STATISTICS**

Current Content:
- **11** Tower Types (up from 5)
- **13** Enemy Types (up from 5)
- **25** Wave Configurations (up from 15)
- **6** Map Layouts (up from 1)
- **4** Difficulty Levels (NEW!)
- **5** Special Abilities (NEW!)
- **12** Achievements (NEW!)
- **Comprehensive particle effects** (NEW!)
- **Full statistics tracking** (NEW!)
- **Save/load system** (NEW!)

## 🎯 **FUTURE ENHANCEMENTS**

Potential additions:
- Full UI integration for all features
- Main menu with difficulty/map selection
- Sound effects and music
- Multiplayer co-op mode
- More tower types (Slow, Teleport, Mind Control)
- More enemy abilities (Splitting, Invisible, Teleporting)
- Tower special abilities and activated powers
- Campaign mode with story
- Custom map editor
- Steam achievements integration

## 📄 **LICENSE**

See LICENSE file for details.

## 🙏 **CREDITS**

Built with:
- Python 3
- Pygame 2.5+

### New Systems Added
- Particle Effects System
- Achievement System
- Statistics Tracking
- Special Abilities System
- Multiple Map Layouts
- Difficulty Levels
- Enhanced Enemy AI
- Status Effects System
- Save/Load System

---

## 🚀 **QUICK START GUIDE**

1. **Install**: `pip install -r requirements.txt`
2. **Run**: `python main.py`
3. **Build** a few basic towers
4. **Start Wave** with Space
5. **Upgrade** towers when you have money
6. **Experiment** with different tower types
7. **Try** the special abilities
8. **Unlock** achievements
9. **Challenge** yourself with higher difficulties!

**Enjoy the massively enhanced tower defense experience!** 🎮🗼✨
