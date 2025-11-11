"""Sound effects manager."""

import pygame
from typing import Dict, Optional


class SoundManager:
    """Manages game sound effects and music."""

    def __init__(self, enabled: bool = True):
        """
        Initialize sound manager.

        Args:
            enabled: Whether to enable sound effects
        """
        self.enabled = enabled
        self.sounds: Dict[str, Optional[pygame.mixer.Sound]] = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7

        # Try to initialize mixer
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.mixer_available = True
        except (pygame.error, AttributeError):
            self.mixer_available = False
            self.enabled = False

        if self.enabled and self.mixer_available:
            self._generate_sounds()

    def _generate_sounds(self):
        """Generate procedural sound effects."""
        # Note: In a real implementation, you would load audio files here
        # For now, we'll create placeholders that won't error even without audio hardware

        sound_list = [
            'tower_place',
            'tower_upgrade',
            'tower_sell',
            'tower_shoot',
            'enemy_hit',
            'enemy_death',
            'wave_start',
            'wave_complete',
            'ability_use',
            'ability_ready',
            'game_over',
            'victory',
            'button_click',
            'money_collect'
        ]

        # Create placeholder sounds (would be actual Sound objects with audio files)
        for sound_name in sound_list:
            self.sounds[sound_name] = None  # Placeholder

    def play(self, sound_name: str):
        """
        Play a sound effect.

        Args:
            sound_name: Name of the sound to play
        """
        if not self.enabled or not self.mixer_available:
            return

        sound = self.sounds.get(sound_name)
        if sound:
            try:
                sound.set_volume(self.sfx_volume)
                sound.play()
            except (pygame.error, AttributeError):
                pass

    def play_tower_shoot(self, tower_type: str):
        """
        Play tower shooting sound based on tower type.

        Args:
            tower_type: Type of tower
        """
        # Different towers could have different shoot sounds
        sound_map = {
            'basic': 'tower_shoot',
            'sniper': 'tower_shoot',
            'rapid': 'tower_shoot',
            'splash': 'tower_shoot',
            'laser': 'tower_shoot',
            'ice': 'tower_shoot',
            'poison': 'tower_shoot',
            'electric': 'tower_shoot',
            'artillery': 'tower_shoot',
            'support': 'tower_shoot',
            'flame': 'tower_shoot'
        }
        self.play(sound_map.get(tower_type, 'tower_shoot'))

    def play_enemy_hit(self):
        """Play enemy hit sound."""
        self.play('enemy_hit')

    def play_enemy_death(self):
        """Play enemy death sound."""
        self.play('enemy_death')

    def play_tower_place(self):
        """Play tower placement sound."""
        self.play('tower_place')

    def play_tower_upgrade(self):
        """Play tower upgrade sound."""
        self.play('tower_upgrade')

    def play_tower_sell(self):
        """Play tower sell sound."""
        self.play('tower_sell')

    def play_wave_start(self):
        """Play wave start sound."""
        self.play('wave_start')

    def play_wave_complete(self):
        """Play wave complete sound."""
        self.play('wave_complete')

    def play_ability(self):
        """Play ability use sound."""
        self.play('ability_use')

    def play_ability_ready(self):
        """Play ability ready notification sound."""
        self.play('ability_ready')

    def play_game_over(self):
        """Play game over sound."""
        self.play('game_over')

    def play_victory(self):
        """Play victory sound."""
        self.play('victory')

    def play_button_click(self):
        """Play button click sound."""
        self.play('button_click')

    def play_money_collect(self):
        """Play money collection sound."""
        self.play('money_collect')

    def set_sfx_volume(self, volume: float):
        """
        Set sound effects volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))

    def set_music_volume(self, volume: float):
        """
        Set music volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        if self.mixer_available:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except (pygame.error, AttributeError):
                pass

    def toggle_enabled(self):
        """Toggle sound effects on/off."""
        self.enabled = not self.enabled and self.mixer_available
        return self.enabled

    def stop_all(self):
        """Stop all currently playing sounds."""
        if self.mixer_available:
            try:
                pygame.mixer.stop()
            except (pygame.error, AttributeError):
                pass
