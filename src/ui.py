"""UI components for the game."""

import pygame
from typing import Optional, Tuple, List, Callable
from src.constants import *
from src.utils import draw_text, point_in_rect


class Button:
    """A clickable button."""

    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                color: Tuple[int, int, int] = BLUE,
                hover_color: Tuple[int, int, int] = CYAN,
                text_color: Tuple[int, int, int] = WHITE,
                font_size: int = 20):
        """Initialize button."""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.enabled = True
        self.hovered = False

    def update(self, mouse_pos: Tuple[int, int]):
        """Update button state."""
        self.hovered = self.rect.collidepoint(mouse_pos) and self.enabled

    def draw(self, surface: pygame.Surface):
        """Draw the button."""
        # Choose color based on state
        if not self.enabled:
            color = DARK_GRAY
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.color

        # Draw button background
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> bool:
        """Check if button was clicked."""
        return self.enabled and self.hovered and mouse_clicked


class TowerButton(Button):
    """Button for selecting and placing towers."""

    def __init__(self, x: int, y: int, width: int, height: int, tower_type: str):
        """Initialize tower button."""
        tower_stats = TOWER_TYPES[tower_type]
        text = f"{tower_stats['name']}\n${tower_stats['cost']}"

        super().__init__(x, y, width, height, tower_stats['name'],
                        color=tower_stats['color'],
                        hover_color=tuple(min(255, c + 50) for c in tower_stats['color']))

        self.tower_type = tower_type
        self.tower_stats = tower_stats
        self.cost = tower_stats['cost']

    def draw(self, surface: pygame.Surface):
        """Draw tower button with stats."""
        # Choose color based on state
        if not self.enabled:
            color = DARK_GRAY
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.color

        # Draw button background
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        # Draw tower name
        font_small = pygame.font.Font(None, 18)
        name_surface = font_small.render(self.tower_stats['name'], True, WHITE)
        name_rect = name_surface.get_rect(center=(self.rect.centerx, self.rect.top + 15))
        surface.blit(name_surface, name_rect)

        # Draw cost
        cost_text = f"${self.cost}"
        cost_surface = self.font.render(cost_text, True, GOLD)
        cost_rect = cost_surface.get_rect(center=(self.rect.centerx, self.rect.centery + 5))
        surface.blit(cost_surface, cost_rect)

        # Draw stats
        stats_font = pygame.font.Font(None, 14)
        stats_y = self.rect.bottom - 25

        # Damage
        dmg_text = f"DMG: {self.tower_stats['damage']}"
        dmg_surface = stats_font.render(dmg_text, True, WHITE)
        surface.blit(dmg_surface, (self.rect.left + 5, stats_y))

        # Range
        rng_text = f"RNG: {self.tower_stats['range']}"
        rng_surface = stats_font.render(rng_text, True, WHITE)
        surface.blit(rng_surface, (self.rect.left + 5, stats_y + 12))


class GameUI:
    """Main game UI manager."""

    def __init__(self, screen_width: int, screen_height: int):
        """Initialize game UI."""
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Fonts
        self.font_small = pygame.font.Font(None, 18)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        self.font_title = pygame.font.Font(None, 48)

        # UI Panel (right side)
        self.panel_x = screen_width - UI_PANEL_WIDTH
        self.panel_y = 0
        self.panel_width = UI_PANEL_WIDTH
        self.panel_height = screen_height

        # Tower buttons
        self.tower_buttons: List[TowerButton] = []
        self.create_tower_buttons()

        # Action buttons
        self.start_wave_button = Button(
            self.panel_x + UI_PADDING,
            screen_height - 150,
            UI_PANEL_WIDTH - UI_PADDING * 2,
            UI_BUTTON_HEIGHT,
            "Start Wave",
            color=GREEN,
            hover_color=DARK_GREEN
        )

        self.upgrade_button = Button(
            self.panel_x + UI_PADDING,
            screen_height - 90,
            (UI_PANEL_WIDTH - UI_PADDING * 3) // 2,
            UI_BUTTON_HEIGHT - 10,
            "Upgrade",
            color=BLUE,
            hover_color=CYAN
        )

        self.sell_button = Button(
            self.panel_x + UI_PADDING * 2 + (UI_PANEL_WIDTH - UI_PADDING * 3) // 2,
            screen_height - 90,
            (UI_PANEL_WIDTH - UI_PADDING * 3) // 2,
            UI_BUTTON_HEIGHT - 10,
            "Sell",
            color=RED,
            hover_color=DARK_RED
        )

        # Special ability buttons (at top of screen)
        self.ability_buttons: List[Button] = []
        self.create_ability_buttons()

        # Selected tower and placement
        self.selected_tower_type: Optional[str] = None
        self.selected_tower: Optional[object] = None
        self.placement_valid = False

    def create_ability_buttons(self):
        """Create buttons for special abilities."""
        ability_types = ['airstrike', 'freeze_all', 'cash_boost', 'damage_boost', 'health_restore']
        button_width = 140
        button_height = 35
        spacing = 10
        total_width = len(ability_types) * (button_width + spacing) - spacing
        start_x = (self.panel_x - total_width) // 2

        for i, ability_type in enumerate(ability_types):
            stats = SPECIAL_ABILITIES[ability_type]
            x = start_x + i * (button_width + spacing)
            y = 10

            button = Button(
                x, y, button_width, button_height,
                f"{stats['name']} (${stats['cost']})",
                color=PURPLE,
                hover_color=(150, 0, 200),
                font_size=18
            )
            button.ability_type = ability_type
            self.ability_buttons.append(button)

    def create_tower_buttons(self):
        """Create buttons for each tower type."""
        button_width = (UI_PANEL_WIDTH - UI_PADDING * 3) // 2
        button_height = 70
        x_offset = self.panel_x + UI_PADDING
        y_offset = 150

        # All 11 tower types
        tower_types = [
            'basic', 'sniper', 'rapid', 'splash', 'laser',
            'ice', 'poison', 'electric', 'artillery', 'support', 'flame'
        ]

        for i, tower_type in enumerate(tower_types):
            row = i // 2
            col = i % 2

            x = x_offset + col * (button_width + UI_PADDING)
            y = y_offset + row * (button_height + UI_PADDING)

            button = TowerButton(x, y, button_width, button_height, tower_type)
            self.tower_buttons.append(button)

    def update(self, mouse_pos: Tuple[int, int], money: int, ability_manager=None):
        """Update UI elements."""
        # Update tower buttons
        for button in self.tower_buttons:
            button.update(mouse_pos)
            button.enabled = money >= button.cost

        # Update action buttons
        self.start_wave_button.update(mouse_pos)
        self.upgrade_button.update(mouse_pos)
        self.sell_button.update(mouse_pos)

        # Update ability buttons
        for button in self.ability_buttons:
            button.update(mouse_pos)
            if ability_manager:
                ability = ability_manager.get_ability(button.ability_type)
                button.enabled = ability.is_ready() and money >= ability.cost

        # Enable/disable upgrade and sell based on selection
        self.upgrade_button.enabled = self.selected_tower is not None
        self.sell_button.enabled = self.selected_tower is not None

    def draw(self, surface: pygame.Surface, game_state: dict, ability_manager=None):
        """
        Draw the UI.

        Args:
            game_state: Dictionary with health, money, wave, score, etc.
            ability_manager: AbilityManager instance for cooldown display
        """
        # Draw ability buttons first
        self.draw_ability_buttons(surface, ability_manager)

        # Draw panel background
        panel_rect = pygame.Rect(self.panel_x, self.panel_y,
                                self.panel_width, self.panel_height)
        pygame.draw.rect(surface, DARK_GRAY, panel_rect)
        pygame.draw.rect(surface, BLACK, panel_rect, 3)

        # Draw title
        draw_text(surface, "Tower Defense", self.font_title, WHITE,
                 self.panel_x + self.panel_width // 2, 30, center=True)

        # Draw game stats
        stats_y = 70
        stats = [
            f"Health: {game_state.get('health', 0)}",
            f"Money: ${game_state.get('money', 0)}",
            f"Wave: {game_state.get('wave', 0)}",
            f"Score: {game_state.get('score', 0)}",
        ]

        for stat in stats:
            draw_text(surface, stat, self.font_medium, WHITE,
                     self.panel_x + UI_PADDING, stats_y)
            stats_y += 25

        # Draw tower shop title
        draw_text(surface, "Tower Shop", self.font_large, WHITE,
                 self.panel_x + self.panel_width // 2, 120, center=True)

        # Draw tower buttons
        for button in self.tower_buttons:
            button.draw(surface)

        # Draw selected tower info
        if self.selected_tower:
            self.draw_selected_tower_info(surface)

        # Draw action buttons
        self.start_wave_button.draw(surface)

        if self.selected_tower:
            self.upgrade_button.draw(surface)
            self.sell_button.draw(surface)

    def draw_selected_tower_info(self, surface: pygame.Surface):
        """Draw information about the selected tower."""
        if not self.selected_tower:
            return

        info_y = self.screen_height - 250
        info_x = self.panel_x + UI_PADDING

        # Draw background
        info_rect = pygame.Rect(info_x, info_y, self.panel_width - UI_PADDING * 2, 110)
        pygame.draw.rect(surface, LIGHT_GRAY, info_rect)
        pygame.draw.rect(surface, BLACK, info_rect, 2)

        # Tower info
        tower = self.selected_tower
        info_y += 10

        draw_text(surface, f"Selected: {tower.type.capitalize()}", self.font_medium,
                 BLACK, info_x + 10, info_y)
        info_y += 25

        draw_text(surface, f"Level: {tower.level}", self.font_small,
                 BLACK, info_x + 10, info_y)
        info_y += 20

        draw_text(surface, f"Damage: {tower.damage}", self.font_small,
                 BLACK, info_x + 10, info_y)
        draw_text(surface, f"Range: {int(tower.range)}", self.font_small,
                 BLACK, info_x + 150, info_y)
        info_y += 20

        # Upgrade cost
        upgrade_cost = tower.get_upgrade_cost()
        if upgrade_cost > 0:
            draw_text(surface, f"Upgrade: ${upgrade_cost}", self.font_small,
                     BLUE, info_x + 10, info_y)
        else:
            draw_text(surface, "MAX LEVEL", self.font_small,
                     GOLD, info_x + 10, info_y)

        # Sell value
        sell_value = tower.get_sell_value()
        draw_text(surface, f"Sell: ${sell_value}", self.font_small,
                 RED, info_x + 150, info_y)

    def handle_tower_button_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Check if any tower button was clicked.

        Returns:
            Tower type if clicked, None otherwise
        """
        for button in self.tower_buttons:
            if button.is_clicked(mouse_pos, True):
                return button.tower_type
        return None

    def is_start_wave_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if start wave button was clicked."""
        return self.start_wave_button.is_clicked(mouse_pos, True)

    def is_upgrade_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if upgrade button was clicked."""
        return self.upgrade_button.is_clicked(mouse_pos, True)

    def is_sell_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if sell button was clicked."""
        return self.sell_button.is_clicked(mouse_pos, True)

    def draw_tower_preview(self, surface: pygame.Surface, mouse_pos: Tuple[int, int],
                          tower_type: str, is_valid: bool):
        """Draw tower placement preview."""
        if not tower_type:
            return

        tower_stats = TOWER_TYPES[tower_type]
        color = tower_stats['color']

        # Draw range circle
        range_surface = pygame.Surface((surface.get_width(), surface.get_height()),
                                      pygame.SRCALPHA)

        if is_valid:
            range_color = (*color, 50)
            tower_color = (*color, 150)
        else:
            range_color = (*RED, 50)
            tower_color = (*RED, 150)

        pygame.draw.circle(range_surface, range_color,
                         mouse_pos, tower_stats['range'])
        surface.blit(range_surface, (0, 0))

        # Draw tower preview
        preview_size = GRID_SIZE // 3
        preview_rect = pygame.Rect(
            mouse_pos[0] - preview_size,
            mouse_pos[1] - preview_size,
            preview_size * 2,
            preview_size * 2
        )
        pygame.draw.rect(surface, tower_color, preview_rect)
        pygame.draw.rect(surface, BLACK, preview_rect, 2)

    def draw_ability_buttons(self, surface: pygame.Surface, ability_manager=None):
        """Draw special ability buttons with cooldown overlays."""
        for button in self.ability_buttons:
            # Draw button
            button.draw(surface)

            # Draw cooldown overlay if not ready
            if ability_manager:
                ability = ability_manager.get_ability(button.ability_type)
                if not ability.is_ready():
                    # Draw cooldown overlay
                    cooldown_percent = ability.get_cooldown_percent()
                    overlay_height = int(button.rect.height * (1.0 - cooldown_percent))

                    if overlay_height > 0:
                        overlay_rect = pygame.Rect(
                            button.rect.x, button.rect.y,
                            button.rect.width, overlay_height
                        )
                        overlay = pygame.Surface((button.rect.width, overlay_height))
                        overlay.set_alpha(180)
                        overlay.fill(BLACK)
                        surface.blit(overlay, overlay_rect.topleft)

                    # Draw cooldown time
                    cooldown_time = int(ability.current_cooldown)
                    font = pygame.font.Font(None, 24)
                    time_text = font.render(str(cooldown_time), True, WHITE)
                    time_rect = time_text.get_rect(center=button.rect.center)
                    surface.blit(time_text, time_rect)

                # Draw active indicator
                if ability.active:
                    pygame.draw.rect(surface, GOLD, button.rect, 3)

    def handle_ability_button_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Check if any ability button was clicked.

        Returns:
            Ability type if clicked, None otherwise
        """
        for button in self.ability_buttons:
            if button.is_clicked(mouse_pos, True):
                return button.ability_type
        return None


class GameOverScreen:
    """Game over screen."""

    def __init__(self, screen_width: int, screen_height: int):
        """Initialize game over screen."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_title = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)

        # Restart button
        button_width = 200
        button_height = 60
        self.restart_button = Button(
            screen_width // 2 - button_width // 2,
            screen_height // 2 + 50,
            button_width,
            button_height,
            "Restart",
            color=GREEN,
            hover_color=DARK_GREEN,
            font_size=32
        )

    def update(self, mouse_pos: Tuple[int, int]):
        """Update game over screen."""
        self.restart_button.update(mouse_pos)

    def draw(self, surface: pygame.Surface, score: int, wave: int, victory: bool = False):
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))

        # Title
        if victory:
            title = "VICTORY!"
            title_color = GOLD
        else:
            title = "GAME OVER"
            title_color = RED

        draw_text(surface, title, self.font_title, title_color,
                 self.screen_width // 2, self.screen_height // 2 - 100, center=True)

        # Stats
        stats_y = self.screen_height // 2 - 20
        draw_text(surface, f"Final Score: {score}", self.font_medium, WHITE,
                 self.screen_width // 2, stats_y, center=True)

        draw_text(surface, f"Waves Completed: {wave}", self.font_medium, WHITE,
                 self.screen_width // 2, stats_y + 40, center=True)

        # Draw restart button
        self.restart_button.draw(surface)

    def is_restart_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if restart button was clicked."""
        return self.restart_button.is_clicked(mouse_pos, True)
