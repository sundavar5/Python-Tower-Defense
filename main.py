#!/usr/bin/env python3
"""
Tower Defense Game - Massive Edition
A comprehensively featured tower defense game built with Pygame.

Features:
- 11 unique tower types with special abilities
- 13 enemy types with unique behaviors
- 25 progressive waves
- 6 different map layouts
- 4 difficulty levels
- 5 special abilities
- 12 achievements
- Particle effects system
- Statistics tracking
- Save/load system

Controls:
- Left Click: Place tower / Select tower / Click UI buttons
- Right Click: Cancel placement / Deselect tower
- Space: Start next wave
- ESC: Cancel tower placement
- F11: Toggle fullscreen
"""

import sys
import pygame
from src.game import Game
from src.menu import MainMenu, GameSetupMenu
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS


def main():
    """Main entry point."""
    print("="*50)
    print("Tower Defense Game - Massive Edition")
    print("="*50)
    print("\nControls:")
    print("  - Left Click: Place/Select towers, Click buttons")
    print("  - Right Click: Cancel/Deselect")
    print("  - Space: Start wave")
    print("  - ESC: Cancel placement")
    print("  - F11: Toggle fullscreen")
    print("\nStarting game...")
    print("="*50)

    try:
        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tower Defense - Massive Edition")
        clock = pygame.time.Clock()

        # Menu state
        current_menu = 'main'  # 'main', 'setup', 'game'
        main_menu = MainMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
        setup_menu = GameSetupMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
        game = None

        running = True
        while running:
            dt = clock.tick(FPS) / 1000.0
            mouse_pos = pygame.mouse.get_pos()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if current_menu == 'main':
                        action = main_menu.handle_click(mouse_pos)
                        if action == 'play':
                            current_menu = 'setup'
                        elif action == 'quit':
                            running = False

                    elif current_menu == 'setup':
                        action = setup_menu.handle_click(mouse_pos)
                        if action == 'start':
                            settings = setup_menu.get_settings()
                            game = Game(
                                difficulty=settings['difficulty'],
                                map_layout=settings['map']
                            )
                            current_menu = 'game'
                        elif action == 'back':
                            current_menu = 'main'

            # Update and draw
            if current_menu == 'main':
                main_menu.update(mouse_pos)
                main_menu.draw(screen)

            elif current_menu == 'setup':
                setup_menu.update(mouse_pos)
                setup_menu.draw(screen)

            elif current_menu == 'game':
                if game:
                    # Run game
                    game.run()
                    # Game finished, return to main menu
                    current_menu = 'main'
                else:
                    current_menu = 'main'

            pygame.display.flip()

        pygame.quit()
        return 0

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
