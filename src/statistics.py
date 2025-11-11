"""Statistics and achievement tracking system."""

import json
import os
from typing import Dict, List, Set
from src.constants import ACHIEVEMENTS


class Statistics:
    """Tracks game statistics."""

    def __init__(self):
        """Initialize statistics."""
        self.total_kills = 0
        self.boss_kills = 0
        self.towers_built = 0
        self.towers_sold = 0
        self.upgrades = 0
        self.waves_completed = 0
        self.money_earned = 0
        self.money_spent = 0
        self.damage_dealt = 0
        self.lives_lost = 0
        self.perfect_waves = 0
        self.games_played = 0
        self.highest_wave = 0
        self.highest_score = 0
        self.total_playtime = 0.0  # in seconds

        # Per-game stats
        self.current_game_kills = 0
        self.current_game_money = 0
        self.current_game_damage = 0
        self.wave_start_health = 0

    def reset_game_stats(self):
        """Reset stats for a new game."""
        self.current_game_kills = 0
        self.current_game_money = 0
        self.current_game_damage = 0
        self.wave_start_health = 0

    def record_kill(self, is_boss: bool = False, reward: int = 0):
        """Record an enemy kill."""
        self.total_kills += 1
        self.current_game_kills += 1
        if is_boss:
            self.boss_kills += 1
        self.money_earned += reward
        self.current_game_money += reward

    def record_tower_built(self, cost: int):
        """Record a tower built."""
        self.towers_built += 1
        self.money_spent += cost

    def record_tower_sold(self, refund: int):
        """Record a tower sold."""
        self.towers_sold += 1
        self.money_earned += refund

    def record_upgrade(self, cost: int):
        """Record a tower upgrade."""
        self.upgrades += 1
        self.money_spent += cost

    def record_wave_complete(self, wave_number: int, health_lost: int):
        """Record wave completion."""
        self.waves_completed += 1
        if health_lost == 0:
            self.perfect_waves += 1

        if wave_number > self.highest_wave:
            self.highest_wave = wave_number

    def record_game_over(self, final_score: int):
        """Record game over."""
        self.games_played += 1
        if final_score > self.highest_score:
            self.highest_score = final_score

    def get_stats_dict(self) -> Dict:
        """Get all stats as a dictionary."""
        return {
            'total_kills': self.total_kills,
            'boss_kills': self.boss_kills,
            'towers_built': self.towers_built,
            'towers_sold': self.towers_sold,
            'upgrades': self.upgrades,
            'waves_completed': self.waves_completed,
            'money_earned': self.money_earned,
            'money_spent': self.money_spent,
            'damage_dealt': self.damage_dealt,
            'lives_lost': self.lives_lost,
            'perfect_waves': self.perfect_waves,
            'games_played': self.games_played,
            'highest_wave': self.highest_wave,
            'highest_score': self.highest_score,
            'total_playtime': self.total_playtime
        }

    def load_from_dict(self, data: Dict):
        """Load stats from a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


class AchievementSystem:
    """Manages achievements."""

    def __init__(self, statistics: Statistics):
        """Initialize achievement system."""
        self.statistics = statistics
        self.unlocked_achievements: Set[str] = set()
        self.newly_unlocked: List[str] = []

    def check_achievements(self) -> List[str]:
        """
        Check for newly unlocked achievements.

        Returns:
            List of newly unlocked achievement IDs
        """
        self.newly_unlocked = []

        for achievement_id, achievement in ACHIEVEMENTS.items():
            if achievement_id in self.unlocked_achievements:
                continue

            condition = achievement['condition']
            threshold = achievement['threshold']

            unlocked = False
            if condition == 'kills':
                unlocked = self.statistics.total_kills >= threshold
            elif condition == 'boss_kills':
                unlocked = self.statistics.boss_kills >= threshold
            elif condition == 'towers_built':
                unlocked = self.statistics.towers_built >= threshold
            elif condition == 'waves':
                unlocked = self.statistics.waves_completed >= threshold
            elif condition == 'money_earned':
                unlocked = self.statistics.money_earned >= threshold
            elif condition == 'perfect_wave':
                unlocked = self.statistics.perfect_waves >= threshold
            elif condition == 'upgrades':
                unlocked = self.statistics.upgrades >= threshold

            if unlocked:
                self.unlocked_achievements.add(achievement_id)
                self.newly_unlocked.append(achievement_id)

        return self.newly_unlocked

    def get_achievement_progress(self, achievement_id: str) -> float:
        """
        Get progress towards an achievement (0.0 to 1.0).

        Args:
            achievement_id: ID of the achievement

        Returns:
            Progress as a float between 0 and 1
        """
        if achievement_id in self.unlocked_achievements:
            return 1.0

        achievement = ACHIEVEMENTS.get(achievement_id)
        if not achievement:
            return 0.0

        condition = achievement['condition']
        threshold = achievement['threshold']

        current = 0
        if condition == 'kills':
            current = self.statistics.total_kills
        elif condition == 'boss_kills':
            current = self.statistics.boss_kills
        elif condition == 'towers_built':
            current = self.statistics.towers_built
        elif condition == 'waves':
            current = self.statistics.waves_completed
        elif condition == 'money_earned':
            current = self.statistics.money_earned
        elif condition == 'perfect_wave':
            current = self.statistics.perfect_waves
        elif condition == 'upgrades':
            current = self.statistics.upgrades

        return min(1.0, current / threshold)

    def get_unlocked_count(self) -> int:
        """Get number of unlocked achievements."""
        return len(self.unlocked_achievements)

    def get_total_count(self) -> int:
        """Get total number of achievements."""
        return len(ACHIEVEMENTS)

    def is_unlocked(self, achievement_id: str) -> bool:
        """Check if an achievement is unlocked."""
        return achievement_id in self.unlocked_achievements


class SaveSystem:
    """Handles saving and loading game data."""

    SAVE_FILE = 'towerdefense_save.json'

    @staticmethod
    def save_game(statistics: Statistics, achievements: AchievementSystem) -> bool:
        """
        Save game statistics and achievements.

        Returns:
            True if save was successful
        """
        try:
            save_data = {
                'statistics': statistics.get_stats_dict(),
                'achievements': list(achievements.unlocked_achievements)
            }

            with open(SaveSystem.SAVE_FILE, 'w') as f:
                json.dump(save_data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    @staticmethod
    def load_game() -> tuple:
        """
        Load game statistics and achievements.

        Returns:
            Tuple of (Statistics, Set of achievement IDs) or None if load failed
        """
        try:
            if not os.path.exists(SaveSystem.SAVE_FILE):
                return None

            with open(SaveSystem.SAVE_FILE, 'r') as f:
                save_data = json.load(f)

            statistics = Statistics()
            statistics.load_from_dict(save_data.get('statistics', {}))

            achievements = set(save_data.get('achievements', []))

            return (statistics, achievements)
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    @staticmethod
    def save_exists() -> bool:
        """Check if a save file exists."""
        return os.path.exists(SaveSystem.SAVE_FILE)

    @staticmethod
    def delete_save() -> bool:
        """Delete the save file."""
        try:
            if os.path.exists(SaveSystem.SAVE_FILE):
                os.remove(SaveSystem.SAVE_FILE)
            return True
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False
