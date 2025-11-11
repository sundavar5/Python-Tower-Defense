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


class Game:
    """Main game class."""

    def __init__(self):
        """Initialize the game."""
        # Pygame initialization
        pygame.init()
        self.fullscreen = False
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game state
        self.game_active = True
        self.victory = False

        # Initialize game objects
        self.game_map = GameMap()
        self.wave_manager = WaveManager(self.game_map.waypoints_pixel)
        self.towers: List[Tower] = []

        # Game resources
        self.health = STARTING_HEALTH
        self.money = STARTING_MONEY
        self.score = 0

        # UI
        self.ui = GameUI(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.game_over_screen = GameOverScreen(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Tower placement
        self.placing_tower_type: Optional[str] = None
        self.selected_tower: Optional[Tower] = None

        # Particles and effects
        self.particles = []

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
            self.ui.update(mouse_pos, self.money)
        else:
            self.game_over_screen.update(mouse_pos)

    def handle_game_click(self, mouse_pos: Tuple[int, int]):
        """Handle clicks during active gameplay."""
        # Check UI button clicks first
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
            return

        # Sell button
        if self.ui.is_sell_clicked(mouse_pos) and self.selected_tower:
            sell_value = self.selected_tower.get_sell_value()
            self.money += sell_value
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
        # Update wave manager and enemies
        enemies_killed, enemies_reached_end, boss_kills = self.wave_manager.update(dt)

        # Handle enemy deaths (give money and score)
        if enemies_killed > 0:
            # Calculate rewards from killed enemies
            for enemy in self.wave_manager.enemies[:]:
                if not enemy.alive:
                    self.money += enemy.reward
                    self.score += enemy.reward

        # Handle enemies reaching the end (lose health)
        if enemies_reached_end > 0:
            self.health -= enemies_reached_end

        # Check game over
        if self.health <= 0:
            self.game_active = False
            self.victory = False

        # Update towers
        for tower in self.towers:
            # Pass all enemies to splash towers
            if hasattr(tower, 'projectiles'):
                for projectile in tower.projectiles:
                    if isinstance(projectile, SplashProjectile):
                        projectile.all_enemies = self.wave_manager.enemies

            tower.update(dt, self.wave_manager)

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
        self.ui.draw(self.screen, game_state)

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

        # Reset game objects
        self.game_map = GameMap()
        self.wave_manager = WaveManager(self.game_map.waypoints_pixel)
        self.towers = []

        # Reset resources
        self.health = STARTING_HEALTH
        self.money = STARTING_MONEY
        self.score = 0

        # Reset UI state
        self.placing_tower_type = None
        self.selected_tower = None
        self.ui.selected_tower = None
