#!/usr/bin/env python3
"""
Tower Defense Game
A fully-fledged tower defense game built with Pygame.

Features:
- Multiple tower types with unique abilities
- Various enemy types with different characteristics
- Wave-based gameplay with increasing difficulty
- Tower upgrades and strategic placement
- Comprehensive UI and game management

Controls:
- Left Click: Place tower / Select tower / Click UI buttons
- Right Click: Cancel placement / Deselect tower
- Space: Start next wave
- ESC: Cancel tower placement
"""

import sys
from src.game import Game


def main():
    """Main entry point."""
    print("="*50)
    print("Tower Defense Game")
    print("="*50)
    print("\nControls:")
    print("  - Left Click: Place/Select towers, Click buttons")
    print("  - Right Click: Cancel/Deselect")
    print("  - Space: Start wave")
    print("  - ESC: Cancel placement")
    print("\nStarting game...")
    print("="*50)

    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
