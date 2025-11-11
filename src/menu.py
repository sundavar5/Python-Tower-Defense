"""Main menu and game setup screens."""

import pygame
from typing import Optional, Tuple
from src.constants import (
    BLACK, WHITE, GRAY, GREEN, RED, BLUE, PURPLE, GOLD, CYAN,
    DIFFICULTY_SETTINGS, MAP_LAYOUTS
)
from src.utils import draw_text


class Button:
    """Generic button class."""

    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, color: Tuple[int, int, int],
                 hover_color: Tuple[int, int, int]):
        """Initialize button."""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def update(self, mouse_pos: Tuple[int, int]):
        """Update button hover state."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pygame.Surface):
        """Draw the button."""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)

        # Draw text
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if button is clicked."""
        return self.rect.collidepoint(mouse_pos)


class MainMenu:
    """Main menu screen."""

    def __init__(self, width: int, height: int):
        """Initialize main menu."""
        self.width = width
        self.height = height

        # Buttons
        button_width = 300
        button_height = 60
        button_x = (width - button_width) // 2
        start_y = height // 2 - 50

        self.play_button = Button(
            button_x, start_y,
            button_width, button_height,
            "Play Game", GREEN, (0, 200, 0)
        )

        self.quit_button = Button(
            button_x, start_y + 100,
            button_width, button_height,
            "Quit", RED, (200, 0, 0)
        )

    def update(self, mouse_pos: Tuple[int, int]):
        """Update menu."""
        self.play_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)

    def draw(self, surface: pygame.Surface):
        """Draw main menu."""
        # Background
        surface.fill(BLACK)

        # Title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("TOWER DEFENSE", True, GOLD)
        title_rect = title_text.get_rect(center=(self.width // 2, 150))
        surface.blit(title_text, title_rect)

        # Subtitle
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("Massive Edition", True, CYAN)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 210))
        surface.blit(subtitle_text, subtitle_rect)

        # Buttons
        self.play_button.draw(surface)
        self.quit_button.draw(surface)

        # Version info
        version_font = pygame.font.Font(None, 24)
        version_text = version_font.render("v2.0 - 11 Towers, 13 Enemies, 25 Waves", True, GRAY)
        version_rect = version_text.get_rect(center=(self.width // 2, self.height - 30))
        surface.blit(version_text, version_rect)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """Handle mouse click. Returns action: 'play', 'quit', or None."""
        if self.play_button.is_clicked(mouse_pos):
            return 'play'
        if self.quit_button.is_clicked(mouse_pos):
            return 'quit'
        return None


class GameSetupMenu:
    """Game setup screen for selecting difficulty and map."""

    def __init__(self, width: int, height: int):
        """Initialize setup menu."""
        self.width = width
        self.height = height

        # Selected options
        self.selected_difficulty = 'normal'
        self.selected_map = 'classic'

        # Difficulty buttons
        diff_button_width = 180
        diff_button_height = 50
        diff_start_x = 150
        diff_y = 250

        self.difficulty_buttons = {}
        for i, (key, info) in enumerate(DIFFICULTY_SETTINGS.items()):
            button = Button(
                diff_start_x + (i % 2) * (diff_button_width + 20),
                diff_y + (i // 2) * (diff_button_height + 15),
                diff_button_width, diff_button_height,
                info['name'], BLUE, (0, 100, 200)
            )
            self.difficulty_buttons[key] = button

        # Map buttons
        map_button_width = 180
        map_button_height = 50
        map_start_x = 150
        map_y = 450

        self.map_buttons = {}
        for i, (key, info) in enumerate(MAP_LAYOUTS.items()):
            button = Button(
                map_start_x + (i % 3) * (map_button_width + 20),
                map_y + (i // 3) * (map_button_height + 15),
                map_button_width, map_button_height,
                info['name'], PURPLE, (100, 0, 150)
            )
            self.map_buttons[key] = button

        # Start button
        self.start_button = Button(
            width - 350, height - 100,
            300, 60,
            "Start Game", GREEN, (0, 200, 0)
        )

        # Back button
        self.back_button = Button(
            50, height - 100,
            200, 60,
            "Back", RED, (200, 0, 0)
        )

    def update(self, mouse_pos: Tuple[int, int]):
        """Update setup menu."""
        for button in self.difficulty_buttons.values():
            button.update(mouse_pos)
        for button in self.map_buttons.values():
            button.update(mouse_pos)
        self.start_button.update(mouse_pos)
        self.back_button.update(mouse_pos)

    def draw(self, surface: pygame.Surface):
        """Draw setup menu."""
        # Background
        surface.fill(BLACK)

        # Title
        title_font = pygame.font.Font(None, 56)
        title_text = title_font.render("Game Setup", True, GOLD)
        title_rect = title_text.get_rect(center=(self.width // 2, 50))
        surface.blit(title_text, title_rect)

        # Difficulty section
        section_font = pygame.font.Font(None, 40)
        diff_text = section_font.render("Select Difficulty:", True, WHITE)
        surface.blit(diff_text, (150, 200))

        # Draw difficulty buttons with highlight for selected
        for key, button in self.difficulty_buttons.items():
            # Draw selection highlight
            if key == self.selected_difficulty:
                highlight_rect = button.rect.inflate(8, 8)
                pygame.draw.rect(surface, GOLD, highlight_rect, 3)

            button.draw(surface)

        # Show difficulty info
        diff_info = DIFFICULTY_SETTINGS[self.selected_difficulty]
        info_font = pygame.font.Font(None, 24)
        info_lines = [
            f"Health: {int(diff_info['health_multiplier'] * 100)}%",
            f"Money: {int(diff_info['money_multiplier'] * 100)}%",
            f"Enemy Health: {int(diff_info['enemy_health_multiplier'] * 100)}%",
            f"Enemy Speed: {int(diff_info['enemy_speed_multiplier'] * 100)}%"
        ]
        for i, line in enumerate(info_lines):
            text = info_font.render(line, True, CYAN)
            surface.blit(text, (650, 250 + i * 25))

        # Map section
        map_text = section_font.render("Select Map:", True, WHITE)
        surface.blit(map_text, (150, 400))

        # Draw map buttons with highlight for selected
        for key, button in self.map_buttons.items():
            # Draw selection highlight
            if key == self.selected_map:
                highlight_rect = button.rect.inflate(8, 8)
                pygame.draw.rect(surface, GOLD, highlight_rect, 3)

            button.draw(surface)

        # Show map info
        map_info = MAP_LAYOUTS[self.selected_map]
        map_info_text = f"Difficulty: {map_info['difficulty'].title()}"
        map_info_surface = info_font.render(map_info_text, True, CYAN)
        surface.blit(map_info_surface, (650, 450))

        # Draw buttons
        self.start_button.draw(surface)
        self.back_button.draw(surface)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """Handle mouse click. Returns action: 'start', 'back', or None."""
        # Check difficulty buttons
        for key, button in self.difficulty_buttons.items():
            if button.is_clicked(mouse_pos):
                self.selected_difficulty = key
                return None

        # Check map buttons
        for key, button in self.map_buttons.items():
            if button.is_clicked(mouse_pos):
                self.selected_map = key
                return None

        # Check start/back buttons
        if self.start_button.is_clicked(mouse_pos):
            return 'start'
        if self.back_button.is_clicked(mouse_pos):
            return 'back'

        return None

    def get_settings(self) -> dict:
        """Get selected game settings."""
        return {
            'difficulty': self.selected_difficulty,
            'map': self.selected_map
        }
