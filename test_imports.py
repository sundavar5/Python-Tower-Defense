#!/usr/bin/env python3
"""
Test script to verify all imports work correctly.
This doesn't run the game but checks that all modules load properly.
"""

import sys

def test_imports():
    """Test that all game modules can be imported."""
    print("Testing imports...")

    try:
        print("  - Importing constants...", end=" ")
        from src import constants
        print("✓")

        print("  - Importing utils...", end=" ")
        from src import utils
        print("✓")

        print("  - Importing map...", end=" ")
        from src import map
        print("✓")

        print("  - Importing enemy...", end=" ")
        from src import enemy
        print("✓")

        print("  - Importing projectile...", end=" ")
        from src import projectile
        print("✓")

        print("  - Importing tower...", end=" ")
        from src import tower
        print("✓")

        print("  - Importing ui...", end=" ")
        from src import ui
        print("✓")

        print("  - Importing game...", end=" ")
        from src import game
        print("✓")

        print("\n✓ All imports successful!")
        print("\nGame structure verified. Run 'python main.py' to play!")
        return 0

    except ImportError as e:
        print(f"\n✗ Import failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(test_imports())
