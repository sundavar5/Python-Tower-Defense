"""Special abilities system."""

import pygame
from typing import Optional, Tuple, List
from src.constants import SPECIAL_ABILITIES


class SpecialAbility:
    """Base class for special abilities."""

    def __init__(self, ability_type: str):
        """Initialize ability."""
        self.type = ability_type
        self.stats = SPECIAL_ABILITIES[ability_type]
        self.name = self.stats['name']
        self.cost = self.stats['cost']
        self.cooldown = self.stats['cooldown']
        self.description = self.stats['description']
        self.current_cooldown = 0
        self.active = False
        self.duration = self.stats.get('duration', 0)
        self.time_active = 0

    def use(self) -> bool:
        """
        Try to use the ability.

        Returns:
            True if ability was used successfully
        """
        if self.is_ready():
            self.current_cooldown = self.cooldown
            self.active = True
            self.time_active = 0
            return True
        return False

    def update(self, dt: float):
        """Update ability cooldowns and duration."""
        if self.current_cooldown > 0:
            self.current_cooldown -= dt

        if self.active and self.duration > 0:
            self.time_active += dt
            if self.time_active >= self.duration:
                self.active = False
                self.time_active = 0

    def is_ready(self) -> bool:
        """Check if ability is ready to use."""
        return self.current_cooldown <= 0

    def get_cooldown_percent(self) -> float:
        """Get cooldown progress (0 to 1)."""
        if self.cooldown == 0:
            return 1.0
        return max(0.0, 1.0 - (self.current_cooldown / self.cooldown))


class AirStrike(SpecialAbility):
    """Air strike ability - deals damage in an area."""

    def __init__(self):
        super().__init__('airstrike')
        self.damage = self.stats['damage']
        self.radius = self.stats['radius']
        self.target_pos: Optional[Tuple[float, float]] = None

    def activate(self, target_pos: Tuple[float, float]):
        """Activate airstrike at target position."""
        self.target_pos = target_pos


class FreezeAll(SpecialAbility):
    """Freeze all enemies ability."""

    def __init__(self):
        super().__init__('freeze_all')


class CashBoost(SpecialAbility):
    """Double money for duration."""

    def __init__(self):
        super().__init__('cash_boost')
        self.multiplier = self.stats['multiplier']


class DamageBoost(SpecialAbility):
    """Increase tower damage for duration."""

    def __init__(self):
        super().__init__('damage_boost')
        self.multiplier = self.stats['multiplier']


class HealthRestore(SpecialAbility):
    """Restore health ability."""

    def __init__(self):
        super().__init__('health_restore')
        self.restore_amount = self.stats['restore_amount']


class AbilityManager:
    """Manages all special abilities."""

    def __init__(self):
        """Initialize ability manager."""
        self.abilities = {
            'airstrike': AirStrike(),
            'freeze_all': FreezeAll(),
            'cash_boost': CashBoost(),
            'damage_boost': DamageBoost(),
            'health_restore': HealthRestore()
        }
        self.pending_airstrike: Optional[Tuple[float, float]] = None

    def update(self, dt: float):
        """Update all abilities."""
        for ability in self.abilities.values():
            ability.update(dt)

    def use_ability(self, ability_type: str, money: int,
                   target_pos: Optional[Tuple[float, float]] = None) -> bool:
        """
        Try to use an ability.

        Args:
            ability_type: Type of ability to use
            money: Current money
            target_pos: Target position (for airstrike)

        Returns:
            True if ability was used
        """
        ability = self.abilities.get(ability_type)
        if not ability:
            return False

        # Check if ready and affordable
        if not ability.is_ready() or money < ability.cost:
            return False

        # Use ability
        if ability.use():
            # Special handling for airstrike
            if ability_type == 'airstrike' and target_pos:
                ability.activate(target_pos)
                self.pending_airstrike = target_pos
            return True

        return False

    def get_ability(self, ability_type: str) -> Optional[SpecialAbility]:
        """Get an ability by type."""
        return self.abilities.get(ability_type)

    def is_cash_boost_active(self) -> bool:
        """Check if cash boost is active."""
        return self.abilities['cash_boost'].active

    def is_damage_boost_active(self) -> bool:
        """Check if damage boost is active."""
        return self.abilities['damage_boost'].active

    def get_damage_multiplier(self) -> float:
        """Get current damage multiplier."""
        if self.is_damage_boost_active():
            return self.abilities['damage_boost'].multiplier
        return 1.0

    def get_money_multiplier(self) -> float:
        """Get current money multiplier."""
        if self.is_cash_boost_active():
            return self.abilities['cash_boost'].multiplier
        return 1.0

    def consume_airstrike(self) -> Optional[Tuple[float, float, int, int]]:
        """
        Consume pending airstrike.

        Returns:
            Tuple of (x, y, damage, radius) or None
        """
        if self.pending_airstrike:
            ability = self.abilities['airstrike']
            result = (*self.pending_airstrike, ability.damage, ability.radius)
            self.pending_airstrike = None
            return result
        return None

    def check_freeze_all(self) -> bool:
        """
        Check if freeze all was just activated.

        Returns:
            True if freeze all should be applied
        """
        ability = self.abilities['freeze_all']
        if ability.active and ability.time_active < 0.1:  # Just activated
            return True
        return False

    def is_freeze_all_active(self) -> bool:
        """Check if freeze all is currently active."""
        return self.abilities['freeze_all'].active
