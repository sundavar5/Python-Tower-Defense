"""Main game logic and state management."""

import pygame
from typing import List, Optional, Tuple
from src.constants import *
from src.map import GameMap
from src.enemy import WaveManager
from src.tower import Tower, create_tower
from src.ui import GameUI, GameOverScreen
from src.utils import pixel_to_grid, distance
from src.projectile import SplashProjectile
from src.particles import ParticleSystem
from src.statistics import Statistics, AchievementSystem, SaveSystem
from src.abilities import AbilityManager
from src.sound import SoundManager


class Game:
    """Main game class."""

    def __init__(self, difficulty: str = 'normal', map_layout: str = 'classic'):
        """Initialize the game."""
        # Pygame initialization
        pygame.init()
        self.fullscreen = False
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game settings
        self.difficulty = difficulty
        self.map_layout = map_layout
        self.difficulty_settings = DIFFICULTY_SETTINGS[difficulty]

        # Game state
        self.game_active = True
        self.victory = False

        # Initialize game objects
        self.game_map = GameMap(map_layout)
        difficulty_mult = {
            'health': self.difficulty_settings['enemy_health_multiplier'],
            'speed': self.difficulty_settings['enemy_speed_multiplier']
        }
        self.wave_manager = WaveManager(self.game_map.waypoints_pixel, difficulty_mult)
        self.towers: List[Tower] = []

        # Game resources (apply difficulty multipliers)
        self.health = int(STARTING_HEALTH * self.difficulty_settings['health_multiplier'])
        self.money = int(STARTING_MONEY * self.difficulty_settings['money_multiplier'])
        self.score = 0

        # UI
        self.ui = GameUI(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.game_over_screen = GameOverScreen(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Tower placement
        self.placing_tower_type: Optional[str] = None
        self.selected_tower: Optional[Tower] = None

        # Particles and effects
        self.particle_system = ParticleSystem()

        # Statistics and achievements
        self.statistics = Statistics()
        self.achievement_system = AchievementSystem(self.statistics)
        self.save_system = SaveSystem()

        # Load saved data
        saved_data = self.save_system.load()
        if saved_data:
            self.statistics.load_from_dict(saved_data.get('statistics', {}))
            self.achievement_system.load_from_dict(saved_data.get('achievements', {}))

        # Special abilities
        self.ability_manager = AbilityManager()

        # Sound manager
        self.sound_manager = SoundManager(enabled=True)

        # Track wave health at start for perfect wave achievement
        self.wave_start_health = self.health

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            self.handle_events()

            if self.game_active:
                self.update(dt)

            self.draw()

        pygame.quit()

    def handle_events(self):
        """Handle user input events."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

                if self.game_active:
                    self.handle_game_click(mouse_pos)
                else:
                    # Game over - check for restart
                    if self.game_over_screen.is_restart_clicked(mouse_pos):
                        self.restart_game()

            # Right click to cancel placement or deselect
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.placing_tower_type = None
                self.selected_tower = None
                if self.ui.selected_tower:
                    self.ui.selected_tower.selected = False
                    self.ui.selected_tower = None

            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.placing_tower_type = None
                    self.selected_tower = None
                if event.key == pygame.K_SPACE and self.game_active:
                    if self.wave_manager.is_wave_complete():
                        self.wave_manager.start_wave()
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()

        # Update UI
        if self.game_active:
            self.ui.update(mouse_pos, self.money, self.ability_manager)
        else:
            self.game_over_screen.update(mouse_pos)

    def handle_game_click(self, mouse_pos: Tuple[int, int]):
        """Handle clicks during active gameplay."""
        # Check UI button clicks first
        # Special ability buttons
        ability_type = self.ui.handle_ability_button_click(mouse_pos)
        if ability_type:
            self.use_ability(ability_type, mouse_pos)
            return

        # Tower selection buttons
        tower_type = self.ui.handle_tower_button_click(mouse_pos)
        if tower_type:
            self.placing_tower_type = tower_type
            self.selected_tower = None
            if self.ui.selected_tower:
                self.ui.selected_tower.selected = False
                self.ui.selected_tower = None
            return

        # Start wave button
        if self.ui.is_start_wave_clicked(mouse_pos):
            if self.wave_manager.is_wave_complete():
                self.wave_manager.start_wave()
            return

        # Upgrade button
        if self.ui.is_upgrade_clicked(mouse_pos) and self.selected_tower:
            upgrade_cost = self.selected_tower.get_upgrade_cost()
            if upgrade_cost > 0 and self.money >= upgrade_cost:
                if self.selected_tower.upgrade():
                    self.money -= upgrade_cost
                    self.statistics.money_spent += upgrade_cost
                    self.statistics.towers_upgraded += 1
                    # Sound and particle effects
                    self.sound_manager.play_tower_upgrade()
                    self.particle_system.create_money_collect(
                        self.selected_tower.x, self.selected_tower.y
                    )
            return

        # Sell button
        if self.ui.is_sell_clicked(mouse_pos) and self.selected_tower:
            sell_value = self.selected_tower.get_sell_value()
            self.money += sell_value
            self.statistics.towers_sold += 1
            # Sound and particle effects
            self.sound_manager.play_tower_sell()
            self.particle_system.create_explosion(
                self.selected_tower.x, self.selected_tower.y, GRAY
            )
            self.towers.remove(self.selected_tower)
            self.selected_tower = None
            self.ui.selected_tower = None
            return

        # Check if click is on game area (not UI panel)
        if mouse_pos[0] >= self.ui.panel_x:
            return

        # Handle tower placement or selection
        if self.placing_tower_type:
            self.try_place_tower(mouse_pos)
        else:
            self.try_select_tower(mouse_pos)

    def try_place_tower(self, mouse_pos: Tuple[int, int]):
        """Try to place a tower at mouse position."""
        grid_pos = pixel_to_grid(mouse_pos, GRID_SIZE)

        # Check if position is valid
        if not self.is_valid_tower_placement(grid_pos):
            return

        # Get tower cost
        tower_cost = TOWER_TYPES[self.placing_tower_type]['cost']

        # Check if player has enough money
        if self.money < tower_cost:
            return

        # Place tower
        tower = create_tower(self.placing_tower_type, grid_pos, GRID_SIZE)
        self.towers.append(tower)
        self.money -= tower_cost
        self.statistics.money_spent += tower_cost
        self.statistics.towers_built += 1

        # Sound and particle effects
        self.sound_manager.play_tower_place()
        self.particle_system.create_money_collect(
            grid_pos[1] * GRID_SIZE + GRID_SIZE // 2,
            grid_pos[0] * GRID_SIZE + GRID_SIZE // 2
        )

        # Don't clear placement type - allow multiple placements
        # self.placing_tower_type = None

    def try_select_tower(self, mouse_pos: Tuple[int, int]):
        """Try to select a tower at mouse position."""
        # Deselect current tower
        if self.selected_tower:
            self.selected_tower.selected = False
            self.selected_tower = None
            self.ui.selected_tower = None

        # Find tower at position
        for tower in self.towers:
            if tower.contains_point(mouse_pos):
                self.selected_tower = tower
                self.ui.selected_tower = tower
                tower.selected = True
                break

    def is_valid_tower_placement(self, grid_pos: Tuple[int, int]) -> bool:
        """Check if tower can be placed at grid position."""
        row, col = grid_pos

        # Check bounds
        if row < 0 or row >= GRID_HEIGHT or col < 0 or col >= GRID_WIDTH:
            return False

        # Check if buildable (not on path)
        if not self.game_map.is_buildable(row, col):
            return False

        # Check if another tower is already there
        for tower in self.towers:
            if tower.grid_pos == grid_pos:
                return False

        return True

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            # Switch to fullscreen
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        else:
            # Switch to windowed mode
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def update(self, dt: float):
        """Update game state."""
        # Update abilities
        self.ability_manager.update(dt)

        # Update particle system
        self.particle_system.update(dt)

        # Update wave manager and enemies
        enemies_killed, enemies_reached_end, boss_kills = self.wave_manager.update(dt)

        # Handle enemy deaths (give money and score)
        if enemies_killed > 0:
            # Calculate rewards from killed enemies
            money_earned = 0
            for enemy in self.wave_manager.enemies[:]:
                if not enemy.alive:
                    reward = int(enemy.reward * self.ability_manager.get_money_multiplier())
                    self.money += reward
                    self.score += reward
                    money_earned += reward

                    # Create death particles and sound
                    self.particle_system.create_explosion(enemy.x, enemy.y, enemy.color)
                    self.sound_manager.play_enemy_death()

            # Update statistics
            self.statistics.total_kills += enemies_killed
            self.statistics.boss_kills += boss_kills
            self.statistics.money_earned += money_earned

        # Handle enemies reaching the end (lose health)
        if enemies_reached_end > 0:
            self.health -= enemies_reached_end
            self.statistics.lives_lost += enemies_reached_end

        # Check game over
        if self.health <= 0:
            self.game_active = False
            self.victory = False
            self.sound_manager.play_game_over()
            # Save statistics
            self._save_game_data()

        # Check for wave completion and perfect wave achievement
        if self.wave_manager.is_wave_complete() and not self.wave_manager.wave_active:
            if self.wave_start_health == self.health and self.wave_manager.current_wave > 0:
                self.statistics.perfect_waves += 1
            self.wave_start_health = self.health

        # Apply damage boost to towers
        damage_multiplier = self.ability_manager.get_damage_multiplier()

        # Update towers
        for tower in self.towers:
            # Apply damage boost
            if hasattr(tower, '_base_damage'):
                tower.damage = int(tower._base_damage * damage_multiplier)
            else:
                tower._base_damage = tower.damage

            # Pass all enemies to splash towers and electric towers
            if hasattr(tower, 'projectiles'):
                for projectile in tower.projectiles:
                    if isinstance(projectile, SplashProjectile):
                        projectile.all_enemies = self.wave_manager.enemies
                    if hasattr(projectile, 'all_enemies'):  # Electric towers
                        projectile.all_enemies = self.wave_manager.enemies

            # Update tower
            tower.update(dt, self.wave_manager)

            # Create particles for projectile impacts
            if hasattr(tower, 'projectiles'):
                for projectile in tower.projectiles:
                    if hasattr(projectile, 'hit') and projectile.hit:
                        self.particle_system.create_impact_spark(
                            projectile.x, projectile.y, tower.color
                        )

        # Handle special abilities
        self._handle_abilities()

        # Update achievements
        self.achievement_system.update()

        # Check for victory (all waves complete)
        if self.wave_manager.current_wave >= len(WAVES) and self.wave_manager.is_wave_complete():
            self.game_active = False
            self.victory = True
            self.sound_manager.play_victory()
            self.statistics.waves_completed = max(self.statistics.waves_completed,
                                                 self.wave_manager.current_wave)
            self.statistics.highest_wave = max(self.statistics.highest_wave,
                                              self.wave_manager.current_wave)
            self._save_game_data()

    def use_ability(self, ability_type: str, mouse_pos: Tuple[int, int]):
        """Use a special ability."""
        # Check if we can afford it
        ability = self.ability_manager.get_ability(ability_type)
        if not ability or not ability.is_ready() or self.money < ability.cost:
            return

        # Special handling for airstrike (needs target position)
        if ability_type == 'airstrike':
            # Only allow if clicking on game area
            if mouse_pos[0] < self.ui.panel_x:
                if self.ability_manager.use_ability(ability_type, self.money, mouse_pos):
                    self.money -= ability.cost
                    self.sound_manager.play_ability()
        else:
            # Other abilities don't need target position
            if self.ability_manager.use_ability(ability_type, self.money):
                self.money -= ability.cost
                self.sound_manager.play_ability()

                # Health restore - immediately apply
                if ability_type == 'health_restore':
                    self.health = min(
                        int(STARTING_HEALTH * self.difficulty_settings['health_multiplier']),
                        self.health + ability.restore_amount
                    )

    def _handle_abilities(self):
        """Handle special ability effects."""
        # Check for airstrike
        airstrike_data = self.ability_manager.consume_airstrike()
        if airstrike_data:
            x, y, damage, radius = airstrike_data
            # Create massive explosion effect
            for _ in range(50):
                self.particle_system.create_explosion(x, y, (255, 100, 0))

            # Damage all enemies in radius
            for enemy in self.wave_manager.enemies:
                if enemy.alive:
                    dist = distance((x, y), (enemy.x, enemy.y))
                    if dist <= radius:
                        enemy.take_damage(damage)

        # Check for freeze all
        if self.ability_manager.check_freeze_all():
            # Freeze all enemies
            for enemy in self.wave_manager.enemies:
                if enemy.alive:
                    enemy.apply_status_effect('freeze', 3.0)
                    self.particle_system.create_freeze_effect(enemy.x, enemy.y)

    def _save_game_data(self):
        """Save game statistics and achievements."""
        save_data = {
            'statistics': self.statistics.to_dict(),
            'achievements': self.achievement_system.to_dict()
        }
        self.save_system.save(save_data)

    def draw(self):
        """Draw everything."""
        # Clear screen
        self.screen.fill(BLACK)

        # Draw map
        self.game_map.draw(self.screen)

        # Draw towers
        for tower in self.towers:
            show_range = tower == self.selected_tower
            tower.draw(self.screen, show_range)

        # Draw enemies
        self.wave_manager.draw(self.screen)

        # Draw particles
        self.particle_system.draw(self.screen)

        # Draw tower placement preview
        if self.placing_tower_type:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < self.ui.panel_x:  # Only show if over game area
                grid_pos = pixel_to_grid(mouse_pos, GRID_SIZE)
                is_valid = self.is_valid_tower_placement(grid_pos)
                self.ui.draw_tower_preview(self.screen, mouse_pos,
                                          self.placing_tower_type, is_valid)

        # Draw UI
        game_state = {
            'health': self.health,
            'money': self.money,
            'wave': self.wave_manager.current_wave,
            'score': self.score,
        }
        self.ui.draw(self.screen, game_state, self.ability_manager)

        # Draw game over screen
        if not self.game_active:
            self.game_over_screen.draw(self.screen, self.score,
                                      self.wave_manager.current_wave,
                                      self.victory)

        # Update display
        pygame.display.flip()

    def restart_game(self):
        """Restart the game."""
        # Reset game state
        self.game_active = True
        self.victory = False

        # Reset game objects (preserve difficulty and map)
        self.game_map = GameMap(self.map_layout)
        difficulty_mult = {
            'health': self.difficulty_settings['enemy_health_multiplier'],
            'speed': self.difficulty_settings['enemy_speed_multiplier']
        }
        self.wave_manager = WaveManager(self.game_map.waypoints_pixel, difficulty_mult)
        self.towers = []

        # Reset resources (apply difficulty multipliers)
        self.health = int(STARTING_HEALTH * self.difficulty_settings['health_multiplier'])
        self.money = int(STARTING_MONEY * self.difficulty_settings['money_multiplier'])
        self.score = 0

        # Reset UI state
        self.placing_tower_type = None
        self.selected_tower = None
        self.ui.selected_tower = None

        # Reset particle system and abilities
        self.particle_system = ParticleSystem()
        self.ability_manager = AbilityManager()
        self.wave_start_health = self.health
